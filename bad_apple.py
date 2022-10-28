#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import numpy as np
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V3
import time
import os
from PIL import Image,ImageDraw,ImageFont
import traceback




frames_list = list(np.sort(np.array(os.listdir(picdir))))
print(len(frames_list))
for frame in frames_list:
    frame_index = frames_list.index(frame)
    try:
        for z in range(1, 15):
            frames_list.remove(frames_list[frame_index + z])
    except:
        continue
print(len(frames_list))
#frames_list = os.listdir(picdir)
try:

    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    # font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    # font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    image1 = Image.new('1', (epd.height, epd.width), 255)
    epd.displayPartBaseImage(epd.getbuffer(image1))
    
    first = image1
    for frame in frames_list:
        bmp = Image.open(os.path.join(picdir, frame))
        bmp = bmp.resize((255,122)).rotate(180)
        first.paste(bmp, (2,2))
        print(f'Frame - {frame}', end='\r')
        epd.displayPartial(epd.getbuffer(first))

    epd.Clear(0xFF)
    epd.sleep()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
