import cv2
import numpy as np
import time
import sys
import shutil

ASCII_CHARS = '@%#*+=-:. '

def image_to_ascii(image, ascii_width, ascii_height):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(grayscale_image, (ascii_width, ascii_height))
    
    ascii_str = ""
    for row in resized_image:
        for pixel in row:
            normalized_pixel = pixel / 255
            index = int(normalized_pixel * (len(ASCII_CHARS) - 1))
            ascii_str += ASCII_CHARS[index]
        ascii_str += '\n'
    
    return ascii_str

def video_to_ascii(video_file, fps=60):
    cap = cv2.VideoCapture(video_file)
    delay = 1 / fps
    terminal_width, terminal_height = shutil.get_terminal_size()
    ascii_width = terminal_width - 1
    max_ascii_height = min(terminal_height, int(ascii_width / (cap.get(cv2.CAP_PROP_FRAME_WIDTH) / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        ascii_frame = image_to_ascii(frame, ascii_width, max_ascii_height)
        sys.stdout.write(ascii_frame)
        sys.stdout.flush()
        time.sleep(delay)
        
    cap.release()

video_file = 'test4.mp4'
video_to_ascii(video_file)