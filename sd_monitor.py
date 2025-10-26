"""SD card monitoring and frame manager coordination.

This module continuously monitors for SD card insertion/removal and manages
the frame_manager.py subprocess accordingly. It handles automatic restart
of the image processing pipeline when SD cards are swapped.

The monitor reads refresh time configuration from the SD card and passes it
to the frame manager, enabling dynamic display timing control.
"""

import os
import signal
import subprocess
import sys
import time
from typing import List, Optional

# from lib.waveshare_epd import epdconfig

# System configuration and paths
USERNAME: str = os.getenv("SUDO_USER") or os.getenv("USER") or "pi"
SD_MOUNT_BASE: str = f"/media/{USERNAME}"  # Base path for SD card auto-mounts
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
IMAGE_PROCESSING_SCRIPT: str = os.path.join(SCRIPT_DIR, "frame_manager.py")

# Global state variables for SD monitoring
process: Optional[subprocess.Popen] = None  # Subprocess running frame_manager.py
sd_was_removed: bool = False  # Flag to track SD card removal state


def get_refresh_time(sd_path: str, filename: str = "refresh_time.txt") -> int:
    """Read refresh time configuration from SD card.

    Reads the display refresh interval from a text file on the SD card.
    This allows users to control image rotation timing by placing a
    configuration file on their SD card.

    Args:
        sd_path: Path to the mounted SD card directory
        filename: Name of the configuration file (default: "refresh_time.txt")

    Returns:
        Refresh time in seconds (defaults to 600 if file not found or invalid)
    """
    file_path: str = os.path.join(sd_path, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                number: str = f.read().strip()
                if number.isdigit():
                    refresh_time: int = int(number)
                    print(f"Using refresh time from {filename}: {refresh_time} seconds")
                    return refresh_time
                else:
                    print(f"Invalid number in {filename}, defaulting to 600")
                    return 600
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return 600
    else:
        print(f"{filename} not found, defaulting to 600")
        return 600


def start_frame_manager(sd_path: str) -> None:
    """Start the frame manager subprocess for image processing and display.

    Launches frame_manager.py as a separate process to handle image conversion
    and display management. Gracefully terminates any existing process before
    starting a new one.

    Args:
        sd_path: Path to the mounted SD card containing source images
    """
    global process
    # Terminate any existing frame manager process
    if process is not None and process.poll() is None:
        print("Stopping existing image processing script...")
        process.send_signal(signal.SIGTERM)  # Send graceful termination signal
        process.wait()  # Wait for process to fully terminate
        print("Existing image processing script stopped.")

    # Read refresh time configuration from SD card
    refresh_time_sec: int = get_refresh_time(sd_path)

    # Launch frame manager with SD path and refresh time parameters
    print(f"Starting image processing script with path {sd_path}...")
    process = subprocess.Popen(
        ["python3", IMAGE_PROCESSING_SCRIPT, sd_path, str(refresh_time_sec)],
        stdout=sys.stdout,  # Forward output to parent process
        stderr=sys.stderr,  # Forward errors to parent process
        text=True,
    )
    print("Frame manager started successfully")


def monitor_sd_card() -> None:
    """Continuously monitor SD card insertion/removal and manage frame_manager.

    Runs an infinite loop monitoring the SD card mount directory. Automatically
    starts the frame manager when an SD card is detected and handles graceful
    restart when SD cards are swapped.

    The monitor checks every 2 seconds for changes in SD card status.
    """
    global process, sd_was_removed
    sd_inserted: bool = False  # Track current SD card insertion state

    while True:
        try:
            # Scan for mounted SD card directories
            items: List[str] = os.listdir(SD_MOUNT_BASE)
            valid_dirs: List[str] = [item for item in items if os.path.isdir(os.path.join(SD_MOUNT_BASE, item))]

            if valid_dirs:
                # Use the first valid directory as SD card path
                sd_path: str = os.path.join(SD_MOUNT_BASE, valid_dirs[0])

                # Start/restart frame manager on fresh insertion or after removal
                if not sd_inserted or sd_was_removed:
                    if sd_was_removed:
                        print("SD card reinserted. Restarting frame_manager...")
                    else:
                        print("SD card inserted. Starting frame_manager...")

                    start_frame_manager(sd_path)
                    sd_inserted = True
                    sd_was_removed = False  # Reset removal flag after successful start

            else:
                # Handle SD card removal
                if sd_inserted:
                    print("SD card removed.")
                    sd_inserted = False
                    sd_was_removed = True  # Set flag to trigger restart on reinsertion

        except Exception as e:
            print(f"Error monitoring SD card: {e}")

        time.sleep(2)  # Poll interval for SD card status changes


def cleanup_stale_mounts() -> None:
    """Remove stale or inaccessible mount directories.

    Cleans up leftover mount directories that may remain after improper
    SD card removal. This prevents issues with phantom mounts that can
    interfere with proper SD card detection.
    """
    # Scan all directories in the mount base path
    for folder in os.listdir(SD_MOUNT_BASE):
        full_path: str = os.path.join(SD_MOUNT_BASE, folder)

        # Only process actual directories
        if not os.path.isdir(full_path):
            continue

        # Test directory accessibility (read + execute permissions)
        if not os.access(full_path, os.R_OK | os.X_OK):
            print(f"Stale or inaccessible mount detected: {full_path}, attempting to remove...")

            # Attempt to remove stale mount directory
            try:
                subprocess.run(["sudo", "rm", "-r", full_path], check=True)
                print(f"Removed stale mount folder: {full_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to remove {full_path} (subprocess error): {e}")
            except Exception as e:
                print(f"Unexpected error removing {full_path}: {e}")


def main() -> None:
    """Main entry point for SD card monitoring.

    Performs initial cleanup of stale mounts then begins continuous
    monitoring of SD card insertion/removal events.
    """
    print("Starting SD card monitor...")
    cleanup_stale_mounts()  # Clean up any leftover mount directories
    monitor_sd_card()  # Begin continuous monitoring loop


if __name__ == "__main__":
    main()
