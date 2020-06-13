#================================================#
# Program: Association Rule Mining using Apriori #
# Author: Md Mahbub Alam                         #
# Email: emahbub.cse@gmail.com                   #
#================================================#

columns = ['Outlook', 'Temperature', 'Humidity', 'Windy', 'PlayTennis']
columnValues = [['sunny', 'overcast', 'rain'], 
		['hot', 'mild', 'cool'], 
		['high', 'normal'], 
		['TRUE', 'FALSE'],
		['P', 'N']]

#Read data from file and creates a 2D list of datasets
def ReadFromFile(fileName):
	try:
		in_file_ptr = open(fileName, 'r')
	except:
		print('\nThere is no file named \'' + fileName + '\', Please check the file path.\n')
	else:
		firstLine = in_file_ptr.readline().strip().split(',')
		dataLines = list()
		for line in in_file_ptr:
			dataLines.append(line.strip().split(','))
		in_file_ptr.close()
		return firstLine, dataLines
		#return dataLines

#Returns total number of tuples in a dataset
def ReturnNumberOfTuples(dataLines):
	count = 0
	for line in dataLines:
		count += 1
	return count

#Eliminate infrequent itemset by Minimum Support
def FilterWithMinSup(itemSet, minSup, numOfTuples):
	filterItems = list()
	for key, value in itemSet.items():
		if(round(float(value)/numOfTuples, 2) >= minSup):
			continue
		else:
			filterItems.append(key)
	for item in filterItems:
		del itemSet[item]
	return itemSet

#Generate first frequent itemset (frequent 1-itemset)
def GenerateFirstFreqItemset(dataLines, minSup, numOfTuples):
	itemSet = dict()
	for row in dataLines:
		for col in row:
			itemSet[str([col])] = itemSet.get(str([col]), 0) + 1
	itemSet = FilterWithMinSup(itemSet, minSup, numOfTuples)
	return itemSet

#Generate length-(k+1) candidate itemsets from length-k frequent itemsets
def Join(itemSetK, k):
	candidateSetK = list()
	for i in range(len(itemSetK)):
		for j in range(i+1, len(itemSetK)):
			iSet = list(itemSetK[i])[:k-2]
			jSet = list(itemSetK[j])[:k-2]
			if(iSet == jSet): #if first k-2 items are same
				candidateSetK.append(list(set(itemSetK[i]).union(itemSetK[j])))
	return candidateSetK

#return all subsets of a given set
def SubsetsAll(itemSet):
	if(itemSet == []):
		return [[]]
	subSet = SubsetsAll(itemSet[1:])
	return subSet + [[itemSet[0]] + item for item in subSet]

#return subsets of length-k for a given set
def SubsetsK(candSet, start, length, tempList):
	if(length == 0):
		return [tempList]
	else:
		subsetList = list()
		for i in range(start, len(candSet)):
			subsetList.extend(SubsetsK(candSet, i + 1, length - 1, tempList + [candSet[i]]))
		return subsetList

#Eliminate infrequent itemset by second apriori property
#the subsets of a frequent itemset must also be frequent
def Prune(candidateSetK, itemSetK, k):
	filterList = list()
	for candSet in candidateSetK:
		subsetList = SubsetsK(candSet, 0, k - 1, []) #create subset of length-k for a CandidateSet
		#check whether 'itemSetK' contains all the elements of a subset of length-K of a 'candidateSet'
		result =  all(item in itemSetK for item in subsetList) 
		if(result):
			continue
		else:
			filterList.append(candSet)  
	for item in filterList:
		candidateSetK.remove(item)

#Generate candidateSet of length-k+1 using join and prune operation
def GenerateCandidateSet(itemSetK, k):
	candidateSetK = Join(itemSetK, k) #create length-(k+1) candidate itemsets
	Prune(candidateSetK, itemSetK, k) #eliminate infrequent candidateSet
	return candidateSetK

#scan the dataset to eliminate infrequent itemset with minimum support
def FindFreqItemset(dataSets, itemSetK, minSup, numOfTuples):
	freqItemSetK = dict()
	for dataset in dataSets:
		for item in itemSetK:
			if(set(item).issubset(dataset)): #check whether a itemSet is subset of any sets in datasets
				freqItemSetK[str(item)] = freqItemSetK.get(str(item), 0) + 1
	freqItemSetK = FilterWithMinSup(freqItemSetK, minSup, numOfTuples)
	return freqItemSetK

#return k-th itemSet from frequentItemSet for next iteration
def ReturnCurrentItemSetK(freqItemsetK, itemSetK):
	itemSetK.clear()
	for key in freqItemsetK:
		itemSetK.append(eval(key))

#Apriori algorithm to generate frequent itemset
def Apriori(inputData, minSup, numOfTuples):
	#scan dataset once to get frequent 1-itemset
	freqItemsets = GenerateFirstFreqItemset(inputData, minSup, numOfTuples) 

	itemSetK = list()
	ReturnCurrentItemSetK(freqItemsets, itemSetK) #frequent 1-itemset for subsequent iteration
	
	k = 1
	while(len(itemSetK) > 0):
		candidateSetK = GenerateCandidateSet(itemSetK, k + 1) #Generate length-(k+1) candidate itemsets from length-k frequent itemsets
		freqItemsetK = FindFreqItemset(inputData, candidateSetK, minSup, numOfTuples) #Test the candidates against dataset to find frequent (k+1)-itemsets
		ReturnCurrentItemSetK(freqItemsetK, itemSetK)
		freqItemsets.update(freqItemsetK) #update frequent itemsets
		k = k + 1
	return freqItemsets

#return column attribute of dataset for a value
def ReturnColumn(item):
	position = 0
	for colValue in columnValues:
		if item in colValue:
			return columns[position]
		else:
			position += 1

#return association rule as a string
def ReturnString(A, B):
	tempStr = '{'
	for item in A:
		tempStr += ReturnColumn(item) + '=' + item + ', '
	tempStr = tempStr[:-2]
	tempStr += '} => {'
	
	for item in B:
		tempStr += ReturnColumn(item) + '=' + item + ', '
	tempStr = tempStr[:-2]
	tempStr += '}'
	return tempStr

#Generate rules from frequent itemsets
def GenerateRules(freqItemsets, minConf, rules, numOfTuples):
	count = 0
	for key_AB, Sup_AB in freqItemsets.items(): #key==AB
		if(len(eval(key_AB)) > 1):
			subSets = SubsetsAll(eval(key_AB)) #retrieve all subsets of a set
			subSets = list(filter(None, subSets)) #remove empty set
			for A in subSets: #itemSet==A
				B = list(set(eval(key_AB)).difference(A)) #itemSet==B
				if(len(B) > 0):
					conf = Sup_AB/freqItemsets[str(A)] #conf = support(AB)/support(A)
					if(conf >= minConf):
						count += 1
						ruleStr = ReturnString(A, B) #return association rule as a string
						ruleStr = 'Rule#' + str(count) + ': ' + ruleStr
						ruleStr += '\n (Support=' + str(round(float(Sup_AB)/numOfTuples, 2)) + ', Confidence=' + str(round(conf, 2)) + ')'
						rules.append(ruleStr)

#Print generated rules
def PrintRules(rules, minSup, minConf):
	print('\nUser Input:')
	print(' Support: ' + str(minSup) + '\n Confidence: ' + str(minConf))
	print('\nRules:')
	for rule in rules: #writing association rules into a file 'Rules.txt'
		print(' ' + rule + '\n')

#Method for generating rules from a given dataset using Apriori
def RuleMining():
	print('\n')
	while(True):
		try:
			minSup = float(input('Enter the minimum support (fraction value): '))
			minConf = float(input('Enter the minimum confidence (fraction value): '))
		except:
			print('\nSupports only fraction value (float number) for minimum support and confidence!\n')
		else:
			if(minSup <= 0):
				continue

			if(minConf <= 0):
				continue

			#read data from file
			firstLine, dataLines = ReadFromFile('Play_Tennis_Data_Set.csv') #'Play_Tennis_Data_Set.csv'
			break
	
	numOfTuples = ReturnNumberOfTuples(dataLines)

	#Calling Apriori function to generate frequent itemsets
	freqItemsets = Apriori(dataLines, minSup, numOfTuples)

	#Method to generate rules from frequent itemsets
	rules = list()
	GenerateRules(freqItemsets, minConf, rules, numOfTuples)
	
	#write rules into a file named 'Rules.txt'
	PrintRules(rules, minSup, minConf)

	print('Thank you!.\n')

#main function
if __name__ == "__main__":
	RuleMining()
