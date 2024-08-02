import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize the webcam (0 is the default camera)
cam = cv2.VideoCapture(0)
# Initialize MediaPipe FaceMesh with refined landmarks
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# Get the screen dimensions (size of the monitor or display)
screen_width, screen_height = pyautogui.size()

# Buffer to store recent cursor positions
cursor_positions = []

while True:
    _, frame = cam.read()  # Read a frame from the webcam
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirrored view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB color space
    output = face_mesh.process(rgb_frame)  # Process the frame to detect face landmarks
    landmarks_points = output.multi_face_landmarks  # Get the detected face landmarks
    frame_height, frame_width, _ = frame.shape  # Get the dimensions of the webcam frame

    if landmarks_points:
        landmarks = landmarks_points[0].landmark  # Get the landmarks for the first detected face

        # Right eye landmarks (4 specific points)
        right_eye = landmarks[474:478]
        for id, landmark in enumerate(right_eye):
            x = int(landmark.x * frame_width)  # Convert x-coordinate from normalized to pixel value
            y = int(landmark.y * frame_height)  # Convert y-coordinate from normalized to pixel value
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Draw a green circle on the right eye landmarks
            if id == 1:  # Use landmark with id=1 (the second point of the right eye) to control the mouse
                # Map the x and y coordinates from the frame to the screen coordinates
                screen_x = (screen_width / frame_width) * x
                screen_y = (screen_height / frame_height) * y

                # Add the new position to the buffer
                cursor_positions.append((screen_x, screen_y))

                # Keep the buffer size constant (e.g., 10 recent positions)
                if len(cursor_positions) > 10:
                    cursor_positions.pop(0)

                # Calculate the average position
                avg_x = int(np.mean([pos[0] for pos in cursor_positions]))
                avg_y = int(np.mean([pos[1] for pos in cursor_positions]))

                # Move the mouse cursor to the average position
                pyautogui.moveTo(avg_x, avg_y)

        # Left eye landmarks (2 specific points)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_width)  # Convert x-coordinate from normalized to pixel value
            y = int(landmark.y * frame_height)  # Convert y-coordinate from normalized to pixel value
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)  # Draw a cyan circle on the left eye landmarks

        # Check if the distance between the two left eye landmarks is very small (indicating a blink or close eyes)
        if (left_eye[0].y - left_eye[1].y) < 0.004:
            pyautogui.click()  # Perform a mouse click
            pyautogui.sleep(1)  # Wait for 1 second to prevent multiple clicks

    # Display the captured frame in a window named 'Eye Controlled Mouse'
    cv2.imshow('Eye Controlled Mouse', frame)
    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
