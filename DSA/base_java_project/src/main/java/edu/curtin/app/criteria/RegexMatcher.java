package edu.curtin.app.criteria;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/* matches if the line matches a regex (anywhere), implementing the LineMatcher interface to match lines against a regex pattern */
public class RegexMatcher implements LineMatcher{
    private final Pattern pattern;                      // field to store the compiled regex pattern, immutable after construct

    // construct to initialize a RegexMatcher with a regex string, throwing an exception if invalid
    public RegexMatcher(String regex) throws IllegalArgumentException{
        try{
            this.pattern = Pattern.compile(regex);      // compiles the provided regex string into a Pattern object
        } catch (Exception e){
            throw new IllegalArgumentException("Invalid regex: " + regex, e);
        }
    }

    // override the LineMatcher interface method to check if a line matches the regex pattern
    @Override
    public boolean matches(String line){
        if (line == null) {                      // check if the line is null to avoid errors 
            return false;
        }
        Matcher matcher = pattern.matcher(line);          // creates a Matcher object to perform matching against the line
        return matcher.find();                            // return true if the regex matches any part of the line, false otherwise
    }
}