package ija.homework1.uml;

import javax.swing.plaf.multi.MultiButtonUI;

public class ClassDiagram extends Element{
    //private String name;
    public ClassDiagram(String name){
        super(name);
    }
    public UMLClass createClass(String name){
        
        //System.out.println("createClass:"+this.getName());
        //System.out.println("createClass in if statement:"+ name);
        return new UMLClass(name);
        //return null;
        
    }
    public UMLClassifier classifierForName(String name){
        UMLClassifier classifier =  findClassifier(name);
        if(classifier == null){
            classifier = new UMLClassifier(name);
        }
        return classifier; 
    }
    public UMLClassifier findClassifier(String name){
        UMLClassifier find = null;
        return find;
    }
}
