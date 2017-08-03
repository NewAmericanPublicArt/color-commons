# FIEND MEGA-TUTORIAL
###### (c) Sydney Strzempko for NAPA, 2017

### Table of Contents

**I**[Overview, Methods List](../src-fiend/TUTORIAL.md#i-overview-methods-list)

**II**[Instantiating a Fiend](../src-fiend/TUTORIAL.md#ii-instantiating-a-fiend)

**III**[Loading in data](../src-fiend/TUTORIAL.md#iii-loading-in-data)

**IV**[Find Queries](../src-fiend/TUTORIAL.md#iv-find-queries)

**V**[Sort_by Queries](../src-fiend/TUTORIAL.md#v-sort_by-queries)

**VI**[Load (BETA) Queries](../src-fiend/TUTORIAL.md#vi-load-beta-queries)

**VII**[Connecting Fiend to a Server](../src-fiend/TUTORIAL.md#vii-connecting-fiend-to-a-server)

**VIII**[Resources](../src-fiend/TUTORIAL.md#viii-resources)
___

## I. Overview, Methods List

Fiend is essentially a big black-box grouping of methods and elements to manipulate and aggregate data. The Fiend conditions we are working under have shaped some of the methods such that they are calibrated to a specific entry format, and the Fiend log of saved terms also follows a specified format. However, much of the code could be recycled with minor modifications for other projects other than the Color-Commons application.

The list of methods pertaining to Fiend is as follows;
- \_\_init\_\_
- \_\_deepcopy\_\_ [both custom hooks]
- get_log
- get_time
- get_date
- send_to_csv
- get_fr_csv
- new_entry
- new_entry2
- load
- defaultload
- thu_load [ TODO - REMOVE ]
- find
- range_find
- in_range
- sort_by
- get_hashable
- generate_alias
- get_jsdt
- rm_dt
- compute_range
- daylabel
- get_ms
- convertexcel
- convert_to_str
- parse_command
- complement
- look_up_color

For a description of each, refer to README.md for the Fiend module for usage guidelines.

## II. Instantiating a Fiend

In order to generate a Fiend, a call must be made to the \_\_init\_\_ function. In the color-commons project, the server creates a Fiend before the first request; namely, before the server is *sent* info, it must spawn a new Fiend to handle that info. When using the Fiend module standalone, we don't need to worry about server-side @before-first-request decorators; we can simply instantiate a local instance of Fiend devoid of server-side machinations.
Simply;
1. Open a new file in the /src-fiend directory; let's call this "sample.py". Make sure to save with the .py encoding or it will not be read as a Python file.
2. Copy-and-paste the "page header" as found in the /src-fiend/resources folder under "header.py". This imports the Fiend library from its corresponding file.
3. Create a new instance of Fiend using the \_\_init\_\_ call. Under the covers, the \_\_init\_\_ call accepts 2 variables; log and hash. These can be useful in specifying pre-formatted logs and deepcopies of Fiend instances. For now however, we only must pass them in as "[]" (eg, an empty list object indicating that Fiend starts out empty) and "None" (eg, a Nonetype object indicating Fiend should generate its own hasher). **Weird Note** about the \_\_init\_\_ call - due to its hook status we actually never write out the weird underscores, but instead call it as the title of that class itself. eg;
```python
[ header code ]
dansfiend = Fiend( [], None )
```

4. Begin writing your instance-specific code!

## III. Loading in data

SO now that we have our particular instance of Fiend, `dansfiend`, we need him to possess information in order to manipulate it. The two methods allowing for entry are `new_entry` and `new_entry2` (which is instantiated by `get_fr_csv`). The main difference between these two functions is the format of an entry when it is passed in via a new_entry call.

`new_entry`: accepts entries of format `{ 'name': x, 'msg': y }`

`new_entry2`: accepts entries of format `{ 'name': x, 'msg': y, 'date': z, 'time': a}`

As we mentioned,, the 2nd entry style can be called from the master-method, `get_fr_csv`. This function allows for the importation of an unspecified number of entries into Fiend rapidly from the .csv file format.
**Weird Note:** There is a specific format for this entry style for .csvs. Refer to */resources/csvs* for examples on how to correctly set up fields for mass importation. Of particular note is the |x| brackets for the 'msg' field in order to allow for commas in the message body without messing up the csv format.

*ASSUMING WE ALREADY IMPORTED THE HEADER AND CALLED THE INIT AS FOUND IN SEGMENT II*, Here are three different ways to import an entry from someone with the phone number '5089001000' and the message 'purple':

1. **new_entry**
```python
entry = { 'name': '5089001000', 'msg':'purple'} # This simply declares an intermediate variable in dictionary format
dansfiend.new_entry(entry) # returns True/False depending on success of entry; can be assigned a variable or ignored
```
*Note*: If you don't know what is/how to construct a python dictionary, refer to [Docs](https://docs.python.org/3/reference/expressions.html#dict)

2. **new_entry2**
```python
entry = { 'name': '5089001000', 'msg':'purple', 'date': dansfiend.get_date(), 'time':dansfiend.get_time() } # This will give exact same date & time values as above
dansfiend.new_entry2(entry) # also returns True/False depending on success of entry; can be assigned a variable or ignored
```
3. **get_fr_csv** 
Make a .csv document in the src-fiend folder with the format:
```
[THROWAWAY FIRST LINE - From,To,Body,SentDate,AcctSid,Sid]
5089001000,[placeholder],|purple|,2017-07-11 17:00:00 UTC,[placeholder],[placeholder]
```
Let's name this file 'import.csv'. Then in the file you've set up from (II), write the following;
```python
dansfiend.get_fr_csv('import.csv')
```
To put in another entry? Use any of the three previous formats all over again; Fiend never hard-programs to only accept 1 entry style, and you can always change the method by which data is being inputted. As you can see, there is a *TIME AND PLACE* for all of these method calls; the 1st is best suited to a fresh Twilio SMS message request, the 2nd best suited to entries where the Date and Time fields can't be defaulted to the current date and time, and the 3rd best suited to huge backlogs of entries in the .csv format.

**Weird Note:** You may be wondering why the .csvs are set up in such a strange format. In the development of Fiend, all of the old data we were working with came from direct dowmloads of status logs on the Twilio console, which had very particular field formats upon download. Although we maintained a few placeholders, like the 'To' and 'Sid' fields, the intent was to allow for a relatively standardized CSV format, with some wiggle room, that could be used by other services.

## IV. Find Queries

Now that we have *hundreds* of log entries loaded into dansfiend and ready to go (let's say that this is the case), we want to find a subset of data with particular attributes. The method to focus on here is `find`; it requires two parameters, a source-array (from which to draw), and a query. For those who don't know, a 'query' is a set of parameters from which the Fiend attempts to find matching entries for. In our Fiend implementation, queries take a dictionary format (the same class of object as the entry format we saw above) of really any length.
**Weird Note:** Passing in a None as the source-array value defaults searching on the current Fiend's log of all values. Passing in an empty dictionary ({}) as a query value returns the full source-array.

For illustration, we will be providing three increasingly complex example scenarios; seeking a subset of all entries where the message was "orange" or "redorange", seeking a subset of all entries between the hours of 12AM and 6AM, and seeking a subset of all entries where the message was "orange" between the hours of 12AM and 6AM on Christmas 2017 *(trick question - that's in the future! But we're still going to show it)*.

1. **"orange" or "redorange" query**
```python
oquery = {'msg':'orange'} # Setting up both of our queries
roquery = {'msg':'redorange'}
set1 = dansfiend.find(None,oquery) # First search, for oranges
set2 = dansfiend.find(None,roquery) # Second search, for redoranges
redoranges = set1 + set2 # To find all, simply combine the two; obviously no overlap/repeated values here
```
2. **all 12AM-6AM (early-morning) query**
*Note:* uses datetime format. Refer to [this](https://docs.python.org/2/library/datetime.html#time-objects) for more, but if you are using the header file provided as a template then this object-type should already be included and not cause an error.
```python
t0 = datetime.time(6,0,0) # In hr, min, sec format
t1 = datetime.time(12,0,0) # If we wanted PM we would use 24 or 0
query = {'time': {'start':t0, 'end':t1} } # NOTE - CAN PUT RANGE INTO ANYTHING. So we couldve used the alphabet to our advantage on our last prompt - how?
mornings = dansfiend.find(query) # Now mornings should hold all 12AM-6AM entries regardless of date
```
3. **Christmas "orange" early-morning query**
```python
christmas = datetime.date(2017,1,25)
t0 = datetime.time(6,0,0)
# Let's also say we don't want to use t1. We could add a TIMEDELTA object of 6 hours to our t0 in order to simulate this
# So constructing our query will go as follows;
query = { 'msg': 'orange', 'date': christmas, 'time': {'start': t0, 'end': (t0 + datetime.timedelta(hours=6)) } }
xmasmorningoranges = dansfiend.find(query) # Now xmasmorningoranges should hold a list of all fitting the narrow criteria
```

## V. Sort_by Queries

As witnessed above, we can get a surprisingly high degree of specificity from combining these multi-key queries on data sets. But this methodology is limited in its scope; for example, let's look at the first `find` query we performed. The (concatenated) list we got back at the end of those commands contained data for just two (orange, redorange) of over 1000 colors recognized by the color-commons library that translates to manipulation of the light blades. What if we wanted to know all of the different colors people sent in? Sure, we could run a `find` for all of the colors in /resources/xkcd_colors.py, but what about misspelled or undefined colors, like "blaqq" or "old shoe"? We wouldn't even know *to* search for them, let alone if we forgot to include them in our list of all colors submitted. Instead, we introduce a new functionality; `sort_by`. This accepts two parameters; a root string deciding what quality to sort by, and a source/raw/array from which to draw.
**Weird Note** Although leaving the source in `find` blank substitutes log, we must actually manually write `dansfiend.get_log()` or `dansfiend.log` as the second parameter in `sort_by` or it will *not* default on its own log.
Thus, to solve our problem introduced above, we'd simply query the following;
```python
allcolors = dansfiend.sort_by( "color", dansfiend.get_log() ) 
# Or, optionally, this;
allcolors2 = dansfiend.sort_by( "color", dansfiend.log )
```
This would return something like
```
[{'name':'aubergine', 'children': [....entries] },
 {'name': 'avocado', 'children': [...entries] },
 {'name': 'basalt', 'children': [...entries] }
 ...more color groupings...] #As 1 big list object of nested node-lists
```
The sort queries ("month","day","hour","user","newuser","color","color2") are hardwired into evry instance of Fiend, and organize by their category name, respectively. The "month" and "hour" sorts default to 12- and 24-entry subsets per yr or day. "user" refers to a unique user with their subset of all entries, and newuser" refers to a first-time user with a subset of entries compared against all past entries. 
Sorts can be nested inside each other, although only to one degree of nesting, as `sort_by` is not smart enough to intuitively work its way through complex tree systems. Thus I could call sort_by for unique users on `{'name':'aubergine', 'children':[]}` and sort_by would know to refer to the children subset, but not be able to call sort_by on each color from the main object without a for loop calling sort_by multiple times.

## VI. Load (BETA) Queries

Load is the query-type that ties together finds and sort_bys and then processes it for non-python applications. The load suite can be broken down into 3 big steps;
1. Create fiend copy, call get_jsdt
2. Sort/find queries into a tree
3. Calling rm_dt on tree

TODO

## VII. Connecting Fiend to a Server

So now that we understand Fiend, and a 'sample.py' file with a series of commands, how do we run this file on Python? Depending on what version of Python you have installed, this command-line command could be a little different, but essentially;
```
>> python sample.py
```
should run your program. Be sure to include `print(x)` or `send_to_csv()` messages so that you can actually get it to spit out the results of your aggregation onto terminal or to a file. Otherwise it'll just run, work fine, and not really "say" anything to you, the caller of the program. Also remember that every "python x" command instantiates a *new* instance of Fiend, so no data entered into the Fiend in an earlier, different iteration of the sample file will hang around when respecified in a later iteration of sample.py. With this in might, it might be easier to understand why `get_fr_csv` can be such a powerful tool on multiple instantiations of Fiend.

But what about the color-commons `server.py` file, and that one point earlier where we mentioned @before-first-request or something equally confusing?? Is this a completely different "thing" from the Fiend?
*The answer is no;* the server simply spawns its own Fiend and gives it very specific instructions using POST/GET APIs (this can get confusing if you've never done web apps - refer to [Flask](http://flask.pocoo.org/) if it's a serious roadblock to understanding what we are trying to accomplish here) so that the Fiend takes new entries in through the Twilio /SMS API, and displays a `load`-ed version of its log through the / or /index API. Essentially, the Fiend is just a venus flytrap that catches flies; the server is the homeowner that puts the Fiend near the window that flies are coming in through. 

## VIII. Resources
