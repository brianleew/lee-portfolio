// page 270 check point 5.8
#include <iostream>
#include <string>
using namespace std;

int main ()
{
    int number; // declaring variables
    char decision;
    
    do
    {
        cout << "Enter a whole number: "; // asks the user to enter a whole number
        cin >> number; // user enters a whole number
        
        if (number % 2 == 0) // if user enters a whole number and gets divided by 2 with no remainer, then the number is even 
            cout << "The number is even." << endl;
        else
            cout << "The number is odd." << endl; // if user enters a whole number and gets divided by 2 with a remainder, then the number is odd
        
        cout << "Do you want to enter another whole number (Y/N)? "; // asks the user if they want to enter another number
        cin >> decision; // user makes a decision
    } while (decision == 'Y' || decision == 'y'); // if entered y or Y, runs the program from the start // if n or N, program exits

    return 0;
}

