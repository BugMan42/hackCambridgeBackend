import os
import sys
import codecs
import gzip

coOccurrenceMatrix = dict()
overallFrequency = dict()
tokenIds = dict()
tokenNames = dict()
tokenCounter = 0
filesProcessed = 0
wikipediaCorpusPath = "/media/sb/C7F2-F305/Wikipedia/corpus/"
testWord = "abseiling"

halt = False

for d in os.listdir(wikipediaCorpusPath):
	if halt == True:
		break
	for f in os.listdir(wikipediaCorpusPath + d):

		fileName = wikipediaCorpusPath + d + "/" + f

		print fileName
		if not fileName.endswith(".gz"):
			continue
		with gzip.open(fileName, 'rb') as f:
			filesProcessed+=1
			print str(filesProcessed) + " files processed."
			if filesProcessed == 1000:
				halt = True
				break
			for l in f:

				if l.startswith("<doc"):
					docTokens = set()

				elif l.startswith("</doc>"):

					continue

				else:
					tokens = l.strip().split(" ")
					for token in tokens:
						if not token in tokenIds:
							tokenNames[tokenCounter] = token
							tokenIds[token] = tokenCounter
							overallFrequency[tokenCounter] = 0
							tokenCounter += 1

						tokenId = tokenIds[token]
						overallFrequency[tokenId] += 1
						docTokens.add(tokenId)

				for tokenId1 in docTokens:
					if not tokenNames[tokenId1] == testWord:
						continue
					if not tokenId1 in coOccurrenceMatrix:
						coOccurrenceMatrix[tokenId1] = dict()
					for tokenId2 in docTokens:
						if not tokenId2 in coOccurrenceMatrix[tokenId1]:
							coOccurrenceMatrix[tokenId1][tokenId2] = 0
			#			if not tokenId1 in coOccurrenceMatrix[tokenId2]:
			#				coOccurrenceMatrix[tokenId2][tokenId1] = 0
						coOccurrenceMatrix[tokenId1][tokenId2] += 1
			#			coOccurrenceMatrix[tokenId2][tokenId1] += 1

	#print len(coOccurrenceMatrix)

#print overallFrequency

tokenIdTest = tokenIds[testWord]
ranks = dict()
for tokenIdRec in coOccurrenceMatrix[tokenIdTest]:
	if overallFrequency[tokenIdRec] < 1000:
		continue
	if len(tokenNames[tokenIdRec]) == 0 or str(tokenNames[tokenIdRec][0]).isupper():
		continue
	ranks[tokenNames[tokenIdRec]] = coOccurrenceMatrix[tokenIdTest][tokenIdRec] / float(overallFrequency[tokenIdRec])

maxNum = 100
numCnt = 0

for w in sorted(ranks, key=ranks.get, reverse=True):
	print w, ranks[w]
	numCnt +=1
	if maxNum == numCnt:
		break

print "Done."

