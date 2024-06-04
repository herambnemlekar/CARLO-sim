import pickle
import numpy as np
from itertools import product
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting
from geometry import Point
import time

human_controller = False

# training
# h_vel_list = [0.4, 0.7, 1.0]
# h_dy_list = [12., 18., 24.]

# testing
h_vel_list = np.linspace(0.4, 1.0, 8)[1:-1]
h_dy_list = np.linspace(12, 24, 8)[1:-1]

demo_data = []

for h_style in product(h_vel_list, h_dy_list):

    print("Simulating style:", h_style)
    h_vel_y, h_dist_y = h_style
    h_vel_x = 0.
    h_dist_x = 10
    h_goal_y = 100
    vel_noise = 0.01
    dist_noise = 0.1

    # other car
    a_vel_x = 0.
    a_vel_y = 0.1

    # BUILD WORLD -----------------------------------------------------------------------------------------------------

    dt = 0.1  # time steps in terms of seconds. In other words, 1/dt is the FPS.
    w = World(dt, width=120, height=120, ppm=6)  # The world is 120 meters by 120 meters. ppm is the pixels per meter.

    # Let's add some sidewalks and RectangleBuildings.
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

    w.render()  # This visualizes the world we just constructed.

    # Let's implement some simple scenario with all agents
    # p1.set_control(0, 0.22)  # The pedestrian will have 0 steering and 0.22 throttle.
    # c2.set_control(0, 0.11)  # The second car will keep moving forward.

    # SIMULATE DEMO ---------------------------------------------------------------------------------------------------

    demo = []

    if not human_controller:

        while c1.center.y < h_goal_y:
            ha_dist_x = np.linalg.norm(c1.center.x - c2.center.x)
            ha_dist_y = np.linalg.norm(c1.center.y - c2.center.y) + np.clip(np.random.normal(loc=0., scale=dist_noise),
                                                                            -2*dist_noise, 2*dist_noise)
            if (ha_dist_x < h_dist_x) and (ha_dist_y < h_dist_y):
                # c1.set_control(0, -2*h_acc)
                c1.center.x += h_vel_x + np.clip(np.random.normal(loc=0., scale=vel_noise), -2*vel_noise, 2*vel_noise)
                c1.center.y += a_vel_y + np.clip(np.random.normal(loc=0., scale=vel_noise), -2*vel_noise, 2*vel_noise)

                c2.center.x += a_vel_x
                c2.center.y += a_vel_y
                print('Breaking...')
            else:
                # c1.set_control(0, h_acc)
                c1.center.x += h_vel_x + np.clip(np.random.normal(loc=0., scale=vel_noise), -2*vel_noise, 2*vel_noise)
                c1.center.y += h_vel_y + np.clip(np.random.normal(loc=0., scale=vel_noise), -2*vel_noise, 2*vel_noise)

                c2.center.x += a_vel_x
                c2.center.y += a_vel_y
                print('Accelerating...')

            w.tick()  # This ticks the world for one time step (dt second)
            w.render()
            time.sleep(dt/4)  # Let's watch it 4x

            # if w.collision_exists(p1):  # We can check if the Pedestrian is currently involved in a collision.
            #     print('Pedestrian has died!')
            if w.collision_exists():  # Or we can check if there is any collision at all.
                print('Collision exists somewhere...')

            demo.append([c1.center.x, c1.center.y, c2.center.x, c2.center.y])

        w.close()

    else:  # Let's use the steering wheel (Logitech G29) for the human control of car c1
        # p1.set_control(0, 0.22)  # The pedestrian will have 0 steering and 0.22 throttle.
        c2.set_control(0, 0.11)

        from interactive_controllers import SteeringWheelController
        controller = SteeringWheelController(w)
        while c1.center.y < h_goal_y:
            c1.set_control(controller.steering, controller.throttle)
            w.tick()  # This ticks the world for one time step (dt second)
            w.render()
            time.sleep(dt/4)  # Let's watch it 4x
            if w.collision_exists():
                import sys
                sys.exit(0)

            demo.append([c1.center.x, c1.center.y, c2.center.x, c2.center.y])

    demo_data.append(demo)

pickle.dump(demo_data, open("data/test_carlo_highway_2_1.pkl", "wb"))

print("Done.")
