import cv2

cap = cv2.VideoCapture('rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp')

#while True:
for i in range(25):
    ret, frame = cap.read()
    fnam='c:/temp/capture/frame'+str(i)+'.jpg'
    cv2.imwrite(fnam, frame)

    #cv2.imshow("Capturing",frame)

#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

cap.release()
cv2.destroyAllWindows()