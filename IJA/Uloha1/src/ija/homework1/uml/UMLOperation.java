package ija.homework1.uml;

import java.util.List;

public class UMLOperation extends UMLAttribute{
    //private String name;
    //private UMLClassifier type;
    //private UMLAttribute inst;
    //private List<UMLAttribute> args;
    public UMLOperation(String name, UMLClassifier type){
        super(name, type);
    }
    public static UMLOperation create(String name, UMLClassifier type, UMLAttribute... args){
        UMLOperation inst = new UMLOperation(name, type);
        
        //inst.args = args;
        return inst;        
    }
    public boolean addArgument(UMLAttribute arg){
        return false;
    }
    public List<UMLAttribute> getArguments(){
        return null;
    }
}
