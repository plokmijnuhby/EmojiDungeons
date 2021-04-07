# EmojiDungeons
A mod designed to add emojis to Dicey Dungeons!
To run this mod, download the files, move the "emoji" folder into your mods folder, and follow the instructions in the readme inside.

## Building the mod
To make the files, go to the src folder. You may first need to adjust DUNGEONS_ROOT in the translate.py file. The emojis here are drawn from Twemoji, and can be found at https://github.com/twitter/twemoji, in the assets/svg folder. To build the necessary pngs, make sure ImageMagick is installed and run graphics.py. The files in other_graphics are related to the base game, and can be adjusted using diceymodgeons (https://github.com/TerryCavanagh/diceymodgeons). After this, run build.py to get a development build of the mod in the emoji folder, with one file for each emoji. When the build works, run pack.tpproj using GDX Texture Packer. Then run convert_atlas.py to replace the emoji files with packed textures.
