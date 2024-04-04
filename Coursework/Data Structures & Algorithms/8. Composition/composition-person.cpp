// Composition-Person.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include "stdafx.h"
using namespace std;

// HAS A

class Birthdate {
private:
	int month;
	int day;
	int year;

public:
	Birthdate(int month, int day, int year) {
		this->month = month;
		this->day = day;
		this->year = year;
	}

	void setMonth(int month) {
		this->month = month;
	}

	void setDay(int day) {
		this->day = day;
	}

	void setYear(int year) {
		this->year = year;
	}
};

class Person {
private:
	string name;
	int age;
	double weight;
	Birthdate *bd = nullptr;
	

public:
	
	//Birthdate *bd = nullptr;
	//Person(string name, int age, double weight, Birthdate *bd) {
	//	this->name = name;
	//	this->age = age;
	//	this->weight = weight;
	//	this->bd = bd;
	//}

	Person(string name, int age, double weight) {
		this->name = name;
		this->age = age;
		this->weight = weight;
	}

	//void setBD(int month, int day, int year) {
	//	bd->setMonth(month);
	//	bd->setDay(day);
	//	bd->setYear(year);
	//}
	
	void setMonth(int month) {
		bd->setMonth(month);
	}



};

int main()
{
	
	//Person jb("Josh Bond", 43, 180);
	//Birthdate *bd = new Birthdate(10, 7, 1975);
	//Person jb("Josh Bond", 43, 180, bd);
	Person jb2("Josh Bond", 43, 180);
	jb2.setMonth(10);
	
}
