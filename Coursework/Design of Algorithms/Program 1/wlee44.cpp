/*
Name: Brian (Won) Lee
Section: Design of Algorithms CSC-2400-001
Purpose: Outputs the GCD of two inputs as integers using Euclid's Algorithm
Date: May 31, 2022
*/
#include <iostream>
#include <cstdlib>
using namespace std;

int main() {
    int m,n,r,mm,nn;
    
    cout << "Enter two integers separated by a space: ";
    cin >> m >> n; // getting user input
    cout << endl;
    mm = m; // placeholder variables to show original input in the output
    nn = n;
    
    if ( (n == 0 && m == 0) || (n == 0) || (m == 0) ) {
        cout << endl;
        cout << "gcd(" << m << ", " << n << ")" << " is " << "undefined" << endl; // if input is (n,0), (0,m), or (0,0) GCD is undefined
    }
    else {
        cout << "gcd(" << m << ", " << n << ")" << " =" << endl; // showing work
        cout << "gcd(" << n << ", " << "("<<m<<"%"<<n<<")"<<")" << " =" << endl; // showing work
        while (nn != 0) {
        r = mm%nn; // calculating the GCD
        mm = nn;
        nn = r;
            if (nn > 0) {
                cout << "gcd(" << nn << ", " << "("<<mm<<"%"<<nn<<")"<<")" << " =" << endl; // showing work of each calculated iterations
            }
            if (nn == 0) {
                cout << endl;
                cout << "SOLUTION: " << "gcd(" << m << ", " << n << ")" << " is " << abs(mm) << endl; // outputs the GCD of two integers
                break;
            }
        }   
    
    }

    return 0;
}