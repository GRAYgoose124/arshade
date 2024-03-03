import arcade
import logging

from .window import SwappableViewWindow


log = logging.getLogger(__name__)


class GooeyApp(SwappableViewWindow):
    def __init__(self, *args, **kwargs):
        SwappableViewWindow.__init__(self, *args, **kwargs)

    def start(
        self,
        components_path,
        default_view="PrimaryView",
        blacklist=["MetaView"],
        whitelist=None,
    ):
        log.info("Gooey Cade starting up")

        # load components
        log.info("Loading components from %s", components_path)
        self.append_component_path_to_sys(components_path)

        log.debug("Loading core views")
        core_vs = ["PrimaryView", "PauseView"]
        for c in self.load_components(components_path, whitelist=core_vs):
            self.add_view(c)

        log.debug("Loading other views")
        for c in self.load_components(
            components_path, blacklist=core_vs + blacklist, whitelist=whitelist
        ):
            self.add_view(c)

        # set up views
        log.debug("Setting up views")
        self.setup_views()
        self.set_default_view(default_view)
        self.show_view()

        # start app
        log.info("App started")
        self.center_window()
        arcade.run()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_view("PauseView")
