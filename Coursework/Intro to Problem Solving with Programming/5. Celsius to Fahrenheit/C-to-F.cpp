// Return to Fahrenheit
#include <iostream>
using namespace std;

int main ()
{
    double celsius, fahrenheit; // declared variables
    cout << "This program converts Celsius to Fahrenheit and displays a table. \n"; // explains the program
    cout << "What is the temperature in Celsius? "; // asks the user to input celsius value
    cin >> celsius; // user enters celsius value
    
    fahrenheit = (1.8 * celsius) + 32; // calculates celsius to fahrenheit
    
    cout << "Celsius \t Fahrenheit\n"; // part of the table
    
    for (int i = 0; i <= 30; i++) // displays 0 through 30 celsius then calculates and displays fahrenheit accordingly
    {
        cout << i << "       |        " << (1.8 * i) + 32 << endl;
    }
    
    cout << "The temperature is " << fahrenheit << " degrees Fahrenheit."; // displays exact temperature in fahrenheit
    return 0;
}

