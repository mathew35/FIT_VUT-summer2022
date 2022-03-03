package ija.homework1.uml;

import java.util.List;

public class UMLClass  extends UMLClassifier{
    private boolean isAbstract;
    public UMLClass(String name){
        super(name);
        this.isAbstract = false;
    }
    public boolean isAbstract(){
        return this.isAbstract;
    }
    public void setAbstract(boolean isAbstract){
        this.isAbstract = isAbstract;
    }
    public boolean addAttribute(UMLAttribute attr){
        int pos = getAttrPosition(attr);
        if(pos == -1){
            //addAttribute
        }
        return false;
    }
    public int getAttrPosition(UMLAttribute attr){
        return 1;
    }
    public int moveAttrAtPosition(UMLAttribute attr, int pos){
        return 1;
    }
    public List<UMLAttribute> getAttributes(){
        return null;
    }
}
