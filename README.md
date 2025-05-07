# eInkFrame - An eInk Digital Picture Frame Powered by Raspberry Pi and Python

### The eInkFrame is a robust digital picture frame powered by Raspberry Pi that utilizes a [Waveshare 7.3 inch 7-Color ePaper Display]([https://www.waveshare.com/7.3inch-e-paper-hat-f.htm]) for a natural look. Simply upload images in a supported format to a micro SD card, and the display will automatically cycle through them at a customizable interval!

## Contents:
- [Required Hardware](#required-hardware)
- [Pi Setup](#setup)
- [Assembly](#assembly)
- [Using The Frame](#using)

## Required Hardware

- **Raspberry Pi Zero 2 W**
- **ePaper Display:** The current version of this application only supports the [Waveshare 7.3 inch 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)
- **Picture Frame**: 3D print files available [here](https://www.printables.com/model/1287334-eink-picture-frame)
    - Note: Requires 2 M3x20mm screws and nuts
- **2 Micro SD cards (one for the Pi, one for images) ([link](https://amzn.to/3EoRUhC))**
- **Micro USB to Micro SD Card reader**
- **Micro USB Power Cable**

## Pi Setup

**Before starting**, ensure that your Pi is running Pi OS 32 or 64 bit (Pi OS Lite is not supported), and is connected to your home network.
If you need more guidance on setting up Pi OS, follow the [steps outlined here](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system)

Once your Pi has booted, open Command Prompt (Windows) or Terminal (Mac), and SSH into the Pi using the following command (replace 'pi' and 'pi.local' with your configured username and hostname)
```
ssh pi@pi.local
```

Once you are connected to the PI via SSH, run the following commands to complete the setup:
```
git clone https://github.com/EnriqueNeyra/eInkFrame.git 
cd eInkFrame
sudo bash setup.sh
```

Be sure to reboot the Pi after the setup is complete!


