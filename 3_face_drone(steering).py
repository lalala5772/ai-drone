import cv2
import mediapipe as mp
from time import sleep
import keyboard
from CodingRider.drone import *
from CodingRider.protocol import *

# is_takeoff 변수로 이륙했는지 확인합니다.
is_takeoff = False

# 드론 객체를 만듭니다.
drone = Drone()
drone.open('COM4')

capture = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection 
mp_drawing = mp.solutions.drawing_utils 

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection:
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            continue
        frame.flags.writeable = False
        frame = cv2.flip(frame, 1) 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)       
        results = face_detection.process(frame)         
        frame.flags.writeable = True   
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)              
        if results.detections:          
            for detection in results.detections:
                keypoints = detection.location_data.relative_keypoints 
                nose = keypoints[2] 
                height, width, channel = frame.shape
                nose_position = (int(nose.x * width), int(nose.y * height))               
                cv2.circle(frame, nose_position, 50, (0,0,255), 10, cv2.LINE_AA)
        if keyboard.is_pressed('enter'):
            print('이륙')
            sleep(2)
            drone.sendTakeOff()
            sleep(5)
            print('이륙 완료')
            is_takeoff = True               
        if keyboard.is_pressed('space'):
            print('착륙')
            drone.sendControlWhile(0, 0, 0, 0, 500) 
            drone.sendLanding()
            sleep(3)
            print('착륙 완료')
            is_takeoff = False
        if keyboard.is_pressed('q'):
            print('정지')
            drone.sendControlWhile(0, 0, 0, 0, 500)
            drone.sendStop()
            sleep(3)   
            is_takeoff = False
        # 이륙했다면 코의 좌표로 드론을 움직입니다.   
        if is_takeoff: 
            # 롤과 피치 값을 정합니다.          
            roll = int(((nose.x * 200) - 100) * 0.5)
            pitch = -int(((nose.y * 200) - 100) * 0.5)
            drone.sendControl(roll, pitch, 0, 0)

            # 롤과 피치 값을 나타냅니다.
            text = f'r : {roll}, p : {pitch}'
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
        cv2.imshow('MediaPipe Face Detection', frame)
        if cv2.waitKey(1) == 27:
            break  
                  
capture.release()
cv2.destroyAllWindows()