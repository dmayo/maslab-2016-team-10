#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <sstream>

using namespace std;
using namespace cv;

const int RED = 2;
const int GREEN =1;
const int BLACK = 0;
const int screenWidth = 160;	// width to downscale camera image to 
const int screenHeight = 120;   // height to downscale camera image to
const int minSizePx = 500;		// threshold for an object to be reported

int floodFillUtil(int x, int y, int currColor,int pxCount,int& maxY,int& maxX);
void detectObject(int i, int j);
int getColor(int i, int j);
char const*getColorName(int color);

Mat_<Vec3b> _img;			// global variable for convenience


int main(int argc, char** argv)
{     
    int c;
    Mat img;
    int i, j;
      
    VideoCapture capture(0);
    namedWindow("mainWin", CV_WINDOW_AUTOSIZE);
    bool readOk = true;
    capture.set(CV_CAP_PROP_FRAME_WIDTH,screenWidth);
    capture.set(CV_CAP_PROP_FRAME_HEIGHT,screenHeight);

    while (capture.isOpened()) {

        // read a frame from the webcam
        readOk = capture.read(img);

        // make sure we grabbed the frame successfully 
        if (!readOk) {
            std::cout << "No frame" << std::endl;
            break;
        }

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
         img = _img;
             
        // just for debugging purposes, show the frame in a window
        if (!img.empty()) imshow("mainWin", img);
        
        // look for break key to end
        c = waitKey(10);
        if (c == 27)
        {
            // clean up camera
            capture.release();
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
	   int distanceFromCenter = (j + center) - (screenWidth / 2);	// distance of objects horizontal center from  center of image
	   int distance = screenHeight-maxY;    // distance of lowermost point from the bottom of the screen
		
		std::cout << "Found a "  << getColorName(color) << " object";
		std::cout << " of size: " << pxCount <<  " and distance " << distance << std::endl;
		std::cout << " width: " << width <<  " and height " << height <<  std::endl;
		std::cout << " distanceFromCenter: " << distanceFromCenter << std::endl;
		std::cout << "===========================================================";
		}
	}
}

int floodFillUtil( int x, int y, int currColor, int pxCount, int& maxY, int& maxX)
{
    // based on the recursive flood fill algorithm but modified to:
    // count the number of contiguous pixels found as well as the maximum x and y values (Which are returned by reference)
    
    // Base cases
    if (x < 0 || x >= screenWidth || y < 0 || y >= screenHeight)
        return pxCount;
    if (getColor(y,x) != currColor)
        return pxCount;
 
	//found the color so set to black (to avoid in detectObject ) and increment
	 _img(y,x)[0] = 0;
	 _img(y,x)[1] = 0;
	 _img(y,x)[2] = 0;
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
