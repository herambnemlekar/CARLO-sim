import pickle
import numpy as np
from itertools import product
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting
from geometry import Point
import time


h_vel_list = [0.4, 0.7, 1.0]
h_dy_list = [12., 18., 24.]
h_style_list = [h_style for h_style in product(h_vel_list, h_dy_list)]

train_data = pickle.load(open("results/train_data_intersection_3.pkl", "rb"))
recon_data = pickle.load(open("results/train_recon_intersection_3.pkl", "rb"))

zs_list = pickle.load(open("results/test_zs_list_3.pkl", "rb"))
test_data = pickle.load(open("results/test_recon_intersection_3.pkl", "rb"))

plot_train_data = False

for i, recon_demo in enumerate(test_data):

    # print("Simulating style:", h_style_list[i])
    print("Simulating style:", zs_list[i])

    # BUILD WORLD -----------------------------------------------------------------------------------------------------

    dt = 0.5  # time steps in terms of seconds. In other words, 1/dt is the FPS.
    w = World(dt, width=120, height=120,
              ppm=6)  # The world is 120 meters by 120 meters. ppm is the pixels per meter.

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

    if plot_train_data:
        c1_train = Car(Point(64, 45), np.pi / 2, 'red')
        w.add(c1_train)
        c2_train = Car(Point(72, 90), np.pi, 'blue')
        w.add(c2_train)

    c1_recon = Car(Point(64, 45), np.pi / 2, 'orange')
    w.add(c1_recon)
    c2_recon = Car(Point(72, 90), np.pi, 'cyan')
    w.add(c2_recon)

    w.render()  # This visualizes the world we just constructed.

    # SIMULATE DEMO ---------------------------------------------------------------------------------------------------

    for j, recon_state in enumerate(recon_demo):
        if plot_train_data:
            train_state = train_data[i][j]
            c1_train.center.x, c1_train.center.y, c2_train.center.x, c2_train.center.y = train_state
        c1_recon.center.x, c1_recon.center.y, c2_recon.center.x, c2_recon.center.y = recon_state

        w.tick()
        w.render()
        time.sleep(dt)

    time.sleep(4*dt)
    w.close()

print("Done.")
