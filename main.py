import sys
import cv2 as cv
import niproc
import numpy as np

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
        print('Video Stream')
        ret, frame = cap.read()
        pimg = niproc.processimage(frame)
        cv.imshow("Current frame", pimg.cleanImage )
        cv.imshow("HSV", pimg.HSV)
        cv.imshow("What Code Sees", pimg.BlackWhite)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

else:
    # There's input, read it!
    for uin in sys.argv[1:]:
        print("Loading ", uin)
        img = cv.imread(uin)
        imgtype = (img.dtype)
        print(imgtype)
        if imgtype == "uint8":
            print("Found image")

            pimg = img
            pimg = niproc.processimage(pimg)
            HSV = cv.pyrDown(pimg.HSV)
            WCS = cv.pyrDown(pimg.BlackWhite)
            img = cv.pyrDown(pimg.cleanImage)


            cv.imshow("Current image", img)
            cv.imshow("HSV", HSV)
            cv.imshow("What Code Sees", WCS)

            cv.waitKey()
            cv.destroyAllWindows()

        else:
            print("Couldn't read that file. Does it exist at the location specified?")

