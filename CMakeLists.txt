cmake_minimum_required(VERSION 2.8.3)
project(robotec_pid)

#
find_package(catkin REQUIRED COMPONENTS std_msgs sensor_msgs message_generation dynamic_reconfigure)

#
catkin_python_setup()

generate_dynamic_reconfigure_options(
    cfg/pid.cfg
)

catkin_install_python(PROGRAMS src/robotec_pid/pid.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

#
catkin_package(
    CATKIN_DEPENDS message_runtime dynamic_reconfigure
    )
#add_dependencies(example_node ${PROJECT_NAME}_gencfg)
