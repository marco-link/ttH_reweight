#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import pandas
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot


alpha_sample = numpy.arccos(numpy.linspace(-1, 1, 21))


def xy_to_ralpha(x, y):
    return numpy.sqrt(x*x + y*y), numpy.arctan2(y, x)


def ralpha_to_xy(r, alpha):
    return r * numpy.cos(alpha), r * numpy.sin(alpha)


def samplepoints(alpha_s):
    x, y = ralpha_to_xy(1, alpha_s)
    return x, 2/3 * y

def truealpha(alpha_s):
    return xy_to_ralpha(*samplepoints(alpha_s))[1]


def proposed_circular():
    grid = numpy.array([0.5, 1, 1.5, 2, 3])
    grid = numpy.append(-grid, grid)
    alpha = truealpha(alpha_sample)[1:]

    r, a = numpy.meshgrid(grid, alpha)

    x, y = ralpha_to_xy(r.flatten(), a.flatten())


    print('proposed points: {}'.format(len(x)))


    return x, y



def proposed_grid():
    grid = numpy.array([0.25, 0.5, 1, 1.5, 2])
    grid = numpy.append(-grid, grid)
    alpha = truealpha(alpha_sample)
    limit = max(grid)

    x, y = [], []

    for g in grid:
        x.append(0)
        y.append(g)

        for a in alpha:
            t = g * numpy.tan(a)
            if t > limit:
                x.append(limit/numpy.tan(a))
                y.append(limit)
            elif t < -limit:
                x.append(-limit/numpy.tan(a))
                y.append(-limit)
            else:
                x.append(g)
                y.append(t)

    x = numpy.array(x)
    y = numpy.array(y)

    a = numpy.array([])
    b = numpy.array([])
    # cleanup duplicated points
    for f1 in numpy.unique(x):
        f2 = numpy.unique(y[x==f1])
        a = numpy.append(a, numpy.full(len(f2), f1))
        b = numpy.append(b, f2)


    print('proposed points: {}'.format(len(b)))


    return a, b






def reweighting_points():
    # generate scan
    cosa = numpy.array([-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.0001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    sina= numpy.sin(numpy.arccos(cosa))
    ktcosa = numpy.array([-2. ,-1.7, -1.5,-1.4,-1.2, -1.,-0.8 , -0.5, -0.25, -0.15, 0., 0.15, 0.25 ,  0.5, 0.8, 1. ,1.2,1.4  ,1.5,1.7,  2.])

    cosacosa, ktcosaktcosa = numpy.meshgrid( cosa, ktcosa)
    ktkt = numpy.divide( ktcosaktcosa, cosacosa)
    ktsinakitsina = numpy.multiply( ktkt, numpy.sin(numpy.arccos(cosacosa)))

    ktcosa = ktcosaktcosa.flatten()
    ktsina = ktsinakitsina.flatten()
    ktkt   = ktkt.flatten()

    # the grid will be (ktcosa, ktsina)
    mask = ktsina<2.1
    ktcosa = ktcosa[mask]
    ktsina = ktsina[mask]

    ktkt = ktkt[mask]
    cosa = ktcosa/ktkt

    # filter nans
    mask = numpy.logical_not( numpy.isnan( cosa ))
    ktkt = ktkt[mask]
    cosa = cosa[mask]


    alpha = numpy.arccos(cosa)

    return ktkt * cosa, 2/3 * numpy.sin(alpha)









# plotting stuff

fig = matplotlib.pyplot.figure(figsize=(12,6))

p1 = fig.add_subplot(121)
p2 = fig.add_subplot(122)





for p in [p1, p2]:
    for x, y in zip(*samplepoints(alpha_sample)):
        p.plot([-10 * x, 10 * x], [-10 * y, 10 * y], 'r-')
        p.plot([x], [y], 'r.')
    p.plot([-100], [0], 'r.', label='orignal sample')

    p.set_xlim(-3, 3)
    p.set_ylim(-3, 3)


    p.set_xlabel('kt')
    p.set_ylabel('kt~')






p1.plot(*reweighting_points(), 'b.', label='reweighting')




#p1.plot(*proposed_circular(), 'go', label = 'proposal')
p2.plot(*proposed_grid(), 'b.', label = 'proposal ({} points)'.format(len(proposed_grid()[0])))

p1.legend(loc=0)
p2.legend(loc=0)


fig.tight_layout()
fig.savefig('points.pdf', dpi=300, transparent=False)
matplotlib.pyplot.show()
matplotlib.pyplot.close()
