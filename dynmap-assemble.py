from __future__ import print_function

# magic that makes input work as raw_input in both py2 and py3
try:
    input = raw_input
except NameError:
    pass

from PIL import Image
from collections import OrderedDict
import os

try:
    from tqdm import tqdm
    tqdm_imported = True
except ImportError:
    tqdm_imported = False
    print('You should consider installing tqdm for nice progress bar;)')

bgcolors = OrderedDict()
bgcolors['transparent'] =                   None
bgcolors['overworld (lightblue)'] =         (0x64, 0x95, 0xED)
bgcolors['nether (somewhat dark red)'] =    (0x30, 0x08, 0x06)
bgcolors['the_end (somewhat violet)'] =     (0x11, 0x0D, 0x18)
bgcolors['black'] =                         (0x00, 0x00, 0x00)
bgcolors['white'] =                         (0xFF, 0xFF, 0xFF)

world_excludes = ['.git', '_markers_', 'faces']
cwd = os.getcwd()

# user choices
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

place = cwd + os.sep + world + os.sep + mapp

bgs = tuple(bgcolors.keys())
bg_key = user_choice(bgs, 'background color', do_sort=False)
bgcolor = bgcolors[bg_key]

print('Assembling map \'{}\' of world \'{}\' located at \'{}\' using \'{}\' as background color'.format(mapp, world, place, bg_key))

# collecting locations
print('Collecting tile locations...')
alltiles = list()
tilefolders = [tf for tf in os.listdir(place) if os.path.isdir(place + os.sep + tf)]
for tf in tilefolders:
    tiles = [t for t in os.listdir(place + os.sep + tf) if not t.startswith('z')]
    for t in tiles:
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
print('Should we reduce final image? {}px per tile -> x (y/n)'.format(side))
doreduce = input('> ')
if len(doreduce) > 0 and doreduce.strip()[0] in 'yY1':
    doreduce = True
    print('Enter new tile size in px')
    newside = int(input('> ').strip())
else:
    doreduce = False

if doreduce:
    print('Reducing: {}->{} => final size {}x{} px'.format(side, newside, newside*hsize, newside*vsize))
else:
    newside = side

# assemble big image
print('Assembling final image...')
res = Image.new('RGBA', (newside*hsize, newside*vsize))


if tqdm_imported:
    alltiles = tqdm(alltiles)
else:
    print('Processing tiles')

for tile in alltiles:
    src = Image.open(tile['loc'])
    if doreduce:
        src = src.resize((newside, newside), Image.BICUBIC)
    h, v = tile['h'], tile['v']
    res.paste(src,
        (
            (h - hstart) * newside,
            -(v - vstart - vsize + 1) * newside
        ))

# applying background
if bgcolor is not None:
    print('Applying background...')
    background = Image.new('RGBA', (newside*hsize, newside*vsize), bgcolor)
    res = Image.alpha_composite(background, res)

# saving
print('Saving...')
fn = cwd + os.sep + world + '_' + mapp + '.png'
res.save(fn, 'PNG')
print('Final image saved under \'{}\''.format(fn))
