import random
import copy
def weighted_random(weights):
    counter = random.random() * sum(weights)
    for i,w in enumerate(weights):
        counter -= w
        if counter <=0:
            return i

class GibbsTransitionModel(object):
    def __init__(self):
        pass
        
    def transition(self, network, state, constant_nodes):
        nodes = network.get_nodes([])
        nodes_to_resample=list(set(nodes)-set(constant_nodes))
        for node in nodes_to_resample:
            parents=network.get_parents(node)
            if parents:
                evidence=[(parent,state[parent]) for parent in parents]
                reduced_cpd = node.get_cpd_reduced(evidence)
            else:
                reduced_cpd = node.get_cpd()
                
            #print "--reduced cpt"
            #print reduced_cpd
                
            #reduce the children's cpds
            children = network.get_children(node)
            for child in children:
                
                #reduce this node's cpd
                parents=network.get_parents(child)
                evidence=[(parent,state[parent]) for parent in parents if parent != node]
                evidence.append((child,state[child]))
                reduced_child_cpd = child.get_cpd_reduced(evidence)

                #print "--reduced child cpt"
                #print reduced_child_cpd
                reduced_cpd = reduced_cpd.multiplication(reduced_child_cpd)
                
            new_state=weighted_random(reduced_cpd.get_table())
            #print state[node]
            #print new_state
            #print node.get_value_range()
            state[node]=node.get_value_range()[new_state]
            #print state[node]
        return state
            
        

class MarkovChainSampler(object):
    def __init__(self):
        pass
        
    def generateMarkovChain(self, network, time_steps, transition_model, initial_state, evidence=[], variables_of_interest=[]):
        state=initial_state
        if evidence:
            for node in evidence.keys():
                if state[node] != evidence[node]:
                    raise Exception("The evidence given does not fit to the initial_state specified")
            constant_nodes = evidence.keys()
        else:
            constant_nodes=[]
        for t in xrange(time_steps):
            if variables_of_interest:
                yield self._reduce_state_to_variables_of_interest(state, variables_of_interest)
            else:
                yield state
            state=transition_model.transition(network, state, constant_nodes)
            
    def _reduce_state_to_variables_of_interest(self, state, variables_of_interest):
        return dict((k,v) for (k,v) in state.iteritems() if k in variables_of_interest)
        
