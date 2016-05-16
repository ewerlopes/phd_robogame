#ifndef SKELETON_H_
#define SKELETON_H_

#include <Windows.h>
#include <Kinect.h>
#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <map>
#include "ofxKinectFeatures.h"


template<class Interface>
inline void SafeRelease(Interface *& pInterfaceToRelease)
{
    if(pInterfaceToRelease != 0)
    {
        pInterfaceToRelease->Release();
        pInterfaceToRelease = 0;
    }
}

class Skeleton{
public:
	Skeleton(); //constructor
	void skeletonTracking();
	void drawSkeleton(cv::Mat canvas, Joint joint[JointType::JointType_Count]);
	const cv::Scalar GREEN = cv::Scalar(0, 255, 0);
	cv::Point changeCoordinates(Joint joint[JointType::JointType_Count], int type);
private:
	int colorWidth;                                   // width for RGB Image
	int colorHeight;
	int depthWidth;                                   // width for Depth Image
	int depthHeight;
	IKinectSensor* pSensor;
	IColorFrameSource* pColorSource;
	IBodyFrameSource* pBodySource;
	IDepthFrameSource* pDepthSource;
	IColorFrameReader* pColorReader;
	IBodyFrameReader* pBodyReader;
	IDepthFrameReader* pDepthReader;
	IFrameDescription* pColorDescription;
	IFrameDescription* pDepthDescription;
	ICoordinateMapper* pCoordinateMapper;

	//Kinect feature extractor object.
	ofxKinectFeatures featExtractor;
};


#endif /* SKELETON_H_ */
