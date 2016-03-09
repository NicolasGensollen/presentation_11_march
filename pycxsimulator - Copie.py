import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random


K = 5. # coupling strength
Dt = 0.1 # Delta t


def initialize():
    global g, nextg
    random.seed(76502)
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes_iter():
        g.node[i]['natural_freq'] = random.random()
    for i in g.nodes_iter():
        g.node[i]['theta'] = random.random()
    print g.node[0]['natural_freq']
    nextg = g.copy()


def observe():
    global g, nextg
    subplot(1, 2, 1)
    cla()
    nx.draw(g, cmap = cm.hsv, vmin = -1, vmax = 1,
            node_color = [sin(g.node[i]['theta']) for i in g.nodes_iter()],
            pos = g.pos)
    axis('image')
    subplot(1, 2, 2)
    cla()
    plot([cos(g.node[i]['theta']) for i in g.nodes_iter()],
            [sin(g.node[i]['theta']) for i in g.nodes_iter()], '.')
    title('K='+str(K)+r', $\gamma = \frac{\pi}{8}$', fontsize=15)
    axis('image')
    axis([-1.1, 1.1, -1.1, 1.1])


def update():
    global g,nextg
    N = g.number_of_nodes()
    for i in g.nodes_iter():
        theta_i = g.node[i]['theta']
        omega_i = g.node[i]['natural_freq']
        nextg.node[i]['theta'] = theta_i + (omega_i + \
        K/N * sum( sin( g.node[j]['theta'] - theta_i) for j in g.neighbors(i))) * Dt
    g, nextg = nextg, g


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])