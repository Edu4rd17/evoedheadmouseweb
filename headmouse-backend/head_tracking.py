import cv2
import pyautogui
import mediapipe as mp
import time

# Initialize MediaPipe Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False
)

# Screen size for PyAutoGUI
screen_width, screen_height = pyautogui.size()

# Variables for cursor control
landmark_x0 = 0.5
landmark_y0 = 0.5
prev_screen_x, prev_screen_y = pyautogui.position()
tolerance = 50
prev_pos = pyautogui.position()
last_click_time = 0

def process_frame_for_cursor_control(frame):
    global prev_screen_x, prev_screen_y, landmark_x0, landmark_y0, prev_pos, last_click_time

    # Convert the image to RGB for MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = face_mesh.process(image_rgb)
    image_rgb.flags.writeable = True

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Tracking the nose tip and moving the cursor
            landmarks = face_landmarks.landmark
            nose_tip = landmarks[4]

            # Get frame dimensions
            frame_height, frame_width, _ = frame.shape

            # Convert nose tip to screen coordinates
            x = int(nose_tip.x * frame_width)
            y = int(nose_tip.y * frame_height)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

            # Calculate screen position for pyautogui
            screen_x = (nose_tip.x - landmark_x0) * (screen_width * 6) + screen_width * landmark_x0
            screen_y = (nose_tip.y - landmark_y0) * (screen_height * 6) + screen_height * landmark_y0

            # Move the cursor based on nose position
            if abs(screen_x - prev_screen_x) > tolerance or abs(screen_y - prev_screen_y) > tolerance:
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(screen_x, screen_y)
                prev_screen_x, prev_screen_y = screen_x, screen_y

            # Eye blink detection logic (left eye)
            left_eye = [landmarks[145], landmarks[159]]
            if (left_eye[0].y - left_eye[1].y) < 0.006:
                current_pos = pyautogui.position()
                if current_pos != prev_pos:
                    prev_pos = current_pos
                    continue
                else:
                    if time.time() - last_click_time > 2:  # Click every 2 seconds
                        pyautogui.click()
                        last_click_time = time.time()

    return frame
