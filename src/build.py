import csv
import shutil
import os

import translate
from translate import DUNGEONS_ROOT

print('Writing translations...')
shutil.rmtree('../emoji', ignore_errors=True)
os.mkdir('../emoji')

shutil.copyfile('_polymod_meta.json',
                '../emoji/_polymod_meta.json')
shutil.copyfile('README.txt', '../emoji/README.txt')
shutil.copyfile('../LICENSE.txt', '../emoji/LICENSE.txt')
shutil.copyfile('translate.py', '../emoji/translate.py')
translate_data = '../emoji/translate_data/'
shutil.copytree('translate_data', translate_data)

en = '../emoji/data/text/locale/en/'
os.makedirs(en)
text_folder = DUNGEONS_ROOT + 'data/text/'

with open(en + 'fighters.csv', 'w', newline='') as destfile:
    writer = csv.writer(destfile)
    with open('translate_data/fighters.csv', 'r', newline='') as srcfile:
        reader = csv.reader(srcfile)
        # Skip the header
        writer.writerow(next(reader))
        for row in reader:
            row[2] = translate.parse(row[2], True)
            writer.writerow(row)

with open(translate_data + 'template-strings.csv', 'w', newline='') as destfile:
    writer = csv.writer(destfile)
    with open('translate_data/strings.csv', 'r', newline='') as srcfile:
        reader = csv.reader(srcfile)
        writer.writerow(next(reader))
        for row in reader:
            row[2] = translate.parse(row[2], True)
            writer.writerow(row)
    translate.add_statuses(text_folder + 'statuseffects.csv', writer)
    translate.add_remixes(text_folder + 'remix.csv', writer)

with open(translate_data + 'template-equipment.csv', 'w', newline='') as destfile:
    writer = csv.writer(destfile)
    writer.writerow(['Changed?', 'Name', 'Description',
                     'Name_en', 'Description_en', ''])
    translate.add_equipment(text_folder + 'equipment.csv', writer)
    for item in ['Judgement', 'Precious Egg', 'Rotten Egg', 'Transformer',
                 'Uptick']:
        writer.writerow(['', item, '(special)',
                         translate.item_names[item], '(special)', ''])
    fk = ('After the battle[comma] '
          'keep[newline]one piece of equipment')
    fk_activated = ('After the battle[comma] keep[newline]'
                    'one piece of equipment[newline][gray](activated)')
    writer.writerow(['', '(generic)', fk,
                     '(generic)', translate.translate(fk), ''])
    writer.writerow(['', '(generic)', fk_activated,
                     '(generic)', translate.translate(fk_activated), ''])

with open(translate_data + 'template-skills.csv', 'w', newline='') as destfile:
    writer = csv.writer(destfile)
    writer.writerow(['Changed?', 'Name', 'Description',
                     'Name_en', 'Description_en', ''])
    translate.add_skills(text_folder + 'skills.csv', writer)

translate.add_mods('../emoji/',
                 ['halloweenspecial', 'frogurt', 'plasticshield'],
                 DUNGEONS_ROOT + 'mods/',
                 True)

graphics = '../emoji/data/graphics/'
os.makedirs(graphics + 'ui/limit_break')
shutil.copyfile('other_graphics/limit_break/merged.atf',
                graphics + 'ui/limit_break/pack_1080.atf')
os.makedirs(graphics + 'ui/win_combat')
shutil.copyfile('other_graphics/win_combat/merged.atf',
                graphics + 'ui/win_combat/pack_1080.atf')
os.makedirs(graphics + 'titlescreen/new')
shutil.copyfile('other_graphics/titlescreen/merged.atf',
                graphics + 'titlescreen/new/dice_1080.atf')
fight = '../emoji/data/animations/fight_transition/'
os.makedirs(fight)
shutil.copyfile('other_graphics/fight_transition/merged.atf',
                fight + 'pack_1080.atf')
append_text = '../emoji/_append/data/text/'
os.makedirs(append_text)

with open(append_text + 'symbols.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name','Value','Colour','Type'])
    print('Setting up emojis...')
    for emoji in translate.emojis:
        writer.writerow([emoji, emoji, '0x000000', 'IMAGE'])
        shutil.copyfile(f'png/{emoji}.png', graphics + f'{emoji}.png')
    with open(DUNGEONS_ROOT + 'data/text/symbols.csv',
              newline='') as symbols:
        reader = csv.reader(symbols)
        for row in reader:
            if row[0] in translate.bordered_symbols:
                symbol = row[0] + '-border'
                writer.writerow([symbol, symbol, '0x000000', 'IMAGE'])
                shutil.copyfile(f'symbols/symbol-{row[1]}.png',
                                graphics + f'{symbol}.png')
