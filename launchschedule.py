# Scrapes SpaceFlightNow.com's launch schedule and displays upcoming rocket launch data
# Requires: RPi_I2C_driver.py
# Requires: BeautifulSoup 4
# Designed to run on a 20x4 I2C LCD

# Ryan McCabe (YouTube: GreenTechNetwork) - Started: 7/30/16 - Last Updated: 7/31/16



# Imports required libraries
from bs4 import BeautifulSoup
import urllib
import RPi_I2C_driver.py
import time

# Set to true if you want to print out all the launches in the terminal
terminalprint = True

# Initializes LCD
mylcd = I2C_LCD_driver.lcd()


# Runs indefinitely (updates once every hour, press CNTRL+C to stop loop)
while True:
	
	# Clears LCD	
	mylcd.lcd_clear()
	
	# Scrapes SpaceFlightNow's launch schedule
	r = urllib.urlopen('http://spaceflightnow.com/launch-schedule/').read()
	soup = BeautifulSoup(r)
	
	# Finds mission names and mission dates based off of span class
	missionnameshtml = soup.find_all("span", class_="mission")
	missiondateshtml = soup.find_all("span", class_="launchdate")
	
	# Finds other mission data based off of div class
	missiondatahtml = soup.find_all("div", class_="missiondata")
	
	# Creates blank dictionaries/lists/arrays? (I'm new to python) for later
	missionnames = {}
	missiondates = {}
	missiondata = {}
	missionwindows = {}
	missionsites = {}
	sitestempa = {}
	sitestempb = {}
	sitestempc = {}

	# Ensures all lists are same length so data isn't mismatched
	if len(missionnameshtml) == len(missiondateshtml) and len(missionnameshtml) == len(missiondatahtml) and len(missiondateshtml) == len(missiondatahtml):
		
		# Removes HTML formatting from lists
		for element in range(len(missionnameshtml)):
			missionnames[element] =  missionnameshtml[element].get_text()
			missiondates[element] = missiondateshtml[element].get_text()
			missiondata[element] =  missiondatahtml[element].get_text()

			# Prints all launch data into terminal if setting is true
			if terminalprint == True:
				print "Launch name: " + missionnames[element]
				print "Launch date: " + missiondates[element]
				print missiondata[element]
				print('')	
			else:
				pass
				
		# Splits missiondata into missionwindows and missionsites	
		for element in range(len(missiondata)):
			missionwindows[element], missionsites[element] = missiondata[element].splitlines()
			 
		# Removes non-ASCII chars from launch name since the LCD cannot display non-ASCII 
		upcomingname = missionnames[0]
		upcomingname = "".join([x if ord(x) < 128 else '-' for x in upcomingname])
		
		# Truncates lengthy strings to fit on LCD properly
		upcomingnametrunc = upcomingname[:20]
		upcomingdate = missiondates[0]
		upcomingdatetrunc = upcomingdate[:20]
		upcomingwindow = missionwindows[0]

		# Removes "Launch window:" and "Launch time:" to save LCD space		
		# Removes EDT time conversion shown in parenthesis so time is only shown in GMT
		if upcomingwindow.startswith("Launch window:"):
			upcomingwindow =  upcomingwindow[15:]
		elif upcomingwindow.startswith("Launch time:"):
			upcomingwindow =  upcomingwindow[13:]
		upcomingwindow = upcomingwindow.split("(")[0]
		
		# Truncates lengthy strings to fit on LCD properly
		upcomingwindowtrunc = upcomingwindow[:19]
		upcomingsite = missionsites[0]

		# Removes launch site launch pad prefixes to save LCD space
		if '-' in upcomingsite or 'pad' in upcomingsite:
			sitestempa, sitestempb, sitestempc = upcomingsite.split(',')
			upcomingsite = sitestempb + "," + sitestempc
		else:
			pass

		# Truncates lengthy strings to fit on LCD properly		
		upcomingsite = upcomingsite[1:]
		upcomingsitetrunc = upcomingsite[:20]
		

		# Displays mission name, date, time, and site on LCD		
		mylcd.lcd_display_string("%s" %upcomingnametrunc,1)
		mylcd.lcd_display_string("%s" %upcomingdatetrunc,2)
		mylcd.lcd_display_string("%s" %upcomingwindowtrunc,3)
		mylcd.lcd_display_string("%s" %upcomingsitetrunc,4)

		
	else:
		# Displays a data mismatch error if one exists
		mylcd.lcd_display_string("Data Mismatch",1)
	

	# Pauses script for one hour
	time.sleep(3600)
