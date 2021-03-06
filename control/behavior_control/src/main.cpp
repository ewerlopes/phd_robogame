#include <ros/ros.h>
#include "behavior_control/planner.h"

int main(int argc, char** argv){
    ros::init(argc, argv, "planner_node");
    ros::NodeHandle nh;
    ros::ServiceServer service;
    bool isService;

    if (!nh.getParam("/planner_node/is_service", isService)){
        ROS_ERROR("BEHAVIOR MANAGER: could not read '/planner_node/is_service' from rosparam!");
        exit(-1);
    }
    
    Behavior::Planner b_manager;

    // Loop at 100Hz until the node is shutdown.
    ros::Rate rate(10);
    if(isService){
        service = nh.advertiseService("planning/goal_service", &Behavior::Planner::goalRequestHandler, &b_manager);
        ROS_INFO_STREAM("SERVICE IS UP!");
        ros::spin();
    }
    else{
        ROS_INFO("The Behavior Planner will wait 5secs before starting!");
        ros::Duration(5.0).sleep(); // sleep for 5 seconds before beginning.
        while(ros::ok()){
            b_manager.updateLoop();
            ros::spinOnce();
            // Wait until it's time for another iteration.
            rate.sleep() ;
        }
    }
    return 0;
}