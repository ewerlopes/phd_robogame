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
This piece of code was originally desined by the Music Technology Group - Universitat Pompeu Fabra / Escola Superior de Música de Catalunya. Specifically, it was created and maintained by Álvaro Sarasúa, in the github repository:  <https://github.com/asarasua/ofxKinectFeatures>, being an application strongly dependent on OpenFrameworks. Here, the code has been modified to fit the research developed  at the Artificial Intelligence and Robotics Laboratory (AIRLab) at Politecnico di Milano (Milano-Italy) under the purpose of my PhD research. 

## LICENSE
KinectFeatures is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License (LGPL v3) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. KinectFeatures is distributed in the hope that it will be useful, but WITHOUT  ANY WARRANTY; without even the  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License (LGPL v3). See <http://www.gnu.org/licenses/>.
