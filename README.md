___

# README for COLOR COMMONS 2017
###### (c) Sydney Strzempko for New American Public Art, Aug 2017

## Overview

The Color Commons project was developed by [New American Public Art](http://www.newamericanpublicart.com/) for usage on the Boston Greenway as early as 2013; the current version of this project was last updated in 2017 and is still being developed for client-side applications.
This directory of New American Public Art's Github has all associated files for implementing your own Color-Commons system. Our hope is with this information, to empower the reader to develop their own large-scale public art projects as a centering force in local communities.
All information contained in this repository is protected under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0).

## Structure

There are 2 main components to this implementation; the server and the Pi controller. The two are housed in */src-fiend* and */src-vault* respectively. The vault-side code is light; it mainly deals with receiving and converting messages from the server to be relayed onwards to the relevant lighting architecture (see */docs/Specs.md* for product specifications). The server-side code houses the Fiend module and surrounding architecture; essentially, it keeps track of all the commands sent in by users in a big array that can be run against queries to find interesting results about usage patterns.

For an in-depth description of the intake and logging process, as well as a breakdown of each API, refer to [this link](http://prezi.com/mmt0cdq5fzi2/?utm_campaign=share&utm_medium=copy&rc=ex0share) for an interactive schema.

## Interaction

The server and pi server are both instantiated and managed by [UWSGI](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html). The server IP is connected to a [Twilio SMS forwarder](https://www.twilio.com/docs/quickstart/python/sms) with a unique phone number; this is the number users text their color-command messages to. When the SMS is converted to a POST request, the [Flask](http://flask.pocoo.org/) Python framework in */src-fiend/server.py* handles the request by passing the relevant information in to Fiend for statistics later. The Fiend processes the message and hashes the number of the sender for confidentiality. The server then packages the original message into a new request and sends it as a POST request to the Pi's IP address. The Flask server set up over there receives the message, parses out the contents further for the Open Lighting Architecture ([OLA](https://www.openlighting.org/ola/tutorials/ola-on-raspberry-pi/)) specifications and sends it along to the Pharos Lighting Controller to manipulate the display lights on the Greenway. *(For a full list of technologies used, refer to /docs/Specs.md)*

The 1st server also contains an API for GET requests on the */index.html* or */* path of the IP address; this renders a page from Fiend manipulation of data into a [D3](https://d3js.org/) Sunburst data visualization from Partition architecture. The information is loaded from a JSON rendered on a */serve* route API.

## RESOURCES

* [NAPA Page Link](http://www.newamericanpublicart.com/color-commons-2017/)
* [Vault Readme](../master/src-vault/README.md)
* [Server Readme](../master/src-fiend/README.md)
* [Fiend Readme](../master/src-fiend/README2.md)
* [Fiend Tutorial](../master/src-fiend/TUTORIAL.md)
* [Data Visualization](http://97.107.136.63:12345/)
* [Flask](http://flask.pocoo.org/)
* [Twilio](https://www.twilio.com/docs/quickstart/python/sms)
* [OLA](https://www.openlighting.org/ola/tutorials/ola-on-raspberry-pi/)
* [UWSGI](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)
* [D3](https://d3js.org/)

___
![cc logo](http://www.etcs.ipfw.edu/~dupenb/Pictures/CC-BY-SA%20logo.jpg)
