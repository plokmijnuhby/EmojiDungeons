import shutil
import subprocess
from translate import DUNGEONS_ROOT

shutil.rmtree(DUNGEONS_ROOT + 'mods/emoji', ignore_errors=True)
shutil.copytree('../emoji', DUNGEONS_ROOT + 'mods/emoji')
process = subprocess.Popen([DUNGEONS_ROOT + 'diceydungeons.exe',
                            'mod=emoji', '-translator'],
                           stdout=subprocess.PIPE)

for line in process.stdout:
    print(line.decode(), end='')
