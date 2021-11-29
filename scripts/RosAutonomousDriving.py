#!/usr/bin/env python
from driving.turtle_move import TurtleMove
from driving.PickLine import PickLine

t = TurtleMove()
p = PickLine()

def run():
    t.move()

if __name__=="__main__":
    while not rospy.is_shutdown():
        run()
