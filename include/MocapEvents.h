/*
*** MocapEvents.h

This file is part of the KinectFeature Project.

Originally desined by the Music Technology Group - Universitat Pompeu Fabra / Escola Superior de Música de Catalunya.
Specifically, it was created and maintained by Álvaro Sarasúa in the github repository:  <https://github.com/asarasua/ofxKinectFeatures>,
being an application strongly dependent on OpenFrameworks. Here, the code has been modified to fit the research developed
at the Artificial Intelligence and Robotics Laboratory at Politecnico di Milano, Milano, Italy.

LICENSE INFORMATION: KinectFeatures is free software: you can redistribute it and/or modify it under the terms
of the GNU Lesser General Public License (LGPL v3) as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.
KinectFeatures is distributed in the hope that it will be useful, but WITHOUT  ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License (LGPL v3). See <http://www.gnu.org/licenses/>.
*/

#pragma once
#include "Event.h"
#include "EventUtils.h"

#define MOCAP_X 0
#define MOCAP_Y 1
#define MOCAP_Z 2
#define NO_JOINT 999

//-----------------------------------------------
// event arguments, this are used in oF to pass
// the data when notifying events

class EventArgs {};


enum
{
    FEAT_VELOCITY,
    FEAT_VELOCITY_MAG,
    FEAT_VELOCITY_MEAN,
    FEAT_ACCELERATION,
    FEAT_ACCELERATION_MAG,
    FEAT_ACCELERATION_MEAN,
    FEAT_ACCELERATION_TRAJECTORY,
    FEAT_ACCELERATION_TRAJECTORY_MEAN,
    FEAT_DISTANCETOTORSO,
    FEAT_RELATIVEPOSTOTORSO,
    FEAT_QOM,
    FEAT_CI
};

class MocapMaxEvent : public EventArgs {
    
public:
    
    unsigned int axis, joint, feature;
    float value;
    
    MocapMaxEvent() {}
    
    static ofEvent <MocapMaxEvent> events;
};

class MocapMinEvent : public EventArgs {
    
public:
    
    unsigned int axis, joint, feature;
    float value;
    
    MocapMinEvent() {}
    
    static ofEvent <MocapMinEvent> events;
};


