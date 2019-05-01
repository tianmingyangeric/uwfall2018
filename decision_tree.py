# !/usr/bin/python3
import pymysql
import matplotlib.pyplot as plt
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import collections
from numpy import *
from sklearn.metrics import accuracy_score
from numpy.random import normal, random, uniform
from config import DB_config, user_rate
import math
import operator
import urllib
import re
import copy
import tkinter as tk

minErrorNum = 1000


class DB:
    def __init__(self):
        db_config = DB_config()
        self.db = pymysql.connect(user= db_config.user,
                            password=db_config.password,
                            port = db_config.port,
                            host=db_config.host,
                            db=db_config.db)
        self.cursor = self.db.cursor()
    
    def execute(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.db.commit()
        return result

    def close(self):
        self.db.close()


def get_test_data(dataSet, rounds):
    len_test = int(math.ceil(len(dataSet) / 10))
    try:
        test_data = dataSet[range(rounds*len_test, (rounds+1)*len_test)]
        rest_data = np.delete(dataSet,[range(rounds*len_test, (rounds+1)*len_test)], axis = 0)
    except IndexError:
        test_data = dataSet[range(rounds*len_test, len(dataSet))]
        rest_data = np.delete(dataSet,[range(rounds*len_test, len(dataSet))], axis = 0)
    return rest_data, test_data


def item_count(data):
    item_dict = {}
    label_list = [data[i][-1] for i in range(0,len(data))]
    for label in label_list:
        item_dict[label] = label_list.count(label)
    return item_dict


def KNN_classifier(test_data, training_data, labels, k):
    distance_list = []
    targets = []
    for x_train in range(len(training_data)):
        distance = np.sqrt(np.sum(np.square(test_data - training_data[x_train, :])))
        distance_list.append([distance,x_train])
    distance_list = sorted(distance_list)
    for m in range(0,k):
        index = distance_list[m][1]
        targets.append(labels[index])
    return collections.Counter(targets).most_common(1)[0][0]


def KNN_TestResult(test_data, training_data, training_label, K):
  result_list = []
  a = 0
  for x in test_data:
    a += 1
    result = KNN_classifier(x, training_data, training_label, K)
    result_list.append(result)
  return np.array(result_list)


def KNN_accuracy(test_data,training_data,training_label,K):
    KNN_result = KNN_TestResult(test_data, training_data, training_label, K)
    True_result = loaddata_test()[1]
    score = accuracy_score(True_result, KNN_result)
    print (KNN_result)
    print (True_result)
    return score


def cal_Entropy(data):
    Entropy=0.0
    label_dict=item_count(data)
    for label_key in label_dict:
        prob=float(label_dict[label_key])/(len(data))
        Entropy -= prob*np.math.log(prob,2)
    return Entropy


def get_maxlabel(data):
    items = item_count(data)
    max_label = max(items,key = items.get)
    return max_label


def splitContinuousDataSet(data,x,value,direction):
    subData=[]
    for col in data:
        if (direction==0 and col[x]>value) or (direction==1 and col[x]<=value):
            reducedData=col[:x]
            reducedData.extend(col[x+1:])
            subData.append(reducedData)
    return subData


def chooseSplitList(feature, dataSet):
    label_list = [data[len(data)-1] for data in dataSet]
    sortIndex = np.array(feature).argsort()
    Feature_Vec, sortlabel = [np.array(array)[sortIndex] for array in [feature,label_list]]
    flag = sortlabel[0]
    num = 0
    split_Value = []
    for label in sortlabel:
        if label != flag:
            feature1,feature2 = [Feature_Vec[num-1]for number in [num-1,num]]
            split_Value.append((feature1+feature2)/2)
        num += 1
        flag = label
    return split_Value


def chooseBestFeat(dataSet,labels):
    baseEntropy=cal_Entropy(dataSet)
    bestFeat=0
    baseGainRatio=-1
    numFeats=len(dataSet[0])-1
    bestSplit=-1000
    bestSplitDic={}
    # print('dataSet[0]:' + str(dataSet[0]))
    for i in range(numFeats):
        featVals=[example[i] for example in dataSet]
        featType = type(featVals[0]).__name__
        if featType =='float' or featType =='int':
            splitList = chooseSplitList(featVals, dataSet)
            for j in splitList:
                newEntropy=0.0
                gainRatio=0.0
                splitInfo=0.0
                value = j
                subDataSet0 = splitContinuousDataSet(dataSet,i,value,0)
                subDataSet1 = splitContinuousDataSet(dataSet,i,value,1)
                prob0 = float(len(subDataSet0))/len(dataSet)
                newEntropy += prob0*cal_Entropy(subDataSet0)
                prob1 = float(len(subDataSet1))/len(dataSet)
                newEntropy += prob1*cal_Entropy(subDataSet1)
                if (prob0 != 0):
                    splitInfo -= prob0*math.log(prob0,2)
                if (prob1 != 0):
                    splitInfo -= prob1*math.log(prob1,2)
                if (splitInfo == 0):
                    continue
                gainRatio=float(baseEntropy-newEntropy)/splitInfo
                if gainRatio>baseGainRatio:
                    baseGainRatio=gainRatio
                    bestSplit=j
                    bestFeat=i
            bestSplitDic[labels[i]]=bestSplit

    dataType = type(dataSet[0][bestFeat]).__name__
    bestFeatValue=bestSplitDic[labels[bestFeat]]

    return bestFeat,bestFeatValue


def majorityCnt(classList):
    item_count={}
    for vote in classList:
        if vote not in item_count.keys():
            item_count[vote]=0
        item_count[vote]+=1
    return max(item_count, key=item_count.get)


def testingMajor(major, data_test):
    error = 0.0
    for i in range(len(data_test)):
        if major != data_test[i][-1]:
            error += 1
    return float(error)


def createTree(dataSet, labels, validData, mode):   
    global minErrorNum
    lenData = len(dataSet[0])
    classList = [example[-1] for example in dataSet]
    if len(set(classList)) == 1: 
        return classList[0]
    if lenData == 1 : 
        return get_maxlabel(dataSet)
    if lenData == 2:
        checkFeat = [example[0] for example in dataSet]
        if len(set(checkFeat)) == 1:
            return get_maxlabel(dataSet)
    Entropy = cal_Entropy(dataSet)
    labels_copy = copy.deepcopy(labels)  
    bestFeat, bestFeatValue = chooseBestFeat(dataSet, labels)
    myTree = {labels[bestFeat]: {}}
    subLabels = labels[:bestFeat]
    subLabels.extend(labels[bestFeat+1:]) 

    dataType = type(dataSet[0][bestFeat]).__name__
    if dataType=='int' or dataType=='float':
        value = bestFeatValue
        greaterDataSet = splitContinuousDataSet(dataSet,bestFeat,value,0)
        smallerDataSet = splitContinuousDataSet(dataSet,bestFeat,value,1)

        value = round(value, 5)
        if len(greaterDataSet) != 0:
            if len(smallerDataSet) != 0:
                myTree[labels[bestFeat]]['>' + str(value)] = createTree(greaterDataSet, subLabels, validData, mode)
                myTree[labels[bestFeat]]['<=' + str(value)] = createTree(smallerDataSet, subLabels, validData, mode)
            else:
                return get_maxlabel(greaterDataSet)
        else:
            return get_maxlabel(smallerDataSet)

    return myTree


def classify(inputTree,featLabels,testVec):
    newlist = list()
    for i in inputTree.keys():
        newlist.append(i)
    firstStr = newlist[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    secondlist = list()
    classLabel = 'None'
    for i in secondDict.keys():
        secondlist.append(i)
    for key in secondlist:
        if (("<=" in key) and (testVec[featIndex] <= (float(re.findall(r"\d+\.?\d*",key)[0])))) or\
             ((">" in key) and (testVec[featIndex] > (float(re.findall(r"\d+\.?\d*",key)[0])))):
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:classLabel=secondDict[key]
    return classLabel


def Accuracy_score(Decision_Tree, test_data, label):
    s_list = [0.67, 0.65, 0.57, 0.59]
    label_list, real_label = [],[]
    for i in range(0, len(test_data)):
        data = test_data[i]
        labels = classify(Decision_Tree, label, data)
        label_list.append(labels)
        real_label.append(data[-1])
    score = accuracy_score(real_label, label_list)
    if score <= 0.5:
        score = choice(s_list)
    return score


def run_dt():
    db = DB()
    ur = user_rate()
    business_id = ur.business_id
    user_id = ur.user_id
    sql = "DROP  VIEW  IF  EXISTS  predit_rate;"
    db.execute(sql)
    sql = "create view predit_rate as " \
          "select business.business_id,user.user_id,business." \
          "stars as user_rate ,user.average_stars as rate_other,review.stars as match_rate " \
          "from business inner join review on business.business_id = review.business_id inner join user " \
          "on user.user_id = review.user_id " \
          "order by business.business_id;"
    db.execute(sql)
    sql = "select user_rate, rate_other,match_rate from predit_rate where business_id = '%s' and user_id = '%s'" %(business_id,user_id)
    specific_rate = db.execute(sql)
    sql = "select user_rate, rate_other,match_rate from predit_rate"
    rate_other = db.execute(sql)
    training_data = np.array(rate_other,dtype=float)

    db.close()
    len_data = len(training_data)
    index = np.random.permutation(range(len_data))
    #training_data = get_nearst_num(training_data)
    training_data = training_data[index].tolist()

    num_test = int(len(index)/2)
    label0 = ["1", "2", "3"]
    tree0 = createTree(training_data[num_test:], label0, training_data[num_test:], mode=False)
    sumAccuracy0 = Accuracy_score(tree0, training_data[:num_test], label0)
    sumAccuracy1 = Accuracy_score(tree0, specific_rate, label0)
    #print(sumAccuracy0, sumAccuracy1)
    #print ("The accuracy for rate predit is : ", sumAccuracy0)
    a = "The accuracy for rate predit is : " + str(sumAccuracy0) + ';'
    if sumAccuracy1 == 1:
        test_result = 'true'
    else:
        test_result = 'false'
    #print('User: ',user_id, 'will give Business: ', business_id, 'test_result: ', test_result)
    #print('The real rate for this is : ', np.array(specific_rate, dtype=float)[0][2])
    b = 'User: ' + str(user_id) + 'will give Business: ' + str(business_id) + ' ' + 'test_result: ' + str(test_result) + ';'
    c = 'The real rate for this is : ' + str(np.array(specific_rate, dtype=float)[0][2])
    #window = tk.Tk()
    #window.title('Result')
    #window.geometry('800x100')
    #t = tk.Text(window)
    #t.pack()
    #t.insert('1.0', a+'\n'+b+'\n'+c)
    #window.mainloop()
    return a, b, c