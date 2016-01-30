import os
import sys
import codecs
import gzip

class WordRecommender:
	def __init__(self):
		self.coOccurrenceMatrix = dict()
		self.rankMatrix = dict()
		self.overallFrequency = dict()
		self.tokenIds = dict()
		self.tokenNames = dict()
		self.tokenCounter = 0
		self.filesProcessed = 0
		self.wikipediaCorpusPath = "/media/sb/C7F2-F305/Wikipedia/corpus/"
		self.halt = False
		self.words = set()

	def precomputeStatistics(self, nRecom):
		self.nRecom = nRecom
		for l in open("words.txt"):
			self.words.add(l.strip())
		print "Words loaded."
		
		for d in os.listdir(self.wikipediaCorpusPath):
			if self.halt == True:
				break
			for f in os.listdir(self.wikipediaCorpusPath + d):

				fileName = self.wikipediaCorpusPath + d + "/" + f

				if not fileName.endswith(".gz"):
					continue
				with gzip.open(fileName, 'rb') as f:
					self.filesProcessed+=1

					#if self.filesProcessed == 1000:
					#	self.halt = True
					#	break

					print "Processing file no " + str(self.filesProcessed)

					for l in f:

						if l.startswith("<doc"):
							docTokens = set()

						elif l.startswith("</doc>"):

							continue

						else:
							tokens = l.strip().split(" ")
							for token in tokens:
								if not token in self.words:
									continue
								if token.strip() == "":
									continue
								if not token in self.tokenIds:
									self.tokenNames[self.tokenCounter] = token
									self.tokenIds[token] = self.tokenCounter
									self.overallFrequency[self.tokenCounter] = 0
									self.tokenCounter += 1

								tokenId = self.tokenIds[token]
								self.overallFrequency[tokenId] += 1
								docTokens.add(tokenId)

					for tokenId1 in docTokens:
						if not tokenId1 in self.coOccurrenceMatrix:
							self.coOccurrenceMatrix[tokenId1] = dict()
						for tokenId2 in docTokens:
							if tokenId1 == tokenId2:
								continue
							if not tokenId2 in self.coOccurrenceMatrix[tokenId1]:
								self.coOccurrenceMatrix[tokenId1][tokenId2] = 0
				#			if not tokenId1 in coOccurrenceMatrix[tokenId2]:
				#				coOccurrenceMatrix[tokenId2][tokenId1] = 0
							self.coOccurrenceMatrix[tokenId1][tokenId2] += 1
				#			coOccurrenceMatrix[tokenId2][tokenId1] += 1

			#print len(coOccurrenceMatrix)

		#print overallFrequency

		#print self.coOccurrenceMatrix

		of_matrixStore = open("matrix.txt", 'w')


		for tokenId1 in self.coOccurrenceMatrix:
			ranks = dict()
			for tokenId2 in self.coOccurrenceMatrix[tokenId1]:
				if self.overallFrequency[tokenId2] < 1000:
					continue
				if len(self.tokenNames[tokenId2]) == 0 or str(self.tokenNames[tokenId2][0]).isupper():
					continue
				ranks[tokenId2] = self.coOccurrenceMatrix[tokenId1][tokenId2] / float(self.overallFrequency[tokenId2])

			maxNum = 10
			numCnt = 0
	
			self.sortedList = sorted(ranks, key=ranks.get, reverse=True)[:self.nRecom]

			of_matrixStore.write(str(tokenId1) + "\t")
			for token2 in self.sortedList:
				of_matrixStore.write("\t" + str(token2))
			of_matrixStore.write("\n")
		
		of_matrixStore.close()

		of_wordIds = open("wordIds.txt", 'w')
		for tokenId in self.tokenNames:
			of_wordIds.write(str(tokenId) + "\t" + self.tokenNames[tokenId] + "\n")
		of_wordIds.close()
		print "Done."

	def loadPrecomputedStatistics(self):

		of_matrixStore = open("matrix.txt", 'r')
		for l in of_matrixStore:
			lspl = l.split("\t\t")
			token1 = int(lspl[0])
			tokens2 = lspl[1]
			self.rankMatrix[token1] = [int(a) for a in tokens2.split("\t")]

		of_matrixStore.close()

		of_wordIds = open("wordIds.txt", 'r')
		for l in of_wordIds:
			lspl = l.strip().split("\t")
			tokenid = int(lspl[0])
			#print lspl
			self.tokenNames[tokenid] = lspl[1]
			self.tokenIds[lspl[1]] = tokenid
		of_wordIds.close()
		#print self.tokenIds
		print "Loaded pre-computed statistics."

	def run(self, word, nRecom):

		self.testWord = word
		self.nRecom = int(nRecom)
		wordList = [self.tokenNames[tokenId] for tokenId in self.rankMatrix[self.tokenIds[word]][:self.nRecom]]
		print wordList
		return wordList

		
def main():
	obj = WordRecommender()
	obj.precomputeStatistics(100)
	#obj.run(word, nRecom)

if __name__ == '__main__':
    main()

