package edu.curtin.app.criteria;

/* matches if the line contains a given substring */
public class PlainTextMatch implements LineMatcher {
    private final String text;          // field to store the substring to match, immutable after construct

    // construct to initialize a plain text matcherwith a substring 
    public PlainTextMatch(String text){
        this.text = text;                   // assign the provided text to the instance field 
    }

    // override the LineMatcher interface method to check if a line contains the stored substring
    @Override
    public boolean matches(String line){         
        if (line == null) {                      // check if the input line is null to avoid NullPointerException
            return false;                        // return false if line in null 
        }
        return line.contains(text);              // returns true if the line contains the substring, false otherwise (hello != Hello)
    }
    
}
