#!/usr/bin/python3
import json
import numpy

class LexiconScore:

		def __init__(self,score):
			self.score=score


def row_data(row):
		row_array = row.strip().split("\t")
		row_array[0].strip()
		#for i in row_array:
		print(row_array[0])
		str.replace(row_array[0],' ','')
		#	str.replace(str.replace(i,' ',''),'\n',''))
			#print(test)
		return row_array


def make_object(line_array):
		score=line_array[1]
		obj = LexiconScore(score)
		return obj


def get_scores(file):
	f = open('Lexicon_dict.json','w')
	dictionary = {}
	with open(file, "r") as fhandle:
		lines = fhandle.readlines()
		for line in lines:
			row_dat = row_data(line)
			o=make_object(row_dat)
			dictionary[row_dat[0]]={"score":int(o.score)}
				
	f.write(json.dumps(dictionary))
	f.close()


get_scores("Lexicons.txt")
