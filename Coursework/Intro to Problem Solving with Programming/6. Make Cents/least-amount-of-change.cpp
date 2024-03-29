// Let's Make Some Cents
#include <iostream>
using namespace std;

int main ()
{
    int totalCentsOwed; // declaring and initializing variables
    int totalCentsPaid;
    int change;
    const int pennies = 1;
    const int nickels = 5;
    const int dimes = 10;
    const int quarters = 25;
    
    cout << "Enter total cent(s) owed: "; // asks user to enter cents owned
    cin >> totalCentsOwed; // user enters total cents owed
    
    if (totalCentsOwed < 1 && totalCentsOwed > 99) // evaluates if entered total cents owed is 1-99
    {
        cout << "You must enter 1-99 cents owed." << endl; // displays an error message, asking user to enter cents 1-99
    }
    
    cout << "Enter total cent(s) paid: "; // asks user to enter cents owned
    cin >> totalCentsPaid; // user enters total cents owed
    
    if (totalCentsPaid < 1 && totalCentsPaid > 99) // evaluates if entered total cents owed is 1-99 
    {
        cout << "You must enter 1-99 cents paid." << endl; // displays an error message, asking user to enter cents 1-99
    }
    
    if (totalCentsPaid >= totalCentsOwed) // evaluates if total cents paid is greater or equal to total cents owed
    {
        change = totalCentsPaid - totalCentsOwed; // calculates the change
        cout << "Your change is " << change << " cent(s)."<< endl; // displays the change
    }
    else
    {
        cout << "The total cents paid has to be greater than equal to total cents owed."; // displays this error message if total cents paid is not greater or equal to total cents owed
    }
    
    int countPenny = 0; // declaring and initializing count of coins starting from 0
    int countNickel = 0;
    int countDime = 0;
    int countQuarter = 0;
    
    while (change > 0) 
    {
    
    if (change >= quarters) // deducts quarter from change
    {
    countQuarter++; // count of quarter(s)
    change -= quarters; // calculates count of quarter(s)
    continue; // goes back to the top of the loop
    }
    
    if (change >= dimes) // deducts dimes from change
    {
    countDime++; // count of dime(s)
    change -= dimes; // calculates count of dime(s)
    continue; // goes back to deduct from the highest coin
    }
    
    if (change >= nickels) // deducts nickel(s) from change
    {
    countNickel++; // count of nickel(s)
    change -= nickels; // calculates count of nickel(s)
    continue; // goes back to the top of the loop
    }
    
    if (change >= pennies) // deducts penny(s) from change
    {
    countPenny++; // count of penny(s)
    change -= pennies; // calculates count of penny(s)
    continue; // goes back to deduct from highest coin
    }
 
    }
 // displays least amount of coins
 cout << "Pennie(s):  " << countPenny << endl;
 cout << "Nickel(s):  " << countNickel << endl;
 cout << "Dime(s):    " << countDime << endl;
 cout << "Quarter(s): " << countQuarter << endl;
    
    return 0;
}




