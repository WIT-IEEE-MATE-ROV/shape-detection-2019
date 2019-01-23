import cv2 as cv
import numpy as np
import collections


"""
processimage
returns a 'processed image' named tuple.
The named tuple contains the image with an overlay, and counts of shapes
in 'squareCount', 'linecount', etc. 
"""
def processimage(image):
    image_tuple = collections.namedtuple('processedImage', ['cleanImage', 'squareCount', 'lineCount', 'circleCount', 'triangleCount'])

    # Pull out only the black parts of the image
    # TODO: Should HSV be used here (Currently using BGR)
    range_lower = np.array([0, 0, 0])
    range_upper = np.array([15, 15, 15])
    mask = cv.inRange(image, range_lower, range_upper)

    image_tuple.cleanImage     = image
    image_tuple.processedImage = mask

    image_tuple = detectsquares(image_tuple)
    image_tuple = detectlines(image_tuple)
    image_tuple = detectcircles(image_tuple)
    image_tuple = detecttriangles(image_tuple)

    return addoverlay(image_tuple)


def addoverlay(image_tuple):
    height = 410                                       #height of new blank image (px)
    width = 200                                        #width of new blank image (px)
    overlay = np.zeros((height,width,3), np.uint8)     #create a new black image
    overlay[:,0:width] = (255,255,255)                 #recolor the image white

    font = cv.FONT_HERSHEY_PLAIN
    position = (20, 5*300)                             # Image is 5"x5", 300 pixel per inch
    fontsize = 5
    color = (0, 0, 255)
    linetype = 2

    """cv.putText(img,  # Image
               'Hello World!',              # Text to be written
               (20, 5*300),                    # Position (Image is 5" by 5", 300 ppi.)
               cv.FONT_HERSHEY_PLAIN,       # One of few font options
               5,                           # Font size
               (0, 0, 255),                 # Color
               2)                           # Line type
    """
    
    maxPer = 6
    maxTotal = 15

    squareCount = processed_img.squareCount
    squareCount = str(squareCount)
    lineCount = processed_img.lineCount
    lineCount = str(lineCount)
    circleCount = processed_img.circleCount
    circleCount = str(circleCount)
    triangleCount = processed_img.triangleCount
    triangleCount = str(triangleCount)
    
    
    """squareCount = 1
    squareCount = str(squareCount)
    lineCount = 1
    lineCount = str(lineCount)
    circleCount = 1
    circleCount = str(circleCount)
    triangleCount = 1
    triangleCount = str(triangleCount)
    """

    """if ((squareCount or lineCount or circleCount or triangleCount) <= maxPer) and 
       ((squareCount + lineCount + circleCount + triangleCount) <= maxTotal):
    """
    cv.putText(overlay, squareCount, (30,80), font, fontsize, color, linetype, cv.LINE_AA)
    cv.putText(overlay, lineCount, (30,180), font, fontsize, color, linetype, cv.LINE_AA)
    cv.putText(overlay, circleCount, (30,280), font, fontsize, color, linetype, cv.LINE_AA)
    cv.putText(overlay, triangleCount, (30,380), font, fontsize, color, linetype, cv.LINE_AA)

    cv.rectangle(overlay, (120,30), (170,80), color, -linetype)
    cv.line(overlay, (145,130), (145,180), color, 2*linetype)
    cv.circle(overlay, (145,255), 25, color, -linetype)
    pts = np.array([[145,330],[120,380],[170,380]], np.int32)
    cv.fillPoly(overlay, [pts], color)
    
    """else:
        retry
        after retrying x times, break
    """

    cv.imshow('overlay', overlay)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return image_tuple


def detectsquares(processed_img):
    #TODO
    print('Detected ', processed_img.squareCount, ' squares.')
    return processed_img


def detectlines(processed_img):
    # TODO
    print('Detected ', processed_img.lineCount, ' lines.')
    return processed_img


def detectcircles(processed_img):
    # TODO
    print('Detected ', processed_img.circleCount, ' circles.')
    return processed_img


def detecttriangles(processed_img):
    # TODO
    print('Detected ', processed_img.triangleCount, ' triangles.')
    return processed_img
