#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from flask_msgs.msg import *

def talker():
    pub = rospy.Publisher('app_json', flaskMsg, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
       sendmsg = flaskMsg()
       sendmsg.jname = 'output-floor1'

       hello_str = '{"Robots": [{"ID": "0054", "Battery Level": -1, "Last Message Time": 1614174089.7997007, "State": {"State": "Movement", "Destination": "Exit"}}, {"ID": "0002", "Battery Level": -1, "Last Message Time": 1614174107.9422169, "State": {"State": "Movement", "Destination": "Reception"}}, {"ID": "0034", "Battery Level": -1, "Last Message Time": 1614174063.5313087, "State": {"State": "Movement", "Destination": "Reception"}}, {"ID": "0023", "Battery Level": -1, "Last Message Time": 1614173992.1921961, "State": {"State": "WaitingAtReception", "Destination": "N/A"}}], "Booths": [{"ID": 1, "Capcity, Humans": 1, "Capacity Robots": 1, "Robots with humans": ["0034"], "Robots without Humans": []}, {"ID": 2, "Capcity, Humans": 1, "Capacity Robots": 1, "Robots with humans": ["0002"], "Robots without Humans": []}, {"ID": 3, "Capcity, Humans": 1, "Capacity Robots": 1, "Robots with humans": [], "Robots without Humans": []}], "Transit Area": {"ID": "1", "Capcity, Humans": 1, "Capacity Robots": 100, "Robots with humans": ["0001"], "Robots without Humans": []}, "Exit Area": {"ID": "1", "Capcity, Humans": 1, "Capacity Robots": 100, "Robots with humans": ["0001"], "Robots without Humans": []}, "Drop Off": {"ID": "1", "Capcity, Humans": 0, "Capacity Robots": 100, "Robots with humans": [], "Robots without Humans": []}, "Reception": {"ID": "1", "Capcity, Humans": 100, "Capacity Robots": 100, "Robots with humans": ["0002", "0023"], "Robots without Humans": []}}'
    #rospy.loginfo(hello_str)
       sendmsg.json = hello_str
       pub.publish(sendmsg)
       rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
