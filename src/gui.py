import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import time

from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from system_controller import SystemController

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture AI Control")

        self.is_running = False
        self.thread = None

        # --- UI Elements ---
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.video_label = ttk.Label(self.main_frame)
        self.video_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.start)
        self.start_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.status_label = ttk.Label(self.main_frame, text="Status: Stopped", font=("Helvetica", 12))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self.video_loop, daemon=True)
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running")

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0) # Wait for the thread to finish
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")
        # Clear the video label
        self.video_label.config(image='')
        self.video_label.image = None

    def video_loop(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            self.stop()
            return

        detector = HandDetector()
        controller = SystemController()

        last_gesture = ""
        gesture_counter = 0
        ACTION_THRESHOLD = 10

        while self.is_running:
            success, frame = cap.read()
            if not success:
                time.sleep(0.1)
                continue

            frame = detector.find_hands(frame, draw=True)
            lm_list = detector.find_position(frame, draw=False)

            current_gesture = 'NO_HAND'
            if lm_list:
                classifier = GestureClassifier(lm_list)
                current_gesture = classifier.classify()

            if current_gesture == last_gesture and current_gesture not in ['UNKNOWN', 'NO_HAND']:
                gesture_counter += 1
            else:
                gesture_counter = 0
                last_gesture = current_gesture

            action_text = ""
            if gesture_counter == ACTION_THRESHOLD:
                controller.perform_action(current_gesture)
                action_text = f"Action: {current_gesture}"
                gesture_counter = 0

            # Update GUI
            self.update_gui_frame(frame, current_gesture, action_text)
            
            time.sleep(0.01) # Small delay to prevent high CPU usage

        cap.release()

    def update_gui_frame(self, frame, gesture, action):
        # Convert frame for tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Update status text
        status_text = f"Gesture: {gesture}"
        if action:
            status_text += f" | {action}"
        self.status_label.config(text=status_text)

    def on_closing(self):
        self.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
