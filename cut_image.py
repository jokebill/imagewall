#!/usr/bin/env python
from scipy import misc
import numpy as np

def cut_image(imgfile, center=(0,0), rate=(4,3),cut=1.0):
    img=misc.imread(imgfile)
    h,w = img.shape[:2]
    imgsize = np.array( (w,h), dtype=float)
    offset = np.array(center,dtype=float) * imgsize
    ratio = float(rate[0])/float(rate[1])
    imgsize1 = imgsize/2.0 - np.abs(offset)
    ratio1 = imgsize1[0]/imgsize1[1]
    if ratio1>=ratio:
        imgsize1[0]=imgsize1[1]*ratio
    else:
        imgsize1[1]=imgsize1[0]/ratio
    imgsize_c = imgsize1 * cut

    #flip y axis
    offset[1]=-offset[1]
    new_center = imgsize/2.0 + offset
    x0,y0 = np.asarray(new_center - imgsize_c,dtype=int)
    x1,y1 = np.asarray(new_center + imgsize_c, dtype=int)

    img_new = img[y0:y1,x0:x1,:]
    return img_new

def split_image(options,imgfile):
    center=[ float(val) for val in options.center.split(',')[:2]]
    rate=[ float(val) for val in options.ratio.split(':')[:2] ]
    cut=options.zoom
    slices=[ int(val) for val in options.slices.split('x')[:2] ]
    boarder=[ float(val) for val in options.boarder.split(',')[:2] ]

    img=cut_image(imgfile, center, rate, cut)
    h,w = img.shape[:2]
    w_set = np.asarray(np.linspace(0, w, slices[0]+1), dtype=float)
    h_set = np.asarray(np.linspace(0, h, slices[1]+1), dtype=float)
    imgs = []
    for j in range(slices[0]):
        w0 = w_set[j]
        w1 = w_set[j+1]
        ws0 = int(w0 + (w1-w0)*boarder[0])
        ws1 = int(w1 - (w1-w0)*boarder[0])
        #if j>0:
            #ws0 = int(w0 + (w1-w0)*boarder[0])
        #else:
            #ws0 = int(w0)
        #if j<slices[0]-1:
            #ws1 = int(w1 - (w1-w0)*boarder[0])
        #else:
            #ws1 = int(w1)
        for i in range(slices[1]):
            h0 = h_set[i]
            h1 = h_set[i+1]
            hs0=int(h0+(h1-h0)*boarder[1])
            hs1=int(h1-(h1-h0)*boarder[1])
            #if i>0:
                #hs0=int(h0+(h1-h0)*boarder[1])
            #else:
                #hs0=int(h0)
            #if i<slices[1]-1:
                #hs1=int(h1-(h1-h0)*boarder[1])
            #else:
                #hs1=int(h1)
            print ws0,ws1,hs0,hs1
            imgs.append(img[hs0:hs1,ws0:ws1,:])

    from os.path import splitext,join,basename
    from scipy.misc import imsave
    filepath,ext = splitext(imgfile)
    filename = basename(filepath)
    if options.output:
        basepath = join(options.output,filename)
    else:
        basepath = filepath


    if options.resolution:
        new_size = [ int(val) for val in options.resolution.split(',')[:2] ]

    import Image
    for i,img in enumerate(imgs):
        f = "{}_{:03}{}".format(basepath,i+1,ext)
        print f
        imsave(f,img)
        im = Image.open(f)
        im=im.resize(new_size, Image.BILINEAR)
        im.save(f)

if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c","--center",
            metavar="X,Y",
            type=str,
            default="0,0",
            help="Center offset in percentage")
    parser.add_option("-r","--ratio",
            metavar="X:Y",
            type=str,
            default="5:2",
            help="Image ratio")
    parser.add_option("-z","--zoom",
            metavar="RATE",
            type=float,
            default=1.0,
            help="Zoom rate")
    parser.add_option("-s","--slices",
            metavar="NxM",
            type=str,
            default="5x3",
            help="Number of slices in row, column")
    parser.add_option("-b","--boarder",
            metavar="PX,PY",
            type=str,
            default="0.05,0.05",
            help="Boarder width in percentage")
    parser.add_option("-o","--output",
                metavar="DIR",
                type=str,
                default=None,
                help="Output folder"
                )
    parser.add_option("--resolution",
                metavar="pX,pY",
                type=str,
                default=None,
                help="Slice resolution")
    options, args = parser.parse_args()
    split_image(options,args[0])

