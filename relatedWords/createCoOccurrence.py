import os
import sys
import codecs
import gzip
import numpy as np
import random
import collections

class WordRecommender:
	def __init__(self):
		self.coOccurrenceMatrix = dict()
		self.rankMatrix = dict()
		self.overallFrequency = dict()
		self.tokenIds = dict()
		self.tokenNames = dict()
		self.tokenCounter = 0
		self.difficultyScores = dict()
		self.userDifficultyScore = 2.0
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

					if self.filesProcessed == 2:
						self.halt = True
						break

					print "Processing file no " + str(self.filesProcessed)
					doc_cnt = 0
					for l in f:

						if l.startswith("<doc"):
							#print "doc_cnt", doc_cnt
							doc_cnt += 1
							docTokens = set()

						elif l.startswith("</doc>"):
							for tokenId in docTokens:
								if not tokenId in self.coOccurrenceMatrix:
									self.coOccurrenceMatrix[tokenId] = dict()

							for tokenId1 in docTokens:
								for tokenId2 in docTokens:

									if tokenId1 == tokenId2:
										continue
									if not tokenId2 in self.coOccurrenceMatrix[tokenId1]:
										self.coOccurrenceMatrix[tokenId1][tokenId2] = 0
									self.coOccurrenceMatrix[tokenId1][tokenId2] += 1

						else:
							tokens = l.strip().split(" ")
							for token in tokens:
								if token.startswith("'"):
									continue
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

		print "len(self.coOccurrenceMatrix):", len(self.coOccurrenceMatrix)
		print "len(tokenNames):", len(self.tokenNames)
		print "len(self.overallFrequency)", len(self.overallFrequency)

		of_matrixStore = open("matrix.txt", 'w')


		for tokenId1 in self.coOccurrenceMatrix:
			ranks = dict()
			for tokenId2 in self.coOccurrenceMatrix[tokenId1]:
				if self.overallFrequency[tokenId2] < 100:
					continue
				if len(self.tokenNames[tokenId2]) == 0 or str(self.tokenNames[tokenId2][0]).isupper():
					continue
				ranks[tokenId2] = self.coOccurrenceMatrix[tokenId1][tokenId2] / float(self.overallFrequency[tokenId2])

			maxNum = 10
			numCnt = 0
	
			self.sortedList = sorted(ranks, key=ranks.get, reverse=True)[:self.nRecom]

			of_matrixStore.write(str(tokenId1) + "\t")
			for token2 in self.sortedList:
				of_matrixStore.write("\t\t" + str(token2) + "\t" + str(ranks[token2]))
			of_matrixStore.write("\n")
		
		of_matrixStore.close()

		of_wordIds = open("wordIds.txt", 'w')
		for tokenId in self.tokenNames:
			of_wordIds.write(str(tokenId) + "\t" + self.tokenNames[tokenId] + "\n")
		of_wordIds.close()
		print "Done."

		of_wordIds = open("frequency.txt", 'w')
		for tokenId in self.tokenNames:
			of_wordIds.write(str(tokenId) + "\t" + str(self.overallFrequency[tokenId]) + "\n")
		of_wordIds.close()
		print "Done."

		freqdist = self.overallFrequency.values()
		p1 = np.percentile(freqdist, 20)
		p2 = np.percentile(freqdist, 40)
		p3 = np.percentile(freqdist, 60)
		p4 = np.percentile(freqdist, 80)

		of_wordIds = open("difficulty.txt", 'w')
		for tokenId in self.overallFrequency:
			freq = self.overallFrequency[tokenId]
			difficulty = 0
			if freq >= p4:
				difficulty = 1
			elif freq >= p3:
				difficulty = 2
			elif freq >= p2:
				difficulty = 3
			elif freq >= p1:
				difficulty = 4
			else:
				difficulty = 5
			of_wordIds.write(str(tokenId) + "\t" + str(difficulty) + "\n")
		of_wordIds.close()
		print "Done."

	def loadPrecomputedStatistics(self):

		of_matrixStore = open("matrix.txt", 'r')
		for l in of_matrixStore:
			lspl = l.split("\t\t\t")
			token1 = int(lspl[0])
			tokens2 = lspl[1]
			odict = collections.OrderedDict()
			for a in tokens2.split("\t\t"):
				#print a
				aspl = a.split("\t")
				odict[int(aspl[0])] = float(aspl[1])
			self.rankMatrix[token1] = odict

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

		of_frequency = open("frequency.txt", 'r')
		for l in of_frequency:
			lspl = l.strip().split("\t")
			tokenid = int(lspl[0])
			#print lspl
			self.overallFrequency[tokenid] = int(lspl[1])
		of_frequency.close()
		#print self.tokenIds

		of_wordIds = open("difficulty.txt", 'r')
		for l in of_wordIds:
			lspl = l.strip().split("\t")
			tokenid = int(lspl[0])
			#print lspl
			self.difficultyScores[tokenid] = int(lspl[1])
		of_wordIds.close()
		#print self.tokenIds


		print "Loaded pre-computed statistics."

	def run(self, word, nRecom):

		self.testWord = word
		self.nRecom = int(nRecom)
		
		if not self.testWord in self.tokenIds:
			return []

#		matrix = self.rankMatrix[self.tokenIds[self.testWord]]
		matrix = self.rankMatrix[self.tokenIds[self.testWord]]
		for key in matrix.keys():
#			print matrix[key]
			matrix[key] = matrix[key] - abs(matrix[key] - self.userDifficultyScore)
#		print "matrix: ", matrix
#		print self.tokenNames
		tokenList = matrix.keys()[:min(len(matrix),self.nRecom)]
		wordList = [self.tokenNames[tokenId] for tokenId in tokenList]
		return wordList

	def updateChosenWords(self, discardedWords, discarded):
		updatedAvg = 0.0
		summands = 0
		for wordToUpdate in wordsToUpdate:
			if not wordToUpdate in self.tokenIds:
				continue
			wordId = self.tokenIds[wordToUpdate]
			# just to be on the safe side
			if wordId == None:
				continue
			summands += 1
			difficulty = self.difficultyScores[wordId]
			updatedAvg += difficulty
		if summands > 0:
			updatedAvg /= summands
		# make no change in this case
		else:
			updatedAvg = self.userDifficultyScore
		
		if discarded:
			print "Avg score of discarded words: ", updatedAvg
		else:
			print "Avg score of accepted words: ", updatedAvg

		if discarded:
			self.userDifficultyScore = self.userDifficultyScore + 0.5 * (updatedAvg - self.userDifficultyScore)
		else:
			self.userDifficultyScore = self.userDifficultyScore + 0.5 * (self.userDifficultyScore - updatedAvg)
		if self.userDifficultyScore < 1.0:
			self.userDifficultyScore = 1.0
		if self.userDifficultyScore > 5.0:
			self.userDifficultyScore = 5.0
		
	def updateDiscardedWords(self, discardedWords):
		self.updateChosenWords(discardedWords, True)

	def updateAcceptedWords(self, acceptedWords):
		self.updateChosenWords(acceptedWords, False)

	def filterListOfWords(self, words, nWords):
		#print words
		newWords = list()
		weights = list()
		weightSum = 0.0
		for word in words:
			if not word in self.tokenIds:
				continue
			tokenId = self.tokenIds[word]
			newWords.append(tokenId)
			#print self.difficultyScores
			#print self.overallFrequency
			weight = abs(self.difficultyScores[tokenId] - self.userDifficultyScore) / self.overallFrequency[tokenId]
			weightSum += weight
			weights.append(weight)
		weights = [(v / float(weightSum)) for v in weights]
		print weights
		results = [self.tokenNames[tokenId] for tokenId in np.random.choice(newWords, size=nWords, replace=False, p=weights)]
		print "Results: ", results
		return results
		
def main():
	obj = WordRecommender()
#	obj.precomputeStatistics(100)
	obj.loadPrecomputedStatistics()
#	sys.exit(0)

	#print obj.userDifficultyScore
	#for i in range(0,10):
	#	sample = random.sample(obj.tokenIds.keys(), 50)
	#	obj.updateDiscardedWords(sample)
	#	print "New user score: ", obj.userDifficultyScore
#
#	print obj.userDifficultyScore
#	for i in range(0,10):
#		sample = random.sample(obj.tokenIds.keys(), 50)
#		obj.updateAcceptedWords(sample)
#		print "New user score: ", obj.userDifficultyScore
	obj.run("football", 10)

if __name__ == '__main__':
    main()

