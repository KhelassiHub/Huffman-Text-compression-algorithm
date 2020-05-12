# an alternative solution to calculate the recurrence number of a character and store it in a dictionary is to use Counter of the collections module
# from collections import Counter  # an alternative solution for findFrequences

class Node: 
	""" The Node class contains all information related to the node"""
	def __init__(self, character, freq, left=None, right=None): # constructor receives as an argument the charactere,
		# its repetetion frequency, its left successor node and its right successor node, 
		# if not specified, the 2 successor nodes are considered as leafs and they'll be assigned the value None
		self.character = character 	# The character attribute stores the character (or the string) represented by the node
		self.freq = freq 	# The freq attribute represents the frequency of the node or the number of repetitions of the represented character divided by the total number of characters
		self.next = {'left': left, 'right': right} 	# dictionary called next which contains 2 nodes 
		# the next node in the left direction and the next node in the right direction,
		# knowing that the left and right nodes are the successor nodes linked with their root node, 
		# if the values of the next dictionary are respectively None then we can deduce that the node is a leaf of the tree  
		self.encoding = ""  # Attribute that contains the huffman encoding equivalent to the character of the node 
	
	def getcharacter(self):
		""" getcharacter method that returns the attribut character of the node """
		return self.character

	def getFreq(self):
		""" getFreq method that returns the attribut freq of the node """
		return self.freq

	def __add__(self, other):
		""" Implementation of the add method of 2 nodes, used in the constructor of the tree class when we need to define a 3rd node from 2 successor nodes """
		node = Node(self.getcharacter() + other.getcharacter(), self.getFreq() + other.getFreq() , self, other)
		return node

	def __str__(self):
		""" Str method which is used to display a node (print (node)) in this case we decided to display the 2 attributes character and freq as display result"""
		return 'character = {} Frequency = {}'.format(self.getcharacter(),self.getFreq())

class Tree:
	""" The Tree class contains all information related to the tree and it's nodes """
	def __init__(self,dicofreq): # the constructor receives as argument the dicofreq dictionary which contains in his keys the characters and in his values their frequency of repetition
		self.codes={} 	# the codes attribute containes the characters of the text as keys, and their equivalent huffman coding as values
		self.NodeList=[]  	 # a tree contains several nodes that they'll be stored in the ListNodes list (from the root node to the leaf nodes)
		for key,value in dicofreq.items():	# browsing the dicofreq dictionary to fill the list of nodes with the created nodes
			self.addNode(Node(key,value)) # use of the addNode method defined below
		while len(self.NodeList)>1:		# browsing the nodes to create the tree, specifying each time for the created node his 2 successor nodes
			NodeMin1 = self.findMin() 		# looking for a second minimum value node
			self.removeNode(NodeMin1)		# removing the node Min1 from the list of nodes 
			NodeMin2 = self.findMin() 		# looking for a second minimum value node
			self.removeNode(NodeMin2) 	# removing the node Min2 from the list of nodes
			Node3 = NodeMin1 + NodeMin2  # create a new node from the values of nodeMin1 and nodeMin2
			self.addNode(Node3) 			# adding the created node in the list

	def compress(self,text):
		""" compress method which is used to compress the text given as an argument based on the self.codes attribute which contains the equivalent coding for each character """
		CompressedText="" # compressed text creation 
		for i in text:	  # browse each character in the text
			CompressedText+=self.codes[f'{i}']  # concatenate the equivalent encoding of each character and store it in CompressedTexter
		return CompressedText # return the final string which contains the equivalent huffman coding of each character of the text given as argument

	def uncompress(self,textComp):
		""" method which is used to decompress the text given as an argument based on the self.codes attribute which contains the equivalent character for each huffman coding value """
		OriginalText=""  # decompressed text creation
		start=0			   # start index of a binary string
		for i in range(1,len(textComp)+1):
			for key,value in self.codes.items():
				if textComp[start:i]==value:	# browse a binary sequence until you find its equivalent in the dictionary self.codes
					OriginalText+=key 		
					start=i 					# updating the starting index 
					break			# optimizing the execution time, if we find the equivalent character of the binary sequence, there is no need to continue browsing the dictionary  
		return OriginalText

	def labeling(self,node):
		""" labeling method which browses the tree by assigning each leaf its equivalent Huffman coding, starting with the root node up to the leaves """
		for direction,FutureNode in node.next.items():		
			if FutureNode==None:					# if we got to the leaves of the tree 
				self.codes[node.character]=node.encoding	# assignment of huffman coding equivalent to character
				return 	# inside the recursive loop we take a step back
			else:
				if direction=='left':
					FutureNode.encoding=f"{node.encoding}0"	# by taking a step to the left we do the concatenation by a character 0
				else:
					FutureNode.encoding=f"{node.encoding}1" 	# by taking a step to the right we do the concatenation by a character 1
			self.labeling(FutureNode) 	# recursive loop

	def findMin(self):
		""" findMin method which returns the Node with the lowest frequency of occurrence """
		freqMinimum = 1		# initial frequency chosen so that freqMinimum takes the 1st value of the 1st iteration because there is no frequency of occurrence greater than 1
		for i in range(len(self.NodeList)):
			if self.NodeList[i].getFreq() < freqMinimum:
				freqMinimum = self.NodeList[i].getFreq()
				index=i
		return self.NodeList[index]

	def removeNode(self,node):
		""" method which removes the node given in argument from the NodeList attribute """
		self.NodeList.remove(node)

	def addNode(self,node):
		""" method which adds the node given as an argument to the NodeList attribute"""
		self.NodeList.append(node)

def findFrequences(text):
	""" Fonction which returns a dictionnary that contains the (set) of characters contained in 
	the text as keys, and as values the number of occurences of each key (character) """
	textLength=len(text)	
	dicofreq={}		
	for character in text:		# for every character in our text
		if character in dicofreq.keys(): # if we already browsed the character and calculated it's number of occurences, we don't need to browse it again 
			pass
		else:
			# for i in range(0,textLength):		# Old way
			# 	if text[i]==character:
			# 		recurence+=1
			recurence = text.count(character)  	# string method count that calculates the number of occurrences of the character in text
			dicofreq[f'{character}']=recurence/textLength  # the value of the character is the frequency of appearance of the character devided by the total size of the characters of the text
	return dicofreq
	# count = Counter(text)     		   # Alternative solution
	# for key,value in count.items():	   # using the dictionnary Counter
	# 	count[key]=value/textLength
	# return count

def main():
	textToCompress=""
	for line in open('VictorHugo.txt','r',encoding='latin-1'): 
	# I had to take in consideration the special characters so i changed the encoder to Latin-1 instead of UTF-8
		textToCompress+=line
	# print(textToCompress) 
	dicofreq = findFrequences(textToCompress)
	G = Tree(dicofreq)
	G.labeling(G.NodeList[0]) # We pass in argument the root node to label the whole tree
	# code displaying 
	# for c,encoding in G.codes.items():
	# 	print('{} : {}'.format(c,encoding))
	CompressedText=G.compress(textToCompress)
	with open("compressedFile.txt", "w") as file:
		file.write(CompressedText)
	# print(CompressedText)
	# Compression ratio display
	print(f'Compression ratio: {100*(len(textToCompress)*8-len(CompressedText))/(len(textToCompress)*8)} %')
	# decomposing the compressed text
	text=G.uncompress(CompressedText)
	# print(text)
	# test to verify that everything works !
	if text == textToCompress:
		print('Nice everything works perfectly !')
	else:
		print('Something is not right, recheck the code or the file !')

if __name__ == '__main__':
	main()
