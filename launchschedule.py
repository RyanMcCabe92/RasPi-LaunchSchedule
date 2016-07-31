# Scrapes SpaceFlightNow.com's launch schedule and displays upcoming rocket launch data
# Requires: RPi_I2C_driver
# Requires: BeautifulSoup 4
# Designed to run on a 20x4 I2C LCD

# Ryan McCabe - Started: 7/30/16 - Last updated: 7/31/16


# Imports required libraries
from bs4 import BeautifulSoup
import urllib
import RPi_I2C_driver
import time

# Initializes LCD
mylcd = I2C_LCD_driver.lcd()


# Runs indefinitely (updates once every hour)
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
	
	# Creates blank dictionaries/lists? (I'm new to python) for later
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

		# Splits missiondata into missionwindows and missionsites	
		for element in range(len(missiondata)):
			missionwindows[element], missionsites[element] = missiondata[element].splitlines()
			

		# Truncates and removes excess verbiage from all lists 
		upcomingname = missionnames[0]
		upcomingnametrunc = upcomingname[:19]
		upcomingdate = missiondates[0]
		upcomingdatetrunc = upcomingdate[:19]
		upcomingwindow = missionwindows[0]
		# Removes "Launch window:" and "Launch time:" to save LCD space		
		if upcomingwindow.startswith("Launch window:"):
			upcomingwindow =  upcomingwindow[15:]
		elif upcomingwindow.startswith("Launch time:"):
			upcomingwindow =  upcomingwindow[13:]
		upcomingwindowtrunc = upcomingwindow[:19]
		upcomingsite = missionsites[0]
		# Removes launch site launch pad prefixes to save LCD space
		if '-' in upcomingsite or 'pad' in upcomingsite:
			sitestempa, sitestempb, sitestempc = upcomingsite.split(',')
			print sitestempa
			print sitestempb
			print sitestempc
			upcomingsite = sitestempb + "," + sitestempc
		else:
			pass		
		upcomingsite = upcomingsite[1:]
		upcomingsitetrunc = upcomingsite[:19]
		

		# Displays mission name, date, time, and site on LCD		
		mylcd.lcd_display_string("%s" %upcomingnametrunc,1)
		mylcd.lcd_display_string("%s" %upcomingdatetrunc,2)
		mylcd.lcd_display_string("%s" %upcomingwindowtrunc,3)
		mylcd.lcd_display_string("%s" %upcomingsitetrunc,4)

		
	else:
		# Displays a data mismatch error if one exists
		mylcd.lcd_display_string("Data Mismatch",1)
	
	time.sleep(3600)
