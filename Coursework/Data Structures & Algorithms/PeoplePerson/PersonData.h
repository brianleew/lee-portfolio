/**
CISP 1020
Assignment The People Person Assignment
Description: First, I declared PersonData variables.
            resizeCopy is increasing records then copying contents of cold array to new array
            from dynamically created array.
            The add function increases capacity as records increase.
@author Brian Lee
@version 1.0 01/03/2020
*/ 
#pragma once
#define PERSONDATA_H
#include <string>
#include "Person.h"
using namespace std;

class PersonData {
private:
    int capacity;
    int records;
    int *arrayPtr = nullptr;

public:
    PersonData(int records)
    {
        capacity = 1;
        this->records = 0;
        arrayPtr = new int[records];
    }
    
    void resizeCopy() {
        records += records; // add one to records
        int *newArray = new int[records]; // dynamically create new array
        for (int i = 1; i <= capacity; i++) {
            newArray[i] = arrayPtr[i]; // copy contents of old array to new array
        }
        delete[] arrayPtr;
        arrayPtr = newArray;
    }
    
    void add(int num) {
        if (capacity == records) {
            resizeCopy();
            capacity++;
        }
        arrayPtr[capacity] = num;
        records = capacity;
    }
    
    int *getPtr() {
        return arrayPtr;
    }
    
    int getRecords() {
        return records;
    }
    
    int getCapacity() {
        return capacity;
    }
    
};
