// Programming Challenge: Markup
#include <iostream>
#include <iomanip>
using namespace std;

double calculateRetail(); // function prototype

int main()
{
	double RetailPrice; // declaring variable
	cout << "This program calculates and displays the retail price of an item.\n"; // program discription 
	RetailPrice = calculateRetail(); // retail price is function
	cout << setprecision(2) << fixed; // sets the retail price to two decimal places
	cout << "The retail price of the item is $" << RetailPrice << "." << endl; // displays the retail price
	return 0;
}

double calculateRetail() // function header
{
	double cost, markup; // declaring variables

	do 
	{
		cout << "What is the wholesale cost of item? "; // asks user wholesale cost of item
		cin  >> cost; // user enters value of the cost
		if (cost < 0) // if user enters any value of cost less than 0, displays message from body of the function 
		{
			cout << "Wholesale cost must be a positive number.\n" << "Please try again.\n"; // the message in body of the function
		}
	} while (!(cost > 0)); // loops back to the top (after 1st do) until positive number is entered 
	
	do
	{
		cout << "What is the markup percentage of item? "; // asks user markup % of an item
		cin  >> markup; // user enters value of the markup
		if (markup < 0) // if user enters any markup % less than 0, displays message from body of the function
		{
			cout << "The markup percentage must be a positive number.\n" << "Please try again.\n"; // the message in body of the function	
		}
	} while (!(markup > 0)); // loops back to the top (after 2nd do) until positive number is entered 

	markup = markup / 100; // calculates markup % to decimal number 
	return cost * (1 + markup); // calculates the retail price
}

