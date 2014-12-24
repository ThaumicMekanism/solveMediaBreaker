#!/usr/bin/python

import classifyImage, getShots
import json

number = 1000
urls = json.loads(open('captchaUrls').read())

for url in urls:
	path = '/home/zaphod/pictures/screens/' + url['folder']
	getShots.getShots(number, path, 'adcopy-puzzle-image', url['url'])
	classifyImage.moveAllImages(path)
