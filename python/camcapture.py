#!/usr/bin/python3

from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import imutils
import copy
import cv2

from imutils.video import VideoStream

display = None
vidSrc = None
txtBox = None
thread = None
mainWin = None
stopEvent = None
inputFrame = None

def videoLoop():
	global display
	global inputFrame

	try:
		while not stopEvent.is_set():
			tlpw = 0.25
			tlph = 0.1
			brpw = 0.75
			brph = 0.9

			displayFrame = vidSrc.read()
			inputFrame = copy.deepcopy(displayFrame)

			width = inputFrame.shape[1]
			height = inputFrame.shape[0]
			tl = (int(tlpw*width), int(tlph*height))
			br = (int(brpw*width), int(brph*height))

			inputFrame = inputFrame[tl[1]:br[1],tl[0]:br[0]]

			displayFrame = imutils.resize(displayFrame, width=500)
	
			width = displayFrame.shape[1]
			height = displayFrame.shape[0]

			tl = (int(tlpw*width), int(tlph*height))
			br = (int(brpw*width), int(brph*height))

			cv2.rectangle(displayFrame, tl, br,
				(255, 0, 125), 3)
			displayImage = cv2.cvtColor(displayFrame, 
				cv2.COLOR_BGR2RGB)
			displayImage = Image.fromarray(displayImage)
			displayImage = ImageTk.PhotoImage(displayImage)
	
			if display is None:
				display = tki.Label(mainWin, image=displayImage)
				display.image = displayImage
				display.pack(side="left", padx=10, pady=10)
			else:
				display.configure(image=displayImage)
				display.image = displayImage

	except RuntimeError as e:
		print(e)

def checkLiveness():
	global inputFrame
	#add algorithm here inputFrame is the input

	curTxt = txtBox.get(1.0, END)
	txtBox.delete(1.0, END)
	txtBox.tag_configure("center", justify='center')
	if "LIVE" in curTxt:
		txtBox.configure(bg="red")
		txtBox.insert(INSERT, "SPOOF")
	else:
		txtBox.configure(bg="green")
		txtBox.insert(INSERT, "LIVE")
	txtBox.tag_add("center", "1.0", "end")

def onClose():
	stopEvent.set()
	vidSrc.stop()
	mainWin.quit()

if __name__ == "__main__":
	global txtBox
	global thread
	global vidSrc
	global mainWin
	global stopEvent

	mainWin = tki.Tk()
	mainWin.resizable(width=False, height=False)
	mainWin.geometry("500x500")

	vidSrc = VideoStream(0).start()

	guiframe = Frame(mainWin)
	guiframe.pack(side="bottom")
	btn = tki.Button(guiframe, text="Check Liveness",
		command=checkLiveness)
	btn.pack(side="left", fill="y", expand="no", padx=10,
		pady=10)

	txtBox = Text(guiframe, height=0, width=10, spacing1=0.5,
		font=("Rouge", 16), fg="white")
	txtBox.pack(side="right", fill="x", expand="no", 
		padx=10, pady=10)
	
	stopEvent = threading.Event()
	thread = threading.Thread(target=videoLoop, args=())
	thread.start()

	mainWin.wm_title("Liveness Checking Software")
	mainWin.wm_protocol("WM_DELETE_WINDOW", onClose)
        
mainWin.mainloop();
