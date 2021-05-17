dynmap-assemble
===============

Assembles one great map from many tiles, produces by DynMap, MC Bukkit map plugin/MC Forge mod

### Dependencies ###

* pillow (PIL)
* tqdm (optional)

### Usage ###

1. Put script into `%SERVER_FOLDER%\plugins\dynmap\web\tiles\` folder
2. Launch it (with arguments or in interactive mode)
3. Enjoy!

```
usage: dynmap-assemble.py [-h] [-i] [-w WORLD] [-m MAP] [-b BGCOLOR] [-r RESIZE]

DynMap map assembler

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Use interactive mode. Helps determine arguments
  -w WORLD, --world WORLD
                        Server world to create map for. This is directory in <server>/dynmap/web/tiles. Default is
                        'world'
  -m MAP, --map MAP     Map defined in dynmap config. This is directory in <server>/dynmap/web/tiles/<world>. Default
                        is 't'
  -b BGCOLOR, --bgcolor BGCOLOR
                        Background color. Choose one of the following ['transparent', 'overworld', 'nether',
                        'the_end', 'black', 'white'] or use hex form (#6495ed)
  -r RESIZE, --resize RESIZE
                        Size in px to which each tile will be resized
```

#### BG Colors cheatsheet ####

- `overworld`
- `nether`
- `the_end` (this one isn't black, just very dark violet)

![palette](https://user-images.githubusercontent.com/5108025/118475069-78de5e00-b714-11eb-9870-21e939c971e3.png)

### Example ###

![world_t](https://user-images.githubusercontent.com/5108025/80891706-71e1da80-8cce-11ea-84f8-38c1ff8310d6.png)

shrinked 10x (original one is way too big)
![minified example image here](https://cloud.githubusercontent.com/assets/5108025/23752237/884058de-04e5-11e7-92f6-ba12cdc4dbd3.png)
