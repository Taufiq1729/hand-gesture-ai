# 🖥️ Virtual Mouse and Keyboard using Hand Tracking

This project enables users to control their **mouse and keyboard using hand gestures** captured through a webcam.  
It leverages **OpenCV**, **MediaPipe**, and **cvzone** for efficient hand detection and tracking.

---

## 🧩 Features

### 🖱️ Virtual Mouse
- Move the cursor using your **index finger**.  
- Perform a **left-click** by bending your **index finger**.  
- Perform a **right-click** by bending your **middle finger**.  
- Perform a **double-click** by bending **both the index and middle fingers** together.  
- Open your **thumb** to pause cursor movement.  
- Close your **thumb** to resume movement from the **current cursor position**.  

> **Note:** For best results, perform all click gestures **with your thumb open**.

---

### ⌨️ Virtual Keyboard
- Provides an **on-screen keyboard** that allows typing using hand gestures.  
- Move your **index finger** to select a key.  
- Bring the **index finger** and **thumb** close together to press a key.  

---

## ⚙️ Requirements

- **Python 3.8 or higher**  
- A functional **webcam**

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### On macOS / Linux
```bash
python3 VirtualMouseFinal.py
```
or  
```bash
python3 VirtualKeyboardFinal.py
```

### On Windows
```bash
python VirtualMouseFinal.py
```
or  
```bash
python VirtualKeyboardFinal.py
```

---

## 🧠 Libraries Used

| Library | Purpose |
|----------|----------|
| **opencv-python** | Video capture and image processing |
| **mediapipe** | Hand landmark detection |
| **cvzone** | Simplified integration of OpenCV and MediaPipe |
| **numpy** | Mathematical operations |
| **pyautogui** | Simulating mouse and keyboard events |

---

## ⚠️ Troubleshooting

- If the webcam doesn’t open, ensure it’s not being used by another application.  
- On **macOS**, allow camera access for Terminal or Python:  
  *System Preferences → Security & Privacy → Camera*  
- On **Windows**, make sure camera permissions are enabled for applications.

---

## 📁 Project Structure

```
│
├── VirtualMouseFinal.py
├── VirtualKeyboardFinal.py
├── requirements.txt
└── README.md
```

---

