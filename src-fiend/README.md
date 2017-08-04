# README for SERVER.py
###### (c) Sydney Strzempko for New American Public Art

## Overview

*Describe that it essentially houses Fiend with some added outside components*

For information on FIEND, refer [here](../blob/master/src-fiend/README2.md) or [here](../blob/master/src-fiend/TUTORIAL.md).

## Structure
<dl>
<dt>/sms API</dt>
    <dd>Takes POST request objects, strips lower set, passes in to Fiend instance created @before-first-request for storage. Then repackages message into a new request object and forwards on to Pi server.</dd>
<dt>/ API</dt>
    <dd>Renders <i>index.html</i> page by filling in data visualization from Fiend load return. TODO- convert to JSON render load</dd>
<dt>/serve API</dt>
    <dd>Posts raw JSON content of Fiend load when requested; potentially integrated into / API with D3 architecture.</dd>
</dl>

## Methods

`initialize()`: contained within before_first_request route; instantiates an instance of Fiend for usage in this logging session. Prints ready message

`add_no_cache()`: contained within after_request route; sets response cache content control to no-cache behavior

`serve()`: contained within */index* route; generates a hierarchy of data from Fiend and sends in as template objects on *index.html* page render. Otherwise, throws *except.html* page

`parse_sms()`: contained within */sms* route; performs minimal POST request handling and passes object into Fiend, then forward to request to Pi server

`send_to_json()`: contained within */serve* route; generates a hierarchy of data from Fiend and renders raw as a JSON object

## Interaction

Essentially, triggered by POST requests from the */sms* route or GET requests from the  */index* or */* route. Does a significant amount of passing around in `parse_sms` method. *Note for Future Use:* Ideally, Fiend `load` call will be retriggered upon each subsequent POST request rather than */index* request.

## Resources

* [All Documentation](../blob/master/README.md)
* [Fiend Documentation](../blob/master/src-fiend/README2.md)

___
![cc logo](http://www.etcs.ipfw.edu/~dupenb/Pictures/CC-BY-SA%20logo.jpg)
