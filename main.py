import cv2
import mediapipe as mp
import numpy as np
import json
import math
import time
import threading
import pygame

from agent import GestureAgent


# ============================================================
# SETUP
# ============================================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarksConnections = mp.tasks.vision.HandLandmarksConnections


# ============================================================
# SOUND SETUP
# ============================================================

pygame.mixer.init()

try:
    shoot_sound = pygame.mixer.Sound("web_shoot.wav")
    shoot_sound.set_volume(0.8)
    print("Web shooting sound loaded.")
except Exception as e:
    shoot_sound = None
    print("web_shoot.wav nahi mila.")
    print("Sound error:", e)


def play_shoot_sound():
    if shoot_sound is not None:
        try:
            shoot_sound.play()
        except Exception as e:
            print("Sound play error:", e)


# ============================================================
# SCREEN CALIBRATION
# ============================================================

try:
    with open("screen_calibration.json", "r") as f:
        calibration = json.load(f)

    screen_corners = np.array(
        calibration["screen_corners"],
        dtype=np.float32
    )

    print("Screen calibration loaded.")

except Exception as e:
    screen_corners = None
    print("screen_calibration.json nahi mila.")
    print("Screen targeting disabled.")


# ============================================================
# AGENT
# ============================================================

agent = GestureAgent()


# ============================================================
# HAND DETECTOR
# ============================================================

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)


# ============================================================
# SPIDER-MAN GESTURE
# ============================================================

def is_spiderman_gesture(hand):

    index_up = hand[8].y < hand[6].y
    middle_down = hand[12].y > hand[10].y
    ring_down = hand[16].y > hand[14].y
    little_up = hand[20].y < hand[18].y

    return (
        index_up
        and middle_down
        and ring_down
        and little_up
    )


# ============================================================
# SCREEN TARGET
# ============================================================

def get_screen_target(finger_x, finger_y, frame_width, frame_height):

    if screen_corners is None:
        return (
            frame_width // 2,
            frame_height // 2
        )

    # Convert finger position into normalized coordinates
    nx = finger_x / frame_width
    ny = finger_y / frame_height

    # Screen center
    center = np.mean(screen_corners, axis=0)

    # Approximate target on calibrated laptop screen
    target_x = center[0]
    target_y = center[1]

    # Use finger horizontal direction
    if nx < 0.45:
        target_x = np.min(screen_corners[:, 0])
    elif nx > 0.55:
        target_x = np.max(screen_corners[:, 0])

    # Use finger vertical direction
    if ny < 0.45:
        target_y = np.min(screen_corners[:, 1])
    elif ny > 0.55:
        target_y = np.max(screen_corners[:, 1])

    target_x = int(np.clip(
        target_x,
        np.min(screen_corners[:, 0]),
        np.max(screen_corners[:, 0])
    ))

    target_y = int(np.clip(
        target_y,
        np.min(screen_corners[:, 1]),
        np.max(screen_corners[:, 1])
    ))

    return target_x, target_y


# ============================================================
# WEB EFFECT
# ============================================================

def draw_web_shot(frame, start, target, progress):

    sx, sy = start
    tx, ty = target
    cx = int(sx + (tx - sx) * progress)
    cy = int(sy + (ty - sy) * progress)

    dx = tx - sx
    dy = ty - sy
    length = max(1.0, math.hypot(dx, dy))
    px = -dy / length
    py = dx / length

    # Soft cinematic glow behind the moving web
    glow = np.zeros_like(frame)
    cv2.line(glow, (sx, sy), (cx, cy), (255, 255, 255), 10, cv2.LINE_AA)
    glow = cv2.GaussianBlur(glow, (0, 0), 10)
    frame = cv2.addWeighted(frame, 1.0, glow, 0.22, 0)

    web = frame.copy()

    # Seven fine twisting strands
    strand_count = 7
    for s in range(strand_count):
        points = []
        base_offset = (s - (strand_count - 1) / 2) * 2.2

        for i in range(35):
            t = i / 34
            x = sx + (cx - sx) * t
            y = sy + (cy - sy) * t
            wave1 = math.sin(t * math.pi * 10 + s * 0.7) * 2.2
            wave2 = math.sin(t * math.pi * 4 + s) * 1.4
            offset = base_offset + wave1 + wave2
            x += px * offset
            y += py * offset
            points.append((int(x), int(y)))

        for i in range(len(points) - 1):
            cv2.line(
                web, points[i], points[i + 1], (250, 250, 250),
                2 if s in (2, 3, 4) else 1, cv2.LINE_AA
            )

    # Curved cross threads
    for ring in range(2, 13):
        t = ring / 13
        center_x = sx + (cx - sx) * t
        center_y = sy + (cy - sy) * t
        half_width = 5 + 16 * t
        cv2.ellipse(
            web,
            (int(center_x), int(center_y)),
            (max(2, int(half_width)), max(1, int(half_width * 0.30))),
            math.degrees(math.atan2(dy, dx)),
            0, 180, (235, 235, 235), 1, cv2.LINE_AA
        )

    # Bright web head
    cv2.circle(web, (cx, cy), 7, (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(web, (cx, cy), 14, (235, 235, 235), 1, cv2.LINE_AA)

    frame = cv2.addWeighted(frame, 0.45, web, 0.95, 0)

    # Sticky web spread at the laptop screen
    if progress >= 1.0:
        impact = frame.copy()

        cv2.circle(impact, (tx, ty), 8, (255, 255, 255), -1, cv2.LINE_AA)

        # Concentric web rings
        for radius in (18, 34, 52, 72):
            cv2.circle(impact, (tx, ty), radius, (245, 245, 245), 2, cv2.LINE_AA)

        # Radial strands with a slight curve
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            points = []
            end_distance = 88

            for j in range(18):
                t = j / 17
                x = tx + math.cos(rad) * end_distance * t
                y = ty + math.sin(rad) * end_distance * t
                curve = math.sin(t * math.pi) * 6
                x += -math.sin(rad) * curve
                y += math.cos(rad) * curve
                points.append((int(x), int(y)))

            for j in range(len(points) - 1):
                cv2.line(impact, points[j], points[j + 1], (245, 245, 245), 2, cv2.LINE_AA)

        # Fine secondary spokes
        for angle in range(15, 360, 30):
            rad = math.radians(angle)
            ex = int(tx + math.cos(rad) * 62)
            ey = int(ty + math.sin(rad) * 62)
            cv2.line(impact, (tx, ty), (ex, ey), (220, 220, 220), 1, cv2.LINE_AA)

        # Impact glow
        impact_glow = np.zeros_like(frame)
        cv2.circle(impact_glow, (tx, ty), 45, (255, 255, 255), -1, cv2.LINE_AA)
        impact_glow = cv2.GaussianBlur(impact_glow, (0, 0), 18)
        frame = cv2.addWeighted(frame, 1.0, impact_glow, 0.22, 0)
        frame = cv2.addWeighted(frame, 0.55, impact, 0.95, 0)

    return frame

# ============================================================
# MAIN CAMERA
# ============================================================

with HandLandmarker.create_from_options(options) as detector:

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera open nahi hua!")
        exit()

    # --------------------------------------------------------
    # SHOOT STATE
    # --------------------------------------------------------

    shooting = False
    shoot_start_time = 0

    shoot_start = (0, 0)
    shoot_target = (0, 0)

    shoot_duration = 0.65

    # Gesture stability
    gesture_frames = 0
    required_gesture_frames = 4

    # Prevent immediate repeated shooting
    last_shot_time = 0
    shot_cooldown = 1.0

    print("----------------------------------")
    print("AI Gesture Agent Started")
    print("Spider-Man gesture ready")
    print("Press Q to quit")
    print("----------------------------------")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera frame nahi mila!")
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = detector.detect(mp_image)

        # ====================================================
        # HAND DRAWING
        # ====================================================

        detected_spiderman = False
        shooting_hand = None

        if result.hand_landmarks:

            for hand in result.hand_landmarks:

                # --------------------------------------------
                # RED DOTS
                # --------------------------------------------

                for landmark in hand:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (0, 0, 255),
                        -1,
                        cv2.LINE_AA
                    )

                # --------------------------------------------
                # GREEN CONNECTION LINES
                # --------------------------------------------

                for connection in HandLandmarksConnections.HAND_CONNECTIONS:

                    start_idx = connection.start
                    end_idx = connection.end

                    x1 = int(
                        hand[start_idx].x * width
                    )
                    y1 = int(
                        hand[start_idx].y * height
                    )

                    x2 = int(
                        hand[end_idx].x * width
                    )
                    y2 = int(
                        hand[end_idx].y * height
                    )

                    cv2.line(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )

                # --------------------------------------------
                # CHECK SPIDER-MAN GESTURE
                # --------------------------------------------

                if is_spiderman_gesture(hand):

                    detected_spiderman = True
                    shooting_hand = hand

        # ====================================================
        # GESTURE STABILITY
        # ====================================================

        if detected_spiderman:

            gesture_frames += 1

        else:

            gesture_frames = 0

        # ====================================================
        # SHOOT ONLY WHEN GESTURE IS CONFIRMED
        # ====================================================

        current_time = time.time()

        if (
            detected_spiderman
            and gesture_frames >= required_gesture_frames
            and not shooting
            and current_time - last_shot_time > shot_cooldown
        ):

            index_tip = shooting_hand[8]

            finger_x = int(
                index_tip.x * width
            )

            finger_y = int(
                index_tip.y * height
            )

            # --------------------------------------------
            # AGENT DECISION
            # --------------------------------------------

            decision = agent.decide(
                "WEB_SHOOT",
                1.0,
                finger_x,
                finger_y
            )

            # --------------------------------------------
            # EXECUTE ONLY IF AGENT APPROVES
            # --------------------------------------------

            if decision.get("execute", False):

                shoot_start = (
                    finger_x,
                    finger_y
                )

                shoot_target = get_screen_target(
                    finger_x,
                    finger_y,
                    width,
                    height
                )

                shooting = True
                shoot_start_time = time.time()
                last_shot_time = current_time

                # Play cinematic web sound
                threading.Thread(
                    target=play_shoot_sound,
                    daemon=True
                ).start()

                print("WEB SHOOT!")

            gesture_frames = 0

        # ====================================================
        # DRAW SHOOTING EFFECT
        # ====================================================

        if shooting:

            elapsed = time.time() - shoot_start_time

            progress = elapsed / shoot_duration

            if progress >= 1.0:

                progress = 1.0

                frame = draw_web_shot(
                    frame,
                    shoot_start,
                    shoot_target,
                    progress
                )

                # Keep impact briefly
                if elapsed > shoot_duration + 0.25:
                    shooting = False

            else:

                frame = draw_web_shot(
                    frame,
                    shoot_start,
                    shoot_target,
                    progress
                )

        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "AI Gesture Agent",
            frame
        )

        # Q = quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()