# Kasin Sparks
# 2019 August 25
# Prime Converter 3000
# A simple proof of concept I made to map a prime number to a word
# for my WOW-Classic Character 'Primenumber'

import os
import re
import sys
import requests

encode_mode = 0
decode_mode = 1

encode_string = "/encode"
decode_string = "/decode"

try:
	import readline
except ImportError:
	import pyreadline as readline

file = 'words'

def runCommand(command):
	os.system(command)


## Dr. Cheng's function from class
def is_prime(n):
    if n < 2: return False

    i = 2
    while(i*i <= n):
        if n % i == 0: return False
        i += 1
    return True


## Dr. Cheng's primes function from class
def primes():
    yield 2
    i = 3
    while True:
        if is_prime(i):
            yield i
        i += 2

## Generate the same number of primes as there are words to be used
def createPrimeFile():
	with open('primes', 'w') as f:
		count = 0
		for i in primes():
			if(count >= 466551):
				break
			else:
				print("Generating prime #: " + str(count))
			f.write(str(i) + '\n')
			count += 1
	f.close()

## createPrimeFile()

## For init. start up to map prime number to a word
def createMainFile():
	with open('primes', 'r') as primeFile:
		with open('words.txt', 'r') as wordFile:
			with open('dict.csv', 'w') as dictFile:
				for i in range(0, 466551):
					str1 = primeFile.readline().rstrip('\n')
					str2 = wordFile.readline().rstrip('\n')
					str3 = str1 + ',' + str2 + '\n'
					dictFile.write(str3)
					print('line ' + str(i) + ': ' + str3)
			dictFile.close()
		wordFile.close()
	primeFile.close()


## createMainFile()

## Find a prime based on the given word (key) in the master file
def findInFile(key):
	str0 = key.lower()
	str0 = str0.strip()

	primeNumber = -1

	with open('dict.csv', 'r') as dictFile:

		for line in dictFile:
			str1 = line.rstrip('\n')
			str1 = str1.lower()
			splitResult = str1.split(',')

			if(splitResult[1] == str0):
				primeNumber = splitResult[0]
				break
	dictFile.close()

	return primeNumber

## Load the words and mapped primes to memory
def loadWordsIntoMemory():
	dict = {}

	with open('dict.csv', 'r') as dictFile:

		for line in dictFile:
			str1 = line.rstrip('\n')
			str1 = str1.lower()
			splitResult = str1.split(',')

			dict[splitResult[1]] = splitResult[0]
	dictFile.close()

	return dict

## test
## print(findInFile('test'))

## Convert the list of prime number to a string
def primeListToString(primeList):
	prime_string = ""

	for i in primeList:
		prime_string += str(i)

	return prime_string

## Usage statment
def printHelp():
	print("Usage: python3 main.py [arg]")

## main function
def main():
	mode = encode_mode

	line_string = "Enter a string for conversion >> "

	## Check for command line args
	if len(sys.argv) == 2:
		if(sys.argv[1] == '-e'):
			mode = encode_mode
			line_string = "Enter a prime for conversion >> "
		elif(sys.argv[1] == '-d'):
			mode = decode_mode
			line_string = "Enter a string for conversion >> "
		else:
			printHelp()
			return
	elif len(sys.argv) > 2:
		printHelp()
		return

	## exit string
	exit_string = '/exit'

	## Load the words and primes into memory
	dictionary = loadWordsIntoMemory()

	## Start the auto-completer
	completer = MyCompleter([x[0].lower() for x in dictionary.items()])
	readline.set_completer(completer.complete)
	readline.parse_and_bind('tab: complete')

	## Print the welcome message
	print("Welcome to Prime Number Converter 3000!\n\n")

	while(True):
		user_input = input(line_string).lower()

		#print(user_input[0])

		## Command mode
		if(user_input[0] == '/'):
			user_input = user_input.lower()
			if(user_input == exit_string):
				break
			elif(user_input == encode_string):
				mode = encode_mode
				print("Encoding mode activated")
				line_string = "Enter a prime for conversion >> "
				continue
			elif(user_input == decode_string):
				mode = decode_mode
				print("Decoding mode activated")
				line_string = "Enter a string for conversion >> "
				continue
			elif(user_input == '/help'):
				print("Commands: /exit, /encode, /decode, /help\n"
					  "\tExit: will quit the program.\n"
					  "\tEncode: will take in known English words and convert them to prime numbers based upon the given table of values.\n"
					  "\tDecode: will take a string of prime number and convert them to English words based on the table values.\n"
					  "\tHelp: will give you the list of options and usage.\n"
					  "\tBy hitting tab, a list of possible words will appear.\n")
			else:
				print("Type in /help for help.")
		else:
			## Decode or encode the user's string
			word_list = re.split(r"(\.|\,|\s|\!|\?|\:|\;)", user_input)

			if(mode == encode_mode):
				encode(word_list, dictionary)
				post(user_input)
			elif(mode == decode_mode):
				decode(word_list, dictionary)

## Decode the string of prime numbers
def decode(word_list, dictionary):
	words = []

	for i in word_list:
		##print(i)
		if (i == '\s' or i == ' '):
			words.append(i)
			continue
		elif(i == ''):
			continue

		word = 'NULL'

		for key,value in dictionary.items():
			if i == value:
				word = key
				break

		words.append(word)



	sentence = ""

	for i in words:
		sentence += i

	print("Prime Conversion: " + sentence + '\n')

## Encode the user's string to a list a prime numbers
def encode(word_list, dictionary):
	prime_list = []

	for i in word_list:
		if(i == '\s' or i == ''):
			continue

		try:
			primeNumber = dictionary[i.lower()]
		except:
			primeNumber = i
		finally:
			prime_list.append(primeNumber)

	prime_list_string = primeListToString(prime_list)
	print("Prime Conversion: " + prime_list_string + '\n')

	## copy to the clipboard
	command = 'echo ' + prime_list_string + ' | clip.exe'
	runCommand(command)


## Modified code from https://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python?lq=1
class MyCompleter(object):  # Custom completer

	def __init__(self, options):
		self.options = sorted(options)

	def complete(self, text, state):
		if state == 0:  # on first trigger, build possible matches
			if text:  # cache matches (entries that start with entered text)
				self.matches = [s for s in self.options
								if s and s.startswith(text)]
			else:  # no text entered, all matches possible
				self.matches = self.options[:]

		# return match indexed by state
		try:
			return self.matches[state]
		except IndexError:
			return None

## To post the data to custom web server
def post(rawData):
	try:
		r = requests.post("http://192.168.1.28:5000/submit", data={'word_list': rawData})
		print(r.status_code, r.reason)
	except requests.exceptions.ConnectionError:
		print("Could not connect to the web server.")

## Call to main funciton
main()
