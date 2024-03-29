// page 500 Car class
#include <iostream>
#include <string>
using namespace std;

class Car
{
    // member variables
    private:
        int year; // declaring car model year variable
        string make; // declaring car make variable
        int speed; // declaring car speed variable
        
    public:
        // constructor with default parameters
        Car(int y = 2020, string m = " ") // passing year and make of the car 
        {
            year = y;
            make = m;
            speed = 0;
        }
        
        // Accessors
        int getYear()
        {
            return year;
        }
            
        string getMake()
        {
            return make;
        }
            
        int getSpeed()
        {

            return speed;
        }
        // Mutators  
        void accelerate()
        {
            speed +=5;
        }
            
        void brake()
        {
            if (speed >= 5)
            speed -=5;
            else
            speed = 0;
        }
        
};
// main function

int main ()
{
    Car name(2020, "BMW"); // car object
    // Acceleration
    cout << "I'm accelerating!!! \n\n";
    for (int i = 1; i <= 5; i++) // loop for displaying acceleration 5 times
    {
        name.accelerate();
        cout << "Current Speed: " << name.getSpeed() << " mph. \n";
    }
    
    // Brake
    cout << "\nNow, I'm stopping!!! \n\n";
    for (int i = 1; i <= 5; i++) // loop for displaying slowing down 5 times
    {
        name.brake();
        cout << "Current Speed: " << name.getSpeed() << " mph. \n";
    }
    return 0;
}











