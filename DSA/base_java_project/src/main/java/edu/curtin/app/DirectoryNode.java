package edu.curtin.app;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.logging.Logger;

/* Represent a dir containing files and subdirs, implements the fsnode interface to represent a dir */
public class DirectoryNode implements FsNode {
    private static final Logger logger = Logger.getLogger(DirectoryNode.class.getName());  // static logger tied to this class
    private String name;                        // field to store the dir name
    private List<FsNode> children;              // field to store a list of child nodes (files or subdirs)

    // construct to initialize a DirectoryNode with a name 
    public DirectoryNode(String name){
        this.name = name;                        // assign the provided name to the instance field 
        this.children = new ArrayList<>();       // initialize the children list as an empty arraylist
    }

    // Overrides the FsNode interface method to return the directory's name
    @Override
    public String getName(){
        return name;
    }

    // Overrides the FsNode interface method to indicate if this node is a dir
    @Override
    public boolean isDirectory(){
        return true;
    }

    // Overrides the FsNode interface method to add a child node to the dir 
    @Override
    public void addChild(FsNode child) {
        logger.info("Adding child: " + child.getName() + " to directory: " + name);
        children.add(child);
    }

    // Overrides the FsNode interface method to retrieve the list of child nodes
    @Override
    public List<FsNode> getChildren() {
        List<FsNode> sorted = new ArrayList<>(children);         // create a new arraylist with a copy of the children list to avoid modifying the original 
        sorted.sort(Comparator.comparing(FsNode::getName));      // sort the copied list alphabetically by node name via a comparator 
        return sorted;
    }

    // Overrides the FsNode interface method to return the directory's contents
    @Override
    public List<String> getContents() {
        return new ArrayList<>();               // return an empty list as dir do not have content (only files do)
    }
    
}
    

