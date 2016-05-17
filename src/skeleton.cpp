#include "skeleton.hpp"

cv::Point Skeleton::changeCoordinates(Joint joint[JointType::JointType_Count], int type)
{
	ColorSpacePoint colorSpacePoint = { 0 };
	pCoordinateMapper->MapCameraPointToColorSpace(joint[type].Position, &colorSpacePoint);
	int x = static_cast<int>(colorSpacePoint.X);
	int y = static_cast<int>(colorSpacePoint.Y);

	return cv::Point(x, y);
}

Skeleton::Skeleton() {
	featExtractor.setup(JointType_Head, JointType_SpineMid);	//Necessary for the featExtractor calculations.
	output.open("LogFile.csv");
}

void Skeleton::drawSkeleton(cv::Mat canvas, Joint joint[JointType::JointType_Count])
{
	cv::line(canvas, changeCoordinates(joint, JointType_Head), changeCoordinates(joint, JointType_Neck), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_Neck), changeCoordinates(joint, JointType_SpineShoulder), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineShoulder), changeCoordinates(joint, JointType_ShoulderLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineShoulder), changeCoordinates(joint, JointType_ShoulderRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineShoulder), changeCoordinates(joint, JointType_SpineMid), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_ShoulderLeft), changeCoordinates(joint, JointType_ElbowLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_ShoulderRight), changeCoordinates(joint, JointType_ElbowRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_ElbowLeft), changeCoordinates(joint, JointType_WristLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_ElbowRight), changeCoordinates(joint, JointType_WristRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_WristLeft), changeCoordinates(joint, JointType_HandLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_WristRight), changeCoordinates(joint, JointType_HandRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_HandLeft), changeCoordinates(joint, JointType_HandTipLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_HandRight), changeCoordinates(joint, JointType_HandTipRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_WristLeft), changeCoordinates(joint, JointType_ThumbLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_WristRight), changeCoordinates(joint, JointType_ThumbRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineMid), changeCoordinates(joint, JointType_SpineBase), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineBase), changeCoordinates(joint, JointType_HipLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_SpineBase), changeCoordinates(joint, JointType_HipRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_HipLeft), changeCoordinates(joint, JointType_KneeLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_HipRight), changeCoordinates(joint, JointType_KneeRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_KneeLeft), changeCoordinates(joint, JointType_AnkleLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_KneeRight), changeCoordinates(joint, JointType_AnkleRight), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_AnkleLeft), changeCoordinates(joint, JointType_FootLeft), GREEN, 3);
	cv::line(canvas, changeCoordinates(joint, JointType_AnkleRight), changeCoordinates(joint, JointType_FootRight), GREEN, 3);
} 

void Skeleton::skeletonTracking()
{
    cv::setUseOptimized(true);

    // sensor
    HRESULT hResult = S_OK;
    hResult = GetDefaultKinectSensor(&pSensor);
    if (FAILED(hResult))
    {
        std::cerr << "Error: GetDefaultKinectSensor" << std::endl;
        exit(-1);
    }

    hResult = pSensor->Open();
    if (FAILED(hResult))
    {
        std::cerr << "Error: IKinectSensor::Open()" << std::endl;
        exit(-1);
    }

    // Source
    hResult = pSensor->get_ColorFrameSource(&pColorSource);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IKinectSensor::get_ColorFrameSource()" << std::endl;
        exit(-1);
    }

    hResult = pSensor->get_BodyFrameSource(&pBodySource);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IKinectSensor::get_BodyFrameSource()" << std::endl;
        exit(-1);
    }

    hResult = pSensor->get_DepthFrameSource(&pDepthSource);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IKinectSensor::get_DepthFrameSource()" << std::endl;
        exit(-1);
    }

    // Reader
    hResult = pColorSource->OpenReader(&pColorReader);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IColorFrameSource::OpenReader()" << std::endl;
        exit(-1);
    }

    hResult = pBodySource->OpenReader(&pBodyReader);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IBodyFrameSource::OpenReader()" << std::endl;
        exit(-1);
    }

    hResult = pDepthSource->OpenReader(&pDepthReader);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IDepthFrameSource::OpenReader()" << std::endl;
        exit(-1);
    }

    // Description
    hResult = pColorSource->get_FrameDescription(&pColorDescription);
    if(FAILED(hResult))
    {
        std::cerr << "Error: IColorFrameSource::get_FrameDescription()" << std::endl;
        exit(-1);
    }

    hResult = pDepthSource->get_FrameDescription(&pDepthDescription);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IDepthFrameSource::get_FrameDescription()" << std::endl;
        exit(-1);
    }

    colorWidth = 0;
    colorHeight = 0;
    depthWidth = 0;
    depthHeight = 0;
    pColorDescription->get_Width(&colorWidth);   // 1920
    pColorDescription->get_Height(&colorHeight); // 1080
    pDepthDescription->get_Width(&depthWidth);   // 512
    pDepthDescription->get_Height(&depthHeight); // 424
    unsigned int colorbufferSize = colorWidth * colorHeight * 4 * sizeof(unsigned char);
    unsigned int depthbufferSize = depthWidth * depthHeight * 4 * sizeof(unsigned char);

    cv::Mat colorBufferMat(colorHeight, colorWidth, CV_8UC4);
    cv::Mat depthBufferMat(depthHeight, depthWidth, CV_16UC1);
    cv::Mat bodyMat(colorHeight/2, colorWidth/2, CV_8UC4);
    cv::Mat depthMat(depthHeight, depthWidth, CV_8UC1);
    std::string colorWinName = "Skeleton RGB";
    std::string depthWinName = "Skeleton Depth";
    cv::namedWindow(colorWinName);
    cv::namedWindow(depthWinName);

    // Color Table
    cv::Vec3b color[BODY_COUNT];
    color[0] = cv::Vec3b(255, 0, 0);
    color[1] = cv::Vec3b(0, 255, 0);
    color[2] = cv::Vec3b(0, 0, 255);
    color[3] = cv::Vec3b(255, 255, 0);
    color[4] = cv::Vec3b(255, 0, 255);
    color[5] = cv::Vec3b(0, 255, 255);

    // Range (Range of Depth is 500-8000[mm], Range of Detection is 500-45000[mm])
    unsigned short min = 0;
    unsigned short max = 0;
    pDepthSource->get_DepthMinReliableDistance(&min);
    pDepthSource->get_DepthMaxReliableDistance(&max);
    std::cout << "Range: " << min << " - " << max << std::endl;

    // Coordinate Mapper
    hResult = pSensor->get_CoordinateMapper(&pCoordinateMapper);
    if (FAILED(hResult))
    {
        std::cerr << "Error: IKinectSensor::get_CoordinateMapper()" << std::endl;
        exit(-1);
    }

    while(1)
    {
        // Frame
        IColorFrame* pColorFrame = 0;
        IDepthFrame* pDepthFrame = 0;
        hResult = pDepthReader->AcquireLatestFrame(&pDepthFrame);
		if (SUCCEEDED(hResult))
		{
			hResult = pDepthFrame->AccessUnderlyingBuffer(&depthbufferSize, reinterpret_cast<UINT16**>(&depthBufferMat.data));
			if (SUCCEEDED(hResult)) {
				if (SUCCEEDED(depthHeight) && SUCCEEDED(depthWidth)) {
					UINT16 *depthBuffer = new UINT16[depthHeight * depthWidth];
					hResult = pDepthFrame->CopyFrameDataToArray(depthHeight * depthWidth, depthBuffer);
					if (SUCCEEDED(hResult)) {
						cv::Mat depthMap = cv::Mat(depthHeight, depthWidth, CV_16U, depthBuffer);
						cv::Mat img0 = cv::Mat::zeros(depthHeight, depthWidth, CV_8UC1);
						cv::Mat img1;
						double scale = 255.0 / (max -
							min);
						depthMap.convertTo(img0, CV_8UC1, scale);
						applyColorMap(img0, img1, cv::COLORMAP_JET);
						depthMat = img1;
					}
				}
			}
        }
        hResult = pColorReader->AcquireLatestFrame(&pColorFrame);
        if (SUCCEEDED(hResult))
        {
            hResult = pColorFrame->CopyConvertedFrameDataToArray(colorbufferSize, reinterpret_cast<BYTE*>(colorBufferMat.data), ColorImageFormat::ColorImageFormat_Bgra);
            if (SUCCEEDED(hResult))
                cv::resize(colorBufferMat, bodyMat, cv::Size(), 0.5, 0.5);
        }
        // SafeRelease(pColorFrame);

        IBodyFrame* pBodyFrame = 0;
        hResult = pBodyReader->AcquireLatestFrame(&pBodyFrame);
        if (SUCCEEDED(hResult))
        {
            IBody* pBody[BODY_COUNT] = {0};
            hResult = pBodyFrame->GetAndRefreshBodyData(BODY_COUNT, pBody);
			if (SUCCEEDED(hResult))
			{
				for (int count = 0; count < BODY_COUNT; count++)
				{
					BOOLEAN bTracked = false;
					hResult = pBody[count]->get_IsTracked(&bTracked);
					if (SUCCEEDED(hResult) && bTracked)
					{
						Joint joint[JointType::JointType_Count];
						hResult = pBody[count]->GetJoints(JointType::JointType_Count, joint);
						if (SUCCEEDED(hResult) && TrackingConfidence_High)
						{
							std::map <int, ofPoint> toFeatjoints; //this is the map of joints need for the KinectFeatures extractor 
							// Joints
							for (int type = 0; type < JointType::JointType_Count; type++)
							{
								Joint j = joint[type];
								toFeatjoints[type] = ofPoint(j.Position.X, j.Position.Y, j.Position.Z); // storing the joints.
								cv::Point jointPoint = changeCoordinates(joint, type);
								if ((jointPoint.x >= 0) && (jointPoint.y >= 0) && (jointPoint.x < colorWidth) && (jointPoint.y < colorHeight))
								{
									cv::circle(colorBufferMat, jointPoint, 8, static_cast<cv::Scalar>(color[count]), -1, CV_AA);
								}
							}
							featExtractor.update(toFeatjoints); //calculating skeleton data.
							std::cout << "Qnt of motion: " << featExtractor.getQom() << std::endl; //getting data.
							output << featExtractor.getQom() << std::endl; //saving data to the log file.
							std::cout << "Contraction index: " << featExtractor.getCI() << std::endl; //getting data.
							drawSkeleton(colorBufferMat, joint);
						}

						// Lean
						PointF amount;
						hResult = pBody[count]->get_Lean(&amount);
						if (SUCCEEDED(hResult))
							std::cout << "Lean amount: " << amount.X << ", " << amount.Y << std::endl;
					}
				}
				cv::resize(colorBufferMat, bodyMat, cv::Size(), 0.5, 0.5);
			}
			for (int count=0; count<BODY_COUNT; count++)
			{
				SafeRelease(pBody[count]);
			}
		}
		SafeRelease(pColorFrame);
		SafeRelease(pBodyFrame);
		SafeRelease(pDepthFrame);

		// save color image, depth image
		cv::imshow(colorWinName, bodyMat);
        cv::imshow(depthWinName, depthMat);

		if (cv::waitKey(10) == VK_ESCAPE)
			break;
    }

    SafeRelease(pColorSource);
    SafeRelease(pBodySource);
    SafeRelease(pColorReader);
    SafeRelease(pBodyReader);
    SafeRelease(pColorDescription);
    SafeRelease(pCoordinateMapper);
    SafeRelease(pDepthSource);
    SafeRelease(pDepthReader);
    SafeRelease(pDepthDescription);
    if (pSensor)
        pSensor->Close();
    SafeRelease(pSensor);
    cv::destroyAllWindows();

	//Close file.
	output.close();
}
