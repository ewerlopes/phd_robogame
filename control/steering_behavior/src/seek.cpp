#include "steering_behavior/seek.h"
#include <geometry_msgs/Point32.h>
#include <geometry_msgs/Vector3.h>
#include <ros/ros.h>

geometry_msgs::Vector3 SteeringBehavior::Seek::calculate_desired_velocity(geometry_msgs::Point32 current_pos){
    geometry_msgs::Vector3 output;
    output = VectorUtility::vector_difference(current_pos, target_);
    return output;
}

geometry_msgs::Vector3 SteeringBehavior::Seek::calculate_steering_force(geometry_msgs::Vector3 current_vel, geometry_msgs::Vector3 desired_vel){
    geometry_msgs::Vector3 output;
    
    output = VectorUtility::vector_difference(current_vel, desired_vel);
    return output;
}