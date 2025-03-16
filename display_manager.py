import os
import sys
import time
import random
from PIL import Image
from lib.waveshare_epd import epd7in3f

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(SCRIPT_DIR, 'lib')
sys.path.append(LIB_PATH)

class DisplayManager:

    def __init__(self, image_folder):
        self.last_display_time = time.time()
        self.last_selected_image = None
        self.image_folder = image_folder
        self.rotation = 0
        self.refresh_time = 180
        self.epd = epd7in3f.EPD()
        self.epd.init()


    def fetch_image_files(self):
        return [f for f in os.listdir(self.image_folder)]


    def select_random_image(self, images):
        # If one image or less
        if len(images) <= 1:
            return images[0]
        
        # Select a random image unless it was previously selected
        random_image = random.choice([img for img in images if img != self.last_selected_image])
        
        return random_image


    def clear_display(self):
        self.epd.init()
        self.epd.Clear()


    def display_image(self):
        self.epd.init()
        
        images = self.fetch_image_files()
        random_image = self.select_random_image(images)
        self.last_selected_image = random_image
            
        # Open and display the image
        with Image.open(os.path.join(self.image_folder, random_image)) as pic:
            pic = pic.rotate(self.rotation)
            self.epd.display(self.epd.getbuffer(pic))
            self.last_display_time = time.time()
            #self.epd.sleep()

        while True:
            current_time = time.time()
            elapsed_time = current_time - self.last_display_time
            
            if elapsed_time >= self.refresh_time:
                images = self.fetch_image_files()
                random_image = self.select_random_image(images)
                self.last_selected_image = random_image

                # Open and display the image
                with Image.open(os.path.join(self.image_folder, random_image)) as pic:
                    pic = pic.rotate(self.rotation)
                    self.epd.display(self.epd.getbuffer(pic))
                    self.last_display_time = time.time()
                    #self.epd.sleep()
