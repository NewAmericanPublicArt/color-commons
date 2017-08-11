___

# README for FIEND.py MODULE
###### (c) Sydney Strzempko for New American Public Art, Color Commons 2017

## Overview

The impetus behind the creation of this sprawling Fiend was to modularize the work of the Color Commons project, essentially a skeletal API forwarding Twilio requests to a Pi, and flesh it out in order to track, sort and analyze the user input coming in from customers using our interactive exhibit. The hope is that this data can be used to draw conclusions about the engagement of the people with public art, and what spans of time or specific choices as the creator we should be making in order to encourage even more interaction.

Accordingly, the resultant Fiend takes in information from a variety of inputs; as intended, through the `/sms` API in `server.py` which clients interact with through SMS, and, largely for testing purposes or large-scale imports, through a .csv file format. Fiend can also take in information manually from POST requests performed from 3rd-party access, eg curl.

Fiend can display any of its log information at any time, as the attribute is not protected; in later usage of Fiend this may bear addressing, but for the time being input validation is strong enough and the Fiend module resides on the server-side. This design decision allows for easy access of specific components of the log, as indicated by the sorting suite present in the module; more than a few methods implemented have an optional parameter for which large set to draw from when organizing data, and when set to None these sets default to the Fiend's log.

## Structure

A Fiend consists of a **list**-type of entries and a **MD-5-stream** generated upon instantiation with an implicit init call, along with a few hardwired arrays for definition searches and sorts. The MD-5 stream is uniquely generated with each Fiend, though can be passed along in deepcopy. The list of entries is filled depending on the instantiation circumstances and subsequent entry calls to the particular Fiend instance.

#### Queries

In considering search and sort criteria, every design decision was made to encourage ease of access for future users; accordingly, the `find` method (for ex) takes a query parameter similar to MongoDB query patterns, namely a dictionary of variable-length with inclusive selectors. Thus, a search query for the color red would look like this;
```python
{'msg':'red'}
```

whereas a more specific query for the color red *during the month of October* would look like this;
```python
{'msg':'red','date':{'start':date(2017,10,1),'end':date(2017,10,31)}} 
```

Note that the flexible search/sorts allow for nested 'start' and 'end' parameters for all attributes of log entries.

#### Log

The list of entries, referred to as LOG, initially contains entries of the type
```python
{'name':x,'date':y,'msg':z,'time':w}
```

Though when certain methods are called, the log or its copies may be mutated into entries of the type
```python
{'name':x,'msg':y,'jsdt':z}
```

where `jsdt` refers to a combined integer value indicating number of milliseconds past UTC-stdz time (see `get_ms`), necessary in converting the data stored in Pythonic date/time objects into JS Date objects when rendered to the client. 

#### Output

The most important part of Fiend is its ability to process log data once inputted; using a combination of the previously mentioned search/sorts, the `server.py` file can request multi-level hierarchies of information sorted by very specific criteria. For example, Fiend could generate a hierarchy such as:

                                           [ ONE WEEK (ex Jul 31-Aug 6th) ]
                                       [][][][ x7 ONE DAY (ex. Aug 4th) ][][][]
                        [][][][][][][][][][][][][ x24 ONE HOUR (ex. 13:00) ][][][][][][][][][][][]
                      [][][][][][][][][][][][][][x# ONE COLOR (ex. Pink) ][][][][][][][][][][][][][]
    [][][][][][][][][][][][][][][][][][][][ x# unique users for this given spec ][][][][][][][][][][][][][][][][][][][]

or even something such as

                                            [ ONE MONTH (ex Feb 2017) ]
                                  [][][][][][][][ x# UNIQUE COLORS ][][][][][][][]

with complete flexibility in the `load` call. This allows for direct importation from the server-side to the data visualization given by the `index.html` page served in the \templates folder, in a format perfectly suited to the D3 Hierarchy/Partition model for a sunburst.

## Methods

`__init__` : Constructor; creates empty log, hash stream

`__deepcopy__` : Deepcopy custom hook; only passes through log

`get_log` : Getter for log (library of all entries)

`get_time` : Getter for current time(naive) from machine

`get_date` : Getter for current date from machine

`send_to_csv` : Generates new file, `log.csv` and fills with properly formatted data gleaned from log array in Fiend instantiation.

`get_fr_csv( str FILE )` : Opens indicated file and fills log (using `new_entry2` utility) with relevant entries

`new_entry( dict elem )` : Called by `server.py` upon correct POST request handling of incoming SMS message. Creates new entry from *elem*, calling hashing suite, getters for date/time, and inputs to log with this generated material.

`new_entry2( dict elem )` : Same as new_entry but allows for date & time fields to be specified. Called by `get_fr_csv` for each new entry.

`load( str optional, array args )` : Initiator function for generating hierarchy structure of specified log items. Optional parameter calls `get_fr_csv` on file string if given. See Tutorial for more

`defaultload( str optional )` : Initiator function, calls `load` with set day argument list. See Tutorial for more

`find( obj arr, dict query )` : Given array object and dictionary of query parameters, implements helper `range_find` and `in_range` methods

`range_find( obj arr, dict query )` : Actual looped function which appraises each element in the list against query value to test for equivalence, or if 'start' and 'end' inner entries exist, tests within range equivalence. Adds correct entries to temp list to be returned upon loop completion

`in_range( dict elem, dict test )` : Takes 2 elements of expected similar type, compares elem to test & returns true if it matches or falls within the 'start','end'-convention range, false otherwise

`sort_by( str root, obj raw )` : Takes root key, parses into various ways to separate/sort data, returns as a node with a generated name of the sort type and a children list of relevant entries harvested from the raw object

`findmin(self,raw)` : Given some array of vals finds minimum value of date using lambda functionality (allows for nested passing)
  
`get_hashable( str nos )` : Creates 'alias' of username from a string, nos, of a particular phone number in [E.164 formatting](https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers).

`generate_alias( str hash )` : Helper function called by `get_hashable`; uses bitwise operations to map 32-character strings of valid hex to two arrays of possible prefixes & names, with a trailing 3-character string to lend uniqueness in the case of two collisions creating non-unique aliases. Refer to `names.py` in the *rsrcs* folder for list of available combinations used in hashing; names taken from [this resource](https://www.ssa.gov/oact/babynames/limits.html) (publicly available, shortened to 6-char max length names).

`get_jsdt( obj hier )` : Creates ['jsdt'] key for all elements in log; value is `get_ms` calculated ms past 1970.

`rm_dt( obj hier )`: Goes through nested hierarchy shape in order to remove all 'date' and 'time' keys from array objects

`compute_range( obj raw, str key)` : Given an object (essentially a chunk of log) and a key indicating a particular attribute to highlight, generates a nonrepeating list of all values of that attribute from the original raw set. Ie, the computed range of all possible entries with the key 'msg' would generate a list of all possible colors, *as strings* rather than as more complex entries.

`daylabel( int val )` : Given int value, returns string of relevant value plus "st", "nd", "rd" relevant tails

`get_ms( date d, time t )` : Converts (either/or/and) date, time (from Datetime super-class) to an integer value representing number of milliseconds from 1970/1/1; will be used as date constructor vals in JS

`convertexcel( obj raw )` : Converts string in "HH:MM:SS YR-MO-DA UTCHJF....etc" format to Datetime (containing date, time) object in UTC format.

`convert_to_str( obj arr )` : Converts a nested list of RGB integer tuples to a single comma-and-bar separated string of values for passing to the Pi.

`parse_command( str message )` : Parser for light display; *currently* accepts format: `[COLOR]`, `flip [COLOR]`, `rainbow`, `secret`.

`complement( tuple color )` : Returns an RGB-tuple complementary color to the one given

`look_up_color( str name )` : Returns an RGB value either matching the name string in xkcd colors (see `xkcd_colors.py`) or a random color value if a match is not found.

## Interaction

The Fiend is first instantiated by the server, then fed entries with subsequent /SMS POST requests. Performs (in order) `new_entry`, (and within that, `get_hashable`) `parse_command`, `convert_to_str`. When called upon by /index renders, `load` calls a combo of `find` and `sort_by` along with `daylabel`, `get_time`, `get_date`, etc to return a hierarchy object with correctly nested labels and objects. Similarly, /serve pathway calls `load` and associated suite as well.

## Resources

* [Fiend Tutorial](../master/src-fiend/TUTORIAL.md)
* [Server Readme](../master/src-fiend/README.md)
* [Data Visualization](http://97.107.136.63:12345/)
___
![cc-logo](http://www.etcs.ipfw.edu/~dupenb/Pictures/CC-BY-SA%20logo.jpg)
