# codeforces_desktop_notifier
A script which notifies on the desktop you whenever your specified targets give AC in a running contest

Now, you don't need to look again and again to different username's submissions during a codeforces contest.
Just concentrate on your code and the script will do the rest

Features
------------
* It lets you make a target list 
* for the specified time, it monitors the targets and gives you a desktop notification if they grab an AC to a problem

Steps to setup this script
-----------------------------
* sudo pip install beautifulsoup4
* sudo pip install requests
* Install pynotify from [here](http://download.gna.org/py-notify/index.html), extract the tar file and do
 
		sudo python setup.py install
* Now Adding all the dependencies, be free to run 

		python main.py
* Add the target handles to targets.txt , you can keep adding handles in this text file (Tip : better to have a timely backup !)

Tips
--------
* Best to start it sometime before contest 
* Follow the format specified for contest start time and duration to avoid errors
