/*
*** KinectFeatures

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

#ifndef KinectFeatures_h
#define KinectFeatures_h

#include "MocapElement.h"
#include "MocapEvents.h"
#include <algorithm>
#include <math.h>
#include <numeric>

namespace filter
{
    enum
    {
        SOFT = 0,
        MED = 1,
        HARD = 2
    };
} // namespace filter

class KinectFeatures {
public:
    KinectFeatures();
    KinectFeatures(int head, int torso);
    
    void setup(int head, int torso);
    void update(map<int, ofPoint> joints);
    MocapElement* getElement(int _id);
    
    void setFilterLevel(int filterLevel);
    
    void setDepth(int depth);
    int getDepth();

	//auxiliary function
	// re-maps a number from one range to another.
	float remapRange(float value, float fromMin, float fromMax, float toMin, float toMax); 
    
    //DESCIPTOR GETTERS
    //JOINT DESCRIPTORS
    ofPoint getPosition(int j);
    vector<ofPoint> getPositionHistory(int j);
    vector<ofPoint> getPositionHistory(int j, int frames);
    
    ofPoint getPositionFiltered(int j);
    vector<ofPoint> getPositionFilteredHistory(int j);
    vector<ofPoint> getPositionFilteredHistory(int j, int frames);
    
    ofPoint getVelocity(int j);
    vector<ofPoint> getVelocityHistory(int j);
    vector<ofPoint> getVelocityHistory(int j, int frames);
    float getVelocityMagnitude(int j);
    ofPoint getVelocityMean(int j, int frames = 30);
    float getVelocityMagnitudeMean(int j, int frames = 30);
    
    ofPoint getAcceleration(int j);
    vector<ofPoint> getAccelerationHistory(int j);
    vector<ofPoint> getAccelerationHistory(int j, int frames);
    float getAccelerationMagnitude(int j);
    ofPoint getAccelerationMean(int j, int frames = 30);
    float getAccelerationMagnitudeMean(int j, int frames = 30);
    
    
    float getAccelerationTrajectory(int j);
    vector<float> getAccelerationTrajectoryHistory(int j);
    vector<float> getAccelerationTrajectoryHistory(int j, int frames);
    float getAccelerationTrajectoryMean(int j, int frames = 30);
    
    float getDistanceToTorso(int j);
    vector<float> getDistanceToTorsoHistory(int j);
    vector<float> getDistanceToTorsoHistory(int j, int frames);
    
    ofPoint getRelativePositionToTorso(int j);
    vector<ofPoint> getRelativePositionToTorsoHistory(int j);
    vector<ofPoint> getRelativePositionToTorsoHistory(int j, int frames);
    
    //SPECIAL DESCRIPTORS
    float getAngle(int j1, int j2, int j3);
	vector<float> getHeadXYAngle(float headPosX, float headPosY, float headPosZ);
    
    //OVERALL DESCRIPTORS
    float getQom();
    vector<float> getQomHistory();
    vector<float> getQomHistory(int frames);
    
	float getCI();
    vector<float> getCIHistory();
    vector<float> getCIHistory(int frames);
//    float getSymmetry();
//    float getYMaxHands();

	float getFluidity();
	vector<float> getFluidityHistory();
	vector<float> getFluidityHistory(int frames);

    
    bool isNewDataAvailable();
    
private:
    int head_, torso_;
    
    template <typename T>
    vector<T> createVector (T element);
    
    float *aFilter;
    float *bFilter;
    float *aLpd1;
    float *bLpd1;
    float *aLpd2;
    float *bLpd2;
    
    //overall descriptors
    vector<float> qom_, ci_, fluidity_;//, symmetry_, yMaxHands_;
    vector<float> meanVels_, meanAccs_;
    
    bool newValues_;
    
    vector<MocapElement> elements_;
    
    int depth_;
    
    void computeJointDescriptors(int jointId, ofPoint jointPos, const float &h);
    ofPoint applyFilter (vector<ofPoint> x, vector<ofPoint> y, float *a, float *b);
    void checkMaxAndMin(vector<ofPoint> descriptorHistory, unsigned int jointId, unsigned int feature);
    void checkMaxAndMin(vector<float> descriptorHistory, unsigned int jointId, unsigned int feature);
    
    //Functor to look for mocap elements matching a Joint
    struct MatchId
    {
        MatchId(const int& j) : j_(j) {}
        bool operator()(MocapElement& obj) const
        {
            return obj.getElementId() == j_;
        }
    private:
        const int& j_;
    };
};

#endif
