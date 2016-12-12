from flask import Flask, render_template, request
from uwsgidecorators import *
import pytronics
import os, time

public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

# config for upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_DIRECTORIES = set(['static/uploads/', 'static/pictures/'])
LIVE_PINS = ['LED', '2', '3', '4', '5', '6', '7']
# public.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

### Home page ###
@public.route('/')
@public.route('/index.html')
def default_page():
    try:
        with open('/etc/hostname', 'r') as f:
            name = f.read().strip().capitalize()
    except:
        name = 'Rascal'
    return render_template('/index.html', hostname=name, template_list=get_public_templates())

def get_public_templates():
    r = []
    d = '/var/www/public/templates'
    for f in os.listdir(d):
        ff=os.path.join(d,f)
        if os.path.isfile(ff):
            r.append(f)
    return sorted(r)

# Format date/time in Jinja template
@public.template_filter()
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return time.strftime(format, value)

# Return current date and time in specified format
@public.route('/datetime', methods=['POST'])
def datetime():
    try:
        format = request.form['format']
    except:
        format = '%d %b %Y %H:%M %Z'
    return time.strftime(format, time.localtime())

### Generic HTML and Markdown templates, support for doc tab ###
@public.route('/<template_name>.html')
def template(template_name):
    return render_template(template_name + '.html', magic="Hey presto!")

@public.route('/<doc_name>.md')
def document(doc_name):
    return render_markdown('', doc_name)

@public.route('/docs/<doc_name>.md')
def document_docs(doc_name):
    return render_markdown('docs/', doc_name)

def render_markdown(path, doc_name):
    import markdown2
    with open('/var/www/public/templates/' + path + doc_name + '.md', 'r') as mdf:
        return render_template('documentation.html', title=doc_name, markdown=markdown2.markdown(mdf.read()))
    return 'Not Found', 404

@public.route('/get_markdown', methods=['POST'])
def get_markdown():
    import markdown2
    doc_name = request.form['docName']
    try:
        with open('/var/www/public/templates/docs/' + doc_name + '.md', 'r') as mdf:
            return markdown2.markdown(mdf.read())
    except:
        try:
            with open('/var/www/public/templates/' + doc_name + '.md', 'r') as mdf:
                return markdown2.markdown(mdf.read())
        except:
            with open('/var/www/public/templates/docs/default.md', 'r') as mdf:
                return markdown2.markdown(mdf.read())
    return 'Internal server error', 500

### Support for pins ###
def toggle_pin(pin):
    if pytronics.digitalRead(pin) == '1':
        pytronics.digitalWrite(pin, 'LOW')
    else:
        pytronics.digitalWrite(pin, 'HIGH')

@public.route('/pin/<pin>/<state>')
def update_pin(pin, state):
    try:
        if state.lower() == 'on':
            pytronics.digitalWrite(pin, 'HIGH')
            return 'Set pin %s high' % pin
        elif state.lower() == 'off':                       
            pytronics.digitalWrite(pin, 'LOW')
            return 'Set pin %s low' % pin
        elif state.lower() == 'in':
            pytronics.pinMode(pin,'INPUT')
            return 'Set pin %s input' % pin
        elif state.lower() == 'out':
            pytronics.pinMode(pin,'OUTPUT')
            return 'Set pin %s output' % pin
        return "Something's wrong with your syntax. You should send something like: /pin/2/on"
    except:
        return 'Forbidden', 403

@public.route('/read-pins', methods=['POST'])
def read_pins():
    import json
    # return json.dumps(pytronics.readPins(LIVE_PINS))
    pins = pytronics.readPins(LIVE_PINS)
    analog = {}
    for chan in ['A0', 'A1', 'A2', 'A3']:
        analog[chan] = pytronics.analogRead(chan)
    return json.dumps({ 'pins': pins, 'analog': analog })

### Support for serial ###
@public.route('/serial/<port>/<speed>/<message>', methods=['POST'])
def serial_write(port, speed, message):
    pytronics.serialWrite(message, speed, port)
    return 'Tried to write serial data.'

@public.route('/sms', methods=['POST'])
def parse_sms():
    from xkcd_colors import xkcd_names_to_hex
    import serial, webcolors
    message = request.form['Body']
    print("Received text message: " + str(message))
    color = webcolors.hex_to_rgb(xkcd_names_to_hex[str(message.lower())])
    cmd = str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + '\n'
    ser = serial.Serial(port = "/dev/ttyACM0", baudrate=9600)
    ser.write(cmd)
    #
    # Control a Blinkm
    #cmd = 'blinkm set-rgb -d 9 -r ' + str(color[0]) + ' -g ' + str(color[1]) + ' -b ' + str(color[2])
    #subprocess.Popen([cmd], shell=True)
    #
    # Write to a file
    #f = open('/var/www/public/thermostat-target.txt', 'w')
    #f.write(str(message))
    #f.close()
    print('Wrote to USB: {0}'.format(cmd))
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')

@public.route('/sms', methods=['POST'])
def control_lights():
    d = {'airforceblue': '11',
        'airsuperiorityblue': '11',
        'aliceblue': '16',
        'amaranth': '29',
        'amaranthpink': '25',
        'amber': '22',
        'ambergem': '43',
        'america': '78',
        'amethyst': '52',
        'apple': '41',
        'applegreen': '41',
        'apricot': '48',
        'aqua': '13',
        'aquamarine': '51',
        'art': '74',
        'ash': '49',
        'ashgray': '49',
        'asparagus': '41',
        'ass': '72',
        'asshole': '72',
        'atomictangerine': '24',
        'aubum': '29',
        'auburn': '32',
        'avocado': '41',
        'azure': '14',
        'babyblue': '16',
        'barnred': '30',
        'baseball': '71',
        'basketball': '58',
        'battleship': '49',
        'battleshipgray': '49',
        'battlestar': '59',
        'beaver': '33',
        'beige': '46',
        'bevan': '74',
        'beyer': '74',
        'bird': '64',
        'birds': '64',
        'bistre': '36',
        'bittersweet': '24',
        'bleudefrance': '14',
        'blond': '10',
        'blood': '95',
        'blue': '17',
        'bluegray': '11',
        'blueviolet': '20',
        'bondiblue': '19',
        'bos': '71',
        'boston': '70',
        'brandeisblue': '14',
        'brandon': '74',
        'brightgreen': '39',
        'bronze': '31',
        'brown': '31',
        'brown-nose': '31',
        'brownnose': '31',
        'bruin': '65',
        'bruins': '65',
        'buff': '47',
        'bullshit': '72',
        'burgundy': '32',
        'butt': '72',
        'butter': '76',
        'byzantium': '55',
        'cacahuete': '87',
        'cadet': '49',
        'cadetgray': '49',
        'calpolygreen': '38',
        'camel': '33',
        'camo': '97',
        'cardinal': '29',
        'carmine': '30',
        'carnationpink': '25',
        'carolinablue': '16',
        'carrot': '22',
        'carrotorange': '22',
        'celeste': '13',
        'celtics': '58',
        'cerise': '54',
        'cerulean': '19',
        'ceruleanblue': '19',
        'chamoisee': '33',
        'champagne': '48',
        'chartreuse': '39',
        'chartreusegreen': '39',
        'chartreusetraditional': '40',
        'chartreuseweb': '39',
        'chartreuseyellow': '40',
        'cheese': '76',
        'chestnut': '31',
        'chocolate': '31',
        'cobalt': '18',
        'cobaltblue': '18',
        'columbia': '16',
        'confetti': '64',
        'coolgray': '49',
        'copper': '31',
        'coral': '24',
        'cornflower': '12',
        'cornflowerblue': '12',
        'cream': '46',
        'crimson': '29',
        'cuddling': '73',
        'cummingtonite': '94',
        'cyan': '13',
        'dan': '74',
        'darkblue': '18',
        'darkbrown': '36',
        'darkgoldenrod': '45',
        'darkgray': '50',
        'darkgreen': '38',
        'darkred': '30',
        'darksalmon': '24',
        'darkspringgreen': '38',
        'dartmouth': '38',
        'deepcarrotorange': '22',
        'deeppink': '26',
        'deepsky': '13',
        'deepskyblue': '13',
        'denim': '15',
        'desertsand': '35',
        'dick': '72',
        'dodger': '14',
        'dodgerblue': '14',
        'dubstep': '64',
        'duke': '18',
        'dukeblue': '18',
        'dumb': '78',
        'earthyellow': '35',
        'easter': '68',
        'easteregg': '68',
        'ecru': '47',
        'egg': '68',
        'eggplant': '55',
        'eggshell': '10',
        'egyptianblue': '17',
        'electricblue': '51',
        'electriccrimson': '28',
        'electricindigo': '20',
        'everything': '74',
        'fallow': '33',
        'fandango': '54',
        'federalblue': '18',
        'fern': '41',
        'ferngreen': '41',
        'fire': '62',
        'fireenginered': '28',
        'fish': '68',
        'flame': '23',
        'folly': '54',
        'food': '75',
        'forest': '38',
        'forestgreen': '38',
        'free': '78',
        'freedom': '78',
        'fuchsia': '54',
        'fuck': '72',
        'fulvous': '35',
        'gak': '88',
        'galactica': '59',
        'gamboge': '22',
        'glaucous': '11',
        'glitter': '76',
        'gold': '43',
        'goldenrod': '45',
        'goldmetal': '45',
        'goldmetallic': '45',
        'gray': '49',
        'green': '37',
        'greenway': '67',
        'greenyellow': '40',
        'grey': '49',
        'hacker': '79',
        'hackernews': '79',
        'harlequin': '37',
        'heliotrope': '53',
        'helloworld': '82',
        'hn': '79',
        'hockey': '65',
        'hollywoodcerise': '27',
        'honeydew': '10',
        'hotmagenta': '26',
        'hotpink': '26',
        'husband': '73',
        'ica': '66',
        'indiagreen': '38',
        'indigo': '52',
        'interactive': '74',
        'internationalkleinblue': '17',
        'internationalorange': '23',
        'iris': '20',
        'isabelline': '10',
        'islamicgreen': '38',
        'ivory': '10',
        'jonquil': '43',
        'juxtaposition': '69',
        'kawan': '74',
        'kawandeep': '74',
        'khaki': '47',
        'kiss': '73',
        'kleinblue': '17',
        'la': '63',
        'lace': '10',
        'laurel': '41',
        'laurelgreen': '41',
        'lavender': '53',
        'lavenderpink': '25',
        'lawn': '37',
        'lawngreen': '37',
        'lemonchiffon': '46',
        'leo': '73',
        'lightblue': '16',
        'lightgreen': '39',
        'lightyellow': '44',
        'lime': '40',
        'limerick': '41',
        'lion': '45',
        'littlespoon': '73',
        'liver': '50',
        'locks': '87',
        'love': '73',
        'lust': '28',
        'magenta': '54',
        'magicmint': '51',
        'magnolia': '10',
        'mahogany': '34',
        'maize': '43',
        'majorelleblue': '20',
        'make': '78',
        'malachite': '93',
        'mantis': '41',
        'mariah': '73',
        'maroon': '32',
        'mayablue': '16',
        'mediumblue': '17',
        'megan': '73',
        'metalgold': '45',
        'metallicgold': '45',
        'midnight': '18',
        'midnightblue': '18',
        'midori': '40',
        'mikado': '43',
        'mikadoyellow': '43',
        'moon': '66',
        'moonbounce': '66',
        'moonstone': '90',
        'mouse': '68',
        'mush': '75',
        'myrtlegreen': '42',
        'mytrle': '42',
        'napa': '74',
        'naplesyellow': '43',
        'navajo': '48',
        'navajowhite': '48',
        'navy': '18',
        'navyblue': '18',
        'neodya': '77',
        'neodya2': '77',
        'non-photoblue': '16',
        'nothing': '10',
        'nyanza': '39',
        'ochre': '35',
        'officegreen': '38',
        'oldsilver': '49',
        'olive': '41',
        'olivedrab': '41',
        'ooblah': '83',
        'opal': '91',
        'opposite': '69',
        'opposites': '69',
        'orange': '22',
        'orangepeel': '22',
        'orangered': '23',
        'orangeweb': '22',
        'orchid': '53',
        'oxfordblue': '18',
        'pakistangreen': '38',
        'palatinateblue': '17',
        'papaya': '48',
        'papayawhip': '48',
        'park': '67',
        'partner': '73',
        'party': '64',
        'pastel': '86',
        'pastellow': '86',
        'patrick': '58',
        'patty': '58',
        'peach': '48',
        'peachorange': '48',
        'peachyellow': '48',
        'peanut': '87',
        'pear': '41',
        'periwinkle': '21',
        'persianblue': '17',
        'peru': '31',
        'phthaloblue': '18',
        'pinegreen': '19',
        'pink': '25',
        'pistachio': '41',
        'playa': '64',
        'plum': '55',
        'poop': '75',
        'popcorn': '76',
        'portlandorange': '23',
        'powderblue': '16',
        'princetonorange': '22',
        'public': '74',
        'pumpkin': '22',
        'purple': '55',
        'rabbit': '68',
        'rain': '61',
        'rainbow': '57',
        'random': '64',
        'raspberry': '29',
        'ravercamo': '98',
        'rawumber': '33',
        'red': '28',
        'red-brown': '32',
        'redbrown': '32',
        'redorange': '23',
        'redsock': '71',
        'redsocks': '71',
        'redsox': '71',
        'redviolet': '54',
        'redwhiteblue': '78',
        'redwood': '30',
        'river': '76',
        'robin': '13',
        'robinegg': '13',
        'robineggblue': '13',
        'romance': '73',
        'romansilver': '49',
        'rose': '54',
        'rosepink': '26',
        'rosewood': '30',
        'royalblue': '15',
        'ruby': '28',
        'rufous': '32',
        'russet': '31',
        'rust': '34',
        'sacramento': '38',
        'sacramentostate': '38',
        'sacramentostategreen': '38',
        'safetyorange': '22',
        'saffron': '43',
        'salmon': '24',
        'salmonella': '85',
        'salmonpink': '25',
        'sandybrown': '35',
        'sapphire': '15',
        'scanner': '56',
        'scarlet': '28',
        'schoolbus': '44',
        'schoolbusyellow': '44',
        'seafood': '68',
        'seagreen': '42',
        'sealbrown': '36',
        'seaman': '84',
        'seashell': '10',
        'selectiveyellow': '43',
        'semen': '84',
        'sepia': '31',
        'sex': '73',
        'shamrock': '42',
        'shamrockgreen': '42',
        'sharon': '73',
        'shit': '75',
        'shockingpink': '27',
        'shrimp': '68',
        'sides': '69',
        'sienna': '34',
        'silver': '49',
        'silverchalice': '49',
        'silversand': '49',
        'sinopia': '34',
        'skobeloff': '19',
        'sky': '13',
        'skyblue': '16',
        'skycamo': '96',
        'slate': '49',
        'slategray': '49',
        'slimer': '89',
        'slimergreen': '89',
        'smoke': '10',
        'smokeytopaz': '31',
        'snow': '10',
        'sonicsilver': '49',
        'sparkle': '76',
        'sparqule': '76',
        'spoon': '73',
        'springbud': '40',
        'stafford': '74',
        'steelblue': '11',
        'stoplight': '60',
        'stpatrick': '58',
        'stream': '76',
        'sunglow': '43',
        'sunset': '81',
        'tan': '33',
        'tangelo': '23',
        'tangerine': '22',
        'tartar': '95',
        'taupe': '50',
        'tawny': '34',
        'teal': '19',
        'tearose': '24',
        'tiffanyblue': '16',
        'tigereye': '92',
        'timberwolf': '49',
        'toaster': '59',
        'tomato': '23',
        'tonton': '96',
        'trueblue': '14',
        'tufts': '15',
        'tuftsblue': '15',
        'turquoise': '13',
        'tuscanred': '30',
        'uclablue': '11',
        'ultramarine': '18',
        'ultrapink': '26',
        'umber': '50',
        'upforest': '42',
        'upforestgreen': '42',
        'usa': '78',
        'vanilla': '46',
        'vermillion': '28',
        'violet': '52',
        'virdee': '74',
        'webelo': '76',
        'weird': '64',
        'weismann': '74',
        'weissman': '74',
        'wenge': '50',
        'wheat': '35',
        'white': '10',
        'wife': '73',
        'wine': '30',
        'wired': '80',
        'wisteria': '53',
        'wonton': '96',
        'wood': '31',
        'yale': '15',
        'yaleblue': '15',
        'yc': '79',
        'yellow': '44',
        'yellow-green': '40',
        'yellowgreen': '40',
        'zaffre': '18',
        ':(': '18',
        ':)': '73',
        '<3': '62',
        'agreement': '76',
        'ah': '84',
        'ahh': '84',
        'ahhh': '84',
        'ahhhh': '84',
        'ahhhhh': '84',
        'aquarium': '90',
        'aubergine': '54',
        'avacado': '93',
        'baboon': '91',
        'banana': '92',
        'barkingcrab': '62',
        'barn': '29',
        'bathtub': '76',
        'bear': '77',
        'black': '50',
        'bleh': '98',
        'bloom': '66',
        'blur': '76',
        'blurp': '84',
        'blurp!': '84',
        'bluw': '18',
        'bokchoi': '41',
        'bubblegum': '85',
        'burntsiena': '34',
        'butterscotch': '93',
        'cabbage': '42',
        'calman': '84',
        'cat': '92',
        'chair': '17',
        'cherry': '29',
        'christmas': '64',
        'chromacity': '75',
        'chromaticuty': '85',
        'city': '67',
        'clear': '50',
        'comeonlights': '93',
        'connect': '92',
        'couch': '98',
        'crab': '62',
        'cranberry': '30',
        'crazy': '91',
        'cyclon': '59',
        'cylon': '59',
        'discus': '77',
        'disparate': '69',
        'dog': '77',
        'dolphin': '93',
        'dream': '85',
        'eel': '84',
        'ellie': '98',
        'elliefolding': '98',
        'emerald': '40',
        'fever': '75',
        'flash': '72',
        'flu': '75',
        'fuscia': '54',
        'galaxy': '61',
        'goldfish': '92',
        'gopher': '77',
        'grass': '41',
        'hermit': '62',
        'hermitcrab': '62',
        'hermitcrabs': '62',
        'holly': '40',
        'iloveyou': '85',
        'ish': '87',
        'jellyfish': '85',
        'kelly': '75',
        'kelp': '89',
        'lamp': '92',
        'laugh': '91',
        'lemon': '45',
        'light': '93',
        'lightning': '91',
        'limeo': '93',
        'line': '40',
        'lisa': '27',
        'lisamarie': '27',
        'lobster': '62',
        'macaroni': '92',
        'macaroniandcheese': '92',
        'magic': '93',
        'mauve': '53',
        'monkey': '98',
        'moonstones': '93',
        'myrtle': '42',
        'near': '77',
        'nior': '82',
        'nude': '75',
        'off': '50',
        'onyx': '50',
        'pee': '87',
        'penis': '84',
        'phish': '93',
        'pick': '91',
        'piss': '87',
        'plaid': '85',
        'polkadots': '91',
        'poppy': '76',
        'porsche': '92',
        'potpourri': '91',
        'proudmom': '88',
        'puce': '63',
        'putmeincoach': '82',
        'quartz': '91',
        'real': '60',
        'robinsegg': '14',
        'sabertoothtiger': '77',
        'sage': '46',
        'salman': '84',
        'salmonsex': '73',
        'saphire': '76',
        'saturn': '62',
        'science': '91',
        'seaturtle': '93',
        'seaweed': '41',
        'shark': '77',
        'smallcat': '92',
        'soap': '85',
        'starbuck': '21',
        'sunrise': '92',
        'ted': '27',
        'tiger': '62',
        'tin': '49',
        'twilight': '61',
        'twillight': '61',
        'twinkle': '61',
        'viridian': '42',
        'werewolf': '21',
        'yello': '92',
        'youcompletemelights': '92',
        'zebra': '93'}
    allowed_commands = ['X040A',
        'X040B',
        'X040C',
        'X040D',
        'X040E',
        'X040F',
        'X0410',
        'X0411',
        'X0412',
        'X0413',
        'X0414',
        'X0415',
        'X0416',
        'X0417',
        'X0418',
        'X0419',
        'X041A',
        'X041B',
        'X041C',
        'X041D',
        'X041E',
        'X041F',
        'X0420',
        'X0421',
        'X0422',
        'X0423',
        'X0424',
        'X0425',
        'X0426',
        'X0427',
        'X0428',
        'X0429',
        'X042A',
        'X042B',
        'X042C',
        'X042D',
        'X042E',
        'X042F',
        'X0430',
        'X0431',
        'X0432',
        'X0433',
        'X0434',
        'X0435',
        'X0436',
        'X0437',
        'X0438',
        'X0439',
        'X043A',
        'X043B',
        'X043C',
        'X043D',
        'X043E',
        'X043F',
        'X0440',
        'X0441',
        'X0442',
        'X0443',
        'X0444',
        'X0445',
        'X0446',
        'X0447',
        'X0448',
        'X0449',
        'X044A',
        'X044B',
        'X044C',
        'X044D',
        'X044E',
        'X044F',
        'X0450',
        'X0451',
        'X0452',
        'X0453',
        'X0454',
        'X0455',
        'X0456',
        'X0457',
        'X0458',
        'X0459',
        'X045A',
        'X045B',
        'X045C',
        'X045D',
        'X045E',
        'X045F',
        'X0460',
        'X0461',
        'X0462']
    import random
    message = request.form['Body']
    print "Received text message: " + str(message)
    try:
        program = int(d[message[0:25].lower().replace(' ', '')])
    except KeyError:
        print 'color {0} not found'.format(message)
        program = random.randint(10,98)
    command = 'X04%(number)2.2X' % {"number": program}
    print 'Translated {0} to {1}'.format(message, command)
    if (command in allowed_commands):
        pytronics.serialWrite(command, speed=9600)
    else:
        print "Command {0} is not one of the allowed commands.".format(command)
        command = 'FAIL'
    return('<?xml version="1.0" encoding="UTF-8"?><Response>{0}</Response>'.format(command))

# Called from hello.html
@public.route('/flash_led', methods=['POST'])
def flash_led():
    if pytronics.digitalRead('LED') == '1':
        pytronics.digitalWrite('LED', 'LOW')
        message = "LED off"
    else:
        pytronics.digitalWrite('LED', 'HIGH')
        message = "LED on"
    return (message)

if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)
