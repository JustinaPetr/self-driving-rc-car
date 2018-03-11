import numpy as np
import cv2
import time
import os
import serial
import pygame
from picamera.array import PiRGBArray
from picamera import PiCamera
import glob
import re


def get_keys(board):
	'''The function checks which keyboard key is pressed, 
		sends a corresponding key input to Arduino and updates the output list'''
	  
	pygame.event.pump()
	output = [0,0,0,0,0] # create an output vector
	key = pygame.key.get_pressed() #returns a list of currently pressed keyboard keys
	if key[pygame.K_w]:
		board.write("F")
		print("Forward")
		output[0] = 1
	elif key[pygame.K_a]:
		board.write("L")
		print("Left")
		output[1] = 1
	elif key[pygame.K_s]:
		board.write("B")
		print("Backward")
		output[2] = 1
	elif key[pygame.K_d]:
		board.write("R")
		print("Right")
		output[3] = 1
	else:
		board.write("S")
		print("Stop")
		output[4] = 1
	pygame.display.update()
	return output
   
def check_data_dir():
	'''The function checks if data directory exists.
		If not - it creates one.'''
	
	print('Check data directory...')
	dir = './data/'
	if not os.path.exists(dir):
		os.makedirs(dir)

   
def datafile():
	"""The function checks the number of the latest data file
		created in the data directory and returns the number of the 
		next new file."""
		
	print('Return data file number...')
	files = sorted(glob.glob("./data/*.npy"))
	start = 1
	if len(files)>0:
		latest_file = max(files, key=os.path.getctime)
		file_no = re.findall(r'\d+', latest_file)[0]
		start = start + int(file_no)
	return start	
		
def initialise_camera():
	'''The function initialises a camera, sets the
		resolution and a framerate.'''
		
	print('Initialise camera...')
	camera = PiCamera()
	camera.resolution = (640, 480)
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size = (640,480))
	# allow the camera warmup
	time.sleep(0.1)
	return camera, rawCapture


def main():
	'''The function opens the serial port, captures camera frames 
		as well as keyboard inputs, and saves the data files in data directory.'''
		
	print('Initialise pygame input...')
	board = serial.Serial("/dev/ttyACM0", 9600) # open the serial port
	time.sleep(2)

	screen = pygame.display.set_mode([300,100]) #initialise pygame controller
	screen.fill([255,255,255])
	pygame.display.set_caption("Controller")
	
	check_data_dir()
	data_file_no = datafile()
	training_data = []
	
	camera, rawCapture = initialise_camera()
	print('Start capturing data')
	print('1')
	print('2')
	print('3')
	
	for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
		image = frame.array #collect the frame
		k = get_keys(board) # collect the output vector
		training_data.append([image, k]) # append the frame and output vector to training data
		rawCapture.truncate(0)
   
		#save 1000 frames per data file (so that saving the file wouldn't take too long)
		if len(training_data) % 1000 == 0: 
			np.save('./data/file{}'.format(data_file_no), training_data)
			data_file_no += 1
			training_data = []
			
if __name__=='__main__':
	main()