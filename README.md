# RasPi-LaunchSchedule
Displays upcoming shuttle launch information on a 20x4 RasPi LCD. All data is pulled from SpaceFlightNow.com.

I appologize if this code is sloppy and/or processes in an inefficient way. I wrote it less than a day after I started learning about Python so there's probably better ways to process the data.

In order to run this script to it's full extent, you must have a Raspberry Pi along with a 20x4 LCD. In addition, you must also have installed the bs4 (BeautifulSoup) library and urllib library. You are able to modify the code to only export data via the terminal if you do not have a Raspberry Pi or 20x4 LCD as well.

This script also utilizes RPi_I2C_driver.py to display text on the 20x4 LCD. All credit for that library (driver?) goes to Denis Pleic (https://gist.github.com/DenisFromHR).

I have included a boolean named "terminalprint" that allows you to choose whether or not you want to export all (non-truncated) launch data in the terminal to give you a bit more information than the 20x4 LCD can display.


You must make sure your RPi_I2C_driver.py has the propery I2C address of your LCD screen. To determine what the I2C address of your LCD screen is, type in "i2cdetect -y 1" in the terminal of your Raspberry Pi.
