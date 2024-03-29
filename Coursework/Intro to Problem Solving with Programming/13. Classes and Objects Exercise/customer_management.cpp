// lab 13
#include <iostream>
#include <string>
using namespace std;

//Do not change this class
class Date {
	// private data fields
	private:
		int day;
		int month;
		int year;


	//public methods
	public:
		Date(int month, int day, int year) { // constructor
			this->day = day;
			this->month = month;
			this->year = year;
		}

		int getDay() {
			return this->day;
		}
		int getMonth() {
			return this->month;
		}
		int getYear() {
			return this->year;
		}

		void setDay(int day) {
			this->day = day;
		}
		void setMonth(int month) {
			this->month = month;
		}
		void setYear(int year) {
			this->year = year;
		}
};

//Do not change this class
class Customer {
	private: // private data fields
		string name;
		string address;
		Date lastCut; //like a yard cutting service? Or barber shop? 

	public:
		// Constructor 
		// Notice the syntax when we need to include an object as a field in C++. lastCut(lastCut) is an initializer list
		Customer(string name, string address, Date lastCut) : lastCut(lastCut) {  
			this->name = name;
			this->address = address;
		}

		string getName() {
			return this->name;
		}

		void setName(string name) {
			this->name = name;
		}

		string getAddress() {
			return this->address;
		}

		void setAddress(string address) {
			this->address = address;
		}

		Date &getLastCut() { //Pass this object by reference so we can change it later.
			return this->lastCut;
		}

};




int main()
{
	//Lab 13

	// TODO: You write the main method. Do not change the classes above. But DO study them because the ideas are on the final exam.


	//Instantiate a Date object. Set it to a recent date
    Date today(11, 30, 2019);
	//Instantiate a Customer object using the date object you just created
	Customer me("Brian Lee", "108 Brierfield Way, Hendersonville, TN", Date(today));
	//Print the following customer data using the customer object's properties.
	// Customer Name
	// Customer Address
	// Customer Last Cut in this format: Month-Day-Year
	cout << "Customer Name: " << me.getName() << endl;
	cout << "Customer Address: " << me.getAddress() << endl;
	cout << "Customer Last Cut: " << today.getMonth() << "/" << today.getDay() << "/" << today.getYear() << endl;
	cout << endl;

	//Change the lastCut Date to at least a new month and day. Access the date object (to change it) through the customer object.
    Date today2(12, 27, 2019);
    Customer me2("Brian Lee", "108 Brierfield Way, Hendersonville, TN", Date(today2));

	//Print the following customer data using the customer object's properties.
	// Customer Name
	// Customer Address
	// Customer Last Cut in this format: Month-Day-Year
    cout << "Customer Name: " << me2.getName() << endl;
	cout << "Customer Address: " << me2.getAddress() << endl;
	cout << "Customer Last Cut: " << today2.getMonth() << "/" << today2.getDay() << "/" << today2.getYear() << endl;
	
    return 0;
}



