import cv2
from time import sleep
import numpy as np
import board
import neopixel

# Define functions for image processing and LED display
# (Your extractROI, discretizeImage, and imageToLED functions)

def extractROI(image, xCenter, yCenter, windowSize):
    # Your extractROI function code here
    x_startIdx=int(xCenter-windowSize[0]/2)
    y_startIdx=int(yCenter-windowSize[1]/2)
    x_endIdx=int(xCenter+windowSize[0]/2)
    y_endIdx=int(yCenter+windowSize[1]/2)
    roiImage=image[x_startIdx:x_endIdx,y_startIdx:y_endIdx,:]

    return roiImage
def discretizeImage(image, noLevels):
    # Your discretizeImage function code here
    normalizedImage=image/255
    discretizedImage=np.floor(normalizedImage*noLevels).astype(int)
    multiplier=255/noLevels
    discretizedImage=np.floor(discretizedImage*multiplier).astype(np.uint8) #Rescale to range 0-255
    return discretizedImage

def imageToLED(discreteImageRaw, pixels, colorVal):
    # Your imageToLED function code here
    discreteImage=discreteImageRaw[:,:,1]
    discreteImage=discreteImage.flatten()
    pixelArray=np.zeros((len(discreteImage),3))
    pixelArray[:,colorVal]=discreteImage
    pixelArray=pixelArray.astype(int) # Convert to int
    pixelTuple=[tuple(x) for x in pixelArray] #Convert to correctly dimensioned tuple array
    pixels[:]=pixelTuple
        
    return pixels
    
# Parameters for LED grid and video processing
numNeopixels_x = 16
numNeopixels_y = 16
windowSize = (numNeopixels_x, numNeopixels_y)
xCenter = 160 // 2  # Assuming video resolution is 160x120
yCenter = 120 // 2
noLevels = 255
colorVal = 2

# Initialize Neopixel LED
pixelPin = board.D18
numPixels = numNeopixels_x * numNeopixels_y
colorOrder = neopixel.GRB
pixels = neopixel.NeoPixel(pixelPin, numPixels, auto_write=False, pixel_order=colorOrder)

# Open the video file
video_file = '/home/silolab_ksh/Desktop/0214.mp4'
cap = cv2.VideoCapture(video_file)

while cap.isOpened():
    # Read a frame from the video file
    ret, frame = cap.read()
    if not ret:
        break

    # Extract ROI, discretize image, and convert to LED values
    roi_frame = extractROI(frame, xCenter, yCenter, windowSize)
    discretized_frame = discretizeImage(roi_frame, noLevels)
    processed_frame = imageToLED(discretized_frame, pixels, colorVal)

    # Display the LED values on Neopixel LED
    pixels = processed_frame
    pixels.show()

    # Add delay (adjust according to your desired frame rate)
    sleep(0.1)

# Release video capture object
cap.release()
