from scipy import io
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros, arange

mat_file_1 = io.loadmat('no_f_data.mat')
mat_file_2 = io.loadmat('label.mat')

data = mat_file_1['no_f_data'][0]
label = mat_file_2['t_amplifier'][0]

Fs = 30*10**3               
Ts = 1/Fs                   
t = label
inputSig = data

#variables
ty = []
tx = label
dic = dict()
spikes =[]
i = 0

f_cut = 100
w_cut = 2*np.pi*f_cut
tau = 1/w_cut

#define High Pass Filter
def HPF(data, tau, Ts):
    result = zeros((len(data),))
    for n in arange(1, len(data)):
        result[n] = (tau*result[n-1] + tau*(data[n]-data[n-1]))/(tau + Ts)
    return result

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
        
filteredSig = HPF(inputSig, tau, Ts)
ty = filteredSig
#plt.figure(figsize=(12,5))
#plt.plot(t, filteredSig)
#plt.show()


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
        if ty[i] < -80:
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

#spike clustering
for i in range(len(spikes)):
    
    diff1 = check_1(spikes[i])
    diff2 = check_2(spikes[i])
    diff3 = check_3(spikes[i])
    checklist=[diff1,diff2,diff3]
    res = check_min(checklist)
        
    if res !=0:
        result[res] +=1
    else:
        print("error occured at "+str(spikes[i]))

print(result)
print(len(spikes))
