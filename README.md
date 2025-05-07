# eInkFrame - An eInk Digital Picture Frame Powered by Raspberry Pi and Python

### The eInkFrame is a robust digital picture frame powered by Raspberry Pi that utilizes a [Waveshare 7.3 inch 7-Color ePaper Display]([https://www.waveshare.com/7.3inch-e-paper-hat-f.htm]) for a natural look. Simply upload images in a supported format to a micro SD card, and the display will automatically cycle through them at a customizable interval!

## Contents:
- [Required Hardware](#required-hardware)
- [Pi Setup](#setup)
- [Assembly](#assembly)
- [Using The Frame](#using)

## Required Hardware

Micro SD Card Reader (option 1): https://amzn.to/4iNaMVC
Micro SD Card Reader (option 2): https://tinyurl.com/4p8etbcb

- **[Raspberry Pi Zero 2 W](https://amzn.to/3YBvaBV)**
- **[Pi Power Supply](https://amzn.to/42dMak0)**
- **ePaper Display:** The current version of this application only supports the [Waveshare 7.3 inch 7-Color ePaper Display](https://amzn.to/42fzjOk)
- **Picture Frame** 3D print files available [here](https://www.printables.com/model/1287334-eink-picture-frame)
    - Note: Requires 2 M3x20mm screws and nuts
- **2 Micro SD cards (one for the Pi, one for images) - [link](https://amzn.to/3EoRUhC)**
- **Micro USB to Micro SD Card reader** - [link](https://ebay.us/pmuPZh)**

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

## Assembly

1. Attach the Pi and driver board, ensuring that the pin headers are fully inserted into the driver board
![Screenshot 2025-05-06 190519](https://github.com/user-attachments/assets/6a8b445e-f5aa-4209-9d59-1f44771c8c97)

2. Insert the Pi and driver board into the enclosure
![Screenshot 2025-05-06 190430](https://github.com/user-attachments/assets/e239cbd2-ec13-4ce6-b5a3-7ec788c9c889)

3. Insert the M3 nuts into the slots at the bottom of the frame
![Screenshot 2025-05-06 190759](https://github.com/user-attachments/assets/1424cc05-c8ca-4eee-a023-0ed3894e8e58)

4. Carefully slide the eInk display into the frame, ensuring that it is secured under the small notch at the top of the frame
![Screenshot 2025-05-06 190910](https://github.com/user-attachments/assets/0aa116d8-0ff4-4fcd-921d-744f1de8a531)

5. Tuck the ribbon cables into the Pi enclosure, and connect to the display cable. 
![Screenshot 2025-05-06 191044](https://github.com/user-attachments/assets/1f097542-2afd-4506-b957-2a9bd27435b7)
![Screenshot 2025-05-06 191226](https://github.com/user-attachments/assets/05a9b906-0a23-47dd-a1ed-2d7c4fdf8e96)

6. Align the enclosure holes with the display, and attach the stand with 2 M3x20mm screws
![Screenshot 2025-05-06 191325](https://github.com/user-attachments/assets/280c1f53-32ee-486b-861c-43cb786ad754)


Assembly is now complete! Time to test it out...


