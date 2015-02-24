#!/usr/bin/python3

from classifyImage import getImageType, blackAndWhiteImage, getInstructionsFromImage
import pyocr, pyocr.builders
from PIL import Image
import numpy
import sys, os
	
tool = pyocr.get_available_tools()[0]

def cropOutInstructions(image):
	return image.crop((0, 17, image.size[0], image.size[1]))

def doOcr(image):
	return tool.image_to_string(image, lang='eng', builder=pyocr.builders.TextBuilder()).lower()

def thinImage(image):
	pointsDeleted = True
	while pointsDeleted:
		pass

# This function is probably incomplete - population estimation puts the number of challenges at 36
def solveGeneralknowledge(image):
	# Get the text from the image, this should be enough to get the question from the image since they're unobfuscated,
	# also make it lower case and all one line.
	imageText = doOcr(image).replace('\n', ' ')
	if ('liberty' in imageText) or ('country presented' in imageText):
		return "France"
	elif 'impressionist' in imageText:
		return 'Edgar Degas'
	elif 'animal' in imageText and not 'venom' in imageText:
		return 'rhino beetle'
	elif 'national emblem' in imageText:
		return 'bald eagle'
	elif 'book published' in imageText:
		return 'the bible'
	elif 'yoko ono' in imageText:
		return 'john lennon'
	elif 'which us' in imageText:
		return 'seattle'
	elif 'venom' in imageText:
		return 'box jellyfish'
	elif 'dies solis' in imageText:
		return 'sunday'
	elif 'wright' in imageText:
		return 'wright flyer'
	elif 'brand name' in imageText:
		return 'crayola'
	elif 'grapes' in imageText:
		return 'john steinbeck'
	# I know this line is spelled wrong: Tesseract seems to have trouble with 't's and consistently recognises them as 'x'
	elif 'possible temperaxure' in imageText:
		return 'absolute zero'
	elif 'apple' in imageText:
		return 'steve jobs'
	# 'l' fails to recognise, comes out as pipe
	elif 'anima|' in imageText and 'chinese' in imageText:
		return 'giant panda'
	elif 'george orwell' in imageText:
		return 'big brother'
	elif 'never to live in wash' in imageText:
		return 'george washington'
	elif 'rhodes scholar' in imageText:
		return 'oxford university'
	else:
		print(imageText)
		return None

# This solves all known Next Line challenges, there may very well be more.
# UPDATE 20/02/2015: Another added after second image farming run.  Complete again.
def solveNextline(image):
	inst = getInstructionsFromImage(blackAndWhiteImage(image)).lower()
	if 'the n' in inst:
		return 'violets are blue'
	elif 'finish the get' in inst:
		return 'seven years ago'
	elif 'finish this' in inst:
		return 'it tolls for thee'
	elif 'robert' in inst:
		return 'I took the one less travelled by'
	else:
		print(inst)
		return None

# 84.9% success rate on the challenges I have.
def solvePatterns(image):
	# Convert the image to greyscale
	im = image.convert('L')
	# Get greyscale values from our image as a flat array of numbers (0-255)
	data = numpy.array(im).flatten()
	# Get all the UNIQUE values in our numerical data as a sorted NumPy array
	vals = numpy.sort(list(set(data)))
	im = cropOutInstructions(im)
	# Here using the mean of all the unique data values rather than the mean of all values in general
	bw = im.point( lambda x: 0 if x < int(vals.mean()) else 255)
	# Memo to self: resizing here makes results worse.
	imageText = doOcr(bw)
	if '1' in imageText or '2' in imageText or '3' in imageText or '4' in imageText:
		#bw.save(image.filename.split('.')[0] + '_5_.png')
		return '5'
	elif 'a' in imageText or 'b' in imageText or 'c' in imageText or 'd' in imageText:
		#bw.save(image.filename.split('.')[0] + '_E_.png')
		return 'e'
	else:
		# For some reason some images, even clear ones, do not produce anything via straight OCR.
		# Might be worth putting something less conventional in at this point later.
		# Although these present such a small proportion of challenges it's probably not worth it.
		print(image.filename, imageText)
		# Save a copy of the image so far; debug uses.
		#bw.save(image.filename.split('.')[0] + '_fail_.png')
		return None

def solvePleaseenter(image):
	# Applying Jeff Yan's techniques for recaptcha from 'Robustness of Google Captchas' 2011 paper
	# Preprocess: upscale
	im = image.resize( [int(x * 4) for x in image.size] )
	# Preprocess: greyscale
	im = im.convert('L')
	# My addition: crop out instructions
	im = im.crop((0,68,im.size[0],im.size[1]))
	# Preprocess: heuristically convert to B&W only
	data = numpy.array(im).flatten()
	vals = numpy.sort(list(set(data)))
	# In this stage we actually want white letters on a black background so B&W conversion is the opposite of what we would normally use.
	# Thinning code used requires this and I don't know enough C++ to change that.
	bw = im.point( lambda x: 255 if x < int(vals.mean()) else 0)
	# Save image
	filename = image.filename.split('.')[0] + '_blackWhite_.png'
	bw.save(filename)
	# Preprocess: thinning by Zhang-Suen thinning algorithm, code taken from https://github.com/bsdnoobz/zhang-suen-thinning/blob/master/thinning.py
	# Most of the nonstandard modules used by the script are not available for python 3, which is why we're calling an outside script here.
	os.system("python thinning.py " + filename)
	newFilename = filename.split('.')[0] + "_thinned_.png"
	# Open the thinned image and convert back to black on white background (May be superfluous) - No traditional OCR so probably is. TODO: decide
	thinned = Image.open(newFilename)
	thinned = thinned.point( lambda x: 255 if x < 200 else 0)
	# TODO: implement character recognition
	return None

def solvePleasepick(image):
	# TODO: Find out the answers to these
	print("Solving please pick problem")
	return None

def solvePuzzles(image):
	print("Solving puzzle problem")
	return None

def solveUnclassifiable(image):
	# TODO: Possibly classify these better
	print("Solving unclassifiable problem")
	return None

def solveVideo(image):
	print("Cannot solve video problem")
	return None

def solveSingleImage(pathToImage):
	image = Image.open(pathToImage)
	imageType = getImageType(blackAndWhiteImage(image))
	# Each type of captcha presented by solveMedia has its own function
	# so here instead of using a large set of ifs we use Python's introspection
	# to build a function name from the image type and then call that, passing in
	# the image.
	functionName = 'solve' + imageType.title()
	solution = globals()[functionName](image)
	return solution

if __name__ == "__main__":
	path = sys.argv[1]
	if solveSingleImage(path) == None:
		print("No solution for " + path)
