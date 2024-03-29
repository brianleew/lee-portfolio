// The Speed of Sound
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main()
{
    int air = 1100;
    int water = 4900;
    int steel = 16400;
    int selection;
    double distance;
    double time;
    // Display the menu and get user's selection
    cout << "   Select the speed of sound, measured in feet per second, in air, water, and steel\n\n";
    cout << "1. Air\n";
    cout << "2. Water\n";
    cout << "3. Steel\n";
    cout << "4. Distance is less than or equal to 0\n\n";
    cout << "Enter selection: ";
    cin >> selection;
    
// sets the decimal place to 6
    cout << setprecision(6) << fixed;
    
// use the menu selection to execute the correct set of options
    if (selection == 1)
    {   
        cout << "What is the distance in feet(enter positive value greater than 0)? ";
        cin >> distance;
        time = distance / air;
        cout << "\nThe amount of time it will take in air is " << time << " second(s)." << endl;
    }
    
    else if (selection == 2)
    { 
        cout << "What is the distance in feet(enter positive value greater than 0)? ";
        cin >> distance;
        time = distance / water;
        cout << "\nThe amount of time it will take in water is " << time << " second(s)." << endl;
    }
    
    else if (selection == 3)
    {
        cout << "What is the distance in feet?(enter positive value greater than 0) ";
        cin >> distance;
        time = distance / steel;
        cout << "\nThe amount of time it will take in steel is " << time << " second(s)." << endl;
    }
    
    else if (selection == 4)
    {
        cout << "There is no distance.";
    }
    
    return 0;
}




