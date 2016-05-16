/*
 ofxKinectFeatures
 Copyright © 2014 Music Technology Group - Universitat Pompeu Fabra / Escola Superior de Música de Catalunya
 
 This file is part of ofxKinectFeatures, created and maintained by Álvaro Sarasúa <http://alvarosarasua.wordpress.com>
 
 ofxKinectFeatures is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License (LGPL v3) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 
 ofxKinectFeatures is distributed in the hope that it will be useful, but WITHOUT  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License (LGPL v3).
 
 You should have received a copy of the GNU Lesser General Public License long within the ofxKinectFeatures SW package.  If not, see <http://www.gnu.org/licenses/>.
 
 If you are willing to get a (non FOSS) commercial license, please contact us at mtg@upf.edu
 */

#ifndef ofxMocapElement_h
#define ofxMocapElement_h

#include "ofVec3f.h"
#include <vector>

typedef ofVec3f ofPoint;

class ofxMocapElement{
public:
    ofxMocapElement();
    ofxMocapElement(int elementId, int depth);
    
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
