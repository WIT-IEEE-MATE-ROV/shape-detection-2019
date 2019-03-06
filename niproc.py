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
    image_tuple = collections.namedtuple('processedImage', ['cleanImage','HSV','BlackWhite', 'squareCount', 'lineCount', 'circleCount', 'triangleCount'])
    # Pull out only the black parts of the image
    # TODO: Should HSV be used here (Currently using BGR)
    k1 = np.ones((15, 15), np.uint8)
    k2 = np.ones((12, 12), np.uint8)
    range_lower = np.array([0, 0, 0])
    range_upper = np.array([255,180,70])
    blurred = cv.GaussianBlur(image, (5, 5), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    image_tuple.HSV = hsv

    mask = cv.inRange(hsv, range_lower, range_upper)
    mask = cv.dilate(mask, None, iterations=3)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, k1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, k2)
    image_tuple.BlackWhite = mask
    image_tuple.cleanImage     = image
    image_tuple.processedImage = mask
    print (image_tuple.processedImage.dtype)

    image_tuple = detectshapes(image_tuple)
    image_tuple = addoverlay(image_tuple)
    return image_tuple


def addoverlay(image_tuple):
    height, width, channels = image_tuple.cleanImage.shape

    font = cv.FONT_HERSHEY_PLAIN
    x = int(width / 4)
    y = int(height / 5)
    fontsize = 5
    color = (0, 0, 255)
    linetype = cv.LINE_AA

    scale = 6 * fontsize  # allows symbols to grow/shrink based on text size

    if type(image_tuple.squareCount) != int:
        squareCount = '0'
    else :
        squareCount = str(image_tuple.squareCount)

    if type(image_tuple.lineCount) != int:
        lineCount = '0'
    else :
        lineCount = str(image_tuple.lineCount)

    if type(image_tuple.triangleCount) !=int:
        circleCount = '0'
    else:
        circleCount = str(image_tuple.circleCount)

    if type(image_tuple.triangleCount) != int:
        triangleCount = '0'
    else:
        triangleCount = str(image_tuple.triangleCount)




    cv.putText(image_tuple.cleanImage, squareCount, (x, y), font, fontsize, color, linetype)
    cv.putText(image_tuple.cleanImage, lineCount, (x, 2 * y), font, fontsize, color, linetype)
    cv.putText(image_tuple.cleanImage, circleCount, (x, 3 * y), font, fontsize, color, linetype)
    cv.putText(image_tuple.cleanImage, triangleCount, (x, 4 * y), font, fontsize, color, linetype)

    cv.rectangle(image_tuple.cleanImage, (2 * x, y - 2 * scale), (2 * x + 2 * scale, y), color, -linetype)
    cv.line(image_tuple.cleanImage, (2 * x + scale, 2 * y - 2 * scale), (2 * x + scale, 2 * y), color, linetype)
    cv.circle(image_tuple.cleanImage, (2 * x + scale, 3 * y - scale), scale, color, -linetype)
    pts = np.array([[2 * x + scale, 4 * y - 2 * scale], [2 * x, 4 * y], [2 * x + 2 * scale, 4 * y]], np.int32)
    cv.fillPoly(image_tuple.cleanImage, [pts], color)

    return image_tuple


def detectsquares(c, image_tuple, Squares):
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    Squastate = 'false'
    if len(approx) <= 4 and len(approx) > 3:
        (x, y, w, h) = cv.boundingRect(approx)
        ar = w / h
        if ar >= 0.6 and ar <= 1.4:
            Squastate = "rectangle"

        else:
            Squastate = "square"
        return Squastate


def detectlines(c):
    # TODO
    print('Detected ', processed_img.lineCount, ' lines.')
    return processed_img


def detectcircles(c, image_tuple, Circles):
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    Circstate = 'false'
    if len(approx) > 4 :
        Circstate = 'true'
        image_tuple.circleCount = Circles
        return Circstate





def detecttriangles(c, image_tuple, Triangles):
    Tristate = 'false'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3:
        Tristate = 'true'
        return Tristate



def detectshapes(image_tuple):
    Squares = 0
    Triangles = 0
    Circles = 0
    Rectangles = 0

    cnts = findcountours(image_tuple)

    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv.moments(c)

        cX = int((M["m10"] / (M["m00"] + 1e-7)))
        cY = int((M["m01"] / (M["m00"] + 1e-7)))

        Squa = detectsquares(c, image_tuple, Squares)

        Circ = detectcircles(c, image_tuple, Circles)

        Tri = detecttriangles(c, image_tuple, Triangles)

        if Tri == 'true':
            Triangles = Triangles + 1
            image_tuple.triangleCount = Triangles
            print('Detected ', image_tuple.triangleCount, ' triangles.')

        if Circ == 'true':
            Circles = Circles + 1
            image_tuple.circleCount = Circles
            print('Detected ', image_tuple.circleCount, ' circles.')

        if Squa == 'rectangle':
            Squares = Squares + 1
            image_tuple.squareCount = Squares
            print('Detected ', image_tuple.squareCount, ' squares.')

        if Squa == 'square':
            Rectangles = Rectangles + 1

            image_tuple.lineCount = Rectangles
            print('Detected ', image_tuple.lineCount, ' rectangles.')

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = c.astype("int")
        cv.drawContours(image_tuple.cleanImage, [c], -1, (0, 255, 0), 2)
    return image_tuple
def findcountours(image_tuple):
    cnts = cv.findContours(image_tuple.processedImage.copy(), cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts

