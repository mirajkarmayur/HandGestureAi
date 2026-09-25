from pycaw.pycaw import AudioUtilities

devices = AudioUtilities.GetSpeakers()
volume_control = devices.EndpointVolume

# Remember current volume
original_volume = volume_control.GetMasterVolumeLevelScalar()

print(f"Current volume: {int(original_volume * 100)}%")

# Set volume to 30%
volume_control.SetMasterVolumeLevelScalar(0.30, None)

print("Volume changed to 30%")

input("Press Enter to restore your original volume...")

# Restore original volume
volume_control.SetMasterVolumeLevelScalar(original_volume, None)

print(f"Volume restored to {int(original_volume * 100)}%")
