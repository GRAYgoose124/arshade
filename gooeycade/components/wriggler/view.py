import arcade

from ...app.views import ShaderView


class WrigglerView(ShaderView):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        pass
