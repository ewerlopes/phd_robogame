# Kinect Motion Features

Software for motion feature extraction from Kinect v2 on Windows. This version only works on windows.

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
* Fluidity

## Credits
This piece of code was originally desined by the Music Technology Group - Universitat Pompeu Fabra / Escola Superior de Música de Catalunya. Specifically, it was created and maintained by Álvaro Sarasúa, in the github repository:  <https://github.com/asarasua/ofxKinectFeatures>, being an application strongly dependent on OpenFrameworks. 

In this repository, the code has been modified to fit the research developed  at the Artificial Intelligence and Robotics Laboratory (AIRLab) at Politecnico di Milano (Milano-Italy) under the purpose of my PhD research. **The main difference in this code version is that it doesn't depend on OpenFramework anymore, and fluidity as a new descriptor has been included.**

## How to use it
KinectFeatures code was designed to only compute descriptors from motion capture data. To track the skeleton from a Kinect device, linking to the Microsoft Kinect SDK or any other framework is need. 

To link properly, using the Kinect SDK using Visual Studio 2012+, do: 

1. Create a new Project Property sheet. 
2. Add "$(KINECTSDK20_DIR)\inc" value to Project Property -> Configuration Properties -> C/C++ -> Additional Include Directories.
3. Add "$(KINECTSDK20_DIR)\lib\x64" (or x86, depending on your system) value to Project Property -> Configuration Properties -> Linker -> Additional Library Directories.
4. Add "Kinect20.lib" value to Project Property -> Configuration Properties -> Linker -> Input -> Additional Dependencies.

If you are using Kinect One, change the environment variable accordingly.

##API
The API has been designed not to depend on a particular library for the skeleton tracking with Kinect. 

The features are accessed through an `KinectFeatures` object, so declare it in your main:

```cpp
KinectFeatures featExtractor;
```

If you wish to extract features for more than one skeleton, just declare one KinectFeatures object for each (e.g. by creating a `map<int,KinectFeatures>` where keys correspond to an skeleton id).

In setup(), it is necessary to tell KinectFeatures which indices correspond to the **head** and **torso** joints, as some calculations need to know about this. This is easily done depending on the libray being used for skeleton tracking.

```cpp 
featExtractor.setup(JointType_Head, JointType_SpineMid); //Using Kinect SDK 2.0
```

In `update()`, just update skeletons data sending a `map<int, ofPoint>` where keys are integers identifying joints and values are the x, y, z positions of these joints. Here is the general idea in pseudocode:

```cpp
if tackedUsers {
    user = getTrackedUser();
    map<int, ofPoint> joints; // a joint "dictionary"
    for all joints{
        joints[j] = user.getJointPosition();
    }
    featExtractor.update(joints); //update the feature measures
}
```

*Look inside `Skeleton::skeletonTracking()` in this repository code in order to now more.*

With the correct update loop, features can be accessed calling the appropriate methods.

In order to get the x velocity of the right hand, for instance, using the Kinect SDK 2.0:

```cpp
if skeletonExists {
    featExtractor.getVelocity(JointType_HandRight).x;
}
```

For overall descriptors, just call the corresponding method. E.g.:
```cpp
    featExtractor.getQom();
``` 

## LICENSE
KinectFeatures is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License (LGPL v3) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. KinectFeatures is distributed in the hope that it will be useful, but WITHOUT  ANY WARRANTY; without even the  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License (LGPL v3). See <http://www.gnu.org/licenses/>.
