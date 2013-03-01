
import networkx as nx
import copy
from primo.core import Node
from primo.reasoning.factorelemination import Factor
from primo.reasoning.factorelemination import FactorTree
from random import choice

class FactorTreeFactory(object):
    
    def create_random_factortree(self,bayesNet):
        allNodes = bayesNet.get_all_nodes()
        
        if len(allNodes) == 0:
            raise Exception("createRandomFactorTree: No nodes in given bayesNet")
        
        tn = allNodes.pop()
        rootFactor = Factor(tn)

        graph = nx.DiGraph()

        graph.add_node(rootFactor)        
        
        usedNodes = [rootFactor]
        
        for n in allNodes[:]:
            parentNode = choice(usedNodes[:])
            newFactor = Factor(n)
            graph.add_edge(parentNode,newFactor)
            usedNodes.append(newFactor)
            
            
        return FactorTree(graph,rootFactor)
        
    def calculate_seperators_pull(self,factor,graph):
        
        s = set()  
        pullSet = set()
        
        #find all variables in outgoing edges for factor
        for child in graph.neighbors(factor):
            s = self.calculate_seperators_pull(child,graph)
            # add s to incoming vars from child
            if graph[factor][child]['inVars'] == None:
                graph[factor][child]['inVars'] = copy.copy(s)                    
            else:
                tmp = graph[factor][child]['inVars']
                graph[factor][child]['inVars'] = tmp | s
                
            
            for c2 in graph.children(factor):
                if child != c2:
                    #TODO: add s to outgoing vars from c2
                    if graph[factor][child]['outVars'] == None:
                        graph[factor][child]['outVars'] = copy.copy(s)                    
                    else:
                        tmp = graph[factor][child]['outVars']
                        graph[factor][child]['outVars'] = tmp | s
                    
                    #self.calculate_seperators_push(child,graph,s)
                    
            pullSet =  s | pullSet
            
        pullSet =  s | set(factor.get_variables())    
        return pullSet
        
    def calculate_seperators_push(self,factor,graph,setOut):

        #TODO: add local vars to set
        #setOut = 
        
        localSet = copy.copy(setOut)
        setOut.add(localVars)

        for child in graph.children(factor):
            #add setOut to outgoing vars from child
            child.calculate_seperators_push(child,graph,setOut)
            
            
                        
        
        
            
        
        
    
