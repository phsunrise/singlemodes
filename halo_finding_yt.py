import os
import yt
yt.enable_parallelism()

from yt.analysis_modules.halo_finding.halo_objects import FOFHaloFinder

last = 0
while os.path.isdir("DD%04d" % last):
    last += 1
last -= 1

ds = yt.load("DD%04d/data%04d" % (last, last))

link = 0.3
halos = FOFHaloFinder(ds, link=link, padding=0.02)
halos.write_out("FOFhalos_link_%.1f.txt" % link)
