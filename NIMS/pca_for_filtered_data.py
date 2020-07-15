%matplotlib inline
from scipy import io
from matplotlib import pyplot as plt
import numpy as np

#file load
mat_file_1 = io.loadmat('data_2.mat')
mat_file_2 = io.loadmat('label.mat')
data = mat_file_1['data_2']
label = mat_file_2['t_amplifier']
 
#variables
ty = data[0]
tx = label[0]
dic = dict()
spikes =[]
i = 0

#define pca
def check_1(temp):
    start = temp[0]
    end = temp[1]
    i=0
    diff = 0
    
    std = spikes[0][0]

    while start < end:
        diff += ((ty[start] - ty[std+i])**2)/10
        i += 1
        start+=1
    return diff

def check_2(temp):
    start = temp[0]
    end = temp[1]
    i=0
    diff = 0
    std = spikes[1][0]
    while start < end:
        diff += ((ty[start] - ty[std+i])**2)/10
        i += 1
        start+=1
    return diff

def check_3(temp):
    start = temp[0]
    end = temp[1]
    i=0
    diff = 0
    std = spikes[2][0]
    while start < end:
        diff += ((ty[start] - ty[std+i])**2)/10
        i += 1
        start+=1
    return diff

#define check_min
def check_min(temp):
    one = temp[0]
    two = temp[1]
    thr = temp[2]
    if one < two:
        if one < thr:
            return 1
        else:
            return 3
    else:
        if two<thr:
            return 2
        else:
            return 3

#get spikes
while i < len(tx):
    temp = [-1,-1]
    dic[tx[i]] = ty[i]
    if ty[i] > 95:
        if i > 15:
            temp[0] = i-15
            temp[1] = i+30
            spikes.append(temp)
        i += 31
    else:
        if ty[i] < -40:
            if i >15:
                temp[0] = i-15
                temp[1] = i+30
                spikes.append(temp)
            i += 31
        else:
            i+=1
diff1 = 0
diff2 = 0
diff3 = 0
res = 0
result = {1 : 0, 2 : 0, 3 : 0}

#normalization
for i in range(len(spikes)):
    t= ty[spikes[i][0]:spikes[i][1]]
    t = list(t)
    if(max(t) > abs(min(t))):
        x = t.index(max(t))+spikes[i][0]
    else:
        x = t.index(min(t))+spikes[i][0]
    spikes[i][0] = x-20
    spikes[i][1] = x+20


#spike clustering
for i in range(len(spikes)):
    
    diff1 = check_1(spikes[i])
    diff2 = check_2(spikes[i])
    diff3 = check_3(spikes[i])
    checklist=[diff1,diff2,diff3]
    res = check_min(checklist)
    
    if res !=0:
        result[res] +=1 
        if res == 1:
            plt.plot(tx[spikes[0][0]:spikes[0][1]],ty[spikes[i][0]:spikes[i][1]],'y')
        if res == 2:
            plt.plot(tx[spikes[0][0]:spikes[0][1]],ty[spikes[i][0]:spikes[i][1]],'c')
        if res == 3:
            plt.plot(tx[spikes[0][0]:spikes[0][1]],ty[spikes[i][0]:spikes[i][1]],'m')
    else:
        print("error occured at "+str(spikes[i]))
         
plt.show()
print(result)
print(len(spikes))
