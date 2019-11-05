/*
Ginnie White
June 4th, 2018

This is code that creates all anagrams of a given string and adds them into an ArrayList using recursion
*/

//All imports used
import java.util.ArrayList;

public class Anagram{
    //Method that takes in the two desired words as strings and an ArrayList to add them to
    public void makeAnagrams(String aWord, String anotherWord, ArrayList<String> aList){
        //Handles case where the word is one letter
        if (anotherWord.length() == 1){
            aList.add(aWord + anotherWord);
        }
        //Splits the word into smaller strings in order to make a recursive call
        else{
            for (int i = 0; i < anotherWord.length(); i++){
                String string1 = aWord + anotherWord.substring(i, i + 1);
                String string2 = anotherWord.substring(0, i) + anotherWord.substring(i + 1);
                makeAnagrams(string1, string2, aList);
            }
        }
    }
}