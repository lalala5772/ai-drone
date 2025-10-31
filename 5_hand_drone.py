import cv2
import mediapipe as mp
from time import sleep
import keyboard
from CodingRider.drone import *
from CodingRider.protocol import *

# is_takeoff 변수로 이륙했는지 확인합니다.
is_takeoff = False

drone = Drone()
drone.open('COM3')

capture = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as hands:

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            continue 
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:            
            for hand_landmarks in results.multi_hand_landmarks: 
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) 
                finger = hand_landmarks.landmark[8] 
                # 이륙했다면 검지 손가락 좌표로 드론을 움직입니다.   
                if is_takeoff:                
                    # 롤과 피치 값을 정합니다.
                    roll = int(((finger.x * 200) - 100) * 0.5)
                    pitch = -int(((finger.y * 200) - 100) * 0.5)
                    drone.sendControl(roll, pitch, 0, 0)

                    # 롤과 피치 값을 나타냅니다.    
                    text = f'r : {roll}, p : {pitch}'
                    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)                
        cv2.imshow('MediaPipe Hand Detection', frame)
        if keyboard.is_pressed('enter'):   
            print('이륙')       
            sleep(2)
            drone.sendTakeOff()
            sleep(5)
            print('이륙 완료') 
            is_takeoff = True
        if keyboard.is_pressed('space'):
            print('착륙')
            drone.sendControlWhile(0, 0, 0, 0, 500) # 제자리에서 0.5초 멈춥니다.
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
        if cv2.waitKey(1) == 27:
            break
        
capture.release()
cv2.destroyAllWindows()