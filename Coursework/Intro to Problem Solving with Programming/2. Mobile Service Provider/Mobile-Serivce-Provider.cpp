// Mobile Service Provider

#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main()
{
    const double aPrice = 39.99, bPrice = 59.99, cPrice = 69.99,
                 
                 aMinutes = 450, bMinutes = 900,
                 
                 aExtra = 0.45, bExtra = 0.40;
    string name;
    char package;
    
    cout << "What is your name? ";
    cin >> name;
    
    cout << "Which package did you purchase? ";
    cin >> package;
    
    switch (package)
    {
        int customerMinutes;
        float chargeA, chargeB, chargeC;
        
        case 'a':
        case 'A':
        case 'b':
        case 'B':
        case 'c':
        case 'C':
            cout << "How many minutes did you use? ";
            cin >> customerMinutes;
            
            if (customerMinutes < 0)
            {
                cout << "You must enter minutes used greater than 0.\n";
            }
            else
            {
                double save;
                
                chargeA = customerMinutes > aMinutes
                ? aPrice + ((customerMinutes - aMinutes) * aExtra)
                : aPrice;
                
                chargeB = customerMinutes > bMinutes
                ? bPrice + ((customerMinutes - bMinutes) * bExtra)
                : bPrice;
                
                chargeC = cPrice;
           
                cout << setprecision(2) << fixed;
                
                if (package == 'a' || package == 'A')
                {
                    cout << "Package A monthly bill: $" << chargeA << endl;
                    
                    if (chargeA > chargeB)
                    {
                        save = chargeA - chargeB;
                        cout << "You could have saved $" << save << " with Package B." << endl;
                    
                        save = chargeA - chargeC;
                        cout << "Your could have saved $" << save << " with Package C." << endl;
                    }
                }
                else if (package == 'b' || package == 'B')
                {
                    cout << "Package B monthly bill: $" << chargeB << endl;
                    
                    if (chargeB > chargeC)
                    {
                        save = chargeB - chargeC;
                        cout << "You could have saved $" << save << " with package C." << endl;
                    
                        
                    }
                }
                else if (package == 'c' || package == 'C')
                {
                    cout << "Package C monthly bill: $" << chargeC << endl;
                }
            }    
        break;
        default: 
        cout << "Your choices must be A, B, or C." << endl;
        break;
    }
    return 0;
}



