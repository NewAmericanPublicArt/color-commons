# README for FIEND.py MODULE
###### (c) Sydney Strzempko for New American Public Art, Color Commons 2017

## Overview

The impetus behind the creation of this sprawling Fiend was to modularize the work of the Color Commons project, essentially a skeletal API forwarding Twilio requests to a Pi, and flesh it out in order to track, sort and analyze the user input coming in from customers using our interactive exhibit. The hope is that this data can be used to draw conclusions about the engagement of the people with public art, and what spans of time or specific choices as the creator we should be making in order to encourage even more interaction.

Accordingly, the resultant Fiend takes in information from a variety of inputs; as intended, through the `/sms` API in `server.py` which clients interact with through SMS, and, largely for testing purposes or large-scale imports, through a .csv file format. Fiend can also take in information manually from POST requests performed from 3rd-party access, eg curl.

Fiend can display any of its log information at any time, as the attribute is not protected; in later usage of Fiend this may bear addressing, but for the time being input validation is strong enough and the Fiend module resides on the server-side. This design decision allows for easy access of specific components of the log, as indicated by the sorting suite present in the module; more than a few methods implemented have an optional parameter for which large set to draw from when organizing data, and when set to None these sets default to the Fiend's log.

In considering search and sort criteria, every design decision was made to encourage ease of access for future users; accordingly, the `find` method (for ex) takes a query parameter similar to MongoDB query patterns, namely a dictionary of variable-length with inclusive selectors. Thus, a search query for the color red would look like this;
> {'msg':'red'}

whereas a more specific query for the color red *during the month of October* would look like this;
> {'msg':'red','date':{'start':date(2017,10,1),'end':date(2017,10,31)}} 

Note that the flexible search/sorts allow for nested 'start' and 'end' parameters for all attributes of log entries.

The most important part of Fiend is its ability to process log data once inputted; using a combination of the previously mentioned search/sorts, the `server.py` file can request multi-level hierarchies of information sorted by very specific criteria. For example, Fiend could generate a hierarchy such as:

                                           [ ONE WEEK (ex Jul 31-Aug 6th) ]
                                       [][][][ x7 ONE DAY (ex. Aug 4th) ][][][]
                        [][][][][][][][][][][][][ x24 ONE HOUR (ex. 13:00) ][][][][][][][][][][][]
                      [][][][][][][][][][][][][][x# ONE COLOR (ex. Pink) ][][][][][][][][][][][][][]
    [][][][][][][][][][][][][][][][][][][][][ x# unique users for this given spec ][][][][][][][][][][][][][][][][][][][][]

or even something such as

                                            [ ONE MONTH (ex Feb 2017) ]
                                  [][][][][][][][ x# UNIQUE COLORS ][][][][][][][]

with complete flexibility in the `load` call. This allows for direct importation from the server-side to the data visualization given by the `index.html` page served in the \templates folder, in a format perfectly suited to the D3 Hierarchy/Partition model for a sunburst.

## Structure

A Fiend consists of a LIST-type of entries and a UNIQUE md5 hashstream generated upon instantiation with an implicit init call.
The list of entries, referred to as LOG, initially contains entries of the type
> {'name':x,'date':y,'msg':z,'time':w}

Though when certain methods are called, the log or its copies may be mutated into entries of the type
> {'name':x,'msg':y,'jsdt':z}

where `jsdt` refers to a combined integer value indicating number of milliseconds past UTC-stdz time (see `get_ms`), necessary in converting the data stored in Pythonic date/time objects into JS Date objects when rendered to the client. 

A sample hierarchy structure might unfold as follows;
> {'name': "Week of Jul 31st", 'children': [
>	{'name': "31st Jul", 'children': [...] },
>	{'name': "1st Aug", 'children':[
>		{'name': "Mr HAMISH-ef4", 'children': [ ] },
>		{'name': "Ms ADELE-333", 'children': [ ] }
>		] }
>	 ] }  

## Methods

`__init__` : Constructor; creates empty log, hash stream

`get_log` : Getter for log (library of all entries)

`get_time` : Getter for current time(naive) from machine

`get_date` : Getter for current date from machine

`send_to_csv` : Generates new file, `log.csv` and fills with properly formatted data gleaned from log array in Fiend instantiation.

`get_fr_csv( str FILE )` : Opens indicated file and fills log (using `new_entry2` utility) with relevant entries

`load( str optional )` : Initiator function for generating hierarchy structure of specified log items. Standardized currently to 3 tiers; [1-week],[1-day],[1-color]. Optional parameter calls `get_fr_csv` on file string if given.

`get_jsdt( obj hier )` : TODO

`export_to_js( obj hier )` : TODO

`new_entry( dict elem )` : Called by `server.py` upon correct POST request handling of incoming SMS message. Creates new entry from *elem*, calling hashing suite, getters for date/time, and inputs to log with this generated material.

`new_entry2( dict elem )` : Same as new_entry but allows for date & time fields to be specified. Called by `get_fr_csv` for each new entry.

`find( obj arr, dict query )` : TODO 

`range_find( obj arr, dict query )` : TODO

`in_range( dict elem, dict test )` : Takes 2 elements of expected similar type, compares elem to test & returns true if it matches or falls within the 'start','end'-convention range, false otherwise

`compute_range( obj raw, str key)` : Given an object (essentially a chunk of log) and a key indicating a particular attribute to highlight, generates a nonrepeating list of all values of that attribute from the original raw set. Ie, the computed range of all possible entries with the key 'msg' would generate a list of all possible colors, *as strings* rather than as more complex entries.

`sort_by( str root, obj raw )` : TODO

`clean_sort( obj raw )` : Optional; empties [] from generated hierarchies

`get_hashable( str nos )` : Creates 'alias' of username from a string, nos, of a particular phone number in [E.164 formatting](https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers).

`generate_alias( str hash )` : Helper function called by `get_hashable`; uses bitwise operations to map 32-character strings of valid hex to two arrays of possible prefixes & names, with a trailing 3-character string to lend uniqueness in the case of two collisions creating non-unique aliases. Refer to `names.py` in the *rsrcs* folder for list of available combinations used in hashing; names taken from [this resource](https://www.ssa.gov/oact/babynames/limits.html) (publicly available, shortened to 6-char max length names).

`get_ms( date d, time t )` : Converts (either/or/and) date, time (from Datetime super-class) to an integer value representing number of milliseconds from 1970/1/1; will be used as date constructor vals in JS

`convertexcel( obj raw )` : Converts string in "HH:MM:SS YR-MO-DA UTCHJF....etc" format to Datetime (containing date, time) object in UTC format.

`convert_to_str`( obj arr )` : Converts a nested list of RGB integer tuples to a single comma-and-bar separated string of values for passing to the Pi.

`parse_command( str message )` : Parser for light display; *currently* accepts format: `[COLOR]`, `flip [COLOR]`, `rainbow`, `secret`.

`complement( tuple color )` : Returns an RGB-tuple complementary color to the one given

`look_up_color( str name )` : Returns an RGB value either matching the name string in xkcd colors (see `xkcd_colors.py`) or a random color value if a match is not found.

## Interaction

There are 3 main ways in which Fiend works behind the scenes to interact with clientele; in **accepting SMS**, in **manipulating content**, and in **formatting display** of content. This means that each Fiend instance is uniquely tied to an invocation of `server.py`, and interacts/is called upon to do the heavy lifting with all APIs offered on server-side. This allows for complete encapsulation of essentially all server-side and semi-server-side data into a convenient bundle of methods.

#### Accepting SMS

TODO

#### Manipulating Content

TODO

#### Formatting Display

The third and newest component of our Fiend interaction was the development of a new API (given the default "/" route in a GET request scenario) to allow users of the Color Commons project to see an interactive data vizualization of all user input to the Fiend organized by time span, unique user ID, colors, etc - the goal is to make this information accessible and live-updating to the clients interacting with it on the webpage. Accordingly, the handler for this API loads `index.html` which contains extensive js work in `master.js`, as well as the inclusion of the js graphics/data package D3 in order to generate an infographic out of a SVG. 


___

