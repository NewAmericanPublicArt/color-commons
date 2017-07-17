# README for FIEND.py MODULE
###### (c) Sydney Strzempko for New American Public Art, Color Commons 2017

## Overview

TODO; include images

## Structure



## Methods

`__init__` : Constructor; creates empty log, hash stream

`fprint` : Clean prints each line(dict-entry) of log

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

`in_range( dict elem, dict test )` : TODO

`compute_range( obj raw, str key)` : TODO

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

TODO


___

