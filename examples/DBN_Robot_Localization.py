#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
from primo.core import TwoTBN
from primo.reasoning import DiscreteNode
import primo.reasoning.particlebased.ParticleFilterDBN as pf
import numpy
from primo.utils import XMLBIF

# Construct a DynmaicBayesianNetwork
dbn = DynamicBayesNet()
B0 = BayesNet()
twoTBN = TwoTBN(XMLBIF.read("Robot_Localization.xmlbif"))

# Configure TwoTBN
x0 = twoTBN.get_node("x0")
x = twoTBN.get_node("x")
door = twoTBN.get_node("door")
twoTBN.set_initial_node(x0.name, x.name)

# Configure initial distribution
x0_init = DiscreteNode(x0.name, ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"])
B0.add_node(x0_init)
cpt_x0_init = numpy.array([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
x0_init.set_probability_table(cpt_x0_init, [x0_init])

dbn.B0 = B0
dbn.twoTBN = twoTBN

N = 1000
T = 10

pos = 0
evidence = {}
def get_evidence_function():
    global pos
    global evidence    
    if pos == 10:
        pos = 0
    if pos == 1 or pos == 3 or pos == 7:
        evidence = {door:"True"}
    else:
        evidence = {door:"False"}
    pos = pos + 1
    return evidence
    
result = pf.particle_filtering_DBN(dbn, N, T, get_evidence_function)
for samples in result:
    w_hit = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for i in samples:
        (state, w) = samples[i]
        x_ = x
        if x not in state:
            x_ = x0_init
        if state[x_] == "p0":
            w_hit[0] += 1
        if state[x_] == "p1":
            w_hit[1] += 1
        if state[x_] == "p2":
            w_hit[2] += 1
        if state[x_] == "p3":
            w_hit[3] += 1
        if state[x_] == "p4":
            w_hit[4] += 1
        if state[x_] == "p5":
            w_hit[5] += 1
        if state[x_] == "p6":
            w_hit[6] += 1
        if state[x_] == "p7":
            w_hit[7] += 1
        if state[x_] == "p8":
            w_hit[8] += 1
        if state[x_] == "p9":
            w_hit[9] += 1
    print "Real position: " + str(pos) + " (Door: " + str(evidence[door]) + ")"
    print "Partical distribution: " + str(w_hit)