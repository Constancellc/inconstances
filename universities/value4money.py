# requires the unistats data set () and the register of uk learning providers
# (http://learning-provider.data.ac.uk/)

import csv
import matplotlib.pyplot as plt
import numpy as np
import codecs

'''
things still to do:
- main problem is lack of tuition information
- especially with the placement years


'''


salary = [0]*100
salary2 = [0]*100
salary3 = [0]*100

perIncrease = [0]*200

after10yrs = [0]*1000

mW = (2*5.60+4*7.05+7*7.5)*2000/1000

courseLengths = {} # number of years
courseMode = {} #1 -> full time, 2 -> part-time, 3 -> both
courseTitle = {}

institutionName = {}

pathToDocs = '../../Documents/'

tuition = 9.250

with open(pathToDocs+'learning-providers-plus.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        institutionName[row[0]] = row[1] # UKPRN as key

with open(pathToDocs+'unistats16_2017_08_09_14_01_04/KISCOURSE.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:

        courseID = row[14]

        try:
            courseLengths[courseID] = int(row[23])
        except:
            courseLengths[courseID] = 3
        courseTitle[courseID] = row[27]
        courseMode[courseID] = row[15]
        
with open(pathToDocs+'unistats16_2017_08_09_14_01_04/SALARY.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:

        
        courseID = row[2]
        UKPRN = row[1]

        if courseMode[courseID] == '2': #ignore part time courses
            continue

        try:
            uni = institutionName[UKPRN]
            course = courseTitle[courseID]
        except:
            continue
        
        totalEarnings = 0.0-tuition*courseLengths[courseID]

        try:
            medAfter40 = int(row[9])
            medAfter6 = int(row[12])            
            inc = int(100*(medAfter40-medAfter6)/medAfter6*12/34)/100
        except:
            inc = int(25*12/34)/100

        if inc > 0.2:
            inc = 0.2

        med = int(float(row[15])/1000)


        for i in range(0,10):
            totalEarnings += med
            med = med*(1+inc)

        diff = int(totalEarnings-mW)

        if diff < 0:
            diff = 0
            print(course,end=' ')
            print(uni)

        if diff > 400:
            continue
            #print(course,end=' ')
            #print(uni)
    

        after10yrs[diff] += 1
'''
        instLQ = int(float(row[14])/1000)
        instUQ = int(float(row[16])/1000)

        salary[instMed] += 1
        salary2[instLQ] += 1
        salary3[instUQ] += 1

        '''


plt.figure(1)
plt.bar(np.arange(0,1000),after10yrs)
plt.xlim(0,100)
'''
plt.bar(np.arange(0,100)-0.3,salary2,width=0.3)
plt.bar(np.arange(0,100),salary,width=0.3)
plt.bar(np.arange(0,100)+0.3,salary3,width=0.3)
plt.xlim(10,50)
'''
plt.show()
