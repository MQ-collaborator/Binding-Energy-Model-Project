import numpy as np
import math
import csv

trainingdata = []

class function():
    def __init__(self, a_v=15.56, a_s=17.23, a_c = 0.697, a_a = 23.285, a_p = 12):
        self.a_v = a_v
        self.a_s = a_s
        self.a_c = a_c
        self.a_a = a_a
        self.a_p = a_p
        list1 = [a_v, a_s, a_c, a_a, a_p]
        self.vector = np.array(list1)
     

#define a loss function taking as input the entire dataset and a funciton (binding energy funcition)
#TODO:Define a loss functino taking as input the entire dataset and a function (binding energy function)
#Loss function needs named parameters to allow for evaluationwith one coefficient shifted
def Loss(vector):
    Loss = 0
    for row in trainingdata:
        Loss += (((np.dot(vector,row["vector"]))-row["bindingEnergy"])**2)
    return Loss

def derivative(function):
    vector=function.vector
    gradients=[]
    before = float(Loss(vector))
    for i in range(5):
        vector[i] = vector[i]+0.01
        after=float(Loss(vector))
        grad=float((after-before)/0.01)
        gradients.append(grad)
        vector[i] = vector[i] - 0.01
    return np.array(gradients)


#calculate magnitude of a vector
#used to determine when gradient is small enough to stop gradient descent
def magnitude(vector):
    return math.sqrt(sumsquare(vector))
#helper function for magnitude
def sumsquare(vector):
    x=0
    for i in range(vector.size):
        x+= (vector[i])**2
    return x




#create a list of dictionaries out of training data with keys: vector (parameters for function) and binding energy
def makedata(rows):
    for row in rows:
        # create terms for vector
        newdict = {}
        Z = int(row["z"])
        N = int(row["n"])
        A = Z+N
        t1 = A
        t2 = -(A**(2/3))
        t3 = -(Z**(2))*(A**(-1/3))
        t4 = -((Z - N)**2)/A
        t5 = 0.5 * (((-1)**Z)+((-1)**N))*(A**(-1/2))
        list1 =[t1,t2,t3, t4,t5]
        newdict["vector"] = np.array(list1)
        newdict["bindingEnergy"] = row["bindingEnergy"]
        trainingdata.append(newdict)
        
    return trainingdata


#store all binding energy data from csv file into a list of dictinoaries
def main():
    rows = []
    formatteddata=[]
    badinputs=0
    with open("bindingenergydata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    for i in range(len(rows)):
        rows[i]["bindingEnergy"] =  rows[i]["bindingEnergy"][:-3]
        try:
            rows[i]["bindingEnergy"] = float(rows[i]["bindingEnergy"])
            formatteddata.append(rows[i])
        except ValueError:
            #take a note of bad data to exclude later
            #for some reason about 100 datapoints raised exceptions
            #I will fix this later. In all honesty, the model should work with 2.5% of data missing 
            #this problem is kicked down the can
            badinputs+=1
    trainingdata = makedata(formatteddata)
    BEfunction = function()
    
    #the purpose of this page is to get an idea of reasonable derivative values
    print(derivative(BEfunction))
    
main()