/*
Ginnie White
June 4th, 2018

This is code that holds all graph methods used to solve word ladders
*/

//All imports used are here
import java.util.ArrayList;
import java.util.LinkedList;

public class WordLadderGraph{
    //Creates global variables used elsewhere in the code
    ArrayList<Vertex> aGraph = new ArrayList<Vertex>();
    ArrayList<Vertex> traversalList = new ArrayList<Vertex>();
    
    //Private class that creates Vertexes to store info on the graph
    private class Vertex{
        String word;
        LinkedList<Vertex> neighborList;
        Vertex previous;
        int pathLength;
        
        //Constructor
        public Vertex(String aWord){
            word = aWord;
            neighborList = new LinkedList<Vertex>();
            previous = null;
            pathLength = 0;
        }
        
        //Getter methods
        //Method that takes in nothing, and returns a string that contains the word
        //associated with the vertex
        public String getWord(){
            return word;
        }
        //Method that takes in nothing, and returns a string that contains the word
        //associated with the vertex
        public LinkedList<Vertex> getNeighborList(){
            return neighborList;
        }
        //Method that takes in nothing, and returns an integer that contains the path
        //length associated with the vertex
        public int getPath(){
            return pathLength;
        }
        
        //Setter method
        //Method that takes in an integer, updates the path length, then returns nothing
        public void updatePath(int newValue){
            pathLength = newValue;
        }
    }
    
    //Method that checks to see if the two words have only 1 different character. Takes two words
    //as strings and returns a boolean--true if connected, false otherwise.
    public boolean isConnected(String first, String second){
        int difference = 0;
        //Checks every character in the words against each other
        for (int i = 0; i < first.length(); i++){
            if (first.charAt(i) != second.charAt(i)){
                difference++;
            }
        }
        //Takes care of words that are either identical or off by more than 1 letter
        if (difference != 1){
            return false;
        }
        //Returns true if words are only off by 1 letter
        else{
            return true;
        }   
    }
    
    /*Method that takes in a list of all words of the same size as the desired words, and the two
    wanted words as strings. It calls additional methods to create a graph, perform a 
    BFS traversal on the graph and print out the shortest path. It returns nothing.
    */
    public void makeGraph(ArrayList<String> aList, String startWord, String endWord){
        //Creates a vertex for the starting word and adds it into the graph
        Vertex startVertex = new Vertex(startWord);
        aGraph.add(startVertex);
        //Finds all words off by 1 letter and adds them to the start vertex's
        //neighbors and to the big list
        getNeighbors(startVertex, aList);
        int index = 1;
        //Repeats the process for all other words. Stops when the graph contains the ending word
        //or it runs out of words to check for neighbors
        while (!graphContains(endWord) && (index < aGraph.size())){
            getNeighbors(aGraph.get(index), aList);
            index++;
        }
        //Runs if there is no connection between the words
        if (!graphContains(endWord)){
            System.out.println("Words are not connected.");
        }
        //Otherwise, perform a Breadth First Search on the graph to find the shortest path
        else{
            traversalList = BFS(startVertex, endWord);
            //Initializes end vertex so it can be used in the for loop
            Vertex end = traversalList.get(0);
            //Loops through the traversalList to find the ending vertex 
            for (int k = traversalList.size() - 1; k >= 0; k--){
                String word = traversalList.get(k).getWord();
                if (word.equals(endWord)){
                    end = traversalList.get(k);
                }
            }
            //New ArrayList for the printing of the path
            ArrayList<String> finalPath = new ArrayList<String>();
            //Loops back from the ending vertex by using its previous vertices
            while (end.previous != null){
                finalPath.add(end.getWord());
                end = end.previous;    
            }
            //Prints out final word ladder
            System.out.println("*** WORD LADDER ***");
            System.out.println(startWord);
            for (int j = finalPath.size() - 1; j >= 0; j--){
                System.out.println(finalPath.get(j));
            }
            }
        }
        
    //Takes in a vertex and the ending word. Returns an arrayList of all words traversed
    public ArrayList<Vertex> BFS(Vertex aVertex, String endWord){
        //Loops along the vertex's neighbor list 
        for (int i = 0; i < aVertex.getNeighborList().size(); i++){
            //Gets each neighbor by creating a Linked List
            LinkedList<Vertex> temp = aVertex.getNeighborList();
            Vertex currentVertex = temp.get(i);
            //Adds ending Vertex to traversalList and returns
            if (currentVertex.getWord().equals(endWord)){
                currentVertex.previous = aVertex;
                currentVertex.updatePath(aVertex.getPath() + 1);
                traversalList.add(currentVertex);
                return traversalList;
            }
            //Handles all other words
            else{
                int path = (aVertex.getPath() + 1);
                //Checks the vertices' path lengths against each other. If the current vertex is
                //in the graph already, and its current path length is longer than what would be
                //coming from the new vertex, overwrites the previous vertex and path length
                if (traversalList.contains(currentVertex) && (path < currentVertex.getPath())){
                    currentVertex.previous = aVertex;
                    currentVertex.updatePath(path);
                    traversalList.add(aVertex);    
                }
                //Adds word into traversal list if it is not already there
                if (!traversalList.contains(currentVertex)){
                    currentVertex.previous = aVertex;
                    currentVertex.updatePath(path);
                    traversalList.add(aVertex); 
                }
                //Recursive call to traverse entire graph
                BFS(currentVertex, endWord);    
            }
        }
        //Return to deal with compiling errors
        return traversalList;
    }
    
    //Method that takes in the end word as a string. Returns true if there is a corresponding
    //vertex in the graph, returns false otherwise
    public boolean graphContains(String endWord){
        for (int i = 0; i < aGraph.size(); i++){
            if (aGraph.get(i).getWord().equals(endWord)){
                return true;
            }
        }
        return false;
    }
    
    //Takes in a vertex and an ArrayList of all words of desired size. Adds all words off by 2 letter
    //to the vertex's neighbor list
    public void getNeighbors(Vertex aVertex, ArrayList<String> aList){
        for (int i = 0; i < aList.size(); i++){
            if (isConnected(aVertex.getWord(), aList.get(i))){
                Vertex newWord = new Vertex(aList.get(i));
                //Adds the new word to the vertex list and to the neighbor list only if it is not
                //already there
                aVertex.getNeighborList().add(newWord);
                if (!aGraph.contains(newWord)){
                    aGraph.add(newWord);    
                }
                }
            }
    }
}