dynmap-assemble
===============

Assembles one great map from many tiles, produces by DynMap, MC Bukkit map plugin

###Dependencies###

* PIL
* shutil

###Usage###

1. Put script into `%SERVER_FOLDER%\plugins\dynmap\web\tiles\%WORLD_NAME%` folder.
2. Launch it
3. Say him, what folder contains map tiles, eg. `flat`
4. Enjoy. Map image filename will be `%FOLDER%.png` and map will be in the same folder with the script, eg. `%SERVER_FOLDER%\plugins\dynmap\web\tiles\%WORLD_NAME%\flat.png`

###TODO###

* move to Pillow to correctly operate with alpha channel
* include junk self-clean

###NB!###

Do not forget to manually remove `temp` folder from chosen folder with tiles, eg. `flat\temp`