/*
Name: Brian Lee
Class: CSC-2400-001 Design of Algorithms
Date: July 2, 2022
Purpose: Demonstrating Horspools String Matching Algorithm with C++ Code
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
    for (int i = 0; i < text.length(); i++) {
        text[i] = toupper(text[i]); // capitalizes all the letters in the text
    }
    int n = text.length(); // setting the number of characters in the text
    while (n == 0) {
        cout << "Oops! Your text must be greater than zero characters." << endl;
        cout << "TEXT: ";
        getline(cin, text); // getting user input for text again if they entered nothing
        for (int i = 0; i < text.length(); i++) {
            text[i] = toupper(text[i]); // capitalizes all the letters in the text
        }
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
        for (int i = 0; i < pattern.length(); i++) {
            pattern[i] = toupper(pattern[i]); // capitalizes all the letters in the pattern 
        }
        m = pattern.length(); // number of characters in the pattern
        while (m == 0 || m > n) {
            if (m == 0) {
                cout << "Oops! Your pattern must be greater than zero characters." << endl;
                cout << "PATTERN: ";
                getline(cin, pattern); // getting user input for pattern again if they entered nothing
                for (int i = 0; i < pattern.length(); i++) {
                    pattern[i] = toupper(pattern[i]); // capitalizes all the letters in the pattern 
                }
                m = pattern.length(); // updates the number of characters in the pattern
            }
            else if (m > n) {
                cout << "Oops! Your pattern must be less than or equal to " << n << " characters long." << endl;
                cout << endl;
                cout << "PATTERN: ";
                getline(cin, pattern); // getting user input for pattern if they entered a pattern greater than text
                for (int i = 0; i < pattern.length(); i++) {
                    pattern[i] = toupper(pattern[i]); // capitalizes all the letters in the pattern 
                }
                m = pattern.length(); // updates the number of characters in the pattern
            }
            else if (m > 0 || m <= n) {
                break; // break out of repeatedly asking for pattern since input was entered and input was less than equal to text
            }
        }
    }
    cout << endl;

    if (m <= n) {
        // creating a bad match table
        string table[27] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " "};
        int shiftvalue[27];
        for (int i = 0; i <= 26; i++) {
            shiftvalue[i] = m;
        }
        for (int j = 0; j <= m-2; j++) {
            shiftvalue[pattern[j] - 65] = m-1-j;
        }
        cout << "BAD MATCH TABLE: "<< endl;
        for (int x = 0; x <= 26; x++) {
            cout << table[x] << " ";
        }
        cout << endl;
        for (int y = 0; y <= 26; y++) {
            cout << shiftvalue[y] << " ";
        }
        
        cout << endl << endl;

        // implementation of Horspool's algorithm
        int nomatch = 0;
        int match = 0;
        int nCharMatch = 0;
        bool found = 0;
        int ind = m - 1;
        int k;
        while (ind <= n-1) { // run while index is less than equal to text length - 1
            k = 0;
            while ((k <= m-1) && (pattern[m-1-k] == text[ind-k])) { // the condition in which characters of the text and pattern match
                k = k + 1;
                match++;
                nCharMatch++;
                cout << "LETTER MATCHED-" << text[ind-k+1] << ", " << "NUMBER CHARS MATCHED-" << nCharMatch << endl;
            }
            if (k == m) { // when k is equal to pattern length so there exists a pattern within the text
                found = 1;
                if (found == 1) {
                    cout << endl;
                    cout << "Pattern was found at index " << ind-m+1 << "!" << endl;
                    cout << "TOTAL COMPARISONS: " << nomatch + match << endl;
                    cout << endl;
                    break;
                }
            }
            else { // k != pattern length so shift when a letter of pattern and text does not match. Shift value is determined by the letter of text where it did not match. 
                nCharMatch = 0;
                if (text[ind] >= 65 && text[ind] <= 90) {
                    cout << "Shifting pattern by " << shiftvalue[text[ind] - 65] << endl;
                    ind = ind + shiftvalue[text[ind] - 65];
                    nomatch++;
                }
                if (text[ind] == 32) {
                    ind = ind + shiftvalue[26];
                    nomatch++;
                    cout << "Shifting pattern by " << shiftvalue[26] << endl;
                }
                
            }
        }
        if (found == 0) { // after all the iteration(s), the pattern was not found in the text
            cout << endl;
            cout << "Sorry, the pattern was not found in the text" << endl;
            cout << "TOTAL COMPARISONS: " << nomatch + match << endl;
            cout << endl;
        }

    }
    return 0;
}