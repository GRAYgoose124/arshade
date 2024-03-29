import arcade
import logging

from .comp_manager import ComponentManager


log = logging.getLogger(__name__)


class SwappableViewWindow(arcade.Window, ComponentManager):
    def __init__(self, *args, **kwargs):
        arcade.Window.__init__(self, *args, **kwargs)
        ComponentManager.__init__(self)

        self._views = {}
        self._default_view = None
        self._last_view = None

        self.needs_reload = False

    @property
    def views(self):
        return self._views

    @property
    def view_names(self):
        return list(self._views.keys())

    @property
    def view_titles(self):
        return [v.title for v in self._views.values()]

    @property
    def current_view(self):
        return self._current_view

    @property
    def default_view(self):
        return self._default_view

    @property
    def last_view(self):
        return self._last_view

    def show_view(self, view=None):
        """Shows a view."""
        if view is None:
            view = self.default_view

        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._last_view = self.current_view or self.default_view or view

        super().show_view(self.views[view])

    def set_default_view(self, view):
        if view is None:
            return

        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._default_view = view

    def add_view(self, view):
        """Adds a view to the app."""
        if view.name in self._views:
            log.warning("View '%s' already exists, overwriting.", view.name)
            # force GC
            del self._views[view.name]

        self._views[view.name] = view

        if self.default_view is None:
            self.set_default_view(view.name)

    def reload_view(self, vname, pause=True):
        """Updates a view."""
        if self.can_reload(vname):
            if pause:
                self.show_view("PauseView")
            p = self.get_component_path(vname)
            log.debug("Reloading view '%s' from %s", vname, p)
            self.add_view(self.load_component(p))
            self.views[vname].setup()
            log.info("Updated view '%s'", self.views[vname])
            if pause:
                self.show_view(vname)

    def reload_views(self):
        """Updates the views."""
        # TODO: don't reload core views and only load components lazily
        views_copy = self.views.copy()

        current_view = self.current_view
        self.show_view("PauseView")
        for view in views_copy:
            self.reload_view(view, pause=False)
        self.show_view(current_view)

    def remove_view(self, vname, no_reload=False):
        """Removes a view from the app."""
        if vname not in self.views:
            raise ValueError(f"View '{vname}' does not exist.")

        if self.can_reload(vname) and no_reload:
            del self._component_paths[vname]

        if self._default_view == vname:
            self.set_default_view(self.last_view)

        del self._views[vname]

    def remove_views(self):
        """Removes all views from the app."""
        for view in self.views:
            self.remove_view(view)

    def setup_views(self):
        """Sets up the views."""
        for view in self.views.values():
            view.setup()
