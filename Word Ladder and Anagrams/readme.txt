Ginnie White
June 4th, 2018
FINAL PROJECT DESCRIPTION

Included files: WordGames.java, Anagram.java, WordLadderGraph.java, dictionary.txt, readme.txt

**PROGRAM FEATURES***
This program takes on tasks 1 and 2 from the final project list, so it creates word ladders and anagrams. 
The word ladder functionality takes in two strings that the user inputs to the command line and then prints
the shortest ladder between them that uses only valid words (using BFS on a graph). The anagram functionality
takes in one string the user submits to the command line, then prints all anagrams that are valid words using ArrayLists 
and recursion. It should be noted that by "valid words", I mean a word that can be found in dictionary.txt, the same one used
in a previous class assignment. This dictionary does have some weird words in it. Dictionary.txt is included 
in the final zip file. This dictionary could be changed if desired by changing line 36 in WordGames to reflect the new
dictionary file's name.


*** COMMAND LINE SYNTAX ***
For word ladders:

java WordGames ladder startWord endWord

For anagrams:

java WordGames anagram word


*** DATA STRUCTURES ***
In WordGames:

WordGames uses Arrays and ArrayLists, Arrays to parse the command line, and ArrayLists to create word dictionaries
and to print out lists of anagrams and word ladders. It also uses the graph created in WordLadderGraph to solve word
ladders.

In Anagram:

Anagram uses ArrayList. It adds all possible anagrams into an ArrayList.

WordLadderGraph:

WordLadderGraph contains Graphs, LinkedLists, and ArrayLists. LinkedLists and ArrayLists are used in the
construction of the graph, with all vertices in an ArrayList and all neighbors in individual LinkedLists attached
to their respective vertecies.


*** CURRENT STATUS ***
As far as I am aware, both functions of WordGames work as intended. The ladder function can't build ladders 
between words of different lengths, or between strings that aren't valid words. Anagram only prints out words 
that dictionary.txt considers valid.
