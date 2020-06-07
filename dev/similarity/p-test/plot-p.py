import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

import math
from statistics import stdev
import copy

# Genned by shannon.py
shannon = [1.0,
0.9884630786125186,
0.9779063680780861,
0.9670823663352526,
0.9562480935437159,
0.9458791582568702,
0.9354357639018251,
0.9262285524206242,
0.91701533048111,
0.9038639564658724,
0.8986290119258085,
0.8889915068056273,
0.8812026403870312,
0.8749012916921781,
0.8617467562693013,
0.8564688365293252,
0.850243786091179,
0.8395607580321117,
0.8298647538199406,
0.8248330719039476,
0.8156931044276727
]

f = shannon

def load_data():
    c = 0
    res = []
    data = []
    names = []
    with open('tmp_buttons.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            res.append([float(row[3]),float(row[4]),float(row[5])])

            c = c + 1
            if c >= 11:
                c = 0
                names.append(row[0:2])
                data.append(res)
                res = []

    data = add_data(data)

    return names, data

def add_data(data):
    '''
    amt  = [10, 10, 10, 100, 2]

    data = np.asarray(data)
    data = np.reshape(data, (5,5,11,3))
    
    for ind, val in enumerate(amt):
        for ind2, val2 in enumerate(amt):
            for i in range(11):
                AB = data[ind][ind][i][2]
                # add the percentage of probablity times 1/base class
                AB = AB + (1 - AB) * 1 / (val + val2)

                data[ind][ind2][i][2] = AB
    data = np.reshape(data, (25,11,3))
    return list(data)
    '''
    
    # Just AB
    nums = [0,6,12,18,24]
    amt  = [10, 10, 10, 100, 2]
    
    for ind, val in enumerate(data):
        if ind not in nums:
            continue
        
        for ind2, val2 in enumerate(val):
            # AB
            AB = data[ind][ind2][2]
            # add the percentage of probablity times 1/base class
            amnt = amt[nums.index(ind)]
            AB = AB + (1 - AB) * 1 / amnt

            data[ind][ind2][2] = AB
    
    return data

def plot_data(names, data):

    for ind, i in enumerate(data):
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        # evenly sampled proportion
        p = np.arrange(0.0, 1.1, 0.1)
        a = []
        b = []
        c = []

        for j in i:
            a.append(j[0])
            b.append(j[1])
            c.append(j[2])

        #print(a,p)
        plt.plot(p, a, 'r', label='A')
        plt.plot(p, b, 'g', label='B')
        plt.plot(p, c, 'b', label='AB')

        plt.ylabel('some numbers')
        plt.title('A = ' + names[ind][0] + ' B = ' + names[ind][1] )
        plt.legend()
        plt.savefig(str(names[ind][1]) + '.png')
        plt.show()


    return None

def plot_all(a,b,c,d,e,f, tm=False, nam=''):
    
    names = ['Similarity', 'Similarity_Mean', 'AuC', 'Projection', 'AuC_Proj', 'Shannon']

    if tm:
        for ind,val in enumerate([a,b,c,d,e,f]):
            max_val = max(val)
            for ind2, val2 in enumerate(val):
                val[ind2] = val2 / max_val 
    print(c)

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    p = np.arange(0.0, 105.0, 5.0)

    plt.plot(p, a, 'r', label=names[0])
    plt.plot(p, b, 'g', label=names[1])
    plt.plot(p, c, 'b', label=names[2])
    plt.plot(p, d, 'y', label=names[3])
    plt.plot(p, e, 'purple', label=names[4])
    plt.plot(p, f, 'black',  label=names[5])

    plt.ylabel('Measurements')
    plt.title('P-Varied test over random noise injection')
    plt.legend()
    plt.savefig('lots_of_graphs/' + nam + '.png')
    plt.show()


    return None

def plot_one(a, nam=''):
    
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    p = np.arange(0.0, 105.0, 5.0)

    plt.plot(p, a, 'r', label=nam)

    plt.ylabel('Measure')
    plt.title('P-Varied test over random noise injection: ' + nam)
    plt.legend()
    plt.savefig('lots_of_graphs/' + nam + '.png')
    #plt.show()


    return None

def calc_s(data):
    res = []
    for i in data:
        A = i[5][0]
        B = i[5][1]
        AB = i[5][2]
        try:
            s = abs(abs(A - AB) - abs(B - AB))/abs(A - B)
        except:
            print('Exusprosion')
            s = 1
        res.append(s)
        
    return res

def calc_s_mean(data):
    res = []
    for i in data:
        s_sum = 0.0
        s_list = []
        for j in i:
            a = max(j[0], j[1])
            b = min(j[0], j[1])
            ab = j[2] 
            
            if ab > a or ab < b:
                a = 0
                #s_sum = s_sum + 1.0
                #s_list.append(1.0)
            else:
            
                try:
                    s_sum = s_sum + abs(abs(j[0] -j[2]) - abs(j[1] -j[2]))/abs(j[0] - j[1])
                    s_list.append(abs(abs(j[0] -j[2]) - abs(j[1] -j[2]))/abs(j[0] - j[1]))
                except:
                    print('div 0')
                    #s_sum = s_sum + 1
                    #s_list.append(1.0)

        #print(stdev(s_list)/3.16)
        #print(s_list)
        res.append(round(s_sum/len(i),4)) #, stdev(s_list)/3.16])
    
    return res

def calc_auc(data):
    res = []
    for i in data:
        a_avg = 0
        b_avg = 0
        width = 1.0
        for j in i:
            a_avg = a_avg + j[0]
            b_avg = b_avg + j[1]

        a_avg = a_avg / 11.0
        b_avg = b_avg / 11.0

        # A always bigger
        if b_avg > a_avg:
            tmp = b_avg
            b_avg = a_avg
            a_avg = tmp

        # Dont do for outside
        auc = 0.0
        for ind, j in enumerate(i[0:-1]):
            # Triangle
            # 0.5 * b * h
            tri = 0.5 * 0.1 * (i[ind][2] - i[ind+1][2])

            # Rectangle
            # width * height
            rect = 0.1 * ( (min(i[ind][2],i[ind+1][2])) - b_avg)

            trap = abs(tri + rect)
        
            auc = auc + trap

        # window 
        box = (a_avg - b_avg) * 1.0

        # AUC
        AuC = auc / box

        res.append(AuC)
    
    return res

def calc_proj(data):
    res = []
    for i in data:
        a_avg = 0
        b_avg = 0
        for j in i:
            a_avg = a_avg + j[0]
            b_avg = b_avg + j[1]

        a_avg = a_avg / 11.0
        b_avg = b_avg / 11.0  

        # A always bigger
        if b_avg > a_avg:
            tmp = b_avg
            b_avg = a_avg
            a_avg = tmp

        # sum projections
        proj_sum = 0.0

        # Find v (ideal)
        v = np.asarray([0.1, (a_avg-b_avg)/10.0])
        for ind, j in enumerate(i[0:-1]):
            # find s (real)
            s = np.asarray([0.1, i[ind+1][2] - i[ind][2] ])

            # Find proj vector
            proj = np.dot(v,s) / np.dot(s,s) * s

            # FIND MAGNITUDE
            l_proj = abs(np.linalg.norm(proj))
                    
            proj_sum = proj_sum + l_proj

        res.append(proj_sum)

    return res

def calc_proj_auc(data):
    res = []
    for i in data:
        a_avg = 0
        b_avg = 0
        for j in i:
            a_avg = a_avg + j[0]
            b_avg = b_avg + j[1]

        a_avg = a_avg / 11.0
        b_avg = b_avg / 11.0  

        # A always bigger
        if b_avg > a_avg:
            tmp = b_avg
            b_avg = a_avg
            a_avg = tmp

        pro = 0.0
        for ind, j in enumerate(i):
            ideal = ((ind / 10.0) * a_avg + (1.0 - ind / 10.0) * b_avg)/2
            #print(ideal,j[2])
            pro = pro + abs(ideal - j[2])

        res.append(pro)

    return res


def plot_dat(data):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    p = np.arange(0.0, 11.0, 1.0)
    d = data[4]
    a = []
    b = []
    c = []

    for i in d:
        print(i)
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])

    plt.plot(p, a, 'r', label='A')
    plt.plot(p, b, 'b', label='B')
    plt.plot(p, c, 'g', label='AB')

    plt.ylabel('Measure')
    plt.title('P-Varied test over random noise injection: ' + '1')
    plt.legend()
    plt.savefig('lots_of_graphs/' + '1' + '.png')
    plt.show()

# Propigate the uncertainty
# C = AB in this func
def uncer(data):
    deltas = []
    for entry in data:
        # Vars for equation
        A   = 0.0
        dA  = 0.0
        B   = 0.0
        dB  = 0.0
        C  = 0.0
        dC = 0.0

        # To reformat data
        A_arr = []
        B_arr = []
        C_arr = []
        for ind, j in enumerate(entry):
            A_arr.append(j[0])
            B_arr.append(j[1])
            #C_arr.append(j[2])
            
            
            # Use 1-dist from perfect
            p = ind/10
            perfect = (1-p) * j[0] + (p) * j[1]
            C_arr.append(1 - abs(j[2] - perfect))
            #dC_arr.append(0)
            #print(abs(j[2] - perfect))
            

        # Find averages
        A = sum(A_arr)/len(A_arr)
        B = sum(B_arr)/len(B_arr)
        C = sum(C_arr)/len(C_arr)

        # Find delats
        # https://stats.stackexchange.com/questions/48948
        dA = (max(A_arr) - min(A_arr)) / math.pow(len(A_arr), 2)
        dB = (max(B_arr) - min(B_arr)) / math.pow(len(B_arr), 2)
        dC = (max(C_arr) - min(C_arr)) / math.pow(len(C_arr), 2)

        # Equations
        # Part 1:
        num1 = math.pow(dA, 2) + math.pow(dB, 2) + 2 * math.pow(dC, 2)
        den1 = math.pow(abs(A - C) - abs(B - C), 2)
        # Part 2
        num2 = math.pow(dA, 2) + math.pow(dB, 2)
        den2 = math.pow(abs(A - B), 2)

        unc = math.sqrt(num1/den1 + num2/den2)

        deltas.append(round(unc, 4))
        print(unc)

    return deltas

def pareto(data):
    costs = []
    for entry in data:
        # Vars for equation
        A   = 0.0
        dA  = 0.0
        B   = 0.0
        dB  = 0.0
        C  = 0.0
        dC = 0.0

        # To reformat data
        A_arr = []
        B_arr = []
        C_arr = []
        for ind, j in enumerate(entry):
            A_arr.append(j[0])
            B_arr.append(j[1])
            #C_arr.append(j[2])
            
            
            # Use 1-dist from perfect
            p = ind/10
            perfect = (1-p) * j[0] + (p) * j[1]
            C_arr.append(1 - abs(j[2] - perfect))
            #dC_arr.append(0)
            #print(abs(j[2] - perfect))
            

        # Find averages
        A = sum(A_arr)/len(A_arr)
        B = sum(B_arr)/len(B_arr)
        C = sum(C_arr)/len(C_arr)

        # Find delats
        # https://stats.stackexchange.com/questions/48948
        dA = (max(A_arr) - min(A_arr)) / math.pow(len(A_arr), 2)
        dB = (max(B_arr) - min(B_arr)) / math.pow(len(B_arr), 2)
        dC = (max(C_arr) - min(C_arr)) / math.pow(len(C_arr), 2)

        #conf = abs(A - B) / abs(abs(A - C) - abs(B - C))
        #vari = abs(dA - dB) / abs(abs(dA - dC) - abs(dB - dC))
        costs.append([A, B, C, dA, dB, dC])

    costs = np.asarray(costs)
    a = keep_efficient(costs)[0]
   
    t = sum(a)
    for ind,val in enumerate(a):
        a[ind] = val/t

    actual = []
    for entry in data:
        # Vars for equation
        A   = 0.0
        dA  = 0.0
        B   = 0.0
        dB  = 0.0
        C  = 0.0
        dC = 0.0

        # To reformat data
        A_arr = []
        B_arr = []
        C_arr = []
        for ind, j in enumerate(entry):
            A_arr.append(j[0])
            B_arr.append(j[1])
            #C_arr.append(j[2])
            
            
            # Use 1-dist from perfect
            p = ind/10
            perfect = (1-p) * j[0] + (p) * j[1]
            C_arr.append(1 - abs(j[2] - perfect))
            #dC_arr.append(0)
            #print(abs(j[2] - perfect))
            

        # Find averages
        A = sum(A_arr)/len(A_arr)
        B = sum(B_arr)/len(B_arr)
        C = sum(C_arr)/len(C_arr)

        # Find delats
        # https://stats.stackexchange.com/questions/48948
        dA = (max(A_arr) - min(A_arr)) / math.pow(len(A_arr), 2)
        dB = (max(B_arr) - min(B_arr)) / math.pow(len(B_arr), 2)
        dC = (max(C_arr) - min(C_arr)) / math.pow(len(C_arr), 2)

        k = [A,B,C,dA,dB,dC]

        val = np.dot(np.asarray(a), np.asarray(k))
        actual.append(round(val, 4))
    return actual
        
# https://stackoverflow.com/questions/32791911
def keep_efficient(pts):
    'returns Pareto efficient row subset of pts'
    # sort points by decreasing sum of coordinates
    pts = pts[pts.sum(1).argsort()[::-1]]
    # initialize a boolean mask for undominated points
    # to avoid creating copies each iteration
    undominated = np.ones(pts.shape[0], dtype=bool)
    for i in range(pts.shape[0]):
        # process each point in turn
        n = pts.shape[0]
        if i >= n:
            break
        # find all points not dominated by i
        # since points are sorted by coordinate sum
        # i cannot dominate any points in 1,...,i-1
        undominated[i+1:n] = (pts[i+1:] > pts[i]).any(1) 
        # keep points undominated so far
        pts = pts[undominated[:n]]
    return pts

names, data = load_data()
delta = uncer(data)
print('---------')
per   = pareto(data)
print(per)
b = calc_s_mean(data)

# Fill to correct shape
for i in range(5):
    for j in range(i):
        delta.insert(5*i+j,0.0)
        b.insert(5*i+j,0.0)
        per.insert(5*i+j,0.0)

d = np.asarray(b)
d = np.reshape(d,(5,5))

delta = np.asarray(delta)
delta = np.reshape(delta,(5,5))

per = np.asarray(per)
per = np.reshape(per,(5,5))

# Fill 0 vals
for i in range(5):
    for j in range(5):
        d[j][i] = d[i][j]
        delta[j][i] = delta[i][j]
        per[j][i] = per[i][j]

t = copy.deepcopy(d)

for ind,val in enumerate(d):
    for ind2,val2 in enumerate(d):
        t[ind][ind2] = (d[ind][ind2] + d[ind2][ind]) / 2.0

print("--------------")
print(d)
print(delta)
print(per)
for ind, val in enumerate(d):
    print('')
    for ind2, val2 in enumerate(val):
        print(str(d[ind][ind2]) + " ± " + str(delta[ind][ind2]))

#c = calc_auc(data)
#print(c)

#d = calc_proj(data)
#print(d)

#e = calc_proj_auc(data)
#print(e)

#plot_one(a, 'Similarity')
#plot_one(b, 'Similarity_mean')
#plot_one(c, 'AuC')
#plot_one(d, 'Projection')
#plot_one(e, 'AuC_Projection')
#plot_one(f, 'Shannon')

#plot_all(a,b,c,d,e,f, tm=False, nam='Non_normed')
#plot_all(a,b,c,d,e,f, tm=True, nam='Normed')

