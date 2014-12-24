#!/usr/bin/python
# Intended for use with Python 3

import sys, os, time
from selenium import webdriver
from PIL import Image
from helpers import sanitisePath

# Get a single captcha shot with the element ID given, using the number i and the path provided to generate a save location
def getCaptcha(i, path, elementId, driver):
	imageName = 'shot' + str(i) + '.png'

	path = sanitisePath(path)

	# Take a whole-page shot
	driver.save_screenshot(path + imageName)

	# Get the captcha element and the position and size of it on the page
	captchaElem = driver.find_element_by_id(elementId)
	captchaPos = captchaElem.location
	captchaSize = captchaElem.size

	# Figure out a bounding box for the captcha element in the shot
	dims = (captchaPos['x'], captchaPos['y'], captchaPos['x']+captchaSize['width'], captchaPos['y']+captchaSize['height'])

	# Open the full page shot, crop it to the dimensions we figured out and save it
	im = Image.open(path + imageName)
	captcha = im.crop(dims)
	captcha.save(path + 'captcha' + str(i) + '.png')

	# Remove the whole-page shot
	os.remove(path + imageName)

# Use selenium to get the number of captchas required with the given element ID and save them to the path passed in
def getShots(number, path, elementId, url):
	# Open the browser and visit the URL we have
	dr = webdriver.Firefox()
	dr.get(url)

	for i in range(number):
		getCaptcha(i, path, elementId, dr)
		if not i == number - 1:
			dr.refresh()
	dr.quit()

if __name__ == '__main__':
	if sys.argv[1] == '-h':
		print("Please pass in: the number of captchas to grab, the location to save them to, and optionally a URL to grab them from.")
		print("The default URL is 'http://www.escapistmagazine.com/registration/register.php'")
		exit(0)

	elementId = 'adcopy-puzzle-image'

	try:
		shots = int(sys.argv[1])
	except ValueError as e:
		print("Number of captchas to grab is not an integer value.  Defaulting to 10.")
		shots = 10

	path = sys.argv[2]
	if not path[len(path)-1] == '/':
		path += '/'

	try:
		url = sys.argv[3]
	except IndexError:
		url = 'http://www.escapistmagazine.com/registration/register.php'

	getShots(shots, path, elementId)
