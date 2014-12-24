#!/usr/bin/python
def sanitisePath(path):
	# make sure the path we use ends in '/'
	if not path[len(path)-1] == '/':
		path += '/'
	return path
