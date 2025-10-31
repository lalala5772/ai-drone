import cv2

capture = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier() 
cascade.load('haarcascade_frontalface_default.xml') 

while capture.isOpened():
    ret, frame = capture.read()
    if not ret: 
        continue
    frame = cv2.flip(frame, 1) 
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.equalizeHist(grayframe)    
    objects = cascade.detectMultiScale(grayframe, 1.1, 3, 0, (30, 30))
    for (x,y,w,h) in objects:               
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)     
        cv2.putText(frame, 'face', (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0))
    cv2.imshow('haarcascade', frame)
    if cv2.waitKey(1) == 27: 
        break
    
capture.release()
cv2.destroyAllWindows()