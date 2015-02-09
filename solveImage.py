#!/usr/bin/python3

from classifyImage import getImageType, blackAndWhiteImage
from PIL import Image
import sys

def solveGeneralknowledge(image):
	print("Solving general knowledge problem")

def solveNextline(image):
	print("Solving next line problem")

def solvePatterns(image):
	print("Solving pattern problem")

def solvePleaseenter(image):
	print("Solving Please enter problem")

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

if __name__ == "__main__":
	path = sys.argv[1]
	solveSingleImage(path)
