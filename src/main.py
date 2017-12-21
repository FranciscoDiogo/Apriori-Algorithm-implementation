
from numpy import *

#create list of single items
def single_item_list(data):
    C1 = []
    for transaction in data:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
                
    C1.sort()
    #return as frozenset so it can be used as dictionary keys
    return list(map(frozenset, C1)) 

def support_at_k_list(data, Ck, minSupport):
    ssCnt = {}
    for tid in data:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]
        if support >= minSupport:
          retList.insert(0,key)
          supportData[key] = support
    return retList, supportData

def apriori(dataSet, minSupport):
    C1 = single_item_list(dataSet)
    D = list(map(set, dataSet))
    L1, supportData = support_at_k_list(D, C1, minSupport)
    
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = support_at_k_list(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    
    return L, supportData
  
def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: 
                retList.append(Lk[i] | Lk[j]) 
    return retList
    
def main():
  f = open("../categories.txt", 'rU')
  list_items=[]
  for line in f:
    list_items.append(line.rstrip().split(";"))
    
  minSupport =  0.01*len(list_items)
  L1, supportData = apriori(list_items, minSupport)
    
  text_file = open("patterns2.txt", "w")
  for k,v in supportData.items():
    str_write=str(v)+":"
    for i in list(k):
      str_write+=str(i)+";"
    str_write = str_write[:-1]+"\n"
    text_file.write(str_write)
  text_file.close()
  
main()
