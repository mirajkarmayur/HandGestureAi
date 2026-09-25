import cv2
import mediapipe as mp
import time
from collections import deque, Counter

from gesture_detector import detect_gesture
from hand_controller import VolumeController

from config import (
    HISTORY_SIZE,
    STABLE_FRAMES,
    CAMERA_INDEX,
    CAMERA_BUFFER_SIZE,
    MODEL_PATH
)


# =========================================================
# MEDIAPIPE SETUP
# =========================================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE
)


# =========================================================
# GESTURE SETTINGS
# =========================================================

gesture_history = deque(maxlen=HISTORY_SIZE)

candidate_gesture = "NONE"
candidate_count = 0

stable_gesture = "NONE"
last_processed_gesture = "NONE"


# =========================================================
# WINDOWS VOLUME CONTROL
# =========================================================

volume_controller = VolumeController()

volume = volume_controller.get_volume()
muted = volume_controller.is_muted()

print(f"Windows volume: {volume}%")
print(f"Muted: {int(muted)}")


# =========================================================
# MAIN PROGRAM
# =========================================================

with HandLandmarker.create_from_options(options) as landmarker:

    camera = cv2.VideoCapture(CAMERA_INDEX)

    camera.set(
        cv2.CAP_PROP_BUFFERSIZE,
        CAMERA_BUFFER_SIZE
    )

    # =====================================================
    # FPS SMOOTHING
    # =====================================================

    previous_time = time.time()
    fps = 0

    # Smoothed FPS value
    fps_history = deque(maxlen=10)


    while True:

        ret, frame = camera.read()

        if not ret:
            break


        # =================================================
        # MIRROR CAMERA
        # =================================================

        frame = cv2.flip(frame, 1)


        # =================================================
        # FPS
        # =================================================

        current_time = time.time()

        delta_time = current_time - previous_time

        previous_time = current_time

        if delta_time > 0:

            instant_fps = 1 / delta_time

            fps_history.append(instant_fps)

            fps = sum(fps_history) / len(fps_history)


        # =================================================
        # MEDIAPIPE
        # =================================================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = landmarker.detect(mp_image)

        current_gesture = "NO HAND"


        # =================================================
        # HAND DETECTED
        # =================================================

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            current_gesture = detect_gesture(hand)


            # =================================================
            # GESTURE HISTORY
            # =================================================

            if current_gesture != "UNKNOWN":

                gesture_history.append(current_gesture)


            if len(gesture_history) >= 3:

                counts = Counter(gesture_history)

                voted_gesture, vote_count = counts.most_common(1)[0]


                if vote_count >= STABLE_FRAMES:

                    if voted_gesture != candidate_gesture:

                        candidate_gesture = voted_gesture
                        candidate_count = 1

                    else:

                        candidate_count += 1


                    if candidate_count >= 2:

                        if voted_gesture != stable_gesture:

                            stable_gesture = voted_gesture


                            # =================================================
                            # PROCESS GESTURE
                            # =================================================

                            if stable_gesture == "FIST":

                                pass


                            elif stable_gesture == "INDEX":

                                if last_processed_gesture == "FIST":

                                    volume = volume_controller.increase()

                                    muted = volume_controller.is_muted()

                                    print(
                                        f"Volume increased to {volume}%"
                                    )


                            elif stable_gesture == "PEACE":

                                if last_processed_gesture == "FIST":

                                    volume = volume_controller.decrease()

                                    muted = volume_controller.is_muted()

                                    print(
                                        f"Volume decreased to {volume}%"
                                    )


                            elif stable_gesture == "OPEN HAND":

                                muted = volume_controller.toggle_mute()

                                if muted:

                                    print("Windows volume MUTED")

                                else:

                                    print("Windows volume UNMUTED")


                            last_processed_gesture = stable_gesture


        # =================================================
        # NO HAND
        # =================================================

        else:

            current_gesture = "NO HAND"

            gesture_history.clear()

            candidate_gesture = "NONE"
            candidate_count = 0


        # =================================================
        # HAND LANDMARKS
        # =================================================

        if result.hand_landmarks:

            height, width, _ = frame.shape

            points = []

            for landmark in result.hand_landmarks[0]:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                points.append((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 0),
                    -1
                )


            connections = [

                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),

                (0, 5),
                (5, 6),
                (6, 7),
                (7, 8),

                (5, 9),
                (9, 10),
                (10, 11),
                (11, 12),

                (9, 13),
                (13, 14),
                (14, 15),
                (15, 16),

                (13, 17),
                (17, 18),
                (18, 19),
                (19, 20),

                (0, 17)
            ]


            for start, end in connections:

                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    (255, 0, 0),
                    2
                )


        # =================================================
        # COMPACT UI PANEL
        # =================================================

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (15, 15),
            (440, 385),
            (25, 25, 25),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            0.80,
            frame,
            0.20,
            0
        )


        # =================================================
        # TITLE
        # =================================================

        cv2.putText(
            frame,
            "HAND AI",
            (35, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "VOLUME CONTROLLER",
            (35, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (180, 180, 180),
            1
        )


        # =================================================
        # STATUS
        # =================================================

        status_text = (
            "HAND DETECTED"
            if result.hand_landmarks
            else "NO HAND"
        )

        cv2.putText(
            frame,
            status_text,
            (285, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1
        )


        # =================================================
        # GESTURE
        # =================================================

        display_gesture = stable_gesture

        if display_gesture == "NONE":

            display_gesture = "NO HAND"


        cv2.putText(
            frame,
            "GESTURE",
            (35, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (170, 170, 170),
            1
        )

        cv2.putText(
            frame,
            display_gesture,
            (35, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        # =================================================
        # VOLUME
        # =================================================

        cv2.putText(
            frame,
            "VOLUME",
            (35, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (170, 170, 170),
            1
        )


        if muted:

            volume_text = "MUTED"

        else:

            volume_text = f"{volume}%"


        cv2.putText(
            frame,
            volume_text,
            (35, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        # =================================================
        # VOLUME BAR
        # =================================================

        bar_x = 35
        bar_y = 230

        bar_width = 360
        bar_height = 20


        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (70, 70, 70),
            -1
        )


        filled_width = int(
            bar_width * volume / 100
        )


        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + filled_width, bar_y + bar_height),
            (0, 200, 0),
            -1
        )


        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (220, 220, 220),
            1
        )


        # =================================================
        # CONTROLS
        # =================================================

        cv2.putText(
            frame,
            "CONTROLS",
            (35, 285),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (170, 170, 170),
            1
        )


        cv2.putText(
            frame,
            "FIST > INDEX   +5",
            (35, 310),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "FIST > PEACE   -5",
            (35, 332),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "OPEN HAND     MUTE",
            (35, 354),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1
        )


        # =================================================
        # FPS
        # =================================================

        cv2.putText(
            frame,
            f"{int(fps)} FPS",
            (350, 365),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (170, 170, 170),
            1
        )


        # =================================================
        # DISPLAY
        # =================================================

        cv2.imshow(
            "Hand AI Volume Controller",
            frame
        )


        # =================================================
        # QUIT
        # =================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


    # =====================================================
    # CLEANUP
    # =====================================================

    camera.release()
    cv2.destroyAllWindows()
