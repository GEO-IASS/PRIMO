#!/usr/bin/env python
# -*- coding: utf-8 -*-

from primo.core import DynamicBayesNet
from primo.reasoning import DiscreteNode

bn = DynamicBayesNet()
burglary = DiscreteNode("Burglary", ["Intruder", "Safe"])
alarm = DiscreteNode("Alarm", ["Ringing", "Silent", "Kaputt"])
earthquake = DiscreteNode("Earthquake", ["Shaking", "Calm"])
john_calls = DiscreteNode("John calls", ["Calling", "Not Calling"])
mary_calls = DiscreteNode("Mary calls", ["Calling", "Not Calling"])


bn.add_node(burglary)
bn.add_node(alarm)
bn.add_node(earthquake)
bn.add_node(john_calls)
bn.add_node(mary_calls)


bn.add_edge(burglary, alarm)
bn.add_edge(earthquake, alarm)
bn.add_edge(alarm, john_calls)
bn.add_edge(alarm, mary_calls)

bn.add_edge(alarm, alarm, True)


print(bn.is_valid())

bn.draw()
