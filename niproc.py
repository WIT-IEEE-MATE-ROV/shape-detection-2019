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

    image_tuple = detectshapes(image,mask)

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


def detectsquares(c):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 4:
        (x, y, w, h) = cv.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else 'rectangle'
        processed_img.squareCount = processed_img.squareCount + 1
        print('Detected ', processed_img.squareCount, ' squares.')
    return shape
    return processed_img



def detectlines(c):
    # TODO
    print('Detected ', processed_img.lineCount, ' lines.')
    return processed_img


def detectcircles(c):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) > 5:
        shape = "Circle"
        processed_img.circleCount = processed_img.circleCount + 1
        print('Detected ', processed_img.circleCount, ' circles.')
    return shape
    return processed_img


def detecttriangles(c):
    shape = 'Undefined'
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3:
        shape = "triangle"
        processed_img.triangleCount = processed_img.triangleCount + 1
        print('Detected ', processed_img.triangleCount, ' triangles.')
    return shape
    return processed_img

def detectshapes(image,mask):
    cnts = findcountours(mask)
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv.moments(c)

        cX = int((M["m10"] / (M["m00"] + 1e-7)))
        cY = int((M["m01"] / (M["m00"] + 1e-7)))

        shape = detectsquares(c)
        shape = detectcircles(c)
        shape = detecttriangles(c)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = c.astype("int")
        cv.drawContours(image, [c], -1, (0, 255, 0), 2)
        processedImage = cv.putText(image, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)
        return processedImage


def findcountours(mask):
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                            cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return cnts
