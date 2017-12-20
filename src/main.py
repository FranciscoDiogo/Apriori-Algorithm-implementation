
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
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
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
    #if(support<minSupport):
    #  continue;
    list_k = list(k)
    str_write=str(v)+":"
    for i in list_k:
      str_write+=str(i)+";"
    str_write = str_write[:-1]
    str_write+="\n"
    text_file.write(str_write)
  text_file.close()
  
main()

        
"""
import argparse
from itertools import chain, combinations
import json


def joinset(itemset, k):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k])


def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])

def itemset_support(transaction_list, itemset, min_support=0):
    len_transaction_list = len(transaction_list)
    l = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list) 
        for item in itemset
    ]
    return dict([(item, support) for item, support in l if support >= min_support])


def freq_itemset(transaction_list, c_itemset, min_support):
    f_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset(l_itemset, k)
        l_itemset = itemset_support(transaction_list, c_itemset, min_support)
        if not l_itemset:
            break
        f_itemset.update(l_itemset)
        k += 1

    return f_itemset    


def apriori(data, min_support, min_confidence):
    # Get first itemset and transactions
    itemset, transaction_list = itemset_from_data(data)

    # Get the frequent itemset
    f_itemset = freq_itemset(transaction_list, itemset, min_support)

    # Association rules
    rules = list()
    for item, support in f_itemset.items():
        if len(item) > 1:
            for A in subsets(item):
                B = item.difference(A)
                if B:
                    A = frozenset(A)
                    AB = A | B
                    confidence = float(f_itemset[AB]) / f_itemset[A]
                    if confidence >= min_confidence:
                        rules.append((A, B, confidence))    
    return rules, f_itemset




def data_from_file(filename):
  f = open(filename, 'rU')
  list_items=[]
  for line in f:
    list_items.append(line.rstrip().split(";"))
  return list_items

def itemset_from_data(data):
    itemset = set()
    item_list = list(set())
    for irow in range(0, len(data)):
        item_list.append(set())
        for item in data[irow]:
            if item:
                itemset.add(item)
                item_list[irow].add(item)
    return itemset, item_list

def make_assignment_1(Dict, support):
    Dict_good_1 = {}    
    for i in Dict.keys():
      if Dict[i] >= support:
        Dict_good_1[i] = Dict[i]
        
    text_file = open("patterns.txt", "w")
    for i in Dict_good_1.keys():
      str_write=str(Dict_good_1[i])+":"+str(i)+"\n"
      text_file.write(str_write)
    text_file.close()
    return Dict_good_1

def main():
    data = data_from_file("../categories.txt")
    num_lines = len(data)
    support=0.01*num_lines
    itemset, item_list = itemset_from_data(data)
    
    Dict = {}
    for i in itemset:
      Dict[i] = 0
    for row in data:
      for item in row:
        Dict[item] = Dict[item] + 1
    
    survive_1 = make_assignment_1(Dict, support)
    
    
    survived=survive_1
    k=1
    counter=1
    while counter>0:
      survived_new = {}
      len_keys=len(survived.keys())
      for k, v in survived.items():
        for k2, v2 in survived.items():
          if(k2==k):
            continue;
          
          key=(k,k2)
          survive_2[key] = 0
    
    for dset in item_list:
      for k, v in survive_2.items():
        intersec = list(dset.intersection(k))
        if(len(intersec)>=2):
          key = (intersec[0], intersec[1])
          survive_2[key] = survive_2[key] + 1
      
    Dict_good_2 = {}    
    for i in survive_2.keys():
      if survive_2[i] >= support:
        Dict_good_2[i] = survive_2[i]
            
    for i in  Dict_good_2.keys():
      str_write=str( Dict_good_2[i])+":"+str(i[0])+","+str(i[1])+"\n"
      print(str_write)
    
    #rules, itemset = apriori(data, 0.01, 0.01)
    #print_report(rules, itemset)

main()
"""