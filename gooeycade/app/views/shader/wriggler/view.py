import arcade 

from ..shader import ShaderView

class WrigglerView(ShaderView):
    def __init__(self):
        super().__init__()


        self.setup()

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        pass