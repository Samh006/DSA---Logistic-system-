package edu.curtin.app;
import java.util.List;

/* interface for files and directories (Composite design pattern) */
public interface FsNode {
    
    String getName();         // retrieve the name of the node (file or dir)
    boolean isDirectory();    // check if the node is a dir 

    // default; unsupported for files
    default void addChild(FsNode child){                                                      // adding child node, intended for dir, with a default implementation 
        throw new UnsupportedOperationException("Cant add children to this node.");   // throw exception if called on a file
    }

    // default; empty for files
    default List<FsNode> getChildren(){          // retrieve a list of child  nodes, intended for dir, with a default empty 
        return List.of();                        // returns an empty immbutable list, for when no children exist 
    }

    // default; empty for directories 
    default List<String> getContents(){          // retrieve the contents of the node, intended for files, default empty 
        return List.of();                        // returns an empty immbutable list, for when no content exists
    } 

    
}
