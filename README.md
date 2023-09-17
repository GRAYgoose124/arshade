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
Components are the building block of an app. If a component has a view, then it can generally be selected from the pause menu. 

## Views
There are a number of views that can be chosen from the pause menu.

The Primary and Pause views are part of the core app. The rest are from components.

### Meta (unfinished)
A view selector. (Right now the pause menu plays this role)
### Wrigger (unfinished)
Procedural model gen using self-organizing space-filling curves.
### Swarm (unfinished)
Compute shader based swarm/flocking sim. (Just based on arcade' N-body example for now)
### MeshViz (unfinished)
Mesh viewer with rudimentary obj support.
### Mandala (unfinished)
2D LINES based art visualizer.
![](https://raw.githubusercontent.com/GRAYgoose124/arshade/main/screenshots/mand1.jpg)