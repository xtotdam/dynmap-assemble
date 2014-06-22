import Image, os, shutil
side = 128
bgcolor = (0x64,0x95,0xED)
folder = raw_input('Enter name of directory with tiles: ')
os.chdir(folder)
print 'Current working dir: ',os.getcwd()
print 'BgColor: ',bgcolor

# recursively go through folders, delete all junk, move non-junk to root/temp directory
print 'Create temporary directory'
try:
    os.mkdir('temp')
except WindowsError:
    print '   OK, it is already there'
    pass

names = os.listdir(os.getcwd())
for name in names:
    if name[-1:].isdigit():
        print 'Processing tiles folder ',name
        files = os.listdir(os.getcwd()+'/'+name)
        for f in files:
            if f[0]!='z':
                shutil.copyfile(os.getcwd()+'/'+name+'/'+f, os.getcwd()+'/temp/'+f)

# a tribute to Windows
try:
    os.remove(os.getcwd()+'/temp/Thumbs.db')
    print 'Removed Thumbs.db'
except WindowsError: 
    pass

# reveal map array borders
os.chdir('temp')
names = os.listdir(os.getcwd())
hor,ver = [],[]
for name in names:
    hor.append(int(name.split('_')[0]))
    ver.append(int(name.split('_')[1].split('.')[0]))
hstart, hend = min(hor),max(hor)
vstart, vend = min(ver),max(ver)
hsize = hend-hstart+1
vsize = vend-vstart+1

# size of tile + is it square?
side = Image.open(str(hor[0])+'_'+str(ver[0])+'.png').size
if side[0]==side[1]:
    side=side[0]
else:
    print 'It\'s supposed, tiles are square'
    exit()
print 'Images read.\n[ {0} : {1} ]x[ {2} : {3} ]-> H, V: {4}x{5}; size {6}'.format(hstart,hend,vstart,vend,hsize,vsize,side)

# assemble big image
res = Image.new('RGBA',(side*hsize,side*vsize),bgcolor)
for i in range(hsize):
    for j in range(vsize):
        name = '{0:d}_{1:d}.png'.format((hstart + i),(vstart+j))
        try:
            src=Image.open(name)
        except IOError:
            src=Image.new('RGB',(side,side),bgcolor)
#TODO   switch to pillow to evade transparency problems
        res.paste(src,(i*side,(vsize-1-j)*side))
    print i+1,' of ',hsize
        
# save final image
os.chdir('../..')
print 'Pasted it all. Saving to {0}\{1}.png'.format(os.getcwd(), folder)
res.save(folder+'.png','PNG')
print 'Saved final image'
print 'Do not forget to remove temporary folder!  /'+folder+'/temp'