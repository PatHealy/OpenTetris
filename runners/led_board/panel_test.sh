#!/bin/bash
sudo /home/pi/rpi-rgb-led-matrix/examples-api-use/demo -D 4 --led-brightness=10 --led-rows=64 --led-cols=64 &
sudo /home/pi/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example --led-rows=64 --led-cols=64 -C 255,255,255 -s 10 -f /home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf --led-brightness=20 "octopus vore simulator 2k19" &
sudo /home/pi/rpi-rgb-led-matrix/examples-api-use/demo -D 0 --led-rows=64 --led-cols=64 --led-brightness=20
