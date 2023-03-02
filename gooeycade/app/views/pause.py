import arcade
import arcade.gui


class PauseView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()
        return super().on_hide_view()

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            dialog = arcade.gui.UIMessageBox(width=300, height=150, message_text="Are you sure you want to quit?",
                                                buttons=("Ok", "Cancel"))
            
            dialog._callback = lambda button_text: arcade.close_window() if button_text == "Ok" else self.window.show_view("primary")

            self.manager.add(dialog)
