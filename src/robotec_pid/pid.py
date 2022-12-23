#!/usr/bin/env python

import rospy
from simple_pid import PID
from std_msgs.msg import Float64, Float64MultiArray
from dynamic_reconfigure.server import Server

class Node:
    input = 0
    setpoint = 0

    def __init__(self):
        p = rospy.get_param('~p', 1)
        i = rospy.get_param('~i', 0.1)
        d = rospy.get_param('~d', 0.05)
        limMin = rospy.get_param('~limMin', None)
        limMax = rospy.get_param('~limMax', None)
        input_topic = rospy.get_param('~input') 
        adjusted_topic = rospy.get_param('~adjusted')
        setpoint_topic = rospy.get_param('~setpoint')
        configuration_topic = rospy.get_param('~configuration')
        publish_rate = rospy.get_param('~publish_rate', 100)

        rospy.Subscriber(input_topic, Float64, self.inputCallback, queue_size=1)
        rospy.Subscriber(setpoint_topic, Float64, self.setpointCallback, queue_size=1)
        rospy.Subscriber(configuration_topic, Float64MultiArray, self.configurationCallback, queue_size=1)
        self.publisher = rospy.Publisher(adjusted_topic, Float64, queue_size=1)
        
        self.message = Float64()
        self.rate = rospy.Rate(publish_rate)

        if not limMin is None and not limMax is None: 
            self.pid = PID(p, i, d, output_limits=(limMin,limMax))
        else:
            self.pid = PID(p, i, d)
        #self.pid.sample_time = publish_rate
        
    def inputCallback(self, msg):
        self.input = msg.data

    def configurationCallback(self, msg):
        self.pid.Kp = msg.data[0]
        self.pid.Ki = msg.data[1]
        self.pid.Kd = msg.data[2]

    def setpointCallback(self, msg):
        self.setpoint = msg.data

    def reconfigureCallback(config, level):
        self.pid.Kp = config["p"]
        self.pid.Ki = config["i"]
        self.pid.Kd = config["d"]

        return config

    def run(self):
        while not rospy.is_shutdown():
            self.pid.setpoint = self.setpoint
            self.message.data = self.pid(self.input)
            self.publisher.publish(self.message)
            
            self.rate.sleep()

def main():
    rospy.init_node('robotec_pid', anonymous=True)

    node = Node()
    node.run()

if __name__ == '__main__':
    main()
