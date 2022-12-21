#!/usr/bin/python
from os import listdir
from os.path import join, isfile
from PIL import Image
from PIL import ImageDraw
import xml.etree.ElementTree as ET

full = Image.new('RGBA', (154 * 3, 500))

pos = 0
for f in listdir("./png/"):
    if "png" in f and isfile(join("./xml", f.replace(".png", ".xml"))):
        with Image.open(join("./png", f)) as im:
            dst = Image.new('RGBA', (154, 500))
            dst.paste((0, 0, 0), [0, 0, dst.size[0], dst.size[1]])
            l = 154 - im.width
            t = 500 - im.height
            dst.paste(im, (0, 0))
            full.paste(dst, (0, pos * 500))
            tree = ET.parse(join("./xml", f.replace(".png", ".xml")))
            root = tree.getroot()
            rc = root.find("rc")
            bpos = 1
            legend = Image.new('RGBA', (154, 500))
            legend.paste((255, 255, 255), [0, 0, legend.size[0], legend.size[1]])
            ldraw = ImageDraw.Draw(legend)
            ldraw.text((20, 10), f.replace(".png", ""), fill="black")
            for button in rc.findall("button"):
                pp = [int(x.strip()) for x in button.attrib.get("pos", "0").split(",")]
                p_x, p_y = pp[0], pp[1]
                draw = ImageDraw.Draw(dst)
                draw.ellipse((p_x - 10, p_y - 10, p_x + 10, p_y + 10), fill=(255, 255, 255, 50), outline=(255, 255, 0))
                draw.text((p_x - 5, p_y - 5), str(bpos), fill="red")
                txt = "%s - %s" % (str(bpos), button.attrib.get("id"))
                ldraw.text((10, 20 + (bpos * 9)), txt, fill="black")
                bpos += 1

            full.paste(dst, (155, pos * 500))
            full.paste(legend, (155 + 154, pos * 500))
            pos += 1
        full.save(join("./previews", f))
