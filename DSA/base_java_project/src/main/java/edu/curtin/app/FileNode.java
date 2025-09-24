package edu.curtin.app;
import java.util.List;

/* Represents a file and its contects (lines of texts stored) */
public class FileNode implements FsNode {
    private final String name;                 // store the file name, immutable after the construct 
    private final List<String> contents;       // store the files content as a list of strings, immutable after the costruct 

    // construct to initialize a FileNode with a name and its contents 
    public FileNode(String name, List<String> contents){
        this.name = name;                 // assign the provided name to the instance field 
        this.contents = contents;         // assign the provided contents list to the instance field 
    }

    // override the fsnode interface method to return the files name 
    @Override
    public String getName(){
        return name;
    }

    // override the fsnode interface method to indicate if this node is a dir 
    @Override 
    public boolean isDirectory(){
        return false;
    }

    // override the fsnode interface method to return the files contents
    @Override
    public List<String> getContents(){
        return contents;
    }
    
}
