# About
A simple app for various GL views in Python using Arcade.

# Installation
```bash
git clone git@github.com:GRAYgoose124/arshade.git
cd arshade
```
then:
```bash
poetry install
```
or 
```bash
pip install ./arshade
```

> Tip: use pip install -e to install in editable mode. This will allow you to make changes to the code and have them reflected in the installed package.

# Usage
Run the app wih the following:
```bash
gcade
```
    
# Components
Components are the building block of an app. If a component has a view, then it can generally be selected from the pause menu. Components can be hot reloaded. See the [Component Readme](gooeycade/components/README.md) for more information.

## Views
There are a number of views that can be chosen from the pause menu.

The Primary and Pause views are part of the core app. The rest are from components.

### Primary & Pause
The primary view is the main view of the app which is shown when the app is first started.

The pause view is the view that is shown when the app is paused via `Esc`. From here, you can select other views or reload the current view after making changes.

![Pause Menu](https://raw.githubusercontent.com/GRAYgoose124/arshade/main/screenshots/pauseview.png)

### Meta (core)
A view selector. (Right now the pause menu alone plays this role)
### Wrigger 
Procedural model gen using self-organizing space-filling curves.
### Swarm 
Compute shader based swarm/flocking sim. (Just based on arcade' N-body example for now)
### MeshViz 
Mesh viewer with rudimentary obj support.

![MeshViz](https://raw.githubusercontent.com/GRAYgoose124/arshade/main/screenshots/meshview.png)

### Mandala 
2D + 3D LINES based art shader visualizer.

Allowing for a variety of different visualizations.
![](https://raw.githubusercontent.com/GRAYgoose124/arshade/main/screenshots/mand1.jpg)

![](https://raw.githubusercontent.com/GRAYgoose124/arshade/main/screenshots/altmandala3d.png)