To use EmojiDungeons, move the root file into the game's mod folder, then launch
the mod from the command line by navigating to the correct directory and typing
"diceydungeons mod=emoji". Do not launch the mod using the in-game mod menu -
if you do this, the emojis will not display correctly, due to technical reasons.

Dicey Dungeons is not really designed to display emojis, and as such I have had
to make some compromises to get it to work. For one thing, for cards that change
the numbers in their text, these numbers cannot be translated.
More problematically, the inventory menu and upgrade menu do not work correctly
- although they are still very much usable, they aren't quite right.

I have not translated everything in Dicey Dungeons - only the things I consider
important. Cutscenes, for instance, are not translated.

EmojiDungeons is compatible with other base game mods - you can type, for example,
"diceydungeons mod=emoji,halloweenspecial" to load it with the halloween special mod.

If you load the mod with mods not from the base game, it will work but the other
mods may not be entirely translated. A python script is included in the files to
fix this (or at least try to). To run it, first of all check that EmojiDungeons
and the mods you want to run are in the game's mod folder, and make sure python
is installed on your computer. Then open your file explorer, navigate to the
EmojiDungeons root file and double click the script to run it. Alternatively,
open the command line, go to the same folder and type "python -m translate". After
that, running the game with the other mods should be at least slightly better.
The script can translate about 50% of equipment descriptions, although your
mileage may vary, and it is less good with other things a mod might contain.

This version of EmojiDungeons is designed for Dicey Dungeons v1.11. I have not
tested other versions of the game - if you want to play this mod with them, who
knows, they might work.

The emojis in this mod are mostly from Twemoji, although some are drawn from the
base game. Some of them are rendered with a half-transparent black border, which
makes them stand out a little bit better in some cases. The title screen (and a
few other places) required a bit more editing.

More code related to this mod can be found on github, at
https://github.com/plokmijnuhby/EmojiDungeons.