import arcade

from gooeycade.app.shader import ShaderViewComponent


class WrigglerView(ShaderViewComponent):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        pass


ComponentView = WrigglerView
