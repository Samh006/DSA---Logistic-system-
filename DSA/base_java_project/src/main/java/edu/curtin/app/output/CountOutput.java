package edu.curtin.app.output;

import edu.curtin.app.FsNode;
import edu.curtin.app.criteria.CriteriaSet;
import java.util.List;
import java.util.logging.Logger;

/*************************************************************************************
 * Implements the OutputStrat interface to generate count based report, displaying   *
 * line counts for files and directories.                                            *
 *************************************************************************************/
public class CountOutput implements OutputStrat {
    private static final Logger logger = Logger.getLogger(CountOutput.class.getName());            // logger tied to this class

    // override the OutputStrat interface method to initiate report generatio
    @Override
    public void generate(FsNode root, CriteriaSet criteria) {
        printCount(root, criteria, 0);                       // call the recursive printCount method starting with root node and no initial indentation
    }

    // recursive helper method to print count with indentation
    private int printCount(FsNode node, CriteriaSet criteria, int indent) {
        logger.info("Processing node: " + node.getName());         // logs the processing of the curr node
        
        if (node.isDirectory()) {                                       // check if node is a dir
            // For directories: calculate total count first, then print directory, then children
            int totalCount = calculateDirectoryCount(node, criteria);   // calc the total num of matching line in the dir
            
            // Print the directory with its total count FIRST (dir name and its line count with indentation)
            System.out.printf("%s%s: %d lines%n", " ".repeat(indent), node.getName(), totalCount);
            
            // Then print each child (no recursive call to printCount for counting)
            List<FsNode> children = node.getChildren();    // retrieve the sorted list of child nodes
            for (FsNode child : children) {                // iterate over each child node
                printCount(child, criteria, indent + 2);   // recursivly prints the count for each child with increased indentation
            }
            
            return totalCount;    // return total count for the dir 
        } else {
            // For files: count matching lines and print
            List<String> lines = node.getContents();         // get the list of lines from the file
            int matchCount = 0;                              // counter set to 0
            for (String line : lines) {                      // iterate over each line in the file
                if (criteria.matches(line)) {                // checks if the line matches the criteria
                    matchCount++;                            // add to counter if matches
                }
            }
            System.out.printf("%s%s: %d lines%n", " ".repeat(indent), node.getName(), matchCount);      // print the file name and its match count with indentation
            return matchCount;        // return the count of matching lines
        }
    }
    
    // helper method to calc the total count of matching lines in a dir
    private int calculateDirectoryCount(FsNode dirNode, CriteriaSet criteria) {
        int totalCount = 0;                                    // counter set to 0
        List<FsNode> children = dirNode.getChildren();         // gets the sorted list of child nodes
        
        for (FsNode child : children) {                                       // iterate over each child node
            if (child.isDirectory()) {                                        // if is dir
                totalCount += calculateDirectoryCount(child, criteria);       // recursively adds the count from subdir
            } else {                                                          // else, if its file
                List<String> lines = child.getContents();                     // get the list of lines from the file 
                for (String line : lines) {                                   // iterate  over each line
                    if (criteria.matches(line)) {                             // if it matches the criteria, add to the counter
                        totalCount++;
                    }
                }
            }
        }
        
        return totalCount;        // return the total count of matching lines in the directory
    }
}