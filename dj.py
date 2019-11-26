# Automatic DJ 
# ************
# Play all audio files in a directory
# start the next file when the current file is still playing 
# so there is no gap between the songs and the dancers keep dancing

# parameters: see parser.add_argument statements below

# prerequisites: VLC media player, Python3 

# known issues: 
	# does not run on windows (?), positively tested with python3 on Mint 19.4 under Virtualbox

# todo: 
	# parameters for overlap, recursion, loop
	# how to handle non-audio files 
	# error handling 
	# overlap not only as percentage but also as time in seconds
	# interact with user while playing, this will work only with a GUI 
		# interactions: pause/play, stop after current, stop with fadeout, insert a song after current song, progress bar


import vlc
import argparse
from random import randrange, shuffle
import os
import time
import sys

import signal

def keyboardInterruptHandler(signal, frame):
	global Status
	if (Status == "PLAY_LAST"):
		Status = "FADEOUT"
		print (" stopping now")
	else:
		Status = "PLAY_LAST"
		print (" Stopping after current song, press ^C again for immediate stop")


parser = argparse.ArgumentParser(description = "play songs without pause, i.e. start the next song a few seconds before the current song ends", epilog = "To stop playing, press ^C (Ctrl-C, Strg-C,..). Prerequisites: VLC media player and python-vlc (VLC python bindings) installed. Runs on Python2 and Python3. Currently it seems to run on Linux, not on Windows. ")
parser.add_argument("-p", "--path", type=str, default=".",
					help="path to directory with audio files to play")
parser.add_argument("-o", "--overlap", type=int, default=10,
					help="percentage of length when to start next song")
parser.add_argument("-s", "--shuffle", type=str, default="yes",
					help="shuffle yes/no, default=yes")
parser.add_argument("-r", "--recursive", type=str, default="no",
					help="recursively search path yes/no, default=no")
args = parser.parse_args()

extensions = [".mp3", ".wav", ".wma", ".flac", ".m4a"]

files = []
if (('y' in args.recursive) or ('Y' in args.recursive) or ('j' in args.recursive) or ('J' in args.recursive)):
	# r=root, d=directories, f = files
	for r, d, f in os.walk(args.path):
		for file in f:
			filename, file_extension = os.path.splitext(file)
			if (file_extension in extensions):
				# print (file)
				files.append(os.path.join(r, file))
else:
	for entry in os.listdir(args.path):
		filename, file_extension = os.path.splitext(entry)
		# print (file_extension)
		if (file_extension in extensions):
			fullname = os.path.join(args.path, entry)
			# print (fullname)
			if os.path.isfile(fullname):
				files.append(fullname)

NumFiles = len(files)
print (str(NumFiles) + " files found")
if (NumFiles == 0):
	sys.exit()

if (('y' in args.shuffle) or ('Y' in args.shuffle) or ('j' in args.shuffle) or ('J' in args.shuffle)):
	shuffle (files)

p1 = vlc.MediaPlayer("")
p2 = vlc.MediaPlayer("")
# State.Ended --- State.Playing


Status = "START"

while (Status != "FINISH"):
	if (Status == "START"):
		Counter = 1
		Player1Current = True
		PlayerCurrent = p1
		PlayerNext    = p2
		f = files.pop (0)
		print (str(Counter) + "/"+ str(NumFiles) + ": " + f)
		PlayerCurrent.set_mrl (f)
		PlayerCurrent.play()
		PlayerCurrent.audio_set_volume (100)
		PlayerNext.audio_set_volume (100)
		Counter = Counter + 1
		signal.signal(signal.SIGINT, keyboardInterruptHandler)
		Status = "PLAY_SOLO"
	
	if (Status == "PLAY_SOLO"):
		if (PlayerCurrent.get_position() >= (1.0 - args.overlap / 100.0)):
			if (files):
				f = files.pop (0)
				print (str(Counter) + "/"+ str(NumFiles) + ": " + f)
				PlayerNext.set_mrl (f)
				PlayerNext.play()
				PlayerNext.audio_set_volume (100)
				Counter = Counter + 1
				Status = "PLAY_DOUBLE"
			else:
				Status = "PLAY_LAST"
				
	if (Status == "PLAY_DOUBLE"):
		if (str(PlayerCurrent.get_state()) == "State.Ended"):
			
			Player1Current = not Player1Current
			if (Player1Current): 
				PlayerCurrent = p1
				PlayerNext    = p2
			else:
				PlayerCurrent = p2
				PlayerNext    = p1
				
			Status = "PLAY_SOLO"

	if (Status == "PLAY_LAST"):
		if (str(PlayerCurrent.get_state()) == "State.Ended"):
			Status = "FINISH"
	
	if (Status == "FADEOUT"):
		Volume = 100
		while (Volume > 0):
			Volume = Volume - 5
			PlayerCurrent.audio_set_volume (Volume)
			time.sleep (0.1)
		Status = "FINISH"
	
	
	# print (Status + "___" + str(Player1Current) + "___" + str(p1.get_state()) + "___" + str(p1.get_position()) + "___" + str(p2.get_state()) + "___" + str(p2.get_position()))
	time.sleep (1)
	


