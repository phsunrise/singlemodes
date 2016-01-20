import yt

i = 0
while os.path.isdir("DD%04d" % i):
    filename = "DD%04d/data%04d" % (i, i)
    ds = yt.load(filename)

    ds.print_stats()
    plot1 = yt.SlicePlot(ds, 'z', "all_cic")
    plot1.save()

    plot2 = yt.ProjectionPlot(ds, 'z', "all_cic")
    plot2.save()

    i += 1
