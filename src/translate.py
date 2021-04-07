import csv
import re
import os.path
import shutil

DUNGEONS_ROOT = 'C:/Program Files (x86)/Steam/steamapps/common/Dicey Dungeons/'
emojis = set()
bordered_symbols = set()

def parse_emoji(emoji):
    # The '[2:]' removes the '0x' prefix
    return hex(ord(emoji))[2:]


def parse(string, bordered=False):
    result = ''
    code = None
    i = 0
    if len(string) and string[0] == '!':
        bordered = not bordered
        i = 1
    
    while i < len(string):
        char = string[i]
        # ZWJ, joins two emojis into one
        if char == '\u200D':
            i += 1
            if string[i] in ['\u2620','\u2640','\u2642', '\u2696']:
                code += '-200d-' + parse_emoji(string[i]) + '-fe0f'
            else:
                code += '-200d-' + parse_emoji(string[i])
            i += 1
            continue
        # FE0F is an invisible character that comes up in lots of emojis.
        # It isn't included in the filenames of the images,
        # except when it sometimes is for reasons I cannot fathom.
        elif char == '\uFE0F':
            i += 1
            continue

        if code is not None:
            if bordered:
                code += '-border'
            emojis.add(code)
            result += '[' + code + ']'
            code = None
        
        # Special FE0F workaround just for weightlifter
        if char == '\U0001F3CB':
            code = '1f3cb-fe0f'
        # Flags
        elif '\U0001F1E6' <= char <= '\U0001F1FF':
            i += 1
            code = parse_emoji(char) + '-' + parse_emoji(string[i])
        # check whether it is a non-ascii character
        elif char > '~':
            code = parse_emoji(char)
        elif '0' <= char <= '9' or char == '#':
            code = parse_emoji(char) + '-20e3'
        elif char in ['@', '|']:
            result += char
            code = None
        else:
            for group in (('[',']',bordered),
                          ('<','>',False),
                          ('{','}',False),
                          ('%','%',False)):
                if string[i] != group[0]:
                    continue
                start_i = i
                i += 1
                while string[i] != group[1]:
                    i += 1
                code = string[start_i+1:i]
                if group[2] and code:
                    if code[0] == '!':
                        code = code[1:]
                    else:
                        bordered_symbols.add(code)
                        code += '-border'
                result += group[0] + code + group[1]
                code = None
                break
            else:
                raise ValueError(f'Could not parse {string!r}')
        i += 1
    if code is not None:
        if bordered:
            code += '-border'
        emojis.add(code)
        result += '[' + code + ']'
    return result


def makedict(path, do_parse=True):
    result = {}
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        # skip the header
        next(reader)
        for row in reader:
            if do_parse:
                result[row[0]] = parse(row[1], True)
            else:
                result[row[0]] = row[1]
    return result


regexes = makedict('translate_data/regexes.csv', False)
replacements = makedict('translate_data/replacements.csv', False)
item_names = makedict('translate_data/equipment.csv')
skill_names = makedict('translate_data/skills.csv')
status_names = makedict('translate_data/statuseffects.csv')


def translate(text, maxrows=0, debug=False):
    oldtext = text
    if text in replacements:
        text = replacements[text]
    else:
        # Just trying to get all the '|'s in the right places
        text = re.sub(r'\|(?!\()', r' ', text)
        text = re.sub(r'\|\((.*)\)', r'|\1', text)
        text = re.sub(r'\[comma\]', r'[;]', text)
        text = re.sub(r'([^.])\.[ |]', r'\1|', text)
        text = re.sub(r'([^.])\.$', r'\1', text)
        
        # In reusable cards, the game deletes the last line;
        # this is fixed elsewhere.
        text = text.replace('[gray](Reuseable)', '|')

        # We try to place newlines before a capital letter,
        # this is a good way of spotting natural sentence breaks.
        # Percentage chances work too.
        text = re.sub(r'(?<!^)(?<!\|)(?<![Ii]nflict )(?<!is )'
                      '(?!\[fury\]Fury)(?!\[\w+\]ALL)'
                      r'(\[\w+\][A-Z])', r'|\1', text)
        text = re.sub(r'(?<=[^|A-Z\]\d])(?<![|:] )'
                      # These words sometimes contain capitals,
                      # even in the middle of a sentence.
                      r'(?!Jackpot)(?!CPU)(?!Jinx)([A-Z]|\d+% chance)',
                      r'|\1', text)
        text = re.sub(r'\[;\]( ?\|)?', r'|', text)
    text = text.lower()
    for pattern, replacement in regexes.items():
        text = re.sub(pattern, replacement, text)
        if debug:
            print(f'{pattern=}, {replacement=}')
            print(f'{text=}\n')
    if maxrows != 0 and text.count('|') >= maxrows:
        raise ValueError(f'Could not translate {oldtext!r}, got {text!r}.')
    try:
        text = parse(text)
    except Exception as e:
        raise ValueError(f'Could not translate {oldtext!r}.') from e
    return text


def add_statuses(path, writer, strict=True):
    with open(path, newline='') as statuses:
        reader = csv.reader(statuses)
        next(reader)
        for row in reader:
            name = row[1]
            if name in status_names:
                translation = status_names[name]
            elif name[-1] == '?' and name[:-1] in status_names:
                translation = status_names[name[:-1]] + '[2753-border]'
            elif strict:
                raise ValueError(f'Could not translate {name!r}.')
            else:
                continue
            
            writer.writerow(['', name, translation,
                             'Status Effect', '', ''])
            try:
                writer.writerow(['', row[3], translate(row[3]),
                                 'Status Effect', f'Tooltip for {name}', ''])
            except ValueError as e:
                if strict:
                    raise e


def add_remixes(path, writer, strict=True):
    with open(path, newline='') as remixes:
        reader = csv.reader(remixes)
        next(reader)
        for row in reader:
            try:
                writer.writerow(['', row[1], translate(row[1]),
                                 'Remix screen', 'Remixed rule', ''])
            except ValueError as e:
                if strict:
                    raise e


def add_equipment(path, writer, strict=True):
    with open(path, newline='') as srcfile:
        reader = csv.reader(srcfile)
        next(reader)
        for row in reader:
            name = row[0]
            description = row[1]
            # Do we have enough room on the card?
            # Even though we could sometimes fit in more than three rows,
            # if we need more than three something has probably gone wrong
            if row[2] == '1':
                if re.search('REQUIRE\d|DOUBLES', row[5]):
                    maxrows = 2
                elif row[5] != 'COUNTDOWN' and row[6] != '':
                    maxrows = 2
                else:
                    maxrows = 3
            else:
                maxrows = 3
            if '_' not in name:
                if strict:
                    newname = item_names[name]
                else:
                    newname = item_names.get(name, name)
                try:
                    writer.writerow(['', name, description, newname,
                                     translate(description, maxrows),
                                     ''])
                except ValueError as e:
                    if strict:
                        raise e
                text = description
            # We don't want to repeat ourselves
            elif description != text:
                try:
                    writer.writerow(['', name, description, name,
                                     translate(description, maxrows),
                                     ''])
                except ValueError as e:
                    if strict:
                        raise e


def add_skills(path, writer, strict=True):
    with open(path, newline='') as srcfile:
        reader = csv.reader(srcfile)
        next(reader)
        for row in reader:
            name = row[0]
            description = row[1]
            if strict:
                newname = skill_names[name]
            else:
                newname = skill_names.get(name, name)
            try:
                writer.writerow(['', name, description, newname,
                                 translate(description, 1), ''])
            except ValueError as e:
                if strict:
                    raise e


def find_files(mods, mods_folder, name):
    files = []
    for mod in mods:
        files += [mods_folder + f'{mod}/data/text/{name}.csv',
                  mods_folder + f'{mod}/_append/data/text/{name}.csv',
                  mods_folder + f'{mod}/_merge/data/text/{name}.csv']
    return [file for file in files if os.path.exists(file)]


def add_mods(output_folder, mods, mods_folder, template_mode):
    if 'emoji' in mods:
        mods.remove('emoji')
    en = output_folder + 'data/text/locale/en/'
    translate_data = output_folder + 'translate_data/'
    shutil.copyfile(translate_data + 'template-strings.csv', en + 'strings.csv')
    shutil.copyfile(translate_data + 'template-equipment.csv',
                    en + 'equipment.csv')
    shutil.copyfile(translate_data + 'template-skills.csv', en + 'skills.csv')
    with open(en + 'strings.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for file in find_files(mods, mods_folder, 'statuseffects'):
            add_statuses(file, writer, template_mode)
        for file in find_files(mods, mods_folder, 'remix'):
            add_remixes(file, writer, template_mode)

    with open(en + 'equipment.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for file in find_files(mods, mods_folder, 'equipment'):
            add_equipment(file, writer, template_mode)

    with open(en + 'skills.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for file in find_files(mods, mods_folder, 'skills'):
            add_skills(file, writer, template_mode)
    

if __name__ == '__main__':
    add_mods('./', os.listdir('..'), '../', False)
