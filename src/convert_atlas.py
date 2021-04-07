import xml.etree.ElementTree as ET
import re
import shutil
import os

os.mkdir('../emoji/data/temp')
shutil.move('../emoji/data/graphics/ui', '../emoji/data/temp/ui')
shutil.move('../emoji/data/graphics/titlescreen',
            '../emoji/data/temp/titlescreen')
shutil.rmtree('../emoji/data/graphics')
shutil.move('../emoji/data/temp', '../emoji/data/graphics')
shutil.copyfile('packed/packed.png', '../emoji/data/graphics/emojis.png')
shutil.copyfile('packed/packed2.png', '../emoji/data/graphics/emojis2.png')


def convert(image_path, output_path, file):
    file.readline()
    size = re.fullmatch(r'size: (\d+), (\d+)\n', file.readline())
    root = ET.Element('TextureAtlas',
                      {'imagePath': image_path,
                       'width': size[0], 'height': size[1]})
    for i in range(3):
        file.readline() # Irrelevent metadata
    while (line := file.readline()) not in ['\n', '']:
        texture = ET.SubElement(root, 'SubTexture')
        texture.set('name', line[:-1].lower())
        file.readline() # rotate setting, always false       
        xy = re.fullmatch(r'  xy: (\d+), (\d+)\n', file.readline())
        texture.set('x', xy[1])
        texture.set('y', xy[2])
        size = re.fullmatch(r'  size: (\d+), (\d+)\n', file.readline())
        texture.set('width', size[1])
        texture.set('height', size[2])
        for i in range(3):
            file.readline() # More irrelevant data
    ET.ElementTree(root).write(output_path, 'UTF-8', True)
    

with open('packed/packed.atlas') as file:
    file.readline() #skip a blank line
    convert('emojis.png', '../emoji/data/graphics/emojis.xml', file)
    convert('emojis2.png', '../emoji/data/graphics/emojis2.xml', file)
