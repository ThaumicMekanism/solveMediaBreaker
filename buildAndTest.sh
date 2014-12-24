#!/bin/bash

rm -rf testDir
mkdir testDir
cd testDir
find /home/zaphod/pictures/screens/marthaStewart -name '*.png*' -exec cp {} . \;

cd ..
python classifyImage.py testDir
