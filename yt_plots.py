import os
import yt

i = 0
while os.path.isdir("DD%04d" % i):
    ds = yt.load("DD%04d/data%04d" % (i, i))

    plot1 = yt.SlicePlot(ds, 'z', "all_cic")
    plot1.save()

    plot2 = yt.ProjectionPlot(ds, 'z', "all_cic")
    plot2.save()

    i += 1
