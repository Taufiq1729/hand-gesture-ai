import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import pyautogui as keyboard

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# -----------------------------
# Define Button class
# -----------------------------
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# -----------------------------
# Draw all buttons with transparency
# -----------------------------
def drawAll(img, buttonList, capsLock):
    overlay = img.copy()
    alpha = 0.6

    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # CAPS active color
        if button.text == "CAPS" and capsLock:
            color = (0, 200, 0)
        else:
            color = (255, 0, 255)

        cvzone.cornerRect(overlay, (x, y, w, h), 20, rt=0)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, cv2.FILLED)

        # Adjust text position for big buttons
        if button.text == "SPACE":
            text_x = x + w // 2 - 50  # centered text
            text_y = y + h // 2 + 15
            font_scale = 3
            thickness = 3
        elif button.text == "CAPS":
            text_x = x + w // 6 - 10  # move text slightly left
            text_y = y + h // 2 + 15
            font_scale = 2.5
            thickness = 3
        elif button.text == "DEL":
            text_x = x + w // 6
            text_y = y + h // 2 + 15
            font_scale = 2.5
            thickness = 3
        else:
            text_x = x + 25
            text_y = y + 65
            font_scale = 2.5
            thickness = 3

        cv2.putText(overlay, button.text, (text_x, text_y),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), thickness)

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    return img

# -----------------------------
# Keyboard layout with proper margins
# -----------------------------
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["CAPS", "SPACE", "DEL"]
]

buttonList = []
for i, row in enumerate(keys):
    x_start = 50  # starting x for each row
    for j, key in enumerate(row):
        # Set size for special buttons
        if key == "SPACE":
            size = [500, 85]
            x_pos = x_start
        elif key == "CAPS":
            size = [120, 85]
            x_pos = x_start
        elif key == "DEL":
            size = [120, 85]
            x_pos = x_start
        else:
            size = [85, 85]
            x_pos = x_start
        y_pos = 50 + i * 100
        buttonList.append(Button([x_pos, y_pos], key, size=size))
        x_start += size[0] + 15  # margin between keys

capsLock = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList, capsLock)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            key = button.text

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)

                # Draw text on pressed button
                if key == "SPACE":
                    text_x = x + w // 2 - 50
                    text_y = y + h // 2 + 15
                    font_scale = 3
                    thickness = 3
                elif key == "CAPS":
                    text_x = x + w // 6 - 10
                    text_y = y + h // 2 + 15
                    font_scale = 2.5
                    thickness = 3
                elif key == "DEL":
                    text_x = x + w // 6
                    text_y = y + h // 2 + 15
                    font_scale = 2.5
                    thickness = 3
                else:
                    text_x = x + 25
                    text_y = y + 65
                    font_scale = 2.5
                    thickness = 3
                cv2.putText(img, key, (text_x, text_y),
                            cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), thickness)

                # Distance between index and thumb
                x1, y1 = lmList[8][0], lmList[8][1]
                x2, y2 = lmList[4][0], lmList[4][1]
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                l = detector.findDistance([x1, y1], [x2, y2], img)
                distance = l[0] if isinstance(l, tuple) else l

                if distance < 30:
                    if key == "CAPS":
                        capsLock = not capsLock
                    elif key == "SPACE":
                        keyboard.press("space")
                    elif key == "DEL":
                        keyboard.press("backspace")
                    else:
                        if capsLock:
                            keyboard.press(key.upper())
                        else:
                            keyboard.press(key.lower())
                    sleep(0.2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
