1.给ros配置python3环境
sudo apt-get install python3-dev
# 创建虚拟环境
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install catkin_pkg pyyaml empy rospkg numpy
2.编译
cd catkin_ws
catkin_make
source devel/setup.bash
3.roslaunch flask_sdp_main app.launch
4.rosrun flask_sdp_main pub.py
