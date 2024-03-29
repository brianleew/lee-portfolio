// Pass 13
#include <iostream>
#include <string>
using namespace std;

//created a class called Package
class Package
{
    // private data fields
    private:
        string planName;
        int planMinutes;
        double planPrice;
        double addMinutes;
    // public methods
    public:
        Package(string name, int minutes, double price, double extra) // constructor
        {
            this->planName = name;
            this->planMinutes = minutes;
            this->planPrice = price;
            this->addMinutes = extra;
        }
        // public setters and getters to access private fields
        string getPlanName()
        {
            return this->planName;
        }
        int getPlanMinutes()
        {
            return this->planMinutes;
        }
        double getPlanPrice()
        {
            return this->planPrice;
        }
        double getAddMinutes()
        {
            return this->addMinutes;
        }
        void setPlanName(string planName)
        {
            this->planName = planName;
        }
        void setPlanMinutes(int planMinutes)
        {
            this->planMinutes = planMinutes;
        }
        void setPlanPrice(double planPrice)
        {
            this->planPrice = planPrice;
        }
        void setAddMinutes(double addMinutes)
        {
            this->addMinutes = addMinutes;
        }
};

class Bill
{
    private:
        string name;
        int minutesUsed;
        double billTotal;
        Package package;
    public:
        Bill (string name, int minutesUsed, Package package) : package(package)
        {
            this->name = name;
            this->minutesUsed = minutesUsed;
            this->package = package;
        }
        string getName()
        {
            return this->name;
        }
        int getMinutesUsed()
        {
            return this->minutesUsed;
        }
        double getBillTotal()
        {
            return this->billTotal;
        }
        Package &getPackage()
        {
            return this->package;
        }
        void setName(string name)
        {
            this->name = name;
        }
        void setMinutesUsed(int minutesUsed)
        {
            this->minutesUsed = minutesUsed;
        }
        void setBillTotal(double billTotal)
        {
            this->billTotal = billTotal;
        }
        void setPackage(Package package)
        {
            this->package = package;
        }
        void calcBill()
        {
            billTotal = package.getPlanPrice() + ((minutesUsed - package.getPlanMinutes()) * package.getAddMinutes());
        }
};


int main()
{
	// This code has already been written for you. Yay!
	// Do not modify this code except as noted for testing on the "Bill Bill1("Daffy Duck..." line.
	
	// Question: "DUDE, the code you gave me is defective! See, it has errors below!?" 
	// Answer: "You complete the class definitions according to the instructions and it will work." ;)

	//             planName, planMinutes, planPrice, addMinutes) 
	Package packageA("Package A", 450, 39.99, 0.45);
	Package packageB("Package B", 900, 59.99, 0.40);
	Package packageC("Package C", 0, 69.99, 0.0);

	Bill bill1("Daffy Duck", 915, packageB); //Test different minute and package values!
	bill1.calcBill();

	cout << "Loony Toons Mobility Bill" << endl;
	cout << "-------------------------" << endl;
	cout << "Name: " << bill1.getName() << endl;
	cout << "Package: " << bill1.getPackage().getPlanName() << endl;
	cout << "Package Base Price: " << bill1.getPackage().getPlanPrice() << endl;
	cout << "Package Add Cost Per Minute: " << bill1.getPackage().getAddMinutes() << endl;
	cout << "Minutes Used: " << bill1.getMinutesUsed() << endl;
	cout << "-------------------------" << endl;
	cout << "Total Bill: " << bill1.getBillTotal() << endl << endl << endl;

	bill1.getPackage().setPlanName("Exciting New Plan Name");
	bill1.getPackage().setAddMinutes(0.88);
	bill1.calcBill();

	cout << "Loony Toons Mobility Bill" << endl;
	cout << "-------------------------" << endl;
	cout << "Name: " << bill1.getName() << endl;
	cout << "Package: " << bill1.getPackage().getPlanName() << endl;
	cout << "Package Base Price: " << bill1.getPackage().getPlanPrice() << endl;
	cout << "Package Add Cost Per Minute: " << bill1.getPackage().getAddMinutes() << endl;
	cout << "Minutes Used: " << bill1.getMinutesUsed() << endl;
	cout << "-------------------------" << endl;
	cout << "Total Bill: " << bill1.getBillTotal() << endl;


}





