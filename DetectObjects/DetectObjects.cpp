#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <sstream>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <math.h>       

#define PI 3.14159265

using namespace std;
using namespace cv;

const int RED = 2;
const int GREEN =1;
const int BLACK = 0;
const int screenWidth = 160;	// width to downscale camera image to 
const int screenHeight = 120;   // height to downscale camera image to
const int minSizePx = 25;		// threshold for an object to be reported. TODO: Need to tune
const int cropStartFromXCoordinate = 10;  
const int cropStarFromYCoordinate = 20;
const int cropWidth = 140;
const int cropHeight = 100;
const int blockWidth =	2;		// block width in inches
const int focalLength = 160;	// focal length of camera
char const* namedPipe = "./vision";

int floodFillUtil(int x, int y, int currColor,int pxCount,int& maxY,int& maxX);
void detectObject(int i, int j);
int getColor(int i, int j);
char const*getColorName(int color);
float getActualDistance(int width);
float getActualHorizontalDistance(int pxHorizontalDistance,int pxBlockWidth);
int getAngle(float actualDistance, float actualHorizontalDistance);


Mat_<Vec3b> _img;			
Mat img;
Mat_<uchar> _binaryImage[3];

vector<Vec4i> hierarchy;
 

int main(int argc, char** argv)
{     
    int c;   
    Mat origImg;
    int i, j;
    int fd;
  	int counter=0;
  	bool debug = argc > 1 ;

    VideoCapture capture(0);
    if (debug)
    	namedWindow("mainWin", CV_WINDOW_AUTOSIZE);
    bool readOk = true;
    capture.set(CV_CAP_PROP_FRAME_WIDTH,screenWidth);
    capture.set(CV_CAP_PROP_FRAME_HEIGHT,screenHeight);
    
    
        
    while (capture.isOpened()) {

        // read a frame from the webcam
        readOk = capture.read(origImg);

        // make sure we grabbed the frame successfully 
        if (!readOk) {
            std::cout << "No frame" << std::endl;
            break;
        }
        
        // crop image
        Mat img = origImg(Rect(cropStartFromXCoordinate,cropStarFromYCoordinate,cropWidth,cropHeight));
         // zero out the  binary image for use with contour detection algorithm
        _binaryImage[RED] = Mat::zeros(img.rows,img.cols, CV_8UC1);
        _binaryImage[GREEN] = Mat::zeros(img.rows,img.cols, CV_8UC1);
       
        
        // some boilerplate code
        int nChannels = img.channels();
        int nRows = img.rows;
        int nCols = img.cols * nChannels;

        if (img.isContinuous())
        {
            nCols *= nRows;
            nRows = 1;
        }
        // need this object to be able to randomly access a pixel 
        _img = img;        
        // scan through each pixel and look for a red or green one.
        //  if we find one, call detectObject to see if its part of a block
         for( int i = 0; i < img.rows; ++i)
            for( int j = 0; j < img.cols; ++j )
               {             
                  detectObject(i,j);   
			   }     
        img =  _img;
        
        // Find the largest rectangle
		vector<vector<Point> > contours;	
		int largest_area=25;
        int largest_contour_index=0;
        Rect bounding_rect;
		 
		for (int images = 1; images <=2;images++)
		{
			findContours( _binaryImage[images], contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
			for( int i = 0; i< contours.size(); i++ ) // iterate through each contour. 
			{
			   double a=contourArea( contours[i],false);  
			   if(a>largest_area)
			   {
				   largest_area=a;
				   largest_contour_index=i;               
				   bounding_rect=boundingRect(contours[i]);
			   }
			}
      	}
      	
	  	rectangle(img, bounding_rect,  Scalar(0,255,0),1, 8,0); 
	  	
	  	// report on  position
	  	// only if its a square
	  	if (std::abs(1 - (double)bounding_rect.width / bounding_rect.height)<=.02)
	  	{
			float distance = getActualDistance(bounding_rect.width);
			int center = bounding_rect.width / 2;									// center of the object
			int distanceFromCenter = (bounding_rect.x + center) - (cropWidth / 2);	// distance of objects horizontal center from  center of image
			float actualDistanceFromCenter = getActualHorizontalDistance( distanceFromCenter, bounding_rect.width);
			//int distance = cropHeight-(bounding_rect.height+bounding_rect.y);    // distance of lowermost point from the bottom of the screen
			int angle = getAngle(distance, actualDistanceFromCenter);
			if (distance > 0)	
			{
				std::ostringstream strm;
				//strm	 <<  "{\"d\":" << distance << ",\"dc\": " << distanceFromCenter << "}" << std::endl;
				strm	 << distance << " " << angle << std::endl;
				if (debug)
					std::cout	 <<  "{\"distance\": " << distance << "inches , \"angle\": " << angle << " degrees }" << std::endl;
				// write position data to named pipe
				mkfifo(namedPipe, 0666);
				fd = open(namedPipe, O_WRONLY | O_NONBLOCK);
				std::string numStr = strm.str();
				const char* cstr1 = numStr.c_str();
				write(fd, cstr1, sizeof(cstr1));
				close(fd);
			}
		}
		 // just for debugging purposes, show the frame in a window
        if (!img.empty() && debug) imshow("mainWin", img);
       
        // look for break key to end
        c = waitKey(10);
        if (c == 27)
        {
            // clean up camera
            capture.release();
             /* remove the FIFO */
            unlink(namedPipe);
            break;
        }
    }
}

void detectObject(int i, int j)
{
  uchar r, g, b; 
  b=   _img(i,j)[0];
  g =  _img(i,j)[1];
  r =  _img(i,j)[2];
  
   int color = getColor(i,j);
   // its a color we care about
   if (color > BLACK)
	   {
	   int pxCount = 0;
	   int maxY = 0;
	   int maxX = 0;
  	  	
	   pxCount = floodFillUtil( j, i, color,pxCount,maxY,maxX);
	   if (pxCount >= minSizePx)			// determine if the size of the object is above the reporting threshold
	   {
		   int width = maxX - j;
		   int height = maxY -i;
		   int center = width / 2;		// center of the object
		   int distanceFromCenter = (j + center) - (cropWidth / 2);	// distance of objects horizontal center from  center of image
		   int distance = cropHeight-maxY;    // distance of lowermost point from the bottom of the screen
		
			
		}
	}	
}

int floodFillUtil( int x, int y, int currColor, int pxCount, int& maxY, int& maxX)
{
    // based on the recursive flood fill algorithm but modified to:
    // count the number of contiguous pixels found as well as the maximum x and y values (Which are returned by reference)
    
    // Base cases
    if (x < 0 || x >= cropWidth || y < 0 || y >= cropHeight)
        return pxCount;
    if (getColor(y,x) != currColor)
    {
       
        return pxCount;
    }
     
	//found the color so set to a shade of grey
	if (currColor*100 <=255)
	{
	 _img(y,x)[0] = 100*currColor;
	 _img(y,x)[1] = 100*currColor;
	 _img(y,x)[2] = 100*currColor;
	}
	 
	 // mark the pixel in the appropriate binary image
	
	 _binaryImage[currColor](y,x) =100*currColor;
	
   pxCount++;
   if (y > maxY)
     	maxY = y;
    if (x > maxX)
        maxX = x;
 
    // Recurse for north, east, south and west
   pxCount = floodFillUtil( x+1, y, currColor,pxCount,maxY,maxX);
   pxCount = floodFillUtil( x-1, y, currColor,pxCount,maxY,maxX);
   pxCount = floodFillUtil( x, y+1, currColor,pxCount,maxY,maxX);
   pxCount = floodFillUtil( x, y-1, currColor,pxCount,maxY,maxX);
   return pxCount;
}

int getColor(int i,int j )
{
   uchar r, g, b;
    b=   _img(i,j)[0];
	g =  _img(i,j)[1];
	r =  _img(i,j)[2];
	if ((r > g*1.3) && (r > b*1.3))
	{
	  return RED;
	}
	// detect green
	if ((g > r*1.3) && (b > r*1.3))
	{
	  return GREEN;
	}	
	return 0;
}

char const*getColorName(int color)
{
	if (color == RED)
		return  "Red";
	if (color == GREEN)
		return  "Green";
	return "Other";
}

float getActualDistance(int pxWidth)
{
	// converts width of detected block to distance using triangle similarity
	if (pxWidth > 0 )
		return (blockWidth * focalLength) / pxWidth;
	else 	
		return 0;

}

float getActualHorizontalDistance(int pxHorizontalDistance,int pxBlockWidth)
{
	if (abs(pxHorizontalDistance) > 0 && pxBlockWidth > 0)
		return (blockWidth * pxHorizontalDistance) / pxBlockWidth;
	else
		return 0;
}

int getAngle(float actualDistance, float actualHorizontalDistance)
{
	
	if (actualDistance >0 && abs(actualHorizontalDistance) > 0)
	{
		float sinx =  actualHorizontalDistance /actualDistance  ;
		return asin (sinx) * 180.0 / PI;
	}
	return 0;
}




