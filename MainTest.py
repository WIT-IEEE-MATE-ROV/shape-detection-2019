import sys
import cv2
import  TestLib as niproc
import numpy as np
import imutils
# Check if there is any input to be read
if len(sys.argv) is 1:
    print("USAGE: shape-detection.py [file1] (file2) (file3)...")
    print("OR:    shape-detection.py -v (device)")
    print("No files specified, exiting")
# User requested we use video input.
elif sys.argv[1] == "-v":
    cap = None
    # Find which device was specified by user, or default to device 0
    if len(sys.argv) > 2:
        cap = cv.VideoCapture(sys.argv[2])
    else:
        cap = cv.VideoCapture(0)

    # Do video interpretation until process is killed
    while True:
        ret, frame = cap.read()
        pimg = niproc.processimage(frame)
        cv2.imshow("Current frame", pimg.image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

else:
    # There's input, read it!
    for uin in sys.argv[1:]:
        print("Loading ", uin)
        img = cv2.imread(uin)

        if img is not None:
            print("Found image")

            pimg = img
            cnts = niproc.processimage(pimg)
            #pimg = cv.pyrDown(pimg.processedImage)
            # loop over the contours
            for c in cnts:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c)

                cX = int((M["m10"] / (M["m00"] + 1e-7)))
                cY = int((M["m01"] / (M["m00"] + 1e-7)))
                shape = niproc.FindShapes(c)

                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c = c.astype("int")
                cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
                cv2.putText(img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)
            cv2.imshow('Current Img',img)
            cv2.waitKey()
            cv2.destroyAllWindows()

        else:
            print("Couldn't read that file. Does it exist at the location specified?")