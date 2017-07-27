# README for FIEND.py MODULE
###### (c) Sydney Strzempko for New American Public Art, Color Commons 2017

## Overview

The *src-vault* folder contains the Flask implementation of the server running on the Raspberry Pi; essentially, it accepts information in a closed system from the Fiend implementation, performs minimal manipulation on the given string, and passes this information onwards to the DMX light controller to be displayed by the LED light blades. The emphasis in this element of design was on modularizing and simplifying the majority of the work over to Fiend; correspondingly, the `vault.py` implementation of Pi-API is only 70 or so lines of code.

## Structure

The structure is that of a basic Flask app with a single method, POST, called exclusively by the Fiend server when passing information over to be displayed. Thus, the structure of this API is simply a few commands on the received string, then the opening of a socket in order to talk to the DMX controller. _Note:_ Refer to the Open Lighting Architecture [Doc](https://www.openlighting.org/ola/developer-documentation/python-api/).

## Functions

`sendtoDmx()`: Instantiated by post request (with public "/colors" route), main function in app. Calls *convert_barr*, SendDmx (OLA-specified func) with *DmxSent* as function closure. Coordinates RGB parsing of string input (of the form "R,G,B|R,G,B...") into an array of integers as needed by OLA standards. Calls run and returns positive XML success message upon completion of these tasks.

`DmxSent(status)`: Closure function given status object indicating success of SendDmx function call. Prints 'Success!' when things work.

`convert_barr(input)`: Converts bit array (needs clarification on term - potentially misleading) of packed integers in string format back to an array of integers using string parsing, regexing. 

## Interaction

As mentioned in the overview, the Pi server does not directly interact with any Color-Commons users; instead, it relays the command (in the form of a string of RGB values translated from the original phrase) forward to the DMX controller (with infinitely less computational abilities) in order for the controller to coordinate the lighting with the Pharos controller further down the chain of command.
