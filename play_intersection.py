import pickle
import numpy as np
from itertools import product
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting, SpeedMeter, DistanceMeter
from geometry import Point
import time

demo_name = input("Enter speed_distance_iter: ")

h_goal_y = 110.

# other car
a_vel_x = -0.1
a_vel_y = 0.

# BUILD WORLD -----------------------------------------------------------------------------------------------------

dt = 0.1  # time steps in terms of seconds. In other words, 1/dt is the FPS.
w = World(dt, width=120, height=120, ppm=6)  # The world is 120 meters by 120 meters. ppm is the pixels per meter.

# Let's add some sidewalks and RectangleBuildings.
# A Painting object is a rectangle that the vehicles cannot collide with. So we use them for the sidewalks.
# A RectangleBuilding object is also static. But as opposed to Painting, it can be collided with.
# For both of these objects, we give the center point and the size.
w.add(Painting(Point(93.5, 106.5), Point(55, 27), 'gray80'))  # We build a sidewalk.
w.add(RectangleBuilding(Point(94.5, 107.5),
                        Point(52.5, 25)))  # The RectangleBuilding is then on top of the sidewalk.

# Let's repeat this for 4 different RectangleBuildings.
w.add(Painting(Point(27.5, 106.5), Point(55, 27), 'gray80'))
w.add(RectangleBuilding(Point(26.5, 107.5), Point(52.5, 25)))

w.add(Painting(Point(93.5, 41), Point(55, 82), 'gray80'))
w.add(RectangleBuilding(Point(94.5, 40), Point(52.5, 80)))

w.add(Painting(Point(27.5, 41), Point(55, 82), 'gray80'))
w.add(RectangleBuilding(Point(26.5, 40), Point(52.5, 80)))

# Let's also add some zebra crossings, because why not.
w.add(Painting(Point(56, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(57, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(58, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(59, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(60, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(61, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(62, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(63, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(64, 81), Point(0.5, 2), 'white'))
w.add(Painting(Point(65, 81), Point(0.5, 2), 'white'))

w.add(Painting(Point(67, 83), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 84), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 85), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 86), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 87), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 88), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 89), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 90), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 91), Point(2, 0.5), 'white'))
w.add(Painting(Point(67, 92), Point(2, 0.5), 'white'))

# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
c1 = Car(Point(60, 35), np.pi / 2, 'red')
# c1.velocity = Point(h_vel_x, h_vel_y)  # We can also specify an initial velocity just like this.
w.add(c1)

c2 = Car(Point(80, 90), np.pi, 'blue')
# c2.velocity = Point(a_vel_x, a_vel_y)  # We can also specify an initial velocity just like this.
w.add(c2)

# # Pedestrian is almost the same as Car. It is a "circle" object rather than a rectangle.
# p1 = Pedestrian(Point(28,81), np.pi)
# p1.max_speed = 10.0  # (m/s) We can specify min_speed and max_speed of a Pedestrian (and of a Car).
# w.add(p1)

init_speed = 0
sm = SpeedMeter(Point(25, 100), np.pi/2, 'Speed: ' + str(init_speed), 'green')
w.add(sm)

init_distance = np.round(c1.distanceTo(c2))
dm = DistanceMeter(Point(26, 85), np.pi/2, 'Distance: ' + str(init_distance), 'red')
w.add(dm)

w.render()  # This visualizes the world we just constructed.

# Let's implement some simple scenario with all agents
# p1.set_control(0, 0.22)  # The pedestrian will have 0 steering and 0.22 throttle.
# c2.set_control(0, 0.11)  # The second car will keep moving forward.

from interactive_controllers import SteeringWheelController
controller = SteeringWheelController(w)

# from interactive_controllers import KeyboardController
# controller = KeyboardController(w)

demo = []
start_demo = False
while c1.center.y < h_goal_y:

    if controller.throttle > 0.:
        start_demo = True

    if start_demo:
        # move other agent
        c2.center.x += a_vel_x
        c2.center.y += a_vel_y

        c1.set_control(controller.steering / 2.0, controller.throttle * 5.0)

        for agent in w.agents:
            if isinstance(agent, SpeedMeter):
                speed = np.round(controller.throttle * 100)
                agent.text = "Speed: " + str(speed)
            if isinstance(agent, DistanceMeter):
                distance = np.round(c1.distanceTo(c2))
                agent.text = "Distance: " + str(distance)

        demo.append([c1.center.x, c1.center.y, c2.center.x, c2.center.y])

    w.tick()  # This ticks the world for one time step (dt second)
    w.render()
    time.sleep(dt/4)  # Let's watch it 4x
    if w.collision_exists():
        import sys

        sys.exit(0)

    demo.append([c1.center.x, c1.center.y, c2.center.x, c2.center.y])

w.close()

pickle.dump(demo, open("demos/intersection" + demo_name + ".pkl", "wb"))

print("Done.")
