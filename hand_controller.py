
# =========================================================
# WINDOWS VOLUME CONTROLLER
# =========================================================

from pycaw.pycaw import AudioUtilities

from config import (
    VOLUME_STEP,
    MIN_VOLUME,
    MAX_VOLUME
)


# =========================================================
# VOLUME CONTROLLER CLASS
# =========================================================

class VolumeController:

    def __init__(self):

        # Get Windows audio device
        self.devices = AudioUtilities.GetSpeakers()

        # Get volume control interface
        self.volume_control = self.devices.EndpointVolume


    # =====================================================
    # GET CURRENT VOLUME
    # =====================================================

    def get_volume(self):

        volume = int(
            self.volume_control.GetMasterVolumeLevelScalar() * 100
        )

        return volume


    # =====================================================
    # GET MUTE STATUS
    # =====================================================

    def is_muted(self):

        return bool(
            self.volume_control.GetMute()
        )


    # =====================================================
    # INCREASE VOLUME
    # =====================================================

    def increase(self):

        volume = self.get_volume()

        volume += VOLUME_STEP

        if volume > MAX_VOLUME:
            volume = MAX_VOLUME

        self.volume_control.SetMasterVolumeLevelScalar(
            volume / 100,
            None
        )

        # Same behavior as your original program:
        # increasing volume also unmutes Windows.

        self.volume_control.SetMute(0, None)

        return volume


    # =====================================================
    # DECREASE VOLUME
    # =====================================================

    def decrease(self):

        volume = self.get_volume()

        volume -= VOLUME_STEP

        if volume < MIN_VOLUME:
            volume = MIN_VOLUME

        self.volume_control.SetMasterVolumeLevelScalar(
            volume / 100,
            None
        )

        return volume


    # =====================================================
    # TOGGLE MUTE
    # =====================================================

    def toggle_mute(self):

        muted = self.is_muted()

        muted = not muted

        self.volume_control.SetMute(
            int(muted),
            None
        )

        return muted
