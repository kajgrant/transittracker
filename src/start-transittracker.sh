#!/bin/bash

export DISPLAY=:0
xset s off
xset -dpms
xset s noblank
python transittracker.py --d &