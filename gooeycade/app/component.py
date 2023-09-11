import arcade
from pathlib import Path


class Component(arcade.View):
    """Unused - documentation only."""

    def __init__(self):
        super().__init__()
        self._view_cls = None

    def get_component_spec(self):
        # get the path of the view class
        view_path = Path(self._view_cls.__module__.replace(".", "/"))

    @property
    def name(self):
        pass

    @property
    def path(self):
        pass


class ComponentManager:
    pass
