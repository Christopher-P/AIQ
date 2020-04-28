import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from itertools import chain, combinations
from statistics import stdev

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
    with open('results-p-noise.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            res.append([float(row[2]),float(row[3]),float(row[4])])

            c = c + 1
            if c >= 11:
                c = 0
                names.append(row[0:2])
                data.append(res)
                res = []

    return names, data

def plot_data(names, data):

    for ind, i in enumerate(data):
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        # evenly sampled proportion
        p = np.arange(0.0, 1.1, 0.1)
        a = []
        b = []
        c = []

        for j in i:
            a.append(j[0])
            b.append(j[1])
            c.append(j[2])

        plt.plot(p, a, 'r', label='A')
        plt.plot(p, b, 'g', label='B')
        plt.plot(p, c, 'b', label='AB')

        plt.ylabel('some numbers')
        plt.title('A = ' + names[ind][0] + ' B = ' + names[ind][1] )
        plt.legend()
        plt.savefig(str(names[ind][1]) + '.png')
        #plt.show()


    return None

def plot_all(a, f, sd, tm=False, nam=''):
    
    names = ['Similarity','Shannon']# 'Similarity_Mean', 'AuC', 'Projection', 'AuC_Proj', 'Shannon']

    if tm:
        for ind,val in enumerate([a,f]):
            max_val = max(val)
            for ind2, val2 in enumerate(val):
                val[ind2] = val2 / max_val 
    #print(c)

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    p = np.arange(0.0, 105.0, 5.0)

    print(len(a), len(f), len(p))

    plt.plot(p, a, 'r', label=names[0])
    #plt.errorbar(p, a, yerr=sd, label='both limits (default)')
    #plt.plot(p, b, 'g', label=names[1])
    #plt.plot(p, c, 'b', label=names[2])
    #plt.plot(p, d, 'y', label=names[3])
    #plt.plot(p, e, 'purple', label=names[4])
    plt.plot(p, f, 'black',  label=names[1])

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

def calc_s_mean(data):
    res = []
    sd  = []
    for i in data:
        s_sum = 0.0
        s_list = []
        for j in i:
            a = max(j[0], j[1])
            b = min(j[0], j[1])
            ab = j[2] 

            if ab > a or ab < b:
                s_sum = s_sum + 1.0
                s_list.append(1.0)
            else:
                try:
                    s_sum = s_sum + abs(abs(j[0] -j[2]) - abs(j[1] -j[2]))/abs(j[0] - j[1])
                    s_list.append(abs(abs(j[0] -j[2]) - abs(j[1] -j[2]))/abs(j[0] - j[1]))
                except:
                    print('div 0')
                    s_sum = s_sum + 1
                    s_list.append(1.0)

        sd.append(stdev(s_list)/3.16)
        #print(s_list)
        res.append(round(s_sum/len(i),4)) #, stdev(s_list)/3.16])
    
    return res, sd

### All possible combinations
def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

d = list(powerset(set([0,1,2,3,4,5,6,7,8,9,10])))
combs = []
for i in d:
    if len(i) == 0:
        continue
    combs.append(list(i))

names, data = load_data()
'''
print("----")
print(names,data)

true_measure = calc_s_mean(data,[0,1,2,3,4,5,6,7,8,9,10])

comb_res = []

for i in combs:
    comb_measure = calc_s_mean(data, i)    
    res = np.subtract(comb_measure,true_measure)
    res = sum(np.absolute(res)) /4.0
    comb_res.append(res * len(i))
    print(res)

list1, list2 = zip(*sorted(zip(comb_res, combs)))
print(list1[0:10], list2[0:10])
'''
a, sd = calc_s_mean(data)
a = a[0:21]
sd = sd[0:21]

#plot_one(a, 'Similarity')
#plot_one(b, 'Similarity_mean')
#plot_one(c, 'AuC')
#plot_one(d, 'Projection')
#plot_one(e, 'AuC_Projection')
#plot_one(f, 'Shannon')

#plot_all(a,b,c,d,e,f, tm=False, nam='Non_normed')
plot_all(a,f, sd, tm=True, nam='Normed')

