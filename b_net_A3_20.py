"""
CS3243 Assignment 3 (Bayesian Network)
Members:
    Benn Tay Guobin | A0167647N
    Kwek Jun Kai Sean | A0155565X
"""

import sys
import json


class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []
        self.network = {}

    def construct(self):
        # TODO: Your code here to construct the Bayesian network
        for name, vals in self.variables.items():
            # initialise each node as a dict
            self.network[name] = {}
            # initialise value dict & probability table of each node, corresponding value will hold probability
            self.network[name]["Values"] = {}
            self.network[name]["Table"] = []
            for index in vals:
                self.network[name]["Values"][index] = 0  # initialise as 0
            # initialise dependency list of each node, replace with populated list in next loop
            self.network[name]["Dependencies"] = []
        for name, vals in self.dependencies.items():
            self.network[name]["Dependencies"] = vals
        for name, vals in self.prior_probabilities.items():
            for inner_name, inner_vals in vals.items():
                self.network[name]["Values"][inner_name] = inner_vals
        # print(self.network)
        for name, vals in self.conditional_probabilities.items():
            self.network[name]["Tables"] = vals
            temp_dict = {}
            # create list in temp_dict for each discrete value of name
            for key in self.network[name]["Values"].keys():
                temp_dict[key] = []
            # get list of dependencies
            dependency_list = self.network[name]["Dependencies"]
            for dicts in vals:
                # get probabilities of dependencies with respective vals and find probability of intersect of all
                count = 0
                for dependency in dependency_list:
                    if count == 0:
                        probability = self.network[dependency]["Values"][dicts[dependency]]
                        count += 1
                    else:
                        probability = probability * self.network[dependency]["Values"][dicts[dependency]]
                # calculate prob of intersect of all dependencies and own_value
                temp_dict[dicts["own_value"]].append(probability * dicts["probability"])
            # print(temp_dict)
            # sum values within temp_dict to obtain probabilities for name
            for inner_name, inner_vals in temp_dict.items():
                probability = sum(inner_vals)
                self.network[name]["Values"][inner_name] = probability
        # print(self.network)

        pass

    def infer(self):
        # TODO: Your code here to answer the queries given using the Bayesian
        # network built in the construct() method.
        self.answer = []  # your code to find the answer
        # for the given example:
        # self.answer = [{"index": 1, "answer": 0.01}, {"index": 2, "answer": 0.71}]
        # the format of the answer returned SHOULD be as shown above.
        
        # Display all the given attributes plsu constructed network
        #self.displayAttr()
        
        for query in self.queries:
            intIndex = query["index"]
            givenDic = query["given"]
            targetKey = query["tofind"].items()[0][0]
            targetVal = query["tofind"].items()[0][1]
            targetNode = self.network[targetKey]
            probAns = 0

            # Check node to get ans
            targetNodeTablesLst = targetNode["Tables"]
            for targetNodeTablesDic in targetNodeTablesLst:
                found = False
                if targetNodeTablesDic["own_value"] == targetVal:
                    found = True
                    for k, v in givenDic.items():
                        if targetNodeTablesDic[k] != v:
                            found = False
                if found:
                    probAns = targetNodeTablesDic["probability"]
                    dicAns = {}
                    dicAns["index"] = intIndex
                    dicAns["answer"] = probAns
                    self.answer.append(dicAns)
                    break

        return self.answer

    # You may add more classes/functions if you think is useful. However, ensure
    # all the classes/functions are in this file ONLY and used within the
    # BayesianNetwork class.

    # Auxiliary function for displaying attributes and network
    def displayAttr(self):
        print "============VARIABLES============"
        #print self.variables
        for k in self.variables:
            print k, self.variables[k]
            print
        print
        print "============DEPENDENCIES============"
        #print self.dependencies
        for k in self.dependencies:
            print k, self.dependencies[k]
            print
        print
        print "============CONDITIONAL PROBABILITIES============"
        #print self.conditional_probabilities
        for k in self.conditional_probabilities:
            print k, self.conditional_probabilities[k]
            print
        print
        print "============PRIOR PROBABILITES============"
        #print self.prior_probabilities
        for k in self.prior_probabilities:
            print k, self.prior_probabilities[k]
            print
        print
        print "============QUERIES============"
        #print self.queries
        for k in self.queries:
            print k#, self.queries[k]
            print
        print
        print "============NETWORK============"
        #print self.network
        for k in self.network:
            print k, self.network[k]
            print


def main():
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 4:
        print ("\nUsage: python b_net_A3_xx.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")


    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]
    '''
    structure_filename = "structure.json"
    values_filename = "values.json"
    queries_filename = "queries.json"
    '''

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()
    #print answers


if __name__ == "__main__":
    main()
