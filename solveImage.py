#!/usr/bin/python3

from classifyImage import getImageType, blackAndWhiteImage, getInstructionsFromImage
import pyocr, pyocr.builders
from PIL import Image
import numpy
import sys
	
tool = pyocr.get_available_tools()[0]

# This function is probably incomplete - population estimation puts the number of challenges at 36
def solveGeneralknowledge(image):
	# Get the text from the image, this should be enough to get the question from the image since they're unobfuscated,
	# also make it lower case and all one line.
	imageText = tool.image_to_string(image, lang='eng', builder=pyocr.builders.TextBuilder()).lower().replace('\n', ' ')
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

# This needs much work.  Only need to recognise one character from the challenge but it needs to be accurate all the time.
def solvePatterns(image):
	# Probably need to do some dynamic monochrome-ing here, or some more complex processing to make characters monochrome
	# Print image numerical data greyscale for testing
	data = numpy.array(image.convert('L')).flatten()
	#print(int(data.mean()))
	#for x in data:
	#	print(x)
	# Save image as greyscale for testing
	#image.convert('L').save('test1.png')
	# This produces a decent image for the cases I've looked at so far but the OCR is still not returning anything useful.
	# This is going to be more complicated than I thought.
	bw = image.convert('L').point( lambda x: 0 if x < int(data.mean()) else 255)
	#bw.save('test2.png')
	return tool.image_to_string(bw, lang='eng', builder=pyocr.builders.TextBuilder())

def solvePleaseenter(image):
	print("Solving please enter problem")

def solvePleasepick(image):
	# TODO: Find out the answers to these
	print("Solving please pick problem")

def solvePuzzles(image):
	print("Solving puzzle problem")

def solveUnclassifiable(image):
	# TODO: Possibly classify these better
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
	if solveSingleImage(path) == None:
		print("No solution for " + path)
