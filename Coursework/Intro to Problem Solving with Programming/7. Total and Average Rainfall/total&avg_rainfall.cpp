// total and average rainfall
#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
using namespace std;
int main()
{
	// declaring and initializing variables
	ifstream inputFile;
	string month_1, month_2;
    double value, total = 0, average, counter = 0;
	int x = 1;
    
    inputFile.open("Rainfall.txt"); // opens txt file
    
    if (!inputFile) // if no file, display error
	{
		cout << "Error finding and opening the data input file.\n";
		exit(1);
	}

	inputFile >> month_1; // reads the month from file sets April to month_1

	inputFile >> month_2; // reads the month from file sets August to month_2 

	// loops throughout the file until there is nothing to read
	while (inputFile >> value)
	{
		total += value;
		counter++;
	}
	
	// calculates avgerage rainfall
	average = total / counter;
	
	// displays months, total and average rainfall
	cout << "During  the  months  of " << month_1 << "-" << month_2 << " the  total  rainfall  was " << total << " and the average monthly rainfall was " << average << endl;

	inputFile.close();

	return 0;
}
