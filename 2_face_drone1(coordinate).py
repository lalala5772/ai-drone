import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)
                       
# 얼굴을 찾고, 찾은 얼굴에 표시를 해주기 위한 변수를 정의합니다.
# 얼굴 검출을 위해서 face_detection 모듈을 사용합니다.
mp_face_detection = mp.solutions.face_detection 

# 얼굴의 특징을 그리기 위해서 drawing_utils 모듈을 사용합니다.
mp_drawing = mp.solutions.drawing_utils 

# mediapipe 사용방법에 맞게 설정합니다.
# model_selection = 0은 카메라와 가까운 것을 인식합니다.
# model_selection = 1은 카메라와 먼 것을 인식합니다.
# min_detection_confidence=0.7는 70% 확신한다면 얼굴로 본다는 뜻입니다.
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection:
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            continue     

        # 성능을 높이기 위해 프레임을 쓰기 불가능 상태로 변경합니다.        
        frame.flags.writeable = False
        
        # 좌우 반전을 합니다.
        frame = cv2.flip(frame, 1) 

        # BGR 색상을 RGB 색상으로 바꿉니다.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # frame에서 얼굴을 확인합니다. 
        results = face_detection.process(frame) 

        # 다시 프레임을 쓰기 가능 상태로 바꿉니다.      
        frame.flags.writeable = True

        # RGB 색상을 BGR 색상으로 바꿉니다
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  

        # 얼굴을 인식했다면      
        if results.detections:       
            for detection in results.detections:
                # 그 결과를 frame에 그립니다. 
                # 오른쪽 눈, 왼쪽 눈, 코 끝부분, 입 중심, 오른쪽 귀, 왼쪽 귀 위치가 점을 표시됩니다.
                mp_drawing.draw_detection(frame, detection) 

                # 얼굴의 정보를 출력합니다. 
                print(detection)
                
        cv2.imshow('MediaPipe Face Detection', frame)
        if cv2.waitKey(1) == 27:
            break
            
capture.release()
cv2.destroyAllWindows()