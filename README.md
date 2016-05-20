# Kinect Motion Features

Software for motion feature extraction from Kinect v2 on Windows. 

## Features

Features can correspond to a specific joint (e.g. velocity of right hand) or general body movement
(e.g. quantity of motion). They can be extracted from more than one skeleton. The current list of features is:

### Joint features

* Position / filtered position
* Velocity (3D)
* Velocity magnitude (speed)
* Velocity magnitude (speed) mean
* Acceleration (3D)
* Acceleration magnitude
* Acceleration magnitude mean
* Acceleration along the trajectory of movement
* Acceleration along the trajectory of movement mean
* Distance to torso
* Relative position to torso (3D) (goes from -1 to 1 along all 3 axes, calculated relative to user's height)

### Overall descriptors

* Quantity Of Motion
* Contraction Index
