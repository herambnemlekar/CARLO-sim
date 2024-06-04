import pickle
import numpy as np
from itertools import product
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting, SpeedMeter, DistanceMeter
from geometry import Point
import time


h_goal_y = 100.

# other car
a_vel_x = 0.
a_vel_y = 0.1

# BUILD WORLD -----------------------------------------------------------------------------------------------------

dt = 0.1  # time steps in terms of seconds. In other words, 1/dt is the FPS.
w = World(dt, width=120, height=120, ppm=6)  # The world is 120 meters by 120 meters. ppm is the pixels per meter.

# Let's add some sidewalks and RectangleBuildin.gs.
# A Painting object is a rectangle that the vehicles cannot collide with. So we use them for the sidewalks.
# A RectangleBuilding object is also static. But as opposed to Painting, it can be collided with.
# For both of these objects, we give the center point and the size.
w.add(Painting(Point(103.5, 60), Point(35, 120), 'gray80'))  # We build a sidewalk.
w.add(RectangleBuilding(Point(104.5, 60), Point(32.5, 120)))  # The RectangleBuilding is then on top of the sidewalk.

# Let's repeat this for a different RectangleBuilding.
w.add(Painting(Point(37.5, 60), Point(75, 120), 'gray80'))
w.add(RectangleBuilding(Point(36.5, 60), Point(72.5, 120)))

# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
c1 = Car(Point(78, 45), np.pi/2, 'red')
# c1.velocity = Point(h_vel_x, h_vel_y)  # We can also specify an initial velocity just like this.
w.add(c1)

c2 = Car(Point(78, 90), np.pi/2, 'blue')
# c2.velocity = Point(a_vel_x, a_vel_y)  # We can also specify an initial velocity just like this.
w.add(c2)

# # Pedestrian is almost the same as Car. It is a "circle" object rather than a rectangle.
# p1 = Pedestrian(Point(28,81), np.pi)
# p1.max_speed = 10.0  # (m/s) We can specify min_speed and max_speed of a Pedestrian (and of a Car).
# w.add(p1)

init_speed = 0
sm = SpeedMeter(Point(25, 100), np.pi/2, 'Speed: ' + str(init_speed), 'green')
w.add(sm)

init_distance = c1.distanceTo(c2)
dm = DistanceMeter(Point(26, 85), np.pi/2, 'Distance: ' + str(init_distance), 'red')
w.add(dm)

w.render()  # This visualizes the world we just constructed.

# Let's implement some simple scenario with all agents
# p1.set_control(0, 0.22)  # The pedestrian will have 0 steering and 0.22 throttle.
# c2.set_control(0, 0.11)  # The second car will keep moving forward.


x_unit, y_unit = 0., 1.

from interactive_controllers import SteeringWheelController
controller = SteeringWheelController(w)

# from interactive_controllers import KeyboardController
# controller = KeyboardController(w)

while c1.center.y < h_goal_y:

    # move other agent
    c2.center.x += a_vel_x
    c2.center.y += a_vel_y

    h_vel = controller.throttle*6.0
    c1.set_control(controller.steering/2.0, h_vel)

    for agent in w.agents:
        if isinstance(agent, SpeedMeter):
            agent.text = "Speed: " + str(np.round(h_vel*20))
        if isinstance(agent, DistanceMeter):
            agent.text = "Distance: " + str(np.round(c1.distanceTo(c2)))

    w.tick()  # This ticks the world for one time step (dt second)
    w.render()
    time.sleep(dt/4)  # Let's watch it 4x
    if w.collision_exists():
        import sys
        sys.exit(0)

w.close()

print("Done.")
