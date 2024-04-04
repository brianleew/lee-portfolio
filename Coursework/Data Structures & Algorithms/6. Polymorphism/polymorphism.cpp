// Polymorphism.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string>;

using namespace std;


class Animal
{
public:
	//virtual void my_features() = 0; // you MUST override this function in a child class
	virtual void my_features()
	{
		cout << "I am an animal.";
	}
};

class Mammal : public Animal
{
public:
	void my_features()
	{
		cout << "\nI am a mammal.";
	}
};

class Reptile : public Animal
{
public:
	void my_features()
	{
		cout << "\nI am a reptile.";
	}
};




int main()
{
	//Animal *obj1 = new Animal;
	//Mammal *obj2 = new Mammal;
	//Reptile *obj3 = new Reptile;

	Animal *obj1 = new Animal;
	Animal *obj2 = new Mammal;
	Animal *obj3 = new Reptile;

	obj1->my_features();
	obj2->my_features();
	obj3->my_features();

	return 0;
}

void something(Animal animal) {

}

