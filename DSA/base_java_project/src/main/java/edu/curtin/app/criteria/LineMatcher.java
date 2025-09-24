package edu.curtin.app.criteria;

/* interface for matching a line against a condition */
public interface LineMatcher {
    boolean matches(String line);        // checks if a given line matches the condition, true if yes, false if no
    
}
