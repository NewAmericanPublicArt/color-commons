___

# README for COLOR COMMONS 2017
###### (c) Sydney Strzempko for New American Public Art, Aug 2017

## SUMMARY

This directory of New American Public Art's Github has all associated files for implementing your own Color-Commons system, as shown below;

![ex](link.jpg "CC in Action")

There are 2 main components to this implementation; the server and the Pi controller. The two are housed in */src-fiend* and */src-vault* respectively. The vault-side code is light; it mainly deals with receiving and converting messages from the server to be relayed onwards to the relevant lighting architecture (see */docs/Specs.md* for product specifications). The server-side code houses the Fiend module and surrounding architecture; essentially, it keeps track of all the commands sent in by users in a big array that can be run against queries to find interesting results about usage patterns.

## STRUCTURE

For an in-depth description of the intake and logging process, as well as a breakdown of each API, refer to [this link](http://prezi.com/mmt0cdq5fzi2/?utm_campaign=share&utm_medium=copy&rc=ex0share) for an interactive schema.

The only information transmitted between the server and the vault is RGB-encoded color values; for an in-depth look at each component refer to the resources tab below.

## RESOURCES

* [NAPA Page Link](http://www.newamericanpublicart.com/color-commons-2017/)
* [Vault Readme](../master/src-vault/README.md)
* [Server Readme](../master/src-fiend/README.md)
* [Fiend Readme](../master/src-fiend/README2.md)
* [Fiend Tutorial](../master/src-fiend/TUTORIAL.md)
* [Data Visualization](http://97.107.136.63:12345/)

___
