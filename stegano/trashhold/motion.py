import cv2

cap = cv2.VideoCapture('media/try.mp4')
#cap.set(cv2.CAP_PROP_POS_FRAMES, 300)
ret, frame1 = cap.read()
ret, frame2 = cap.read()


while cap.isOpened() and ret:
    frame1 = diff = cv2.absdiff(frame1, frame2)
    # gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh = cv2.threshold(blur, 20, 255, cv2.cv2.THRESH_BINARY)
    # dilated = cv2.dilate(thresh, None, iterations=3)
    # contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    cv2.imshow("feed", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(40) in [27, ord('q')]:
        break

cv2.destroyAllWindows()