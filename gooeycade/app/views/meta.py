import arcade


class MetaView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hello, World!", 300, 100, arcade.color.AMAZON, 54)

    def on_key_press(self, key, modifiers):
        pass
