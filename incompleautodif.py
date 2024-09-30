#failed attempt to implement automatic differentiation using torch. Incomplete
import torch
from torch.autograd import grad
import csv

bindingenergies=[]

def makedata(rows):

    trainingdata = []
    for row in rows:
        # create terms for vector
        
        Z = int(row["z"])
        N = int(row["n"])
        A = Z+N
        t1 = A
        t2 = -(A**(2/3))
        t3 = -(Z**(2))*(A**(-1/3))
        t4 = ((Z - N)**2)/A
        t5 = 0.5 * (((-1)**Z)+((-1)**N))*(A**(-1/2))
        list1 =[t1,t2,t3, t4,t5]
        newtensor=torch.tensor(list1, requires_grad=True)
        trainingdata.append(newtensor)
        bindingenergies.append(row["bindingEnergy"])

        
    return trainingdata

def loss(a_v,a_s,a_c,a_a,a_p, trainingdata):
    list1 = [a_v,a_s,a_c,a_a,a_p]
    function = torch.tensor(list1)
    list2=[0,0,0,0,0]
    x = torch.tensor(0.0)
    for i in range(len(trainingdata)):
        add = torch.matmul(function,trainingdata[i])
        x = torch.add(x,add)
    return x


#pytorch accumulates gradient by default
#we must clear gradient
def main():
    #initialize ceofficinets of BE function
    a_v = torch.tensor(1.0, requires_grad = True)
    a_s = torch.tensor(1.0, requires_grad = True)
    a_c = torch.tensor(1.0, requires_grad = True)
    a_a = torch.tensor(1.0, requires_grad = True)
    a_p = torch.tensor(1.0, requires_grad = True)
    

    
    #get binding energy data and format
    rows = []
    formatteddata=[]
    badinputs=0
    with open("bindingenergydata.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    for i in range(len(rows)):

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

    y = loss(a_v,a_s,a_c,a_a,a_p, trainingdata)
    print(y)
    y.backward()
    learnrate=0.1
    
    print(a_v.grad)

main()