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


def is_display_busy():
     return epdconfig.digital_read(BUSY_PIN) == 0 # 0 means busy, 1 means idle


def wait_for_sd_card():
    """Wait for an SD card to be inserted and return its mount path."""
    while True:
        items = os.listdir(SD_MOUNT_BASE)
        valid_dirs = [item for item in items if os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]

        if len(valid_dirs) == 1:
            sd_path = os.path.join(SD_MOUNT_BASE, valid_dirs[0])
            print(f"SD card detected at: {sd_path}")
            return sd_path

        print("SD card not found. Waiting...")
        time.sleep(5)


def start_frame_manager(sd_path):
    """Start the image processing script as a separate process."""
    global process
    if process is not None and process.poll() is None:
        print("Stopping existing image processing script...")
        process.send_signal(signal.SIGTERM)  # Gracefully terminate the process
        process.wait()

    while not is_display_busy():
        print("Waiting for display to be idle...")
        time.sleep(2)
    
    print("Starting image processing script...")
    process = subprocess.Popen(["python3", IMAGE_PROCESSING_SCRIPT, sd_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def monitor_sd_card():
    """Continuously monitor SD card status and restart the process if needed."""
    global process
    print("Waiting for initial SD card insertion...")
    sd_path = wait_for_sd_card()
    start_frame_manager(sd_path)

    while True:
        time.sleep(2)
        items = os.listdir(SD_MOUNT_BASE)
        valid_dirs = [item for item in items if os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]
        sd_present = len(valid_dirs) >= 1

        if sd_present:
            if process is not None and process.poll() is None:
                print("SD card reinserted. Restarting process...")
                sd_path = wait_for_sd_card()
                start_frame_manager(sd_path)


if __name__ == "__main__":
    monitor_sd_card()
