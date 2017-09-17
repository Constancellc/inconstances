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

I might have to do something different with scottish universities
'''

includeInterest = True

salary = [0]*100
salary2 = [0]*100
salary3 = [0]*100

perIncrease = [0]*200

nYears = 20
afterNyrs = [0]*1000

RPI = 0.03

mW = 0

changeinMW = 0.02

age = 18
for i in range(0,nYears):
    if age <= 20:
        mW += 5.60*np.power(1+changeinMW,i)*2 # *2000 hours / 1000 to convert from £ -> k£
    elif age <= 24:
        mW += 7.05*np.power(1+changeinMW,i)*2
    else:
        mW += 7.5*np.power(1+changeinMW,i)*2
    age += 1

courseLengths = {} # number of years
courseMode = {} #1 -> full time, 2 -> part-time, 3 -> both
courseTitle = {}

institutionName = {}
instCountry = {}

pathToDocs = '../../Documents/'

tuition = 9.250

passes = {}
fails = {}

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

with open(pathToDocs+'unistats16_2017_08_09_14_01_04/INSTITUTION.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        instCountry[row[1]] = row[2]
        # XF - England, XH - Scotland, XG - NI, XI - Wales
        
with open(pathToDocs+'unistats16_2017_08_09_14_01_04/SALARY.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        courseID = row[2]
        UKPRN = row[1]

        if instCountry[UKPRN] == 'XH': # ignore Scotland
            continue

        if courseMode[courseID] == '2': # ignore part time courses
            continue

        try:
            uni = institutionName[UKPRN]
            course = courseTitle[courseID]
        except:
            continue

        if uni not in passes:
            passes[uni] = 0
            fails[uni] = 0

        totalTuition = tuition*courseLengths[courseID]
        
        totalEarnings = 0.0-totalTuition

        loanBalance = 0

        for i in range(0,courseLengths[courseID]):
            if includeInterest == True:
                loanBalance = loanBalance*(1+RPI+0.03)
                loanBalance += tuition
            else:
                loanBalance += tuition
            

        try:
            medAfter40 = int(row[9])
            medAfter6 = int(row[12])            
            inc = int(100*(medAfter40-medAfter6)/medAfter6*12/34)/100
        except:
            inc = int(25*12/34)/100

        if inc > 0.2:
            inc = 0.2

        med = int(float(row[15])/1000)

        for i in range(0,nYears-courseLengths[courseID]):

            if includeInterest == True:
                if med < 21:
                    loanBalance = loanBalance*(1+RPI)
                elif med >= 41:
                    loanBalance = loanBalance*(1+RPI+0.03)
                else:
                    loanBalance = loanBalance*(1+RPI+0.03*((41-med)/20))

            totalEarnings += med
            med = med*(1+inc)

        totalEarnings -= loanBalance

        diff = int(totalEarnings-mW)
        
        if diff < 0:
            diff = 0
            fails[uni] += 1
        else:
            passes[uni] += 1
        if diff > 900:
            continue
            #print(course,end=' ')
            #print(uni)
    

        afterNyrs[diff] += 1
'''
        instLQ = int(float(row[14])/1000)
        instUQ = int(float(row[16])/1000)

        salary[instMed] += 1
        salary2[instLQ] += 1
        salary3[instUQ] += 1

        '''

for uni in fails:
    print(uni,end=': ')
    print(round(100*fails[uni]/(fails[uni]+passes[uni]),1),end='%\n')
S = sum(afterNyrs)
for i in range(0,len(afterNyrs)):
    afterNyrs[i] = afterNyrs[i]/S
plt.figure(1)
plt.bar(np.arange(0,1000),afterNyrs)
plt.xlim(-1,100)
'''
plt.bar(np.arange(0,100)-0.3,salary2,width=0.3)
plt.bar(np.arange(0,100),salary,width=0.3)
plt.bar(np.arange(0,100)+0.3,salary3,width=0.3)
plt.xlim(10,50)
'''
plt.show()
