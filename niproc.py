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
    image_tuple.processedImage = image

    image_tuple = detectsquares(image_tuple)
    image_tuple = detectlines(image_tuple)
    image_tuple = detectcircles(image_tuple)
    image_tuple = detecttriangles(image_tuple)

    return addoverlay(image_tuple)


def addoverlay(image_tuple):
    height, width, channels = image_tuple.cleanImage.shape

    font = cv.FONT_HERSHEY_PLAIN
    x = int(width / 4)
    y = int(height / 5)
    fontsize = 15
    color = (0,0,255)
    linetype = cv.LINE_AA

    scale = 6 * fontsize            # allows symbols to grow/shrink based on text size

    squareCount = str(processed_img.squareCount)
    lineCount = str(processed_img.lineCount)
    circleCount = str(processed_img.circleCount)
    triangleCount = str(processed_img.triangleCount)

    cv.putText(image_tuple.processedImage, squareCount, (x, y), font, fontsize, color, linetype)
    cv.putText(image_tuple.processedImage, lineCount, (x, 2 * y), font, fontsize, color, linetype)
    cv.putText(image_tuple.processedImage, circleCount, (x, 3 * y), font, fontsize, color, linetype)
    cv.putText(image_tuple.processedImage, triangleCount, (x, 4 * y), font, fontsize, color, linetype)

    cv.rectangle(image_tuple.processedImage, (2 * x, y - 2 * scale), (2 * x + 2 * scale, y), color, -linetype)
    cv.line(image_tuple.processedImage, (2 * x + scale, 2 * y - 2 * scale), (2 * x + scale, 2 * y), color, linetype)
    cv.circle(image_tuple.processedImage, (2 * x + scale, 3 * y - scale), scale, color, -linetype)
    pts = np.array([[2 * x + scale, 4 * y - 2 * scale], [2 * x, 4 * y], [2 * x + 2 * scale, 4 * y]], np.int32)
    cv.fillPoly(image_tuple.processedImage, [pts], color)

    return image_tuple


def detectsquares(processed_img):
    #TODO
    print('Detected ', processed_img.squareCount, ' squares.')
    return processed_img


def detectlines(processed_img):
    
    #Use edge function
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    
    threshold = 60
    
    #Set mininmum detection length to 10 pixels
    minLineLength = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, 0, minLineLength, 20);
    
    if (lines is None or len(lines) == 0):
      return
    
    else: 
    print(len(lines))
    
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
