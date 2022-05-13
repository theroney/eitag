import sys
from optparse import OptionParser
import datetime
import base64
import urlparse

version_string = "ei-tag.py v2022-13-05"
usage = "%prog -e EITERM -q OR %prog -u URL -q"

parser = OptionParser(usage=usage)
parser.add_option("-e", dest="eiterm", 
                  action="store", type="string",
                  help="Google search URLs EI parameter value")
parser.add_option("-u", dest="url",
                  action="store", type="string",
                  help="Complete Google search URL")
parser.add_option("-q", dest="quiet",
                  action="store_true", 
                  help="(Optional) Quiet output (only outputs timestamp string)")
(options, args) = parser.parse_args()

if not (options.quiet):
    print "Running " + version_string + "\n"


if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

if ((options.eiterm == None) and (options.url == None)):
    print "Error! Neither ei or URL terms were specified. Choose one!\n"
    parser.print_help()
    exit(-1)

if ((options.eiterm != None) and (options.url != None)):
    print "Error! BOTH ei and URL terms were specified. Choose one!\n"
    parser.print_help()
    exit(-1)

ei = ""
if (options.url != None):    
    parsed = urlparse.urlparse(options.url)

    if ("ei" not in parsed.query):
        if not (options.quiet):
            print "No ei parameter found in URL!"
        exit(-1)

    ei = urlparse.parse_qs(parsed.query)["ei"][0]
    if not (options.quiet):
        print "URL's ei term = " + ei
else:
    ei = options.eiterm
    if not (options.quiet):
        print "Input ei term = " + ei


num_extra_bytes = (len(ei) % 4) 
if (num_extra_bytes != 0):
    padlength = 4 - num_extra_bytes
    padstring = ei + padlength*'='
else:
    padstring = ei

if not (options.quiet):
    print "Padded base64 string = " + padstring


decoded = base64.urlsafe_b64decode(padstring)


timestamp = ord(decoded[0]) + ord(decoded[1])*256 + ord(decoded[2])*(256**2) + ord(decoded[3])*(256**3)

if not (options.quiet):
    print "Extracted timestamp = " + str(timestamp)

try: 
    datetimestr = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')
except:
    datetimestr = "Unknown"

if not (options.quiet):
    print "Human readable timestamp (UTC) = " + datetimestr
else:
    print datetimestr

exit(0)
