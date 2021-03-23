1.python3
sudo apt-get install python3-dev
#venv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install catkin_pkg pyyaml empy rospkg numpy
2.compile
cd catkin_ws
catkin_make
source devel/setup.bash
3.roslaunch flask_sdp_main app.launch
4.rosrun flask_sdp_main pub.py
