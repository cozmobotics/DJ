# DJ
Play audio files, start the next song a few seconds before the current song ends - almost like a real DJ.
This project has nothing to do with Cozmo, it is just in the same repository. 

play songs without pause, i.e. start the next song a few seconds before the current song ends

optional arguments:

*  -h, --help            show this help message and exit
*  -p PATH, --path PATH  path to directory with audio files to play
*  -o OVERLAP, --overlap OVERLAP
                        percentage of length when to start next song
*  -s SHUFFLE, --shuffle SHUFFLE
                        shuffle yes/no, default=yes
*  -r RECURSIVE, --recursive RECURSIVE


To stop playing, press ^C (Ctrl-C, Strg-C,..). 
Then the current song will be played to the end, next song will not be started, and the program ends. 
Press ^C again to stop the current song which will be faded out and the program ends. 

Prerequisites: VLC media player and python-vlc (VLC python bindings) installed. Runs on Python2 and Python3. Currently it seems to run on Linux only, not on Windows, see issues. 

Tested with 
* Mint 19.1 under Virtualbox 6.0.12 r133076 (Qt5.6.2) and VLC Media Player 3.0.4., Python 2.7.15rc1 and Python 3.6.7
* Ubuntu 18.04 under Virtualbox 6.0.14 VLC Media Player 3.0.8, Python 3.6.9

Credits: Thank you for mentioning the solution on stackoverflow https://stackoverflow.com/a/25899180/12436318
