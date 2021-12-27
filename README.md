# My source code for CPT task

"gas_distribution_mapping": Build the gas distribution map using kernel DM+V algorithm
"gauss_process": Chemical plume tracing using Gauss Process 

rosrun urg_node urg_node &
sudo chown root:$USER /dev/gpiomem && sudo chmod g+rw /dev/gpiomem 
rosrun cpt_robot cpt_robot.py &
rosrun cpt_gas_sensing analog_read.py &

roslaunch hector_slam_launch tutorial.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
rosrun cpt_data_saver data_saver.py
rosrun map_server map_saver -f 'file'
