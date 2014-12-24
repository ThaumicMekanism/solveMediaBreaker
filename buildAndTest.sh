#!/usr/bin/bash

rm -rf testDir
mkdir testDir
cd testDir
#cp /home/zaphod/pictures/screens/solveMedia/generalKnowledge/captcha180.png .
#cp /home/zaphod/pictures/screens/solveMedia/pleaseEnter/captcha927.png .
#cp /home/zaphod/pictures/screens/solveMedia/questions/captcha133.png .
#cp /home/zaphod/pictures/screens/solveMedia/unclassifiable/captcha109.png .
#cp /home/zaphod/pictures/screens/solveMedia/patterns/captcha208.png .
find /home/zaphod/pictures/screens/escapist -name '*.png*' -exec cp {} . \;

cd ..
python classifyImage.py testDir
