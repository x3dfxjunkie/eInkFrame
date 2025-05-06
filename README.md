# eInkFrame - An eInk Digital Picture Frame Powered by Raspberry Pi and Python

### The eInkFrame is a robust digital picture frame powered by Raspberry Pi that utilizes a [Waveshare 7.3 inch 7-Color ePaper Display]([https://www.waveshare.com/7.3inch-e-paper-hat-f.htm]) for a natural look. Simply upload images in a supported format to a micro SD card, and the display will automatically cycle through them at a customizable interval!

## Contents:
- [Required Hardware](#required-hardware-and-assembly)
- [Pi Setup](#setup)
- [Assembly](#assembly)
- [Using The Frame](#using)

## Required Hardware

- **Raspberry Pi Zero 2 W**
- **ePaper Display:** The current version of this application only supports the [Waveshare 7.3 inch 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)
- **Picture Frame**: Buy a frame, design your own, or use the 3D print files available [here](link tbd)
    - Note: The 3D printed frame requires 2 M3x20mm screws and nuts
- **2 Micro SD cards (one for the Pi, one for images)**
- **Micro USB to Micro SD Card reader**
- **Micro USB Power Cable**

## Pi Setup

**Before starting**, ensure that your Pi is running Pi OS 32 or 64 bit (Pi OS Lite is not supported), and is connected to your home network

Upload images to the SD card (supported formats are JPG, JPEG, PNG, and BMP) and insert the card using your micro SD card reader adapter.

Run the following commands to complete the setup:
```
git clone https://github.com/EnriqueNeyra/eInkFrame.git 
cd eInkFrame
sudo bash setup.sh
```

Be sure to reboot the Pi after the setup is complete!
