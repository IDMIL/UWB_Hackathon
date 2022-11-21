"""Performs 2-dimensional true-range multilateration.
Based on:
https://en.wikipedia.org/wiki/True-range_multilateration#Two_Cartesian_dimensions,_two_measured_slant_ranges_(trilateration)
"""
# Standard libraries
import math
import threading
from time import sleep

# Third-party libraries
import graphics
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


OSC_IP = '0.0.0.0'
OSC_PORT = 1234

class UwbOscReceiver:
    def __init__(self, U, oscaddr_node1, oscaddr_node2):
        # Distance between two anchors, in meters
        self.U = U
        self.d1 = 0.0
        self.d2 = 0.0
        dispatcher = Dispatcher()
        dispatcher.map(oscaddr_node1, self.node1_handler)
        dispatcher.map(oscaddr_node2, self.node2_handler)

        server = BlockingOSCUDPServer((OSC_IP, OSC_PORT), dispatcher)
        threading.Thread(target=server.serve_forever, daemon=True).start()

    def node1_handler(self, _, val):
        self.d1 = val

    def node2_handler(self, _, val):
        self.d2 = val

    def triangulate(self):
        x = (self.d1*self.d1 - self.d2*self.d2 + self.U*self.U) / (2*self.U)
        y = math.sqrt(abs(self.d1*self.d1 - x*x))
        return (x, y)

def main():
    distance_between_nodes = 1.0
    circle_radius = 10
    receiver = UwbOscReceiver(distance_between_nodes, '/rx0', '/rx2')
    pixel_offset = 50
    pixels_per_meter = 100
    win = graphics.GraphWin("Trilateration", 200, 100)
    c = graphics.Circle(graphics.Point(0,0), circle_radius)
    anchor1 = graphics.Circle(graphics.Point(pixel_offset, pixel_offset), circle_radius)
    anchor1.setFill("red")
    anchor2 = graphics.Circle(graphics.Point(pixel_offset+(distance_between_nodes*pixels_per_meter),
        pixel_offset), circle_radius)
    anchor2.setFill("blue")
    anchor1.draw(win)
    anchor2.draw(win)
    while True:
        x, y = receiver.triangulate()
        x, y = x*pixels_per_meter + pixel_offset, y*pixels_per_meter + pixel_offset
        c.undraw()
        c = graphics.Circle(graphics.Point(x, y), circle_radius)
        c.draw(win)
        sleep(0.01)

if __name__ == '__main__':
    main()
