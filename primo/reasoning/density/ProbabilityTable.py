# -*- coding: utf-8 -*-
import numpy
import copy
from primo.reasoning.density import Density

class ProbabilityTable(Density):
    '''TODO: write doc'''



    def __init__(self):
        super(ProbabilityTable, self).__init__()

        #self.owner = owner
        #self.variables = [owner]

        #size_of_range = len(owner.value_range)
        #self.table = numpy.ones(size_of_range) / size_of_range

        self.variables = []
        self.table = numpy.array(0)

    def get_table(self):
        return self.table

    def add_variable(self, variable):
        self.variables.append(variable)

        ax = self.table.ndim
        self.table=numpy.expand_dims(self.table,ax)
        self.table=numpy.repeat(self.table,len(variable.value_range),axis = ax)

    def set_probability_table(self, table, nodes):
        if not set(nodes) == set(self.variables):
            raise Exception("The list which should define the ordering of the variables does not match"
                " the variables that this cpt depends on (plus the node itself)")
        if not self.table.ndim == table.ndim:
            raise Exception("The provided probability table does not have the right number of dimensions")
        for d,node in enumerate(nodes):
            if len(node.value_range) != table.shape[d]:
                raise Exception("The size of the provided probability table does not match the number of possible values of the node "+node.name+" in dimension "+str(d))

        self.table = table
        self.variables = nodes

    def set_probability(self, value, node_value_pairs):
        index = self.get_cpt_index(node_value_pairs)
        self.table[tuple(index)]=value

    def get_cpt_index(self, node_value_pairs):
        nodes, values = zip(*node_value_pairs)
        index = []
        for node in self.variables:
            index_in_values_list = nodes.index(node)
            value = values[index_in_values_list]
            index.append(node.value_range.index(value))
        return index


    def is_normalized_as_cpt(self,owner):

        dim_of_owner = self.variables.index(owner)
        sum_of_owner_probs = numpy.sum(self.table, dim_of_owner)

        return set(sum_of_owner_probs.flatten()) == set([1])

    def is_normalized_as_jpt(self):
        return numpy.sum(self.table) == 1.0

    def normalized_as_jpt(self):
        '''This method returns a new ProbabilityTable which is a normalized version of this ProbabilityTable (As a joint probability).'''
        return self.table/numpy.sum(self.table)

    def multiplication(self, inputFactor):
        '''This method returns a unified ProbabilityTable which contains the variables of both; the inputFactor
            and this factor(self). The new values of the returned factor is the product of the values from the input factors
            which are compatible to the variable instantiation of the returned value.'''
        #init a new probability tabel
        factor1 = ProbabilityTable()

        #all variables from both factors are needed
        factor1.variables = copy.copy(self.variables)

        for v in (inputFactor.variables):
            if not v in factor1.variables:
                factor1.variables.append(v)

            #the table from the first factor is copied
            factor1.table = copy.copy(self.table)

        #and extended by the dimensions for the left variables
        for curIdx in range(factor1.table.ndim, len(factor1.variables)):
            ax = factor1.table.ndim
            factor1.table=numpy.expand_dims(factor1.table,ax)
            factor1.table=numpy.repeat(factor1.table,len(factor1.variables[curIdx].value_range),axis = ax)

        #copy factor 2 and it's variables ...
        factor2 = ProbabilityTable()
        factor2.variables = copy.copy(inputFactor.variables)
        factor2.table = copy.copy(inputFactor.table)

        #extend the dimensions of factors 2 to the dimensions of factor 1
        for v in factor1.variables:
            if not v in factor2.variables:
                factor2.variables.append(v)

        for curIdx in range(factor2.table.ndim, len(factor2.variables)):
            ax = factor2.table.ndim
            factor2.table=numpy.expand_dims(factor2.table,ax)
            factor2.table=numpy.repeat(factor2.table,len(factor2.variables[curIdx].value_range),axis = ax)

        #sort the variables to the same order
        for endDim,variable in enumerate(factor1.variables):
            startDim = factor2.variables.index(variable);
            if not startDim == endDim:
                factor2.table = numpy.rollaxis(factor2.table, startDim, endDim)
                factor2.variables.insert(endDim,factor2.variables.pop(startDim))

        #pointwise multiplication
        if factor1.table.shape != factor2.table.shape:
            raise Exception("Multiplication: The probability tables have the wrong dimensions for unification!")

        factor1.table = factor1.table *factor2.table;

        return factor1


    def marginalization(self, variable):
        '''This method returns a new instantiation with the given variable summed out.'''        
        
        if not variable in self.variables:        
            raise Exception("Marginalization: The given variable isn't in the ProbabilityTable!")

        #new instance for returning
        retInstance = ProbabilityTable()
        retInstance.table = copy.copy(self.table)
        retInstance.variables = copy.copy(self.variables)                
            
        ax = retInstance.variables.index(variable)
        
        retInstance.table = numpy.sum(retInstance.table,ax)
        retInstance.variables.remove(variable)
        
        return retInstance
        

    def reduction(self, evidence):
        '''Returns a reduced version of this ProbabilityTable, evidence is a list of pairs.
            Important: This node is not being changed!'''
        reduced = ProbabilityTable()
        reduced.variables = copy.copy(self.variables)
        reduced.table = self.table
        for node,value in evidence:

            axis=reduced.variables.index(node)
            position=node.value_range.index(value)
            reduced.table = numpy.take(reduced.table,[position],axis=axis)

            reduced.table=reduced.table.squeeze()
            reduced.variables.remove(node)

        return reduced



    def division(self, factor):
        raise Exception("Called unimplemented function")

    def __str__(self):
        return str(self.table)
