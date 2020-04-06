import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

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
    with open('cart-results.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            res.append([float(row[3]),float(row[4]),float(row[5]), float(row[2])])

            c = c + 1
            if c >= 3:
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
        p = [0.2, 0.3, 0.8]
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
        try:
            s = abs(abs(i[5][0] -i[5][2]) - abs(i[5][1] -i[5][2]))/abs(i[5][0] -i[5][1])
        except:
            print('Exusprosion')
            s = 1
        res.append(s)
    
    return res

def calc_s_mean(data):
    res = []
    for i in data:
        s_sum = 0.0
        for j in i:
            try:
                s_sum = s_sum + abs(abs(j[0] -j[2]) - abs(j[1] -j[2]))/abs(j[0] - j[1])
            except:
                s_sum = s_sum + 1
        res.append(s_sum/len(i))
    
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

names, data = load_data()

#print(names)
print(data)
plot_data(names,data)

#print(names)

#a = calc_s(data)
#print(a)

b = calc_s_mean(data)
print(b)

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

