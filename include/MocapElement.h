/*
*** MocapElement.

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

#ifndef MocapElement_h
#define MocapElement_h

#include "Vec3f.h"
#include <vector>

typedef ofVec3f ofPoint;

class MocapElement{
public:
    MocapElement();
    MocapElement(int elementId, int depth);
    
    unsigned int getElementId();
    void setElementId(int newId);
    
    void setHistoryDepth(int depth);    
    
    std::vector<ofPoint> getPosition();
    void setPosition(ofPoint position);
    
	std::vector<ofPoint> getPositionFiltered();
    void setPositionFiltered(ofPoint positionFiltered);
    
	std::vector<ofPoint> getVelocity();
    void setVelocity(ofPoint velocity);
    
	std::vector<ofPoint> getAcceleration();
    void setAcceleration(ofPoint acceleration);
    
	std::vector<float> getAccelerationTrajectory();
    void setAccelerationTrajectory(float accelerationTrajectory);
    
	std::vector<float> getDistanceToTorso();
    void setDistanceToTorso(float distanceToTorso);
    
	std::vector<ofPoint> getRelativePositionToTorso();
    void setRelativePositionToTorso(ofPoint relativePositionToTorso);

private:
    int historyDepth_;
    int elementId_;
    
	std::vector<ofPoint> position_;
	std::vector<ofPoint> positionFiltered_;
	std::vector<ofPoint> velocity_;
	std::vector<ofPoint> acceleration_;
	std::vector<float> accelerationTrajectory_;
	std::vector<float> distanceToTorso_;
	std::vector<ofPoint> relativePositionToTorso_;
};

#endif
