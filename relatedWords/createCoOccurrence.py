import os
import sys
import codecs
import gzip

class WordRecommender:
	def __init__(self):
		self.coOccurrenceMatrix = dict()
		self.overallFrequency = dict()
		self.tokenIds = dict()
		self.tokenNames = dict()
		self.tokenCounter = 0
		self.filesProcessed = 0
		self.wikipediaCorpusPath = "/media/sb/C7F2-F305/Wikipedia/corpus/"
		self.testWord = "abseiling"
		self.halt = False

	def run(self):
		for d in os.listdir(self.wikipediaCorpusPath):
			if halt == True:
				break
			for f in os.listdir(self.wikipediaCorpusPath + d):

				fileName = self.wikipediaCorpusPath + d + "/" + f

				print fileName
				if not fileName.endswith(".gz"):
					continue
				with gzip.open(fileName, 'rb') as f:
					self.filesProcessed+=1
					print str(self.filesProcessed) + " files processed."
					if self.filesProcessed == 1000:
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
								if not token in self.tokenIds:
									self.tokenNames[self.tokenCounter] = token
									self.tokenIds[token] = self.tokenCounter
									self.overallFrequency[self.tokenCounter] = 0
									self.tokenCounter += 1

								tokenId = self.tokenIds[token]
								self.overallFrequency[tokenId] += 1
								docTokens.add(tokenId)

						for tokenId1 in docTokens:
							if not self.tokenNames[tokenId1] == self.testWord:
								continue
							if not tokenId1 in self.coOccurrenceMatrix:
								self.coOccurrenceMatrix[tokenId1] = dict()
							for tokenId2 in docTokens:
								if not tokenId2 in self.coOccurrenceMatrix[tokenId1]:
									self.coOccurrenceMatrix[tokenId1][tokenId2] = 0
					#			if not tokenId1 in coOccurrenceMatrix[tokenId2]:
					#				coOccurrenceMatrix[tokenId2][tokenId1] = 0
								self.coOccurrenceMatrix[tokenId1][tokenId2] += 1
					#			coOccurrenceMatrix[tokenId2][tokenId1] += 1

			#print len(coOccurrenceMatrix)

		#print overallFrequency

		tokenIdTest = self.tokenIds[self.testWord]
		ranks = dict()
		for tokenIdRec in self.coOccurrenceMatrix[tokenIdTest]:
			if self.overallFrequency[tokenIdRec] < 1000:
				continue
			if len(self.tokenNames[tokenIdRec]) == 0 or str(self.tokenNames[tokenIdRec][0]).isupper():
				continue
			ranks[self.tokenNames[tokenIdRec]] = self.coOccurrenceMatrix[tokenIdTest][tokenIdRec] / float(self.overallFrequency[tokenIdRec])

		maxNum = 100
		numCnt = 0

		for w in sorted(ranks, key=ranks.get, reverse=True):
			print w, ranks[w]
			numCnt +=1
			if maxNum == numCnt:
				break

		print "Done."
		
def main():
	obj = WordRecommender()
	obj.run()

if __name__ == '__main__':
    main()

