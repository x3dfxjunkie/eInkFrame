import os
import sys
import time
import subprocess
import signal
import gpiozero
# from lib.waveshare_epd import epdconfig

SD_MOUNT_BASE = "/media/pi"  # Adjust as needed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PROCESSING_SCRIPT = os.path.join(SCRIPT_DIR, "frame_manager.py")
process = None  # Holds the subprocess running frame_manager.py
sd_was_removed = False  # Track if SD card was removed


def get_refresh_time(sd_path, filename="refresh_time.txt"):
    """Read refresh time (sec) from text file in the SD card directory."""
    file_path = os.path.join(sd_path, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                number = f.read().strip()
                if number.isdigit():
                    return int(number)
                else:
                    print(f"Invalid number in {filename}, defaulting to 600")
                    return 600
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return 600
    else:
        print(f"{filename} not found, defaulting to 600")
        return 600


def start_frame_manager(sd_path):
    """Start the image processing script as a separate process."""
    global process
    if process is not None and process.poll() is None:
        print("Stopping existing image processing script...")
        process.send_signal(signal.SIGTERM)  # Gracefully terminate the process
        process.wait()
        print("Existing image processing script stopped.")
    
    # Read number from file
    refresh_time_sec = get_refresh_time(sd_path)
    
    print(f"Starting image processing script with path {sd_path}...")
    process = subprocess.Popen(
        ["python3", IMAGE_PROCESSING_SCRIPT, sd_path, str(refresh_time_sec)], 
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
            valid_dirs = [item for item in items if os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]
            
            if valid_dirs:
                sd_path = os.path.join(SD_MOUNT_BASE, valid_dirs[0])

                if not sd_inserted or sd_was_removed:  
                    # Restart frame_manager only if it's a fresh insert or after removal
                    if sd_was_removed:
                        print("SD card reinserted. Restarting frame_manager...")
                    else:
                        print("SD card inserted. Starting frame_manager...")
                    
                    start_frame_manager(sd_path)
                    sd_inserted = True
                    sd_was_removed = False  # Reset flag after starting

            else:
                if sd_inserted:
                    print("SD card removed.")
                    sd_inserted = False
                    sd_was_removed = True  # Mark that the SD card was removed

        except Exception as e:
            print(f"Error monitoring SD card: {e}")

        time.sleep(2) # Check every 2 seconds


def cleanup_stale_mounts():

    for folder in os.listdir(SD_MOUNT_BASE):
        full_path = os.path.join(SD_MOUNT_BASE, folder)

        # Skip non-directories
        if not os.path.isdir(full_path):
            continue

        # Try to access the folder (read + execute)
        if not os.access(full_path, os.R_OK | os.X_OK):
            print(f"Stale or inaccessible mount detected: {full_path}, attempting to remove...")

            # Try to remove it
            try:
                subprocess.run(["sudo", "rm", "-r", full_path], check=True)
                print(f"Removed stale mount folder: {full_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove {full_path} (subprocess error): {e}")
            except Exception as e:
                print(f"Unexpected error removing {full_path}: {e}")


if __name__ == "__main__":
    cleanup_stale_mounts()
    monitor_sd_card()
