// chips and salsa p.593 programming challenge
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

// function prototypes
int lowPosition(int[], int);
int highPosition(int [], int);
int findTotal(int [], int);

int main()
{
    // Arrays for the different types of jars and number of sales
    const int numOfTypes = 5;
    int sales[numOfTypes];
    string salsa[numOfTypes] = {"Mild", "Medium", "Sweet", "Hot", "Zesty"};
    
    // declaring variables for total jars sold, product of high sales, and product of low sales
    int total_jarsSold, high_sales, low_sales;
    
    // used for loop to ask user to enter number of salsa sold for each types
    for (int i = 0; i < numOfTypes; i++)
    {
        cout << salsa[i] << " jars sold last month: ";
        cin >> sales[i];
    // incase user enters a negative value, while loop keeps asking user to enter positive value
        while (sales[i] < 0) 
        {
            cout << "Please enter a positive value: ";
            cin >> sales[i];
        }
    }
    // calls function prototypes to find total sales, product of high sales, and product of low sales
    total_jarsSold = findTotal(sales, numOfTypes);
    high_sales = highPosition(sales, numOfTypes);
    low_sales = lowPosition(sales, numOfTypes);
    
    // displays the sales report
    cout << endl << "    Salsa Sales Report" << endl << endl;
    cout << "Salsa Names:       Jars Sold" << endl;
    cout << salsa[0] << "                  " << sales[0] << "\n";
    cout << salsa[1] << "                " << sales[1] << "\n";
	cout << salsa[2] << "                 " <<sales[2] << "\n";
	cout << salsa[3] << "                   " << sales[3] << "\n";
	cout << salsa[4] << "                 " << sales[4] << "\n" << endl;
    //displays total number of jars sold, high and low sales of salsa types
    cout << "Total Jars Sold: " << total_jarsSold << endl;
    cout << "High Seller: " << salsa[high_sales] << endl;
    cout << "Low Seller: " << salsa[low_sales] << endl;
    
    return 0;
}

// calculates and returns total values of the array passed to the function
int findTotal (int array[], int numOfTypes)
{
	int total = 0;

	for (int i = 0; i < numOfTypes; i++)
		total += array[i];
	return total;
}

// Finds and returns largest value in the array position passed to the function
int highPosition(int array[], int numOfTypes)
{
	int indexOfHigh = 0;
	
	for (int i = 1; i < numOfTypes; i++)
	{
		if (array[i] > array[indexOfHigh])
			indexOfHigh = i;
	}
	return indexOfHigh;
}

// Finds and returns lowest value in the array position passed to the function
int lowPosition(int array[], int numOfTypes)
{
	int indexOfLow = 0;
	
	for (int i = 1; i < numOfTypes; i++)
	{
		if (array[i] < array[indexOfLow])
			indexOfLow = i;
	}		
	return indexOfLow;
}


