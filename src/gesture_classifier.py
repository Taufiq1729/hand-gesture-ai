class GestureClassifier:
    """A class to classify hand gestures based on landmark positions."""

    def __init__(self, landmark_list):
        """
        Initializes the GestureClassifier.

        Args:
            landmark_list (list): A list of hand landmarks, where each landmark is [id, x, y].
        """
        self.lm_list = landmark_list
        self.finger_tip_ids = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky

    def classify(self):
        """
        Classifies the gesture based on which fingers are extended.

        Returns:
            str: The name of the classified gesture (e.g., 'FIST', 'PALM', 'THUMBS_UP').
                 Returns 'UNKNOWN' if the gesture is not recognized.
        """
        if not self.lm_list:
            return 'NO_HAND'

        fingers_up = self._get_fingers_up()

        # Rule-based classification
        if fingers_up == [0, 0, 0, 0, 0]:
            return 'FIST'
        elif fingers_up == [1, 1, 1, 1, 1]:
            return 'PALM'
        elif fingers_up == [1, 0, 0, 0, 0]:
            return 'THUMBS_UP'
        elif fingers_up == [0, 1, 0, 0, 0]:
            return 'POINTING_UP'
        elif fingers_up == [0, 1, 1, 0, 0]:
            return 'PEACE'
        elif fingers_up == [0, 0, 0, 0, 1]:
            return 'PINKY_UP'
        elif fingers_up == [0, 0, 0, 0, 0] and self.lm_list[self.finger_tip_ids[0]][2] > self.lm_list[self.finger_tip_ids[0] - 1][2]:
            return 'THUMBS_DOWN'
        
        return 'UNKNOWN'

    def _get_fingers_up(self):
        """
        Determines which fingers are extended upwards.

        Returns:
            list: A list of 5 booleans (0 or 1) representing the state of each finger
                  (thumb, index, middle, ring, pinky).
        """
        fingers = []

        # Thumb
        # Check if the thumb tip is above the knuckle
        if self.lm_list[self.finger_tip_ids[0]][2] < self.lm_list[self.finger_tip_ids[0] - 1][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers (check y-coordinate)
        for id in range(1, 5):
            if self.lm_list[self.finger_tip_ids[id]][2] < self.lm_list[self.finger_tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
