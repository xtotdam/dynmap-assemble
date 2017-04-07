from PIL import Image
from collections import OrderedDict
import os

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
worlds = [w for w in os.listdir(cwd) if os.path.isdir(w) and w not in world_excludes]
worlds.sort()

print 'Choose world (enter number)'
for i, w in enumerate(worlds):
    print '  {:2d}:  {}'.format(i+1, w)

choice = raw_input('> ')
choice = int(choice) - 1
world = worlds[choice]

maps = [m for m in os.listdir(cwd + os.sep + world) if os.path.isdir(world + os.sep + m)]
maps.sort()

print 'Choose map (enter number)'
for i, m in enumerate(maps):
    print '  {:2d}:  {}'.format(i+1, m)

choice = raw_input('> ')
choice = int(choice) - 1
mapp = maps[choice]

place = cwd + os.sep + world + os.sep + mapp

bgs = bgcolors.keys()
print 'Choose background color (enter number)'
for i, bg in enumerate(bgs):
    print '  {:2d}:  {}'.format(i, bg)

choice = raw_input('> ')
choice = int(choice)
bgcolor = bgcolors[bgs[choice]]

print 'Assembling map \'{}\' of world \'{}\' located at \'{}\' using \'{}\' as background color'.format(mapp, world, place, bgs[choice])

# collecting locations
print 'Collecting tile locations...'
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
    print 'It\'s supposed, tiles are square, not', side
    exit()

# info output
print '[ {} : {} ]x[ {} : {} ]-> HxV: {}x{}; side size {}; final size {}x{} px'.format(
    hstart, hend, vstart, vend, hsize, vsize, side, side*hsize, side*vsize)

# ask, if reduce?
print 'Should we reduce final image? {}px per tile -> x (y/n)'.format(side)
doreduce = raw_input('> ')
if len(doreduce) > 0 and doreduce.strip()[0] in 'yY1':
    doreduce = True
    print 'Enter new tile size in px'
    newside = int(raw_input('> ').strip())
else:
    doreduce = False

if doreduce:
    print 'Reducing: {}->{} => final size {}x{} px'.format(side, newside, newside*hsize, newside*vsize)
else:
    newside = side

# assemble big image
print 'Assembling final image...'
res = Image.new('RGBA', (newside*hsize, newside*vsize))

for i, tile in enumerate(alltiles):
    src = Image.open(tile['loc'])
    if doreduce:
        src = src.resize((newside, newside), Image.BICUBIC)
    h, v = tile['h'], tile['v']
    res.paste(src,
        (
            (h - hstart) * newside,
            -(v - vstart - vsize + 1) * newside
        ))
    print '\rProcessing tile # {} of {}...'.format(i+1, len(alltiles)),

print # needed after '\r'

# applying background
if bgcolor is not None:
    print 'Applying background...'
    background = Image.new('RGBA', (newside*hsize, newside*vsize), bgcolor)
    res = Image.alpha_composite(background, res)

# saving
print 'Saving...'
fn = cwd + os.sep + world + '_' + mapp + '.png'
res.save(fn, 'PNG')
print 'Final image saved under \'{}\''.format(fn)
