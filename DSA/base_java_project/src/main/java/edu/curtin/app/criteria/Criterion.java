package edu.curtin.app.criteria;

/* represents one search criterion: inclusion/exclusion + matcher. */
public class Criterion {

    private final boolean include;          // true = include, false = exclude
    private final LineMatcher matcher;      // store the matcher object that determines if a line matches the criterion 

    // construct to initialize a criterion with inclusion status and matcher
    public Criterion(boolean include, LineMatcher matcher){
        this.include = include;       // assign the inclusion status to the instance field 
        this.matcher = matcher;       // assign the matcher object to the instancee field 
    }

    // check if the criterion is for inclusion 
    public boolean isInclude(){ 
        return include;
    }

    // test if a given line matches the criterion's matcher
    public boolean matches(String line){
        return matcher.matches(line);               // delegates the matching logic to the matcher object, returning the result 
    }
    
}
