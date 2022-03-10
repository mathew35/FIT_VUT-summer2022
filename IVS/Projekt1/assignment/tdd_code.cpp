//======== Copyright (c) 2021, FIT VUT Brno, All rights reserved. ============//
//
// Purpose:     Test Driven Development - priority queue code
//
// $NoKeywords: $ivs_project_1 $tdd_code.cpp
// $Author:     Matus Vrablik <xvrabl05@stud.fit.vutbr.cz>
// $Date:       $2022-02-03
//============================================================================//
/**
 * @file tdd_code.cpp
 * @author Matus Vrablik
 * 
 * @brief Implementace metod tridy prioritni fronty.
 */

#include <stdlib.h>
#include <stdio.h>

#include "tdd_code.h"

//============================================================================//
// ** ZDE DOPLNTE IMPLEMENTACI **
//
// Zde doplnte implementaci verejneho rozhrani prioritni fronty (Priority Queue)
// 1. Verejne rozhrani fronty specifikovane v: tdd_code.h (sekce "public:")
//    - Konstruktor (PriorityQueue()), Destruktor (~PriorityQueue())
//    - Metody Insert/Remove/Find/GetHead ...
//    - Pripadne vase metody definovane v tdd_code.h (sekce "protected:")
//
// Cilem je dosahnout plne funkcni implementace prioritni fronty implementovane
// pomoci tzv. "singly linked list", ktera bude splnovat dodane testy
// (tdd_tests.cpp).
//============================================================================//

PriorityQueue::PriorityQueue()
{
    m_pHead = NULL;
}

PriorityQueue::~PriorityQueue()
{   
    if(m_pHead != NULL){
        Element_t* actElem = m_pHead;
        Element_t* tmp = NULL;
        while(actElem->pNext != NULL){
            tmp = actElem;
            actElem = actElem->pNext;
            free(tmp);
            tmp = NULL;        
        }
        free(actElem);
    }
}

void PriorityQueue::Insert(int value)
{
    Element_t* elem = (Element_t*)malloc(sizeof(Element_t*));
    elem->value = value;
    elem->pNext = NULL;
    if(GetHead() == NULL){
        m_pHead = elem;
    }
    else{
        if(m_pHead->value < value){
            elem->pNext = m_pHead;
            m_pHead = elem;
        }
        else{
            Element_t* actElem = GetHead();
            while(actElem->pNext != NULL && actElem->pNext->value > value){
                actElem = actElem->pNext;
            }
            if(actElem->pNext != NULL){
                elem->pNext = actElem->pNext;
            }
            actElem->pNext = elem;
        }
    }
}

bool PriorityQueue::Remove(int value)
{
    Element_t* actElem = GetHead();
    if(actElem == NULL){
        return false;
    }
    if(actElem->value == value){
        m_pHead = actElem->pNext;
        free(actElem);
        return true;
    }
    while(actElem->pNext != NULL && actElem->pNext->value != value){
        actElem = actElem->pNext;
    }
    if(actElem->pNext != NULL){
        Element_t* tmp = actElem->pNext;
        actElem->pNext = tmp->pNext;
        free(tmp);
        return true;
    }

    return false;
}

PriorityQueue::Element_t *PriorityQueue::Find(int value)
{
    Element_t* actElem = GetHead();
    if(actElem == NULL){
        return NULL;
    }
    if(actElem->value == value){
        return actElem;
    }
    while(actElem->pNext != NULL && actElem->pNext->value != value){
        actElem = actElem->pNext;
    }
    return actElem->pNext;
}

size_t PriorityQueue::Length()
{
    Element_t* actElem = GetHead();
    if(actElem == NULL){
        return 0;
    }
    int queue = 0;
    while(actElem != NULL){
        actElem = actElem->pNext;
        queue++;
    }
    return queue;
}

PriorityQueue::Element_t *PriorityQueue::GetHead()
{
    return m_pHead;
}

/*** Konec souboru tdd_code.cpp ***/
