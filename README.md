# Matrix LED display - Dashboard

This is a system meant to be run on a matrix LED display connected to something like the Raspberrypi.  
It is under development, and i have not implemented the acctuall display part yet (i havent received it yet).  
There is however a verry basic (and probably insecure) simulator/viewer implemented.  
My display is 64x32, It works good, havent made my pannels scaleable but shouldnt be hard to implement.

## NOTE

This is a hobby project, i have not prioritized code optimizations or cleanness.  
I'm just having fun here : )

## What you need

* A raspberrypi (tested on RPI-5)
* Rotary encoders (Can be however manny you want, i use 3 (2 properties, 1 menu))
* A matrix LED display (available on ebay, aliexpres, etc. for cheap and from waveshare or genneral hobby-electronics stores at less risk)
    * I use a pitch of P3 (mm between pixels)
    * 64px x 32px ~ 200mm x 100mm
* 3D Printer, or access to one

## Features

* Spotify Integration (Has to be set up, follow guide not written yet :) )
* Sun-possition screen (This took a whole day, please use)
* Menu system
* Make your own pannels!
  * The rendering function takes a matrix of hex values, PIL Image to Matrix function is also supplied in the functions package.
  * The pannel is automatically picked up when in the pannels folder.


## Images
Spotify Integration (The text scroll, I promise)
![Spotify Integration](./images/Spotify_Illustration.png)
Sun Integration
![Sun Integration](./images/Sun_Illustration.png)