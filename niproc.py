import cv2 as cv
import numpy as np
import collections
import imutils

"""
processimage
returns a 'processed image' named tuple.
The named tuple contains the image with an overlay, and counts of shapes
in 'squareCount', 'linecount', etc. 
"""
def processimage(image):
    image_tuple = collections.namedtuple('processedImage', ['cleanImage', 'squareCount', 'lineCount', 'circleCount', 'triangleCount'])
    Squares = 0
    Circles = 0
    Triangles = 0
    # Pull out only the black parts of the image
    # TODO: Should HSV be used here (Currently using BGR)
    range_lower = np.array([0, 0, 0])
    range_upper = np.array([15, 15, 15])
    blurred = cv.GaussianBlur(image, (11, 11), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, range_lower, range_upper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    image_tuple.cleanImage     = image
    image_tuple.processedImage = mask
    print (image_tuple.processedImage.dtype)

    image_tuple = detectshapes(image, mask, image_tuple, Squares, Circles, Triangles)

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


def detectsquares(c, image_tuple, Squares):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 4:
        (x, y, w, h) = cv.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else 'rectangle'
        Squares = Squares + 1
        image_tuple.squareCount = Squares
        processedImage.squareCount = Squares
        print('Detected ', image_tuple.squareCount, ' squares.')
    return shape
    return image_tuple
    return processedImage



def detectlines(c):
    # TODO
    print('Detected ', processed_img.lineCount, ' lines.')
    return processed_img


def detectcircles(c, image_tuple, Circles):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) > 5:
        shape = "Circle"
        Circles = Circles + 1
        image_tuple.circleCount = Circles
        print('Detected ', image_tuple.circleCount, ' circles.')
    return shape
    return image_tuple


def detecttriangles(c, image_tuple, Triangles):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3:
        shape = "triangle"
        Triangels = Triangles + 1
        image_tuple.triangleCount = Triangles
        print('Detected ', image_tuple.triangleCount, ' triangles.')
    return shape
    return image_tuple

def detectshapes(image,mask,image_tuple, Squares, Circles, Triangles):
    cnts = findcountours(mask)
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv.moments(c)

        cX = int((M["m10"] / (M["m00"] + 1e-7)))
        cY = int((M["m01"] / (M["m00"] + 1e-7)))

        shape = detectsquares(c, image_tuple, Squares)
        shape = detectcircles(c, image_tuple, Circles)
        shape = detecttriangles(c, image_tuple, Triangles)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = c.astype("int")
        cv.drawContours(image, [c], -1, (0, 255, 0), 2)
        processedImage = cv.putText(image, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
        return processedImage
        return image_tuple


def findcountours(mask):
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts
