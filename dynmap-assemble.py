from __future__ import print_function

# magic that makes input work as raw_input in both py2 and py3
try:
    input = raw_input
except NameError:
    pass

from PIL import Image
from collections import OrderedDict
import os
import argparse

SIZE_SAME_AS_ORIGIN = -1

try:
    from tqdm import tqdm
    tqdm_imported = True
except ImportError:
    tqdm_imported = False
    print('You should consider installing tqdm for nice progress bar;)')

bgcolors = OrderedDict()
bgcolors['transparent'] =                   {'rgb': None,               'description': ''}
bgcolors['overworld'] =                     {'rgb': (0x64, 0x95, 0xED), 'description': 'light blue'}
bgcolors['nether'] =                        {'rgb': (0x30, 0x08, 0x06), 'description': 'dark red'}
bgcolors['the_end'] =                       {'rgb': (0x11, 0x0D, 0x18), 'description': 'dark violet'}
bgcolors['black'] =                         {'rgb': (0x00, 0x00, 0x00), 'description': ''}
bgcolors['white'] =                         {'rgb': (0xFF, 0xFF, 0xFF), 'description': ''}

world_excludes = ['.git', '_markers_', 'faces']
cwd = os.getcwd()


parser = argparse.ArgumentParser(description='DynMap map assembler', epilog='More info at https://github.com/xtotdam/dynmap-assemble/')

parser.add_argument('-i', '--interactive', action='store_true', help='Use interactive mode. Helps determine arguments')

parser.add_argument('-w', '--world',    type=str, help='Server world to create map for. This is directory in <server>/dynmap/web/tiles. Default is \'world\'')
parser.add_argument('-m', '--map',      type=str, help='Map defined in dynmap config. This is directory in <server>/dynmap/web/tiles/<world>. Default is \'t\'')
parser.add_argument('-b', '--bgcolor',  type=str, help='Background color. Choose one of the following ' + str(list(bgcolors.keys())) + 'or use hex form (#6495ed)')
parser.add_argument('-r', '--resize',   type=int, help='Size in px to which each tile will be resized')

args = parser.parse_args()

# user choices

if not args.interactive:
    # TODO check input
    world = args.world
    mapp = args.map

    bg_key = args.bgcolor
    if bg_key in bgcolors.keys():
        bgcolor = bgcolors[args.bgcolor]['rgb']
    elif bg_key.startswith('#') and len(bg_key) == 7:
        bgcolor = tuple(int(x, 16) for x in (bg_key[1:3], bg_key[3:5], bg_key[5:7]))
    else:
        print('Unknown background color')
        exit()
    
    if args.resize is not None:
        if args.resize < -2 or args.resize = 0: # validate input
            print('Invalid value for option --resize. Valid values: -1 for original size or positive integer for required size.')
            exit()
        newside = args.resize
    else:
        newside = SIZE_SAME_AS_ORIGIN

else:
    def user_choice(iterable, name, do_sort=True):
        if do_sort:
            iterable.sort()

        print('Choose {} (enter number)'.format(name))
        for i, w in enumerate(iterable):
            print('  {:2d}:  {}'.format(i+1, w))

        choice = input('> ')
        choice = int(choice) - 1
        return iterable[choice]


    worlds = [w for w in os.listdir(cwd) if os.path.isdir(w) and w not in world_excludes]
    world = user_choice(worlds, 'world')

    maps = [m for m in os.listdir(cwd + os.sep + world) if os.path.isdir(world + os.sep + m)]
    mapp = user_choice(maps, 'map')

    bgs = ['{} ({})'.format(key, bgcolors[key]['description']) for key in bgcolors.keys()]
    bg_key = user_choice(bgs, 'background color', do_sort=False)
    bgcolor = bgcolors[bg_key.split()[0]]['rgb']


place = cwd + os.sep + world + os.sep + mapp

print('Assembling map \'{}\' of world \'{}\' located at \'{}\' using \'{}\' as background color'.format(mapp, world, place, bg_key))

# collecting locations
print('Collecting tile locations...')
alltiles = list()
tilefolders = [tf for tf in os.listdir(place) if os.path.isdir(place + os.sep + tf)]
for tf in tilefolders:
    tiles = [t for t in os.listdir(place + os.sep + tf) if not t.startswith('z')]
    for t in tiles:
        if t == '.DS_Store':
            continue

        hv = t.split('.')[0]
        h, v = map(int, hv.split('_'))
        alltiles.append({
            'loc': place + os.sep + tf + os.sep + t,
            'h': h,
            'v': v
            })

# determine sizes
hs = [v['h'] for v in alltiles]
vs = [v['v'] for v in alltiles]
hstart, hend = min(hs),max(hs)
vstart, vend = min(vs),max(vs)
hsize = hend - hstart + 1
vsize = vend - vstart + 1

side = Image.open(alltiles[0]['loc']).size
if side[0] == side[1]:
    side = side[0]
else:
    print('It\'s supposed, tiles are square, not', side)
    exit()

# info output
print('[ {} : {} ]x[ {} : {} ]-> HxV: {}x{}; side size {}; final size {}x{} px'.format(
    hstart, hend, vstart, vend, hsize, vsize, side, side*hsize, side*vsize))

# ask, if reduce?
if args.interactive:
    print('Should we reduce final image? {}px per tile -> x (y/n)'.format(side))
    doreduce = input('> ')
    doreduce = (len(doreduce) > 0 and doreduce.strip()[0] in 'yY1')

    if doreduce:
        print('Enter new tile size in px')
        newside = int(input('> ').strip())
    else:
        newside = side

else:
    doreduce = (newside != side and newside != SIZE_SAME_AS_ORIGIN)

if doreduce:
    print('Reducing: {}->{} => final size {}x{} px'.format(side, newside, newside*hsize, newside*vsize))


# assemble big image
print('Assembling final image...')
canvas_side = side if newside == SIZE_SAME_AS_ORIGIN else newside
res = Image.new('RGBA', (canvas_side*hsize, canvas_side*vsize))

if tqdm_imported:
    alltiles = tqdm(alltiles)
else:
    print('Processing tiles...')

for tile in alltiles:
    src = Image.open(tile['loc'])
    if doreduce:
        src = src.resize((newside, newside), Image.BICUBIC)
    h, v = tile['h'], tile['v']
    res.paste(src,
        (
            (h - hstart) * canvas_side,
            -(v - vstart - vsize + 1) * canvas_side
        ))

# applying background
if bgcolor is not None:
    print('Applying background...')
    background = Image.new('RGBA', (canvas_side*hsize, canvas_side*vsize), bgcolor)
    res = Image.alpha_composite(background, res)

# saving
print('Saving...')
fn = cwd + os.sep + world + '_' + mapp + '.png'
res.save(fn, 'PNG')
print('Final image saved under \'{}\''.format(fn))
