# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 23:58:30 2021

@author: ashoaib
"""

import glob
import os
import sys
from queue import Queue
from queue import Empty

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

s1, s2, s3, s4, s5, s6 = [110,95], [70,100], [30,100], [-30,100], [-70,100], [-110,95]

DIST = 6 # let's suppose placed at equidistance of 6cm

SENSORS = [s1, s2, s3, s4, s5, s6]

steering = np.arange(1,360, 1)

x,y = 0,0




def direct_echo(time, sensor):
    dist = sensor[1] + (time * 17165)/2
    return dist

def cross_echo(d1,d2):
    theta = math.cos(((d1*d1) + DIST - (d2*d2)) / (2 * d1 * DIST) ) # given equation in slides or github
    alpha = (d1 * d1) / DIST 
    x = math.tan(theta) * alpha
    if s1[0] > 0:
        s1[0] = s1[0] + x
        if s2[0] > s1[0]:
            s1[1] = s1[1] + alpha
        else:
            s1[1] = s1[1] - alpha 
    else:
        s1[0] = s1[0] - x
        if s2[0] < s1[0]:
            s1[1] = s1[1] + alpha
        else:
            s1[1] = s1[1] - alpha 
    return s1

def sensor_loop(t1,t2, s):
    t = abs(t1-t2)
    direct_dist = direct_echo(t,s)
    if direct_dist > 1:
        d1 = direct_dist[0]
        d2 = direct_dist[1]
        cross_dist = cross_echo(d1,d2) 


# Sensor callback.
# This is where you receive the sensor data and
# process it as you liked and the important part is that,
# at the end, it should include an element into the sensor queue.
def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    sensor_queue.put((sensor_data.frame, sensor_name))


def main():
    # We start creating the client
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()

    try:
        # We need to save the settings to be able to recover them at the end
        # of the script to leave the server in the same state that we found it.
        original_settings = world.get_settings()
        settings = world.get_settings()

        # We set CARLA syncronous mode
        settings.fixed_delta_seconds = 0.2
        settings.synchronous_mode = True
        world.apply_settings(settings)

        # We create the sensor queue in which we keep track of the information
        # already received. This structure is thread safe and can be
        # accessed by all the sensors callback concurrently without problem.
        sensor_queue = Queue()

        # Bluepints for the sensors
        blueprint_library = world.get_blueprint_library()
        cam_bp = blueprint_library.find('sensor.camera.rgb')
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        radar_bp = blueprint_library.find('sensor.other.radar')

        # We create all the sensors and keep them in a list for convenience.
        sensor_list = []

        cam01 = world.spawn_actor(cam_bp, carla.Transform())
        cam01.listen(lambda data: sensor_callback(data, sensor_queue, "camera01"))
        sensor_list.append(cam01)

        lidar_bp.set_attribute('points_per_second', '100000')
        lidar01 = world.spawn_actor(lidar_bp, carla.Transform())
        lidar01.listen(lambda data: sensor_callback(data, sensor_queue, "lidar01"))
        sensor_list.append(lidar01)

        lidar_bp.set_attribute('points_per_second', '1000000')
        lidar02 = world.spawn_actor(lidar_bp, carla.Transform())
        lidar02.listen(lambda data: sensor_callback(data, sensor_queue, "lidar02"))
        sensor_list.append(lidar02)

        radar01 = world.spawn_actor(radar_bp, carla.Transform())
        radar01.listen(lambda data: sensor_callback(data, sensor_queue, "radar01"))
        sensor_list.append(radar01)

        radar02 = world.spawn_actor(radar_bp, carla.Transform())
        radar02.listen(lambda data: sensor_callback(data, sensor_queue, "radar02"))
        sensor_list.append(radar02)


        actual_objet = sensor_loop(lidar02, radar01)
            
        # Main loop
        while True:
            # Tick the server
            world.tick()
            w_frame = world.get_snapshot().frame
            print("\nWorld's frame: %d" % w_frame)

            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(True, 1.0)
                    print("    Frame: %d   Sensor: %s" % (s_frame[0], s_frame[1]))

            except Empty:
                print("    Some of the sensor information is missed")

    finally:
        world.apply_settings(original_settings)
        for sensor in sensor_list:
            sensor.destroy()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
