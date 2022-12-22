#!/usr/bin/python
from os import listdir
from os.path import join, isfile
import xml.etree.ElementTree as ET
from PIL import Image


for f in listdir("./png/"):
    if "png" in f:
        xmlFile = f.replace(".png", ".xml")
        if not isfile(join("./xml", xmlFile)):
            print("**ERROR: '%s' is missing**\n" % xmlFile)
        else:
            with Image.open(join("./png", f)) as im:
                if im.width != 154 or im.height != 500:
                    print("WARNING: '%s' has not the correct size w=%s,h=%s\n" % (f, im.width, im.height))
            tree = ET.parse(join("./xml", xmlFile))
            root = tree.getroot()
            rc = root.find("rc")
            if rc:
                for button in rc.findall("button"):
                    key = button.attrib.get("id")
                    if key:
                        label = button.attrib.get("label", "")
                        if not label and key != "KEY_RESERVED":
                            print("WARNING: '%s' has no label for '%s'\n" % (xmlFile, key))
                    else:
                        print("**ERROR: '%s' is invalid**\n" % xmlFile)
                        break
            else:
                print("**ERROR: '%s' is invalid**\n" % xmlFile)
