import cv2
import pyautogui
import mediapipe as mp
import time

# Initialize MediaPipe Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False
)
screen_width, screen_height = pyautogui.size()
drawing_spec = mp_drawing.DrawingSpec(
    thickness=1, circle_radius=1)

def liveFaceRecognitionTracking(cap):
    # Initialize the webcam
    face_count = 0
    landmark_x0 = 0.5
    landmark_y0 = 0.5
    prev_screen_x, prev_screen_y = pyautogui.position()
    tolerance = 50
    prev_pos = pyautogui.position()
    last_click_time = 0
    while cap.isOpened():
        # generate frame by frame from camera
        success, image = cap.read()
        # flip the frame
        image = cv2.flip(image, 1)
        # convert the frame to RGB
        imageRBG = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # process the rgb_frame using face_mesh
        results = face_mesh.process(imageRBG)
        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        if results.multi_face_landmarks:
            face_count += 1
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                landmarks_points = results.multi_face_landmarks
                # get the height and width of the frame
                frame_height, frame_width, _ = image.shape
                # check if there are landmarks
                if landmarks_points:
                    # get the landmarks of the first face
                    landmarks = landmarks_points[0].landmark
                    nose_tip = landmarks[4]
                    # nose_tip = landmarks[414]
                    if face_count == 3:
                        landmark_x0 = nose_tip.x
                        landmark_y0 = nose_tip.y
                    x = int(nose_tip.x * frame_width)
                    y = int(nose_tip.y * frame_height)
                    # draw a circle on the landmark; x and y are the center ; 3 is the radius and 0, 255, 0 is the color
                    cv2.circle(image, (x, y), 3, (0, 255, 0))
                    # make the cursor move a bigger amount of pixels at a time
                    k = 6
                    screen_x = (nose_tip.x - landmark_x0) * \
                        (screen_width * k) + screen_width * landmark_x0
                    screen_y = (nose_tip.y - landmark_y0) * \
                        (screen_height * k) + screen_height * landmark_y0
                    # set pyauto gui to false
                    if abs(screen_x - prev_screen_x) > tolerance or abs(screen_y - prev_screen_y) > tolerance:
                        pyautogui.FAILSAFE = False
                        pyautogui.moveTo(screen_x, screen_y)
                        prev_screen_x, prev_screen_y = screen_x, screen_y
                    leftEye = [landmarks[145], landmarks[159]]
                    for landmark in leftEye:
                        x = int(landmark.x * frame_width)
                        y = int(landmark.y * frame_height)
                        cv2.circle(image, (x, y), 3, (0, 255, 255))
                    if (leftEye[0].y - leftEye[1].y) < 0.006:
                        current_pos = pyautogui.position()
                        if current_pos != prev_pos:
                            prev_pos = current_pos
                            time.sleep(0.1)
                            continue
                        else:
                            if time.time() - last_click_time > 2:  # check if 2 seconds have passed
                                pyautogui.click()
                                last_click_time = time.time()  # update the last click time
        else:
            # display the text if no face is detected
            cv2.putText(image, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

         # encode the image as JPEG
        ret, buffer = cv2.imencode('.jpg', image)
        # convert the image buffer to bytes
        image = buffer.tobytes()
        # yield the output frame in the byte format
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')