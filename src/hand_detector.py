import cv2
import mediapipe as mp

class HandDetector:
    """A class to detect hands and their landmarks in an image."""

    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initializes the HandDetector.

        Args:
            static_image_mode (bool): Whether to treat the input images as a batch of static
                                      and possibly unrelated images, or a video stream.
            max_num_hands (int): Maximum number of hands to detect.
            min_detection_confidence (float): Minimum confidence value ([0.0, 1.0]) for hand
                                            detection to be considered successful.
            min_tracking_confidence (float): Minimum confidence value ([0.0, 1.0]) for the
                                             hand landmarks to be considered tracked successfully.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode, 
                                          max_num_hands=max_num_hands,
                                          min_detection_confidence=min_detection_confidence, 
                                          min_tracking_confidence=min_tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Finds hands in a BGR image.

        Args:
            img (numpy.ndarray): The image to process.
            draw (bool): Whether to draw the hand landmarks and connections on the image.

        Returns:
            numpy.ndarray: The image with landmarks drawn (if draw=True).
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Finds the landmarks of a specific hand and returns their positions.

        Args:
            img (numpy.ndarray): The image to process.
            hand_no (int): The index of the hand to find landmarks for.
            draw (bool): Whether to draw a circle on the landmarks.

        Returns:
            list: A list of landmarks, where each landmark is [id, x, y].
                  Returns an empty list if the specified hand is not found.
        """
        lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_no]
                for id, lm in enumerate(my_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return lm_list
