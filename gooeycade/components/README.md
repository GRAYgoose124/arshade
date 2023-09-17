# Anatomy of a Component subpackage

A component at it's core is a hot reloadable arcade View. 

It can generally be selected from the gooeycade pause menu.

## Component subpackage structure

```
components/
    __init__.py
    component-name/
        __init__.py # optional
        view.py
        ...
```
The above structure is not strictly necessary, a view file can be placed directly in the components/ directory. However, it is recommended to use the above structure for clarity.

The `components/__init__.py` file helps the ComponentManager find the components. It is not strictly necessary, but it is recommended to use it. In the future, this may be done with a configuration script or by more sophisticated means.
```python
# Do not change these unless you know what you're doing:
core = [PauseView, PrimaryView]

all = core + [
    # Add your views here:
    MandalaView,
    MeshView,
    SwarmView,
    WrigglerView,
    TilerView,
]
```

view.py:
```python
import arcade

from gooeycade.app.component import Component


class NewComponentView(Component):
    def __init__(self):
        super().__init__()

    def setup():
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hello, World!", 300, 100, arcade.color.AMAZON, 54)

    def on_key_press(self, key, modifiers):
        pass

# Necessary for the ComponentManager to find the view on hot reload
ComponentView = NewComponentView
```

Please reference the components which use a `gooeycade.app.shader.ShaderViewComponent` for more complex usage.