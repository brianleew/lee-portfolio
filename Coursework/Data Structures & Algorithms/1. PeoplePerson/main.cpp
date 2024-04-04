/**
CISP 1020
Assignment The People Person Assignment
Description: First, initial records and capacity of the array are shown by instantiating an object called list using PersonData class, then it gets displayed. 
            Second, object called identity and id are containing person information that gets instantiated by using Person class, then it gets displayed.
            Afterwards, by using the list object, calls the function called add which increases the capacity and records depending on parameter, then new capacity and records are displayed.
            
@author Brian Lee
@version 1.0 01/03/2020
*/
#include <iostream>
#include "Person.h"
#include "PersonData.h"
#include <string>

using namespace std;

int main()
{
	PersonData list(0);
	cout << "Capacity of the array: " << list.getCapacity() << endl;
	cout << "Records in the array: " << list.getRecords() << endl << endl;
	
	Person identity("Bob", 28, 165.1);
	cout << identity.getName() << " was added to the database!" << endl << endl;
	cout << "Name: " << identity.getName() << endl;
	cout << "Age: " << identity.getAge() << endl;
	cout << "Weight: " << identity.getWeight() << " lb" << endl << endl;
	
	list.add(1);
	cout << "Capacity of the array: " << list.getCapacity() << endl;
	cout << "Records in the array: " << list.getRecords() << endl << endl;
	
	Person id("Brian", 24, 180.2);
	cout << id.getName() << " was added to the database!" << endl << endl;
	cout << "Name: " << identity.getName() << endl;
	cout << "Age: " << identity.getAge() << endl;
	cout << "Weight: " << identity.getWeight() << " lb" << endl << endl;
	cout << "Name: " << id.getName() << endl;
	cout << "Age: " << id.getAge() << endl;
	cout << "Weight: " << id.getWeight() << " lb" << endl << endl;
	
	list.add(2);
	cout << "Capacity of the array: " << list.getCapacity() << endl;
	cout << "Records in the array: " << list.getRecords() << endl << endl;
}
