#!/usr/bin/python3

from PIL import Image
import pyocr, pyocr.builders
import sys, glob, os
from shutil import move
from helpers import sanitisePath

# Get the tool and language we're using, specifying eng for the language for now
tool = pyocr.get_available_tools()[0]
lang = 'eng'

def moveTo(image, folder, path):
	print("Moving: '" + image + "'")
	fileName = image.split('/')[::-1][0]
	destFolder = path + folder
	if not os.path.exists(destFolder):
		os.makedirs(destFolder)
	dest = path + folder + "/" + fileName
	move(image, dest)

def resizeAndOcr(im):
	# Resize the small part we now have such that Tesseract can read it accurately enough for the next check
	im2 = im.resize( [int(x * 4) for x in im.size] )
	return tool.image_to_string(im2, lang=lang, builder=pyocr.builders.TextBuilder())

def getInstructionsFromImage(image):
	# Open image and crop it to only the top left corner - this may contain instructions
	topLeftCrop = getCroppedSection(image, (0, 0, 133, 17))
	ins = resizeAndOcr(topLeftCrop)
	if ins == '' or blackWhiteBalanceCheck(topLeftCrop):
		midLeftCrop = getCroppedSection(image, (0, 85, 133, 100))
		return resizeAndOcr(midLeftCrop)
	else:
		return ins

def blackWhiteBalanceCheck(image):
	pix = image.histogram()
	whiteCount = pix[255]
	blackCount = pix[0]
	total = blackCount + whiteCount
	return whiteCount < (total * 0.15)

def getCroppedSection(image, boundingBox):
	return image.crop(boundingBox)

def blackAndWhiteImage(image):
	grey = image.convert('L')
	blackAndWhite = grey.point( lambda x: 0 if x < 150 else 255)
	return blackAndWhite

def moveAllImages(path):
	if not len(path) == 0:
		path = sanitisePath(path)
	# Get all the png files in the path used and make sure that there are some we can use there
	files = glob.glob(path + '*.png')
	if len(files) == 0:
		print("There are no matching files.")
	for imagePath in files:
		image = blackAndWhiteImage(Image.open(imagePath))
		imageInstructions = getInstructionsFromImage(image)
		destinationFolder = getDestFolder(imageInstructions)
		if destinationFolder == "unclassifiable" and isAllWhite(image):
			destinationFolder = "video"
		moveTo(imagePath, destinationFolder, path)

def isAllWhite(image):
	# Return whether the number of black pixels in the image is 0; in this case the image is plain white
	return image.histogram()[0] == 0

def getDestFolder(instructions):
	inst = instructions.lower()
	if "en" in inst:
		return "pleaseEnter"
	elif "pick" in inst:
		return "pleasePick"
	elif "next" in inst:
		return "patterns"
	elif "answer:" in inst:
		return "generalKnowledge"
	elif "answer" in inst:
		return "puzzles"
	elif "the n" in inst or "robert" in inst or "finish" in inst:
		return "nextLine"
	else:
		return "unclassifiable"

if __name__ == '__main__':
	# Default to the current location of the script if not path is passed in
	try:
		path = sys.argv[1]
	except IndexError:
		path = ''

	# print the info
	print("OCR Engine: " + tool.get_name())
	print("Language: " + lang + "\n")

	moveAllImages(path)
