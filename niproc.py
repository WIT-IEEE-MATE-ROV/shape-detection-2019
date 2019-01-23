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
    font = cv.FONT_HERSHEY_PLAIN
    position = (20, 5*300) # Image is 5"x5", 300 pixel per inch
    fontsize = 5
    color = (0, 0, 255)
    linetype = 2
    cv.putText(image_tuple.processedImage,  # Image
               'Hello World!',              # Text to be written
               (0, 5*300),                  # Position (Image is 5" by 5", 300 ppi.)
               cv.FONT_HERSHEY_PLAIN,       # One of few font options
               5,                           # Font size
               (0, 0, 255),                 # Color
               2)                           # Line type

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
