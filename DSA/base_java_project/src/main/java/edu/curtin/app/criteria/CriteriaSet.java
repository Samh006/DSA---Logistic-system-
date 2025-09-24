package edu.curtin.app.criteria;
import java.util.ArrayList;          // dynamic storage of criteria
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/* Holds a list of criteria and applies them to lines. */
public class CriteriaSet{
    private static final Logger logger = Logger.getLogger(CriteriaSet.class.getName());     // logging tied to this class 
    private final List<Criterion> criteria = new ArrayList<>();                             // store a list of Criterion objects, initialized as an empty arrlist

    // construct to initialize a criteria set with a default criterion
    // Default: include everything
    public CriteriaSet(){
        try{ 
            criteria.add(new Criterion(true, new RegexMatcher(".*")));        // inc all lines via a regex matching anything
        } catch(Exception e){
            logger.log(Level.WARNING, "Default regex failed", e);
        }
    }

    public void clear(){    // remove all criteria from the set 
        criteria.clear();   // clears the list
    }

    // add a single criterion to the set
    public void addCriterion(Criterion criterion){   
        criteria.add(criterion);                   
    }

    // set criteria based on a list of input lines from the user
    public void setCriteria(List<String> inputLines){
        criteria.clear();                               // clears existing criteria before adding a new one 

        for(String input : inputLines){                 // iterate over each input line 
            if(input.isBlank()){                        // if input line is blank-
                continue;                               // -skip processing
            }

            // try block to handle parsing exception
            try{
                String[] parts = input.trim().split(" ", 3);    // split the input upto 3 parts: include/exclude, type and text 
                if(parts.length < 3){                                       // check if the split was fewer than 3 
                    logger.warning("Invalid criterion: " + input);          // log a warning for it 
                    continue;                                               // skip to the next input
                }

                boolean include = parts[0].equals("+");            // determine if the criterion is inclusive based on the first part 
                String type = parts[1];                                     // extract the type
                String text = parts[2];                                     // extract the text or regex

                if (text.isEmpty() || text.isBlank()) {                     // check if the text part is empty or is blank
                    logger.warning("Invalid criterion - text cannot be empty: " + input); 
                    continue;                                               // skip to the next input 
                }
                
                if (text.contains("\n") || text.contains("\r")) {       // check for prohibited newline or carriage return characters
                    logger.warning("Invalid criterion - text cannot contain newlines or carriage returns: " + input);
                    continue;                                               // skip to the next input 
                }

                // Validate include/exclude part
                if (!parts[0].equals("+") && !parts[0].equals("-")) {             // check if the first part is neither + or -
                    logger.warning("Invalid criterion - must start with + or -: " + input);
                    continue;
                }

                // declare matcher variable 
                LineMatcher matcher;
                if(type.equals("t")){            // check if the type is t for plain text
                    matcher = new PlainTextMatch(text);   // if so, create a PlainTextMatch object for text matching
                }
                else if(type.equals("r")){       // else, if the type is r for regex
                    matcher = new RegexMatcher(text);     // create a RegexMatcher object for regex matching
                }
                else{
                    logger.warning("Unknown type in criterion (must be 't' or 'r'): " + input);
                    continue;
                }

                criteria.add(new Criterion(include, matcher));     // adds a new criterion with the determined include status and matcher

            } catch(Exception e){
                logger.log(Level.SEVERE, "Failed to parse criterion: " + input, e);
            }
        }

        // Ensure at least default "match everything"
        if(criteria.isEmpty()){                             // check if no valid criteria was added 
            try{
                criteria.add(new Criterion(true, new RegexMatcher(".*")));     // adds a default criterion to include all lines
            }
            catch(Exception e){
                logger.log(Level.SEVERE, "Default regex failed", e);
            }
        }
    }

    // Check if a line should be included based on the criteria
    public boolean matches(String line){
        for(Criterion c : criteria){                  // iterate over all criteria
            if(!c.isInclude() && c.matches(line)){    // checks for an exclusion criterion that matches the line
                return false;                         // exclusion wins immediately
            }
        }

        // Then check for inclusions - if any inclusion matches, return true
        for(Criterion c : criteria){
            if(c.isInclude() && c.matches(line)){
                return true;
            }
        }

        // If no inclusions match, return false
        return false;
    }
}