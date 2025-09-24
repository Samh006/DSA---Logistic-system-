package edu.curtin.app.output;

import edu.curtin.app.FsNode;
import edu.curtin.app.criteria.CriteriaSet;
import java.util.Comparator;
import java.util.List;
import java.util.logging.Logger;

/**************************************************************************
 * Generates show-based reports, displaying matching lines with numbers   *
 * Implements the outputstrat class                                       *
***************************************************************************/
public class ShowOutput implements OutputStrat {
    private static final Logger logger = Logger.getLogger(ShowOutput.class.getName());     // logger tied to this class

    // overrides the outputstrat interface to initiate report generation
    @Override
    public void generate(FsNode root, CriteriaSet criteria) {              
        printShow(root, criteria, 0);      // calls the recursive printshow starting with the root node and no initial indentation
    }

    // recursive helper method to print matching line with indentation 
    private void printShow(FsNode node, CriteriaSet criteria, int indent) {
        logger.info("Processing node: " + node.getName());                            // logs the processing of that node
        System.out.printf("%s%s:%n", " ".repeat(indent), node.getName());      // print the node name with indentation, followed by a colon and newline
        if (node.isDirectory()) {                                    // if node is dir
            List<FsNode> children = node.getChildren();              // get the sorted list of child nodes
            children.sort(Comparator.comparing(FsNode::getName));    // sort the children alphabetically by name
            for (FsNode child : children) {                          // iterate over each child node
                printShow(child, criteria, indent + 2);              // recursively print the show output for each child with increased indentation
            }
        } else {         // else if file
            List<String> lines = node.getContents();          // get the list of line from the file
            for (int i = 0; i < lines.size(); i++) {          // iterate over each line with its index
                String line = lines.get(i);                   // get the curr line
                if (criteria.matches(line)) { 
                    System.out.printf("%s%d %s%n", " ".repeat(indent + 2), i + 1, line);          // if line matches critertia, print the line number (1-based) and the matching line with indentation
                }
            }
        }
    }
}