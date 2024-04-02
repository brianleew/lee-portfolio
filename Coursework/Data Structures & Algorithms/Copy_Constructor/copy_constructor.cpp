// CopyConstructor.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
using namespace std;

class MyInteger {

private:
	int * pInt = nullptr;
	int y = 3;

public: 
	//constructor
	MyInteger(int x) {
		pInt = new int;
		*pInt = x;
	}

	int getInt() {
		return *pInt;
	}

	void setInt(int x) {
		*pInt = x;
	}

	// Copy constructor
	MyInteger(MyInteger &integer)
	{
		pInt = new int;
		*pInt = integer.getInt();
	}

	//Overloading the = operator
	MyInteger& operator=(MyInteger &right) {
		pInt = new int;
		*pInt = right.getInt();
		return *this;
	}

	//Overloading the + operator
	MyInteger operator+(MyInteger &right) {
		MyInteger sum(*pInt + right.getInt());
		return sum;
	}


};


int main()
{
	//Test Copy Constructor
	//MyInteger pInt(7);
	//MyInteger pIntNew = pInt;
	//pInt.setInt(8);
	//cout << pInt.getInt() << endl;
	//cout << pIntNew.getInt() << endl;


	//Test Overloading the = operator
	//MyInteger pInt(7);
	//MyInteger pIntNew(3);
	//pIntNew = pInt;
	//pInt.setInt(8);
	//cout << pInt.getInt() << endl;
	//cout << pIntNew.getInt() << endl;

	//Test Overloading the + operator
	MyInteger pInt(7);
	MyInteger pInt2(8);
	MyInteger sum = pInt + pInt2;


	cout << sum.getInt();


	int x = 5;
	int y = x;
    return 0;
}
