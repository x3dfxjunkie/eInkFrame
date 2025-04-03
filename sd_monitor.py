import os
import sys
import time
import subprocess
import signal
from lib.waveshare_epd import epdconfig

SD_MOUNT_BASE = "/media/enriquepi"  # Adjust as needed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PROCESSING_SCRIPT = os.path.join(SCRIPT_DIR, "frame_manager.py")
BUSY_PIN = 24
process = None  # Holds the subprocess running image_processing.py
sd_was_removed = False  # Track if SD card was removed


def is_display_busy():
     return epdconfig.digital_read(BUSY_PIN) == 0 # 0 means busy, 1 means idle


# def wait_for_sd_card():
#     """Wait for an SD card to be inserted and return its mount path."""
#     while True:
#         items = os.listdir(SD_MOUNT_BASE)
#         valid_dirs = [item for item in items if item != "rootfs" and os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]

#         if len(valid_dirs) == 1:
#             sd_path = os.path.join(SD_MOUNT_BASE, valid_dirs[0])
#             print(f"SD card detected at: {sd_path}")
#             return sd_path

#         print("SD card not found. Waiting...")
#         time.sleep(5)


def start_frame_manager(sd_path):
    """Start the image processing script as a separate process."""
    global process
    if process is not None and process.poll() is None:
        print("Stopping existing image processing script...")
        process.send_signal(signal.SIGTERM)  # Gracefully terminate the process
        process.wait()

    while is_display_busy():
        print("Waiting for display to be idle...")
        time.sleep(2)
    
    print(f"Starting image processing script with path {sd_path}...")
    process = subprocess.Popen(
        ["python3", IMAGE_PROCESSING_SCRIPT, sd_path], 
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE,
        stdout=sys.stdout, 
        stderr=sys.stderr,
        text=True)
    print("Started...")


def monitor_sd_card():
    """Continuously monitor the SD card and restart frame_manager if reinserted."""
    global process, sd_was_removed
    sd_inserted = False

    while True:
        try:
            items = os.listdir(SD_MOUNT_BASE)
            valid_dirs = [item for item in items if item != "rootfs" and os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]
            
            if valid_dirs:
                sd_path = os.path.join(SD_MOUNT_BASE, valid_dirs[0])

                if not sd_inserted:
                    print("SD card inserted. Starting frame_manager...")
                    start_frame_manager(sd_path)
                    sd_inserted = True
                    sd_was_removed = False  # Reset removal flag

                elif sd_was_removed:  # Restart only if SD was previously removed
                    print("SD card reinserted. Restarting frame_manager...")
                    start_frame_manager(sd_path)
                    sd_was_removed = False  # Reset flag after restart

            else:
                if sd_inserted:
                    print("SD card removed.")
                    sd_inserted = False
                    sd_was_removed = True  # Mark that the SD card was removed

        except Exception as e:
            print(f"Error monitoring SD card: {e}")

        time.sleep(2)  # Adjust polling rate as needed

if __name__ == "__main__":
    monitor_sd_card()
