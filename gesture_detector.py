
# =========================================================
# GESTURE DETECTOR
# =========================================================

import math


# =========================================================
# DISTANCE BETWEEN TWO LANDMARKS
# =========================================================

def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )


# =========================================================
# DETECT HAND GESTURE
# =========================================================

def detect_gesture(hand):

    index_up = (
        distance(hand[8], hand[0])
        > distance(hand[6], hand[0])
    )

    middle_up = (
        distance(hand[12], hand[0])
        > distance(hand[10], hand[0])
    )

    ring_up = (
        distance(hand[16], hand[0])
        > distance(hand[14], hand[0])
    )

    pinky_up = (
        distance(hand[20], hand[0])
        > distance(hand[18], hand[0])
    )


    # FIST
    if (
        not index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):
        return "FIST"


    # INDEX
    elif (
        index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):
        return "INDEX"


    # PEACE
    elif (
        index_up
        and middle_up
        and not ring_up
        and not pinky_up
    ):
        return "PEACE"


    # OPEN HAND
    elif (
        index_up
        and middle_up
        and ring_up
        and pinky_up
    ):
        return "OPEN HAND"


    # UNKNOWN
    return "UNKNOWN"
