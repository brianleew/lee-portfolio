/*
Name: Brian Lee
Class: CSC-2400-001 Design of Algorithms
Date: June 11, 2022
Purpose: Demonstrating Brute Force String Matching Algorithm with C++ Code
*/

#include <iostream>
using namespace std;

int main() {
    string text;
    string pattern;

    int m = pattern.length(); // setting the number of characters in the pattern

    cout << endl;
    cout << "Enter a string of characters, called text." << endl;
    cout << "TEXT: ";
    getline(cin, text); // getting user input for text
    int n = text.length(); // setting the number of characters in the text
    while (n == 0) {
        cout << "Oops! Your text must be greater than zero characters." << endl;
        cout << "TEXT: ";
        getline(cin, text); // getting user input for text again if they entered nothing
        n = text.length(); // updates number of characters in the text
        if (n > 0) {
            break; // break out of repeatedly asking for a text since they entered an input
        }
    }
    if (n > 0) {
        cout << endl;
        cout << "Enter a search string to find in the text, called the pattern." << endl;
        cout << "Your pattern must be less than or equal to " << n << " characters long." << endl;
        cout << "PATTERN: ";
        getline(cin, pattern); // getting user input for pattern
        m = pattern.length(); // number of characters in the pattern
        while (m == 0 || m > n) {
            if (m == 0) {
                cout << "Oops! Your pattern must be greater than zero characters." << endl;
                cout << "PATTERN: ";
                getline(cin, pattern); // getting user input for pattern again if they entered nothing
                m = pattern.length(); // updates the number of characters in the pattern
            }
            else if (m > n) {
                cout << "Oops! Your pattern must be less than or equal to " << n << " characters long." << endl;
                cout << endl;
                cout << "PATTERN: ";
                getline(cin, pattern); // getting user input for pattern if they entered a pattern greater than text
                m = pattern.length(); // updates the number of characters in the pattern
            }
            else if (m > 0 || m <= n) {
                break; // break out of repeatedly asking for pattern since input was entered and input was less than equal to text
            }
        }
    }

    cout << endl;

    if (m <= n) {
        // the meat of the program, the algorithm
        bool found = 0;
        int nomatch = 0;
        int match = 0;
        int nCharMatch = 0;
        for (int i = 0; i <= n-m; i++) {
            int j = 0;
            while ((j < m) && (pattern[j] == text[i+j])) {
                j = j + 1;
                match++; // counts the number of times characters matched
                nCharMatch++; // counts the number of character matches that will reset when there is a mismatch then recount
                cout << "LETTER MATCHED-" << text[i+j-1] << ", " << "NUMBER CHARS MATCHED-" << nCharMatch << endl; // outputs which character matched and how many times it matched before each shift
            }
            if (j != m) {
                nomatch++; // counts the number of times characters did not match
                nCharMatch = 0; // resets the number of character matches to 0 for the recount of next matches 
            }
            if (j == m) {
                found = 1; // indicates that there is a pattern within the text 
                cout << endl;
                cout << "Pattern was found at index " << i << "!" << endl; // outputs the first index of the matching string 
                cout << "TOTAL COMPARISONS: " << nomatch + match << endl; // outputs the total comparisons by adding up all the times a character matched and not matched
                break;
            } 
        }
        if (found == 0) {
            cout << endl;
            cout << "Sorry, the pattern was not found in the text." << endl; // outputs that there is no pattern string matched within the text
            cout << "TOTAL COMPARISONS: " << nomatch + match << endl; // outputs the total comparisons by adding up all the times a character matched and not matched
        }
    }

    return 0;
}