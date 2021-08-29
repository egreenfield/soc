# Flocking

## Todo
- port FOV to OpenCL
- fix the 'too close' logic so it's not so jarring
- add some randomness to motion of flocks
- persist settings from run to run
- generators + death
- bounce surfaces
- repulsor walls.
- ability to save / load different parameter configurations

## Done
- make screen box force grow the farther you are from the edge
- limit max number of neighbors to consider
- openCL based processing: https://documen.tician.de/pyopencl/
- delete repulsors
- add quad tree / tile tree optimization
- support negative numbers in sparse list
- add repulsor behavior to edge of screen
- ability to change individual parameters at runtime.
- trails
- fix transparency problem?
- angle of visibility


## Later Ideas
- implement DBScan (https://en.wikipedia.org/wiki/DBSCAN)
- try two-teir tiles (one for gravity, one for too close neighbors)
- improve performance (quad tree performance and comparison performance)

## Challenges

### create birds
Get the basic idea of a program that simulates birds up and running.
1. When the mouse is clicked, create a bird at the click location
1. birds should have random direction and speed (within a small range)
1. every frame, draw the birds, and update them based on their speed and direction
    1. figure out how to show the bird's direction in the way it's drawn
1. extra credit: update based on time elapsed.  i.e., figure out how much time has elapsed since the last time they got updated, and figure out their new position based on the time delta and their speed.

### follow the mouse
Now that you've got birds flying, introduce the idea of them changing their motion based on external factors.
1. if the mouse is on screen, have the birds move towards the mouse
1. assume birds can't change direction immediately.  they can only turn up to a maximum # of degrees per second.  (Again, try using time here, not frames).
1. if the mouse isn't on screen, they should just go strait.

### Flocking
Now the fun part...let's see if they can change behavior based on the other birds around them.
1. read about the basic flocking algorithm: [here](Bounds.pdf) and see [sample code here](Boids%20Pseudocode.pdf)
1. try implementing it.  Do it in stages...there are a few rules to the full algorithm...what part can you implement first?
1. think about performance...what do you think is the most expensive part of this algorithm? Can you imagine ways you could make it less expensive?

### Control
For Extra Credit, can you make it easy for you to play with the simulation and experiment? How can you make something that you can interact with?
1. Create a new class that can be used as a slider that you can drag around.
1. The slider needs to draw itself...let's make it simple, a horizontal line, and a circle for the current value.
1. you're going to want to use this for different things, so let's give it some parameters and property.  You'll probably want to change:
    * its position on screen
    * its width on screen
    * the range it represents (minimum and maximum)
    * the current value it represents (where the ball is drawn)
1. make it interactive.  
    * when the user clicks down on the ball, they should start 'dragging' it back and forth along the line.
    * when they let go, it should stop dragging.
    * they shouldn't be able to drag it outside of the line.
1. make it useful!
    * you should be able to get and set the current value of the slider.
    * when the user drags the ball around, it should change the current value based on the ball's position between the minimum and maximum.

Now that you've done this, could you create a button class?  Something that can be positioned on screen, and show a label?  How would you make it easy to run some code when the button is clicked on?
### Nerdery
It might be fun to add some 'diagnostic' info to the birds.  Can a bird also draw something to indicate where it's trying to fly to?  What direction it wants to go?  Which birds it can see?  Which ones it's trying to avoid?  Maybe you can click the mouse or press a key to choose which bird should be showing its diagnostics?
