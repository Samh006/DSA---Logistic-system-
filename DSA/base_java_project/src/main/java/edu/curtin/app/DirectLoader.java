package edu.curtin.app;

import java.io.IOException;
import java.nio.file.*;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;


/* Utility class to load a directory tree into FsNode objects.*/
public class DirectLoader {
    private static final Logger logger = Logger.getLogger(DirectLoader.class.getName());      // logger tied to this class

    // load a dir tree starting from the given rootpath, returning an fsnode
    public FsNode load(Path rootPath) {
        // Skip hidden files or folders (those starting with ".")
        if (rootPath.getFileName().toString().startsWith(".")) {               // check if the path represents a hidden dir or file
            logger.info("Skipping hidden/system file or directory: " + rootPath);     // log that decision 
            return null;                                                              // indicates nothing to add
        }

        if (!Files.exists(rootPath)) {                                            // check if the path provided exists 
            logger.severe("Path does not exist: " + rootPath);                    
            throw new IllegalArgumentException("Invalid path: " + rootPath);      // throw exception for invalid path 
        }

        // check if the path is a dir 
        if (Files.isDirectory(rootPath)) {               
            DirectoryNode dirNode = new DirectoryNode(rootPath.getFileName().toString());    // create a new DirectoryNode with the dir name

            try (DirectoryStream<Path> stream = Files.newDirectoryStream(rootPath)) {        // opens a stram to iterate over dir contents, auto closing 
                for (Path entry : stream) {                                                  // iterate over each entry in the dir
                    FsNode child = load(entry);                                              // recursively laods the child node (file or subdir)
                    if (child != null) {                                                     // only add non-skipped items
                        logger.info("Adding child: " + entry.getFileName() + " to directory: " + rootPath);
                        dirNode.addChild(child);                                             // add the child node to the dir
                    }
                }
            } catch (IOException e) {
                logger.log(Level.WARNING, "Could not read directory: " + rootPath, e);
            }
            return dirNode;               // return the constructed DirectoryNode

        } else {                          // handle the case where the path is a file
            try {
                List<String> lines = Files.readAllLines(rootPath);                       // reads all lines from the file into a list
                return new FileNode(rootPath.getFileName().toString(), lines);           // return a new FileNode with the file name and contents 
            } catch (IOException e) {
                logger.log(Level.WARNING, "Could not read file: " + rootPath, e);
                return new FileNode(rootPath.getFileName().toString(), List.of());       // return a FileNode with empty content list if reading fails 
            } 
        }
    }
}
