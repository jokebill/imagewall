#image wall

## Introduction

This script will cut the input image using a specified width/height ratio and zoom ratio, and split the cut image into several tiles. These tiles will be sent to remote nodes defined in slaves file, using scp command.

You could use this script to automatically change the background image for a screen wall constructed by several linux machines.

## Usage
```
loadwall.py [options] <input_image>

options:
  -h, --help            show this help message and exit
  -c X,Y, --center=X,Y  Image cut center offset, in percentage
  -r X:Y, --ratio=X:Y   Image cut width/height ratio
  -z RATE, --zoom=RATE  Image cut zoom rate
  -s NxM, --slices=NxM  Number of tiles in row, and column
  -b PX,PY, --boarder=PX,PY
                        Boarder width in percentage (to compensate the screen boarders
  -o DIR, --output=DIR  Tile images output folder (Warning: this folder will be overwritten)
  --resolution=pX,pY    Tile image resolution
  --slaves=FILE         The file with defines all slaves' hostnames/ips
  --remote=PATH         The file path and name that a tile should be uploaded to on the slave machine
```
