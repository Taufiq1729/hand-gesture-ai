import pyautogui
import platform

class SystemController:
    """A class to control system functions based on gestures."""

    def __init__(self):
        """Initializes the SystemController."""
        self.os = platform.system()

    def perform_action(self, gesture):
        """
        Performs a system action based on the given gesture.

        Args:
            gesture (str): The name of the gesture to perform an action for.
        """
        if gesture == 'FIST':
            self.play_pause()
        elif gesture == 'PALM':
            self.stop_media()
        elif gesture == 'THUMBS_UP':
            self.volume_up()
        elif gesture == 'THUMBS_DOWN': # We'll add this gesture later
            self.volume_down()
        elif gesture == 'POINTING_UP':
            # Example for switching tabs
            self.next_tab()
        # Add more gesture-to-action mappings here

    def play_pause(self):
        """Presses the play/pause media key."""
        pyautogui.press('playpause')
        print("Action: Play/Pause")

    def stop_media(self):
        """Presses the stop media key."""
        pyautogui.press('stop')
        print("Action: Stop Media")

    def volume_up(self):
        """Increases the system volume."""
        pyautogui.press('volumeup')
        print("Action: Volume Up")

    def volume_down(self):
        """Decreases the system volume."""
        pyautogui.press('volumedown')
        print("Action: Volume Down")

    def next_tab(self):
        """Switches to the next tab in a web browser or application."""
        pyautogui.hotkey('ctrl', 'tab')
        print("Action: Next Tab")

    def prev_tab(self):
        """Switches to the previous tab in a web browser or application."""
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        print("Action: Previous Tab")
