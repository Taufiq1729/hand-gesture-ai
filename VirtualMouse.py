import cv2
import mediapipe as mp
import util
import pyautogui
from pynput.mouse import Button, Controller
import random

# Screen size & mouse controller
screen_width, screen_height = pyautogui.size()
mouse = Controller()

# MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# State for anchor / thumb transitions
prev_thumb_closed = False
anchor_offset_x = 0
anchor_offset_y = 0


# ---------- Helpers ----------
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None


def is_left_click(landmarks_list, thumb_index_distance):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            thumb_index_distance > 50)


def is_right_click(landmarks_list, thumb_index_distance):
    return (util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            thumb_index_distance > 50)


def is_double_click(landmarks_list, thumb_index_distance):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_distance > 50)


def is_screenshot(landmarks_list, thumb_index_distance):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_distance < 50)


# ---------- Gesture detection with anchor offset ----------
def detect_gestures(frame, landmarks_list, processed):
    global prev_thumb_closed, anchor_offset_x, anchor_offset_y

    if len(landmarks_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[5]])

        thumb_closed = thumb_index_dist < 50

        # Transition: thumb was open and now closed -> set anchor offset
        if thumb_closed and (not prev_thumb_closed):
            # determine finger screen coords (if available)
            if index_finger_tip is not None:
                finger_x = int(index_finger_tip.x * screen_width)
                finger_y = int(index_finger_tip.y * screen_height)
            else:
                # fallback: if no finger detected, anchor offset = 0
                finger_x, finger_y = 0, 0

            cur_mouse_x, cur_mouse_y = pyautogui.position()
            anchor_offset_x = cur_mouse_x - finger_x
            anchor_offset_y = cur_mouse_y - finger_y

        # While thumb is closed -> move but using anchor offset (prevents jump)
        if thumb_closed:
            if index_finger_tip is not None:
                finger_x = int(index_finger_tip.x * screen_width)
                finger_y = int(index_finger_tip.y * screen_height)

                # target = finger + anchor offset
                target_x = int(finger_x + anchor_offset_x)
                target_y = int(finger_y + anchor_offset_y)

                # clamp to screen bounds
                target_x = max(0, min(screen_width - 1, target_x))
                target_y = max(0, min(screen_height - 1, target_y))

                pyautogui.moveTo(target_x, target_y)
        else:
            # Thumb open -> freeze cursor (do nothing). Anchor preserved until next close.
            pass

        # Update prev state
        prev_thumb_closed = thumb_closed

        # Click gestures (unchanged)
        if is_left_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elif is_right_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif is_double_click(landmarks_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        elif is_screenshot(landmarks_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


# ---------- Main ----------
def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            processed = hands.process(frameRGB)
            landmarks_list = []

            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            detect_gestures(frame, landmarks_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
