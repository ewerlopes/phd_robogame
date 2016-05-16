//
//  ofxMocapEvents.h
//  kinectFeaturesExample
//
//  Created by Álvaro Sarasúa Berodia on 29/01/15.
//
//

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

class ofEventArgs {};


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

class MocapMaxEvent : public ofEventArgs {
    
public:
    
    unsigned int axis, joint, feature;
    float value;
    
    MocapMaxEvent() {}
    
    static ofEvent <MocapMaxEvent> events;
};

class MocapMinEvent : public ofEventArgs {
    
public:
    
    unsigned int axis, joint, feature;
    float value;
    
    MocapMinEvent() {}
    
    static ofEvent <MocapMinEvent> events;
};


