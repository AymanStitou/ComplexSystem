# ComplexSystem: Boids Simulation  

This repository contains the code for the optional programming assignment on **Boids**, developed for the **Complex Systems** course at UvA. The simulation models flocking behavior inspired by Craig Reynolds' Boids, which is often used to study emergent behaviors in systems of simple agents. The code is functional, but will be revised and improved upon as the documentation was not completed(!!!). Initially inspired by this github repository: https://github.com/Josephbakulikira/simple-Flocking-simulation-python-pygame/blob/master/boid.py. The background image and sprite are free stock images.

## Current Features  
The code provides a functional Boids simulation with the following features:  
- **Flocking Rules**: The classic separation, alignment, and cohesion rules are implemented.  
- **Adjustable Parameters**:  
  - Separation, alignment, and cohesion weights.  
  - Maximum speed and perception radius of the Boids.  
  - Total number of Boids in the simulation.  
- **Visualization**:  
  - Real-time rendering of Boids and their interactions.  
  - Live plots for:  
    - Average velocity of the Boids over time.  
    - Average number of neighbors over time.  
  - Option to display the perception radius of a specific Boid.  
- **Interactive UI**:  
  - Input boxes for dynamically changing simulation parameters.  
  - Buttons for toggling perception radius and resetting to default settings.  
  - A semi-circular "Menu" button for toggling the UI panel.  

## Future Enhancements  
In the future, I plan to:  
- Introduce **predators** to simulate predation and its effects on flocking behavior.  
- Add **obstacles** to study avoidance behaviors in dynamic environments.  
- Optimize and clean up the code to make it more modular and maintainable.  

## Code Structure  
- `main.py`: Entry point for the simulation. Handles the game loop, UI interactions, and integration of flocking logic with visualization.  
- `flock.py`: Contains the `Flock` class, managing the collection of Boids and their interactions.  
- `boid.py`: Defines the `Boid` class, which encapsulates individual Boid behavior and rules.  
- `ui.py`: Contains UI components like panels, input boxes, and buttons for parameter adjustments.  
- `LivePlot.py`: Implements live plotting for average velocity and neighbors using pygame.  
- `settings.py`: Stores constants and default values.

## Running the Simulation  
1. Clone the repository.  
2. Install the required libraries (numpy, pygame, matplotlib, etc...)
3. Run in terminal: python main.py