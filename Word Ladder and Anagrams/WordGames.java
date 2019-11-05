/*
Ginnie White
June 4th, 2018

This is code that runs the main function for the word ladder and anagrams
*/

//Contains all imports needed for the code
import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;

public class WordGames{
    /*
    Main function that parses the command line and runs the appropriate function
    */
    public static void main(String[] args) {
        
        // Check the command-line syntax. Prints errors if needed
        if (args.length > 3 || args.length < 2) {
            System.err.println("Usage for Word Ladders: java WordGames ladder startWord endWord");
            System.err.println("Usage for Anagrams: java WordGames anagram string");
            System.exit(1);
        }
        
        String word = "";
        String startWord = "";
        String endWord = "";
        File inputFile = null;
        Scanner scanner = null;
        String gameType = args[0];
        
       //Reads the given dictionary file
        inputFile = new File("dictionary.txt");
        try {
            scanner = new Scanner(inputFile);
        } catch (FileNotFoundException e) {
            System.err.println(e);
            System.exit(1);
        }
        
        //Puts all the words in the dictionary file into an ArrayList
        ArrayList<String> dictionary = new ArrayList<String>();
        while (scanner.hasNextLine()){
            String line = scanner.nextLine().toLowerCase();
            line.replace("/n", "");
            String[] thisLine = line.split(" ");
            ArrayList<String> listLine = new ArrayList<String>(Arrays.asList(thisLine));
            //Adds every word in the line into the array list
            for (int i = 0; i < listLine.size(); i++){
                dictionary.add(listLine.get(i));
            }
        }
        scanner.close();
        
        //Runs if the user wants anagrams
        ArrayList<String> anagramList = new ArrayList<String>();
        if (gameType.equals("anagram")){
            word = args[1];
            Anagram anagramMaker = new Anagram();
            anagramMaker.makeAnagrams("", word, anagramList);
            //Print out all the combos that are valid words
            System.out.println("*** ANAGRAMS ***");
            for (int i = 0; i < anagramList.size(); i++){
                String wordToCheck = anagramList.get(i);
                //Only prints the word if it is a valid word in the dictionary
                if (dictionary.contains(wordToCheck)){
                    System.out.println(anagramList.get(i));    
            }
        }    
        }
        //Runs if the user wants word ladders
        ArrayList<String> ladderDictionary = new ArrayList<String>();
        WordLadderGraph finalGraph = new WordLadderGraph();
        if (gameType.equals("ladder")){
            startWord = args[1];
            endWord = args[2];
            //Checks to make sure the start and end words are the same length
            int target = startWord.length();
            int secondLength = endWord.length(); 
            if (target != secondLength){
                System.err.println("Error in word selection. Please make sure the"
                                   + " words are the same length.");
                System.exit(1);
            }
            //Checks to make sure the start word is a valid word
            if (!dictionary.contains(startWord)) {
            System.err.println("Start word is not in dictionary.");
            System.exit(1);
            }
            //Checks to make sure the end word is a valid word
            if (!dictionary.contains(endWord)) {
            System.err.println("End word is not in dictionary.");
            System.exit(1);
            }
            //Adds all words of appropriate size into a new list
            for (int i = 0; i < dictionary.size(); i++){
                if (dictionary.get(i).length() == target){
                    ladderDictionary.add(dictionary.get(i));
                }
            }
            //Calls the makeGraph function to print the word ladder
            finalGraph.makeGraph(ladderDictionary, startWord, endWord);
        }
    }
}