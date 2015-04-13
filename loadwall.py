#!/usr/bin/env python
import os,sys
import cut_image
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
        default="16:9",
        help="Image ratio")
parser.add_option("-z","--zoom",
        metavar="RATE",
        type=float,
        default=1.0,
        help="Zoom rate")
parser.add_option("-s","--slices",
        metavar="NxM",
        type=str,
        default="4x3",
        help="Number of slices in row, column")
parser.add_option("-b","--boarder",
        metavar="PX,PY",
        type=str,
        default="0.04,0.08",
        help="Boarder width in percentage")
parser.add_option("-o","--output",
        metavar="DIR",
        type=str,
        default="./output",
        help="Output folder"
        )
parser.add_option("--resolution",
        metavar="pX,pY",
        type=str,
        default="1600,1200",
        help="Slice resolution")
parser.add_option("--slaves",
        metavar="FILE",
        type=str,
        default="slaves",
        help="A file with all slaves' hostnames/ips")
parser.add_option("--remote",
        metavar="PATH",
        type=str,
        default="~/wallpapers/wallpaper01.jpg",
        help="File path and name for the remote picture tile"
        )

options, args = parser.parse_args()
outdir = options.output
imgfile = args[0]

# clear output dir
import shutil
if os.path.exists(outdir):
    shutil.rmtree(outdir)
os.makedirs(outdir)
cut_image.split_image(options, imgfile)

slaves=list()
if os.path.exists(options.slaves):
    with open(options.slaves) as f:
        for line in f:
            lstr=line.strip()
            if lstr[0]<>"#":
                slaves.append(line.strip())
else:
    raise Exception("Cannot find slave definition file")

localfiles = os.listdir(outdir)
localfiles.sort()

if len(slaves)<=len(localfiles):
    raise Exception("Not enough slave nodes to dispatch tiles")

from subprocess import Popen
pipes=list()
for i,lf in enumerate(localfiles):
    ip=slaves[i]
    lfp = os.path.join(outdir,lf)
    cmdstr=['scp', lfp, ip+":"+options.remote]
    #print ' '.join(cmdstr)
    p=Popen(cmdstr)
    pipes.append(p)
exit_codes = [ p.wait() for p in pipes ]
sys.exit(max(exit_codes))
