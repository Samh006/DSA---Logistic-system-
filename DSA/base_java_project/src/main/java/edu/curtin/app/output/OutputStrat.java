package edu.curtin.app.output;

import edu.curtin.app.FsNode;
import edu.curtin.app.criteria.CriteriaSet;

// strat for generating output based node and criteria 
public interface OutputStrat{
    void generate(FsNode root, CriteriaSet criteria);           // gen output , taking root fsnode and criteria set as parameteres 
}
