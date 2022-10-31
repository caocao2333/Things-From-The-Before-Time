import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getSum(i1, i2, i3):
    eta1 = []
    phi1 = []
    eta2 = []
    phi2 = []
    ret = pd.DataFrame()
    for l1 in range(i1 + 1, i2):
        eta1.append(dataFile.loc[l1, "nHits"])
        phi1.append(dataFile.loc[l1, "vZero"])
    for l2 in range(i2 + 1, i3):
        eta2.append(dataFile.loc[l2, "nHits"])
        phi2.append(dataFile.loc[l2, "vZero"])
    if len(eta1) > len(eta2):
        while len(eta2) < len(eta1):
            eta2.append(0)
            phi2.append(0)
        for i in range(0, len(eta1)):
            c = np.absolute(np.average([eta1[i], eta2[i]]))
            d = pd.DataFrame([[eta1[i], eta2[i], phi1[i], phi2[i]]])
            if c < 0.5:
                ret = pd.concat([ret, d])
    else:
        while len(eta2) > len(eta1):
            eta1.append(0)
            phi1.append(0)
        #print(len(eta2))
        #print(len(eta1))
        for i in range(0, len(eta2)):
            c = np.absolute(np.average([eta1[i], eta2[i]]))
            d = pd.DataFrame([[eta1[i], eta2[i], phi1[i], phi2[i]]])
            if c < 0.5:
                ret = pd.concat([ret, d])
    ret = ret.reset_index(drop = True)
    #print(ret)
    return ret

dataFile = pd.read_csv(r"generic file location lol", sep = " ", header = None)
dataFile.columns = ["nHits", "vZero"]
df2 = dataFile[dataFile["vZero"].between(8256, 12354, inclusive = "both")]
print(df2)
index = df2.index

bc = pd.DataFrame()
print(type(bc))
for i in range(0, len(index) - 2, 2):
    bc = pd.concat([bc, pd.DataFrame([[1000000, 1000000, 1000000, 1000000]])])
    if i % 100 == 0:
        print(i)
    t = getSum(index[i], index[i + 1], index[i + 1] + int(df2.loc[index[i + 1], "nHits"]))
    bc = pd.concat([bc, t])
    bc = bc.reset_index(drop = True)
    #print(bc)
bc.to_csv(r'some other generic file location', index = False)
