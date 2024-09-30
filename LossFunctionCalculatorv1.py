import numpy as np
import math
import csv

class function():
    def __init__(self, a_v=15.56, a_s=17.23, a_c = 0.697, a_a = 23.285, a_p = 12.0):
        self.a_v = a_v
        self.a_s = a_s
        self.a_c = a_c
        self.a_a = a_a
        self.a_p = a_p
        list1 = [a_v, a_s, a_c, a_a, a_p]
        self.vector = np.array(list1)

    def lossinstance(self, inputarray, expectval):
        outputval = np.dot(self.vector, inputarray)
        return ((outputval-expectval)**2)

#define a loss function taking as input the entire dataset and a funciton (binding energy funcition)
#TODO:Define a loss functino taking as input the entire dataset and a function (binding energy function)
#Loss function needs named parameters to allow for evaluationwith one coefficient shifted
def Loss(trainingdata, function):
    Loss = 0
    for row in trainingdata:
        Loss += function.lossinstance(row["vector"], row["bindingEnergy"])
    return Loss

#create a list of dictionaries out of training data with keys: vector (parameters for function) and binding energy
def makedata(rows):
    trainingdata = []
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
            #this problem is kicked down the gan
            badinputs+=1
    trainingdata = makedata(formatteddata)
    nucleusnumber=870
    BEfunction = function()
    print(trainingdata[nucleusnumber])
    print("true binding energy "+ str(trainingdata[nucleusnumber]["bindingEnergy"]))
    print("atom vector")
    print(trainingdata[nucleusnumber]["vector"])
    print("function vector")
    print(BEfunction.vector)
    print("calculated binding energy " + str(np.dot(BEfunction.vector, trainingdata[nucleusnumber]["vector"])))
    print("loss for this individual atom " + str(BEfunction.lossinstance(trainingdata[nucleusnumber]["vector"], trainingdata[nucleusnumber]["bindingEnergy"])))

    #testdata = [trainingdata[3000]]
    #print("loss for this datapoint " + str(Loss(testdata, BEfunction)))
    print("Overall for entire dataset")
    print("Value of loss function with current settings for function: " + str(Loss(trainingdata,BEfunction)/(10**9 ))+"billion")
    
    # create a list of dictionaries with input arrays as keys
    
main()