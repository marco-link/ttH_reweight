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
    cosa = numpy.array([-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.0001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    q = numpy.linspace(-3,3,10)

    cosacosa, qq = numpy.meshgrid(cosa, q )

    qq = qq.flatten()
    cosacosa = cosacosa.flatten()
    alpha = numpy.arccos(cosacosa)

    return qq * cosacosa, 2./3 * qq * numpy.sin(alpha)



points = pandas.DataFrame(columns=('name', 'kt', 'ktilde', 'kv'))

def addPoint(name, kt, ktilde, kv):
    points.loc[len(points.index)] = [name, kt, ktilde, kv]


# model: A*kt*(kt-kv)+C*kv*(kv-kt)+(D+A+C)*kt*kv + B*kttilde^2

addPoint('weight_CPfloat_1',      kt=0, ktilde=0, kv=1) # term C
addPoint('weight_CPfloat_2',      kt=0, ktilde=1, kv=0) # term B
addPoint('weight_CPfloat_3',      kt=0, ktilde=1, kv=1)
addPoint('weight_CPfloat_4',      kt=1, ktilde=0, kv=0) # term A
addPoint('weight_CPfloat_5',      kt=1, ktilde=0, kv=1) # SM term D+A+C
addPoint('weight_CPfloat_6',      kt=1, ktilde=1, kv=0)
addPoint('weight_CPfloat_7',      kt=1, ktilde=1, kv=1)
addPoint('weight_CPfloat_8',      kt=-1, ktilde=0, kv=1)
addPoint('weight_CPfloat_9',      kt=-1, ktilde=0, kv=0)


# add fallback grid
i = 0

for x, y in zip(*reweighting_points()):
    i = i + 1
    addPoint('weight_CPgrid_{}'.format(i), kt=x, ktilde=y, kv=0.5)
    i = i + 1
    addPoint('weight_CPgrid_{}'.format(i), kt=x, ktilde=y, kv=1)
    i = i + 1
    addPoint('weight_CPgrid_{}'.format(i), kt=x, ktilde=y, kv=1.5)


points.to_csv('data/mc_rw/points.csv', index=False)



# plot points

fig = matplotlib.pyplot.figure(figsize=(6,6))

p1 = fig.add_subplot(111, projection='3d')


alldata = pandas.read_csv('data/mc_rw/points.csv', sep=',', header=0, converters={0:str}, comment='#', decimal='.')


mask = ['float' in x for x in alldata['name']]

data = alldata[mask]
p1.scatter(data['kt'], data['ktilde'], zs=data['kv'], label = 'floating')



mask = ['grid' in x for x in alldata['name']]

data = alldata[mask]
p1.scatter(data['kt'], data['ktilde'], zs=data['kv'], label = 'grid', s=5)





p1.set_xlabel(r'$\kappa_t$')
p1.set_ylabel(r'$\tilde{\kappa_t}$')
p1.set_zlabel(r'$\kappa_V$')

p1.legend(loc=0)


fig.tight_layout()
fig.savefig('points.pdf', dpi=300, transparent=False)
matplotlib.pyplot.close()












## plotting stuff

#fig = matplotlib.pyplot.figure(figsize=(12,6))

#p1 = fig.add_subplot(121)
#p2 = fig.add_subplot(122)





#for p in [p1, p2]:
    #for x, y in zip(*samplepoints(alpha_sample)):
        #p.plot([-10 * x, 10 * x], [-10 * y, 10 * y], 'r-')
        #p.plot([x], [y], 'ro')
    #p.plot([-100], [0], 'ro', label='orignal sample')

    #p.set_xlim(-3, 3)
    #p.set_ylim(-3, 3)


    #p.set_xlabel('kt')
    #p.set_ylabel('kt~')






#p1.plot(*reweighting_points(), 'b.', label='reweighting ({} points)'.format(len(reweighting_points()[0])))




##p1.plot(*proposed_circular(), 'go', label = 'proposal')
#p2.plot(*proposed_grid(), 'b.', label = 'proposal ({} points)'.format(len(proposed_grid()[0])))

#p1.legend(loc=0)
#p2.legend(loc=0)


#fig.tight_layout()
#fig.savefig('points.pdf', dpi=300, transparent=False)
#matplotlib.pyplot.show()
#matplotlib.pyplot.close()
