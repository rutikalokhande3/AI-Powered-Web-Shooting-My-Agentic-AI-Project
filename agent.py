import time
import pyttsx3


class GestureAgent:

    def __init__(self):

        self.last_action_time = 0
        self.cooldown = 0.8

        # Voice engine
        self.voice = pyttsx3.init()

        self.voice.setProperty("rate", 175)
        self.voice.setProperty("volume", 1.0)


    def speak(self, text):

        print("AI:", text)

        self.voice.say(text)
        self.voice.runAndWait()


    def decide(
        self,
        gesture_name,
        confidence,
        hand_x,
        hand_y
    ):

        current_time = time.time()


        # -------------------------
        # NO GESTURE
        # -------------------------

        if gesture_name is None:

            return {
                "action": "IDLE",
                "execute": False
            }


        # -------------------------
        # CONFIDENCE
        # -------------------------

        if confidence < 0.70:

            self.speak(
                "Gesture confidence is too low."
            )

            return {
                "action": "IGNORE",
                "execute": False
            }


        # -------------------------
        # COOLDOWN
        # -------------------------

        if (
            current_time -
            self.last_action_time
            < self.cooldown
        ):

            return {
                "action": "COOLDOWN",
                "execute": False
            }


        # -------------------------
        # AGENT DECISION
        # -------------------------

        if gesture_name == "WEB_SHOOT":

            self.last_action_time = current_time


            self.speak(
                "Web shooting mode activated."
            )


            return {

                "action": "WEB_SHOOT",

                "execute": True,

                "x": hand_x,

                "y": hand_y,

                "power": 1.0,

                "duration": 1.0

            }


        # -------------------------
        # UNKNOWN
        # -------------------------

        self.speak(
            "Unknown gesture detected."
        )


        return {
            "action": "UNKNOWN",
            "execute": False
        }