import yt

for i in xrange(12):
    filename = "DD%04i/data%04i" % (i, i)
    ds = yt.load(filename)

    ds.print_stats()

    ## show particles (zoomed in)
    #p1 = yt.ParticlePlot(ds, "particle_position_x", "particle_position_y",
    #                    width = (0.05, 0.05), color = 'b')
    #p1.save()
    
    ## show particle_mass
    #p2 = yt.ParticlePlot(ds, "particle_position_x", "particle_position_y",
    #                    "particle_mass", width = (1., 1.))
    #p2.save()

    ## density plots
    p3 = yt.SlicePlot(ds, 'z', "all_cic")
    p3.save()
