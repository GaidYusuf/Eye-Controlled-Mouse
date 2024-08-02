import cv2  # Import OpenCV for computer vision tasks
import mediapipe as mp  # Import MediaPipe for face landmark detection
import pyautogui  # Import pyautogui for controlling the mouse cursor

cam = cv2.VideoCapture(0)  # Initialize the webcam (0 is the default camera)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = pyautogui.size()  # Get the screen dimensions (size of the monitor or display)

while True:  # Continuously capture frames from the webcam
    _, frame = cam.read()  # Read a frame from the webcam
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirrored view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB color space
    output = face_mesh.process(rgb_frame)  # Process the frame to detect face landmarks
    landmarks_points = output.multi_face_landmarks  # Get the detected face landmarks
    frame_height, frame_width, _ = frame.shape  # Get the dimensions of the webcam frame

    # Right eye landmarks (4 specific points)
    if landmarks_points:  # Check if landmarks are detected
        landmarks = landmarks_points[0].landmark  # Get the landmarks for the first detected face
        right_eye = landmarks[474:478]  # 4 specific landmarks for the right eye
        for id, landmark in enumerate(right_eye):
            x = int(landmark.x * frame_width)  # Convert x-coordinate from frame to pixel value
            y = int(landmark.y * frame_height)  # Convert y-coordinate from frame to pixel value
            cv2.circle(frame, (x, y), 3, (0, 255, 0))  # Draw a circle on the landmark
            if id == 1:  # Use one of the landmarks (id=1) to control the mouse
                screen_x = (screen_width / frame_width) * x  # Scale x to match the screen width
                screen_y = (screen_height / frame_height) * y  # Scale y to match the screen height
                pyautogui.moveTo(screen_x, screen_y)  # Move the mouse cursor to the calculated screen position

        # Left eye landmarks (2 specific points)
        left_eye = [landmarks[145], landmarks[159]] # 2 specific landmarks for the left eye
        for landmark in left_eye:
            x = int(landmark.x * frame_width)  # Convert x-coordinate from frame to pixel value
            y = int(landmark.y * frame_height)  # Convert y-coordinate from frame to pixel value
            cv2.circle(frame, (x, y), 3, (0, 255, 255))  # Draw a circle on the landmark

        print(left_eye[0].y - left_eye[1].y)
        # Check if the distance between the two left eye landmarks is very small (indicating a blink or close eyes)
        if (left_eye[0].y - left_eye[1].y) < 0.002:
            pyautogui.click()  # Perform a mouse click
            pyautogui.sleep(1)  # Wait for 1 second to prevent multiple clicks

    cv2.imshow('Eye Controlled Mouse', frame)  # Display the captured frame in a window named 'Eye Controlled Mouse'
    if cv2.waitKey(1) == ord('q'):  # Exit the loop when the 'q' key is pressed
        break

# Release the webcam and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
