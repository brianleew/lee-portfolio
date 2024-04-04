/**
CISP 1020
Assignment The People Person Assignment
Description: getters and setters
@author Brian Lee
@version 1.0 01/03/2020
*/
#include "Person.h"

Person::Person(string name, int age, double weight) {
	this->name = name;
	this->age = age;
	this->weight = weight;
}
void Person::setName(string name) {
	this->name = name;
}
void Person::setAge(int age) {
	this->age = age;
}
void Person::setWeight(double weight) {
    this->weight = weight;
}
string Person::getName() {
	return this->name;
}
int Person::getAge() {
	return this->age;
}
double Person::getWeight() {
    return this->weight;
}