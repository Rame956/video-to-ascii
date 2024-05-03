import cv2
import numpy as np
import time
import sys
import shutil
from moviepy.editor import VideoFileClip
import pygame

ASCII_CHARS = '@%#*+=-:. '
output_audio_file = 'audio.wav'

def extract_audio(video_file, output_audio_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio_file)

def play_audio(audio_file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    time.sleep(1)
    pygame.mixer.music.play()

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

def video_to_ascii(video_file, fps=120):
    cap = cv2.VideoCapture(video_file)
    delay = 1 / fps
    terminal_width, terminal_height = shutil.get_terminal_size()
    ascii_width = terminal_width - 1
    max_ascii_height = min(terminal_height, int(ascii_width / (cap.get(cv2.CAP_PROP_FRAME_WIDTH) / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    play_audio(output_audio_file)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        ascii_frame = image_to_ascii(frame, ascii_width, max_ascii_height)
        sys.stdout.write(ascii_frame)
        sys.stdout.flush()
        time.sleep(delay)
        
    cap.release()

video_file = 'test.mp4'
extract_audio(video_file, output_audio_file)
video_to_ascii(video_file)