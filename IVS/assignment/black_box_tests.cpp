//======== Copyright (c) 2017, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     Red-Black Tree - public interface tests
//
// $NoKeywords: $ivs_project_1 $black_box_tests.cpp
// $Author:     Matus Vrablik <xvrabl05@stud.fit.vutbr.cz>
// $Date:       $2022-03-03
//============================================================================//
/**
 * @file black_box_tests.cpp
 * @author Matus Vrablik
 * 
 * @brief Implementace testu binarniho stromu.
 */

#include <vector>

#include "gtest/gtest.h"

#include "red_black_tree.h"

//============================================================================//
// ** ZDE DOPLNTE TESTY **
//
// Zde doplnte testy Red-Black Tree, testujte nasledujici:
// 1. Verejne rozhrani stromu
//    - InsertNode/DeleteNode a FindNode
//    - Chovani techto metod testuje pro prazdny i neprazdny strom.
// 2. Axiomy (tedy vzdy platne vlastnosti) Red-Black Tree:
//    - Vsechny listove uzly stromu jsou *VZDY* cerne.
//    - Kazdy cerveny uzel muze mit *POUZE* cerne potomky.
//    - Vsechny cesty od kazdeho listoveho uzlu ke koreni stromu obsahuji
//      *STEJNY* pocet cernych uzlu.
//============================================================================//
class NonEmptyTree: public ::testing::Test{
    virtual void SetUp() {
        const std::vector<int> keys = { 10, 85, 15, 70, 20, 60, 30, 50, 65, 80, 90, 40, 5, 55 };
        for(int i = 0; i < 14; ++i)
            tree.InsertNode(keys[i]);
    }
    protected: BinaryTree tree;
};
class EmptyTree : public ::testing::Test{
    protected: BinaryTree tree;
};
class TreeAxioms: public ::testing::Test{
    protected: BinaryTree tree;
};
TEST_F(EmptyTree,InsertNode){
    EXPECT_TRUE(tree.GetRoot() == NULL);
    int keys[] = {2,5,1,3};
    for(int i = 0; i < 4; i++){
        tree.InsertNode(keys[i]);
    }
    ASSERT_TRUE(tree.GetRoot() != NULL);
    EXPECT_EQ(tree.GetRoot()->key, 2);
    EXPECT_EQ(tree.FindNode(2)->key, 2);
    EXPECT_EQ(tree.FindNode(5)->color, BLACK);
    EXPECT_EQ(tree.FindNode(3)->color, RED);
    EXPECT_EQ(tree.FindNode(5)->pLeft->key, 3);
    tree.InsertNode(9);
    tree.InsertNode(11);
    tree.InsertNode(12);
    tree.InsertNode(15);
    ASSERT_TRUE(tree.GetRoot() != NULL);
    EXPECT_EQ(tree.GetRoot()->key, 5);
};
TEST_F(EmptyTree,DeleteNode){
    EXPECT_FALSE(tree.DeleteNode(2));
};
TEST_F(EmptyTree,FindNode){
    EXPECT_TRUE(tree.FindNode(5) == NULL);

};
TEST_F(NonEmptyTree,InsertNode){
    tree.InsertNode(39);
    EXPECT_TRUE(tree.FindNode(39)->color == RED);
    EXPECT_TRUE(tree.FindNode(39)->pParent == tree.FindNode(40));
};
TEST_F(NonEmptyTree,DeletetNode){
    tree.DeleteNode(70);
    EXPECT_TRUE(tree.FindNode(65)->pRight == tree.FindNode(85));
};
TEST_F(NonEmptyTree,FindNode){
    EXPECT_TRUE(tree.FindNode(75) == NULL);
    EXPECT_TRUE(tree.FindNode(70) != NULL);
};
TEST_F(TreeAxioms,Axiom1){
    std::vector<BinaryTree::Node_t*> leaves;
    ASSERT_NO_THROW(tree.GetLeafNodes(leaves));
    for(Node_t* leaf : leaves){
        EXPECT_TRUE(leaf->pLeft == leaf->pRight);
        EXPECT_TRUE(leaf->pLeft == NULL);
        ASSERT_TRUE(leaf->color == BLACK);
    }
};
TEST_F(TreeAxioms,Axiom2){
    std::vector<BinaryTree::Node_t*> nodes;
    ASSERT_NO_THROW(tree.GetNonLeafNodes(nodes));    
    for(Node_t* node : nodes){
        if(node->color == RED){
            EXPECT_TRUE(node->pLeft->color == BLACK);
            EXPECT_TRUE(node->pRight->color == BLACK);
        }
    }
};
TEST_F(TreeAxioms,Axiom3){
    std::vector<BinaryTree::Node_t*> leaves;
    ASSERT_NO_THROW(tree.GetLeafNodes(leaves));
    int maxCount = -1;
    for(Node_t* node : leaves){
        int count = 0;
        while(node != tree.GetRoot()){
            if(node->color == BLACK){
                count++;
            }
            node = node->pParent;            
        }
        if(maxCount < count){
            if(maxCount == -1){
                maxCount == count;
            }
            else{
                ASSERT_TRUE(false);
            }
        }
    }
};



/*** Konec souboru black_box_tests.cpp ***/
