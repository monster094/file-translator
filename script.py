#!/usr/bin/env python
#-*-coding: utf-8 -*-

"""
Script for automating translations of common expressions/words
from English to Vietnamese on vinamachines' website
"""

import csv
import sys
import re
from collections import OrderedDict


link = '<p><a title="Chi tiết thông số kĩ thuật "'+ \
       'href="http://vinamachines.com/en/product/denver-dl760/ '+ \
       'target="_blank">Chi tiết thông số kĩ thuật</a></p>'

def ireplace(string, old, new, count=0):
    ''' Behaves like S.replace(), but does so in a case-insensitive
    fashion. '''
    pattern = re.compile(re.escape(old),re.I)
    return re.sub(pattern, new, string, count)

# Reads a CSV file and create a dictionary with it
def dictionary(filename):
    dic = OrderedDict([])
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='#')
        for raw in spamreader:
            if len(raw) != 2:
                print "Problem in CSV file, more than 2 items in a raw"
                print raw
                return None
            dic[raw[0]] = raw[1]
    return dic

# Read the text and change each word in the dic by its Vietnamese translation
def translate(filename, dic):
    f2 = open(filename+'.tmp', 'w')
    with open(filename, 'r') as myFile: 
        for line in myFile:
            line2 = line.lower()
            for oldWord, newWord in dic.iteritems():
                oldWord2 = oldWord.lower()
                liste = line2.split("<"+oldWord2)
                if len(liste) > 1:
                    continue
                line = ireplace(line, oldWord, newWord)
            f2.write(line)   
    f2.write(link)
    f2.close()
    return

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print "Usage: python script.py file1.txt file2.txt ..."
    else:
        dic = dictionary("dic.csv")
        if dic is not None:
            for filename in args[1:]:
                translate(filename, dic)
