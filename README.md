# pyePaper - A ePaper/eInk Digital Picture Frame Powered by Raspberry Pi

### The pyePaper is a robust digital picture frame powered by Raspberry Pi that utilizes a [Waveshare 7.3 inch 7-Color ePaper Display]([https://www.waveshare.com/5.65inch-e-paper-module-f.htm](https://www.waveshare.com/7.3inch-e-paper-hat-f.htm) for a natural look. Simply upload images in a supported format to an SD card, and the display will actomatically cycle through them at a customizable interval!

## Contents:
- [Required Hardware](#required-hardware-and-assembly)  
- [Setup](#setup)  
- [Video Demo](#video-demo)

## Required Hardware

- **Raspberry Pi Zero 2 W**
- **ePaper Display:** The current version of this application only supports the [Waveshare 7.3 inch 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)
- **Picture Frame**: Buy a frame, design your own, or use the 3D print files available [here](link tbd)

## Setup

**Before starting**, ensure that your Pi is running Pi OS 32 or 64 bit, and is connected to your home network

Upload images to the SD card (supported formats are JPG, JPEG, PNG, and BMP), and plug the SD card in using your micro SD card reader adapter.

Run the following commands to complete the setup:
```
git clone https://github.com/EnriqueNeyra/py-ePaperFrame.git 
cd py-ePaperFrame
sudo bash setup.sh
```

Be sure to reboot the Pi after the setup is complete!

## Video Demo
Note: The video was shortened due to upload size constraints. Actual screen refresh time is ~30 seconds
<video src="" />
