#include <iostream>
#include <fstream>
#include <string>
using namespace std;
// function to find or search "boy" and replace it with "girl" in each line
string replaceString(string read, const string& search, const string& replace) //parameters holding first line, words to search and find
    {
        size_t pos = 0; // initially set the position to 0th line
        while ((pos = read.find(search, pos)) != string::npos) // condition that will find the search word until maximum position
        {   // using the string member function called replace to find position of "boy" in the original text file line
            read.replace(pos, search.length(), replace); //(position, length of "boy", what we want to replace it with which we want "girl")
            pos += replace.length();// moves to next position and changes length of "boy" to "girl"
        }
        return read;
    }
int main()
{
    string search;//I declared it search instead of "find"
    string replace;// I declared it replace instead of "replaceWith"
	string read; //declared it to hold first line of the text file
	ifstream boyFile; //creating a stream object to read from text file
	ofstream girlFile; // used to write contents into text file
 	girlFile.open("boy_wolf_replaced.txt"); // creates a new text file and opens it
	boyFile.open("boy_wolf.txt"); // opens the text file
    if (!boyFile) // incase the text file does not exist, displays a message
    {
    	cout << "Error: File not found.";
    	return 0;
    }
    getline(boyFile, read); // read holds first line of text file
	// displays the whole text file, modifies it, then stores it into girlFile
	while (boyFile) // condition
	{
		cout << read << endl; // reads first line on the screen
		string replacedString = replaceString(read, "boy", "girl"); // declared a string variable called replacedString that initializes the method with string parameters
		girlFile << replacedString << endl; // adds the modified first line 
		getline(boyFile, read); // keeps on printing line by line until it reaches the end of condition which is boyFile
	}
    boyFile.close(); // closes the text file
    girlFile.close(); // closes the new text file

    return 0;
}

