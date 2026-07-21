import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/ros2/install/soarm100_vision'
