#!/usr/bin/python3

from classifyImage import getImageType, blackAndWhiteImage, getInstructionsFromImage
import pyocr, pyocr.builders
from PIL import Image
import numpy
import sys
	
tool = pyocr.get_available_tools()[0]

def solveGeneralknowledge(image):
	imageText = tool.image_to_string(image, lang='eng', builder=pyocr.builders.TextBuilder()).lower()
	if 'liberty' in imageText:
		return "France"
	if 'impressionist' in imageText:
		return 'Edgar Degas'
	else:
		return imageText

# This solves all known Next Line challenges, there may very well be more.
def solveNextline(image):
	inst = getInstructionsFromImage(blackAndWhiteImage(image)).lower()
	print(inst)
	if 'the n' in inst:
		return "violets are blue"
	elif 'finish' in inst:
		return 'it tolls for thee'
	elif 'robert' in inst:
		return 'I took the one less travelled by'
	else:
		return None

def solvePatterns(image):
	# Probably need to do some dynamic monochrome-ing here, or some more complex processing to make characters monochrome
	# Print image numerical data greyscale for testing
	data = numpy.array(image.convert('L')).flatten()
	print(int(data.mean()))
	#for x in data:
	#	print(x)
	# Save image as greyscale for testing
	image.convert('L').save('test1.png')
	bw = image.convert('L').point( lambda x: 0 if x < int(data.mean()) else 255)
	bw.save('test2.png')
	# So... for some reason this isn't working... at all.  Returning nothing.  What the shit?!
	# The 200 constant above will probably need to change to some dynamic value as well.
	# These lines have only been tested with the images from Martha Stewart, probably not good with
	# other images anyway.
	return tool.image_to_string(bw, lang='eng', builder=pyocr.builders.TextBuilder())

def solvePleaseenter(image):
	print("Solving please enter problem")

def solvePleasepick(image):
	print("Solving please pick problem")

def solvePuzzles(image):
	print("Solving puzzle problem")

def solveUnclassifiable(image):
	print("Solving unclassifiable problem")

def solveVideo(image):
	print("Cannot solve video problem")

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
	print(solveSingleImage(path))
