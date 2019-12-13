#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'findKangarooScore' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING_ARRAY words
#  2. STRING_ARRAY wordsToSynonyms
#  3. STRING_ARRAY wordsToAntonyms
#

#Currently not implemented for Kangaroo Cousins
def findKangarooScore(words, wordsToSynonyms, wordsToAntonyms):
    lower_case_words = []
    for item in words:
        lower_case_words.append(item.lower())
    final_score = 0
    syn_score = 0
    ant_score = 0
    #Start with the synonym score
    better_wordsToSynonyms = []
    for item in wordsToSynonyms:
        better_wordsToSynonyms.append(item.split(":"))
    for item in better_wordsToSynonyms:
        print(item)
        word_to_compare = item[0].lower()
        #remove word to compare to get list of synonyms
        if word_to_compare in lower_case_words:
            syn_list = item[1].split(",")
            #compare characters of main word to characters of synonym
            for item in syn_list:
                #If the synonym is in the word to compare, then it is not a kangaroo word
                if item.lower() in word_to_compare:
                    continue
                j = 0
                counter = 0
                #iterate over characters of the main word.
                for char in word_to_compare:
                    if j < len(item) and char == item[j].lower():
                        counter += 1
                        j += 1
                if counter == len(item):
                    syn_score += 1
    print(syn_score)

    #now for antonyms
    better_wordsToAntonyms = []
    for item in wordsToAntonyms:
        better_wordsToAntonyms.append(item.split(":"))
    for item in better_wordsToAntonyms:
        word_to_compare = item[0].lower()
        if word_to_compare in lower_case_words:
            #remove word to compare to get list of antonyms
            ant_list = item[1].split(",")
            #compare characters of main word to characters of synonym
            for item in ant_list:
                #If the antonym is in the word to compare, then it is not a kangaroo word
                if item.lower() in word_to_compare:
                    continue
                j = 0
                counter = 0
                #iterate over characters of the main word.
                for char in word_to_compare:
                    if j < len(item) and char == item[j].lower():
                        counter += 1
                        j += 1
                if counter == len(item):
                    ant_score += 1
    print(ant_score)

    final_score = syn_score - ant_score
    return final_score




    return score

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    words_count = int(input().strip())

    words = []

    for _ in range(words_count):
        words_item = input()
        words.append(words_item)

    wordsToSynonyms_count = int(input().strip())

    wordsToSynonyms = []

    for _ in range(wordsToSynonyms_count):
        wordsToSynonyms_item = input()
        wordsToSynonyms.append(wordsToSynonyms_item)

    wordsToAntonyms_count = int(input().strip())

    wordsToAntonyms = []

    for _ in range(wordsToAntonyms_count):
        wordsToAntonyms_item = input()
        wordsToAntonyms.append(wordsToAntonyms_item)

    result = findKangarooScore(words, wordsToSynonyms, wordsToAntonyms)

    fptr.write(str(result) + '\n')

    fptr.close()
