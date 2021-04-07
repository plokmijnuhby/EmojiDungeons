import subprocess
import shutil
import os
import re
from translate import DUNGEONS_ROOT

shutil.rmtree('png', ignore_errors=True)
os.mkdir('png')
shutil.rmtree('symbols', ignore_errors=True)
os.mkdir('symbols')

trim = ['-define', 'trim:edges=east,west', '-trim']

border = ['-bordercolor', 'none', '-border', '10x10',
          '(', '-clone', '0--1', '-alpha', 'extract',
          '-morphology', 'edgeout', 'disk:10',
          '-fill', 'black', '-colorize', '50%',
          '-background', 'black', '-alpha', 'shape', ')']

subprocess.run(['magick', '-background', 'none',
                DUNGEONS_ROOT + 'data/graphics/ui/symbols.png',
                '-resize', 'x70', '-crop', '33x1@', 'null:']
               + trim + border
               + ['-layers', 'composite', 'symbols/symbol-%d.png'],
               creationflags=subprocess.CREATE_NO_WINDOW)

for file in os.scandir('svg'):
    # We ignore emojis with skin colour modifiers.
    if not re.search('1f3f[b-f]', file.name):
        name = file.name[:-4]
        subprocess.run(['magick', '-background', 'none', '-size', 'x90',
                        file.path] + trim
                       + ['-bordercolor', 'none', '-border', '10x',
                          f'png/{name}.png'],
                       creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['magick', '-background', 'none', '-size', 'x70',
                         file.path] + trim + border
                       + ['-composite', f'png/{name}-border.png'],
                        creationflags=subprocess.CREATE_NO_WINDOW)

