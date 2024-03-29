// page 265 checkpoint 5.6
#include <iostream>
using namespace std;

int main ()
{
    int score, numScores = 0; // declaring and initializing variables
    double total = 0.0;

    cout << "Enter the first test score or -99 to quit the program: "; // asks the user to enter the first test score
    cin >> score; // user enters their score
    
    while (score != -99) // if score value is not -99, then
    {
        numScores++; // add 1 to number of scores
        total += score; // increment total by score
        cout << "Enter the next test score or -99 to see average and quit the program: "; // asks user to enter next test score
        cin >> score; // user enters the next test score
    }
    if (numScores == 0)
        cout << "No scores were entered." << endl; // incase user enters -99 when asked first time 
    else
        cout << "The average of the " << numScores << " score is " << total / numScores << endl; // calculates the average of test scores then displays it
    
    return 0;
}


