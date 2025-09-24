package edu.curtin.app;

import edu.curtin.app.criteria.CriteriaSet;
import edu.curtin.app.output.OutputStrat;
import edu.curtin.app.output.CountOutput;
import edu.curtin.app.output.ShowOutput;
import java.nio.file.Path;                 // file system path 
import java.util.ArrayList;                // dynamic collection 
import java.util.List;                     // collection
import java.util.Scanner;
import java.util.logging.Level;            // logging severity
import java.util.logging.Logger;

/*********************************************************************************************
 * Main application class for directory search, handling user input and report generation.   *
**********************************************************************************************/
public class App {
    private static final Logger logger = Logger.getLogger(App.class.getName());       // static logger to log events

    /*****************************************************************************
     * Entry point: loads directory, initializes criteria, and runs menu loop.   *
     * args Command-line arguments, optionally specifying directory path.        *
     *****************************************************************************/
    public static void main(String[] args){
        String dir = (args.length > 0) ? args[0] : ".";          // dir path set to the first args, else use "." curr dir 
        DirectLoader loader = new DirectLoader();                // instance of DirectLoader to load dir struct 
        FsNode root;                                             // vartiable to hold the root FsNode of the dir tree           

        try{
            root = loader.load(Path.of(dir));                                    // load the dir tree using the loader and assign root node 
            logger.info("Directory tree loaded from: " + dir);                   // logs info 
        } catch (IllegalArgumentException e) {                                   // if dir is invalid
            logger.log(Level.SEVERE, "Failed to load directory: " + dir, e);
            System.out.println("Error: Could not load directory '" + dir + "'. Please check the path and try again.");
            return;                                                              // exit main, relaunch needed 
        }

        CriteriaSet criteria = new CriteriaSet();                    // create a new CriteriaSet instance for managing search criteria 
        criteria.setCriteria(List.of("+ r .*"));                  // set the default criteria to inc all lines via a regex that matches everyting
        OutputStrat outputStrat = new CountOutput();                 // output start set to count by default 
        Scanner sc = new Scanner(System.in);                         // user input

        while (true){
            System.out.println("\nMenu:");
            System.out.println("1) Set Criteria");
            System.out.println("2) Set Output Format");
            System.out.println("3) Report");
            System.out.println("4) Quit");
            System.out.print("Choice: ");

            String choice = sc.nextLine().trim();                    // read user input line, trim space 

            switch (choice){
                case "1": 
                    criteria = setCriteria(sc);                                       // call setCriteria to update the search criteria 
                    logger.info("Criteria updated with " + criteria.toString());      // log the updated criteria 
                    break;
                case "2":
                    outputStrat = setOutputFormat(sc);                                                           // call setOutputFormat to update the output format
                    logger.info("Output strategy updated to: " + outputStrat.getClass().getSimpleName());        // log the updated output strat class name 
                    break;
                case "3":
                    logger.info("Generating report with strategy: " + outputStrat.getClass().getSimpleName());   // logs the start of reporting 
                    runReport(root, criteria, outputStrat);                                                      // call runReport to generate report 
                    logger.info("Report generation completed");                                              // log the completion of reporting 
                    break;
                case "4":
                    System.out.println("Exiting...");
                    logger.info("Application terminated.");                  // log the status of the app  
                    return;
                default:
                    System.out.println("Invalid choice. Try again.");
                    logger.warning("Invalid menu choice: " + choice);            // warning for invalid menu choice 
            }
        }
    }

    /***********************************************************************************
     * Prompts user to enter search criteria and returns a populated CriteriaSet.      *
     * sc Scanner for reading user input.                                              *
     * return returns a CriteriaSet with parsed criteria.                              *
     ***********************************************************************************/
    private static CriteriaSet setCriteria(Scanner sc){
        CriteriaSet newCriteria = new CriteriaSet();           // create a new CriteriaSet instance 
        List<String> inputLines = new ArrayList<>();           // create a new arraylist to store user input lines

        System.out.println("Enter criteria lines ([+/-] [t/r] [text]), blank line to finish:");
        boolean continueReading = true;
        while (continueReading){                   // start a infinite loop to read criteria lines until a blank line 
            String line = sc.nextLine().trim();    // read line, trim space 
            if (line.isEmpty()){                   // check if the line is empty
                continueReading = false;   
            } else {
            inputLines.add(line);                  // add the non empty line to the list 
            }
        }

        newCriteria.setCriteria(inputLines);       // set the criteria in the new CriteriaSet using the input lines
        return newCriteria;                        // return the populated CriteriaSet
    }

    /**************************************************************************
     * Prompts user to choose between count or show output formats.           *
     * sc Scanner for reading user input.                                     *
     * return returns an OutputStrat instance (CountOutput or ShowOutput).    *
     **************************************************************************/
    private static OutputStrat setOutputFormat(Scanner sc){
        System.out.println();
        System.out.println("Choose output format:");
        System.out.println("1) Count (default)");
        System.out.println("2) Show");
        System.out.print("Choice: ");
        String choice = sc.nextLine().trim();                        // read user input, trim space 

        if (choice.equals("2")){
            System.out.println("Output format set to show");
            return new ShowOutput();                                // return a new Showoutput instance 
        } else {
            System.out.println("Output format set to default (count)");
            return new CountOutput();                               // else, return a new CountOutput instance 
        }
    }

    /*****************************************************************************
     * Runs the report using the specified criteria and output strategy.         *
     * Root node of the directory tree.                                          *
     * Criteria for filtering lines.                                             *
     * OutputStrat for formatting the report.                                    *
     *****************************************************************************/
    private static void runReport(FsNode root, CriteriaSet criteria, OutputStrat outputStrat){
        if (outputStrat == null) {               // check if output start is null (as a safeguard)
            outputStrat = new CountOutput();     // sets to default strat
        }
        outputStrat.generate(root, criteria);    // call the generate method on the output strat to generate report 
    }
}
