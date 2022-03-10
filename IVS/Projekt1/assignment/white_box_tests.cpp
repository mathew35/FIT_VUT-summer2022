//======== Copyright (c) 2021, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     White Box - Tests suite
//
// $NoKeywords: $ivs_project_1 $white_box_code.cpp
// $Author:     Matus Vrablik <xvrabl05@stud.fit.vutbr.cz>
// $Date:       $2022-03-03
//============================================================================//
/**
 * @file white_box_tests.cpp
 * @author Matus Vrablik
 * 
 * @brief Implementace testu prace s maticemi.
 */

#include "gtest/gtest.h"
#include "white_box_code.h"

//============================================================================//
// ** ZDE DOPLNTE TESTY **
//
// Zde doplnte testy operaci nad maticemi. Cilem testovani je:
// 1. Dosahnout maximalniho pokryti kodu (white_box_code.cpp) testy.
// 2. Overit spravne chovani operaci nad maticemi v zavislosti na rozmerech 
//    matic.
//============================================================================//
class NonSquareMatrix : public ::testing::Test{
    protected: virtual void SetUp(){
        matS.set({{9},{-2},{4},{11}});
        matR.set({{9,11,3,8}});
    }
    Matrix matS = Matrix(4,1), matR = Matrix(1,4);
};
class OperMatrix : public ::testing::Test{
    protected: virtual void SetUp(){
        mat33a.set({{5,-9,9},{6,-2,97},{120,65,30}});
        mat33b.set({{4,1,-7},{21,-82,17},{10,25,90}});   
        mat22a.set({{16,6},{-4,7}});     
        mat22b.set({{2,-22},{-6,37}});     
        mat11a.set({{5}});
        mat11b.set({{-2}});
    }
    Matrix mat33a = Matrix(3,3),mat33b = Matrix(3,3);
    Matrix mat22a = Matrix(2,2);
    Matrix mat22b = Matrix(2,2);
    Matrix mat11a = Matrix(1,1);
    Matrix mat11b = Matrix(1,1);
};
class NonEmptyMatrix : public ::testing::Test{
    protected: virtual void SetUp(){
        mat.set({{1,2,3},{4,5,6},{7,8,9}});
    }
    Matrix mat;
};
class EmptyMatrix : public ::testing::Test{
    protected: Matrix mat;
};
TEST_F(EmptyMatrix, Insert){
    EXPECT_THROW(Matrix(0,0), std::runtime_error);
    ASSERT_FALSE(mat.set(1,5,3));
    std::vector<std::vector<double>> values = {{5,6,2},{1,4,3}};
    ASSERT_FALSE(mat.set(values));    
};
TEST_F(EmptyMatrix, Get){
    EXPECT_THROW(mat.get(1,5), std::runtime_error);
};
TEST_F(EmptyMatrix, OpEquals){
    ASSERT_TRUE(mat.operator==(Matrix()));
    EXPECT_THROW(mat.operator==(Matrix(20,999)), std::runtime_error);
};
TEST_F(EmptyMatrix, OpPlus){
    ASSERT_TRUE(mat.operator+(Matrix()) == Matrix());
    EXPECT_THROW(mat.operator+(Matrix(20,999)), std::runtime_error);
};
TEST_F(EmptyMatrix, OpMul){
    ASSERT_TRUE(mat.operator*(Matrix()) == Matrix());
    EXPECT_THROW(mat.operator*(Matrix(20,999)), std::runtime_error);
    ASSERT_TRUE(mat.operator*(6.2) == Matrix());
};
TEST_F(EmptyMatrix, SolveEquation){
    std::vector<double> b = {{}};
    EXPECT_THROW(mat.solveEquation(b), std::runtime_error);
};
TEST_F(EmptyMatrix, Transpose){
    ASSERT_TRUE(mat.transpose() == Matrix());
};
TEST_F(EmptyMatrix, Inverse){
    EXPECT_THROW(mat.inverse(), std::runtime_error);
};
TEST_F(NonEmptyMatrix, Insert){
    Matrix mymat = Matrix(3,3);
    ASSERT_TRUE(mymat.set({{1,2,3},{4,5,6},{7,8,9}}));
};
TEST_F(NonEmptyMatrix, OpEquals){
    Matrix mymat = Matrix(3,3);
    Matrix mymat2 = Matrix(3,3);
    ASSERT_TRUE(mymat.set({{1,2,3},{4,5,6},{7,8,9}}));
    ASSERT_TRUE(mymat2.set({{1,2,3},{4,5,6},{7,8,10}}));
    ASSERT_FALSE(mymat.operator==(mymat2));
};
TEST_F(NonEmptyMatrix, solveEquation){
    Matrix mymat = Matrix(3,4);    
    EXPECT_THROW(mymat.solveEquation({1,2,3,4}), std::runtime_error);
    EXPECT_THROW(mymat.solveEquation({1,2,3}), std::runtime_error);
    Matrix mymatT = Matrix(3,3);
    ASSERT_TRUE(mymatT.set({{6,20,3},{7,-5,-6},{17,28,-9}}));
    EXPECT_NO_THROW(mymatT.solveEquation({6,2,9}));
    Matrix mymatT1 = Matrix(2,2);
    ASSERT_TRUE(mymatT1.set({{6,20},{7,-5}}));
    EXPECT_NO_THROW(mymatT1.solveEquation({6,2}));
    Matrix mymatT2 = Matrix(4,4);
    ASSERT_TRUE(mymatT2.set({{6,20,3,1},{7,-5,-6,0},{17,28,-9,4},{6,85,-1,-77}}));
    EXPECT_NO_THROW(mymatT2.solveEquation({6,2,9,1}));
    Matrix mymatT3 = Matrix(1,1);
    ASSERT_TRUE(mymatT3.set({{6}}));
    EXPECT_NO_THROW(mymatT3.solveEquation({1}));
};
TEST_F(NonEmptyMatrix, inverse){
    Matrix mymat = Matrix(3,3);
    ASSERT_TRUE(mymat.set({{1,2,3},{4,5,6},{7,8,9}}));
    EXPECT_THROW(mymat.inverse(), std::runtime_error);
    ASSERT_TRUE(mymat.set({{6,20,3},{7,-5,-6},{17,28,-9}}));
    EXPECT_NO_THROW(mymat.inverse());
    Matrix mymat1 = Matrix(2,2);
    ASSERT_TRUE(mymat1.set({{6,20},{7,-5}}));
    EXPECT_NO_THROW(mymat1.inverse());
};
TEST_F(OperMatrix, OpEquals){
    EXPECT_FALSE(mat33a.operator==(mat33b));
    ASSERT_TRUE(mat33a.operator==(mat33a));
    EXPECT_FALSE(mat22a.operator==(mat22b));
    ASSERT_TRUE(mat22a.operator==(mat22a));
    EXPECT_FALSE(mat11a.operator==(mat11b));
    ASSERT_TRUE(mat11a.operator==(mat11a));
};
TEST_F(OperMatrix, OpPlus){
    Matrix res1 = Matrix(1,1);
    Matrix res2 = Matrix(2,2);
    Matrix res3 = Matrix(3,3);
    res1.set({{3}});
    res2.set({{18,-16},{-10,44}});
    res3.set({{9,-8,2},{27,-84,114},{130,90,120}});
    ASSERT_TRUE(mat11a.operator+(mat11b).operator==(res1));
    ASSERT_TRUE(mat22a.operator+(mat22b).operator==(res2));
    ASSERT_TRUE(mat33a.operator+(mat33b).operator==(res3));
};
TEST_F(OperMatrix, OpMul){
    Matrix res1 = Matrix(1,1);
    Matrix res2 = Matrix(2,2);
    Matrix res3 = Matrix(3,3);
    res1.set({{-10}});
    res2.set({{-4,-130},{-50,347}});
    res3.set({{-79,968,622},{952,2595,8654},{2145,-4460,2965}});
    ASSERT_TRUE(mat11a.operator*(mat11b).operator==(res1));
    ASSERT_TRUE(mat22a.operator*(mat22b).operator==(res2));
    ASSERT_TRUE(mat33a.operator*(mat33b).operator==(res3));
};
TEST_F(NonSquareMatrix, OpMul){
    Matrix res1 = Matrix(1,1);
    res1.set({{159}});
    ASSERT_TRUE(matR.operator*(matS).operator==(res1));
}

/*** Konec souboru white_box_tests.cpp ***/
