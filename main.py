import sys
import cv2 as cv
import niproc


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
        cv.imshow("Current frame", pimg.image)
        
        #Get tick-count to measure performance indirectly
        e1 = cv2.getTickCount()
        for i in xrange(5,49,2):
            img1 = cv2.medianBlur(img1,i)
        e2 = cv2.getTickCount()
        t = (e2 - e1)/cv2.getTickFrequency()
            print t
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

else:
    # There's input, read it!
    for uin in sys.argv[1:]:
        print("Loading ", uin)
        img = cv.imread(uin)

        if img is not None:
            print("Found image")

            pimg = img
            pimg = niproc.processimage(pimg)
            pimg = cv.pyrDown(pimg.processedImage)

            cv.imshow("Current image", pimg)
            cv.waitKey()
            cv.destroyAllWindows()

        else:
            print("Couldn't read that file. Does it exist at the location specified?")

