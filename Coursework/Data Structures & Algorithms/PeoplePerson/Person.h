/**
CISP 1020
Assignment The People Person Assignment
Description: Person class declaration
@author Brian Lee
@version 1.0 01/03/2020
*/
#pragma once
#define PERSON_H
#include <string>

using namespace std;

class Person {
private:
	string name;
	int age;
	double weight;

public:
	Person(string, int, double);
	void setName(string);
	void setAge(int);
	void setWeight(double);
	string getName();
	int getAge();
	double getWeight();
};
