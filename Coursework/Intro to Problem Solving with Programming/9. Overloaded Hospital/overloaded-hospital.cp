// Overloaded Hospital
#include <iostream>
using namespace std;

void inpatient (bool&, int&, double&, double&, double&, double&); // statement that declares a prototype for function inpatient with parameters
void outpatient (bool&, double&, double&, double&); // statement that declares a prototype for function outpatient with parameters

int main()
{
    bool patient; // declraing patient as boolean value
    int days; // declaring days
    double rate, ip_medCharge, ip_hsCharge, op_medCharge, op_hsCharge, totalCharge; // declaring variables
    
    cout << "Is the patient in or out patient? (enter 1 for in or 0 for out)" << endl; // asks user rather patient is in or out patient
    cin >> patient; // user enters 1 or 0
    
    if (patient == true) // if user enters 1(true), returns function inpatient and displays the total for inpatient
    {
        inpatient (patient, days, rate, ip_medCharge, ip_hsCharge, totalCharge); 
        cout << "The total charge is $" << totalCharge << "." << endl;
    }
    
    if (patient == false) // if user enters 0(false), returns function outpatient and displays the total for outpatient
    {
        outpatient (patient, op_medCharge, op_hsCharge, totalCharge);
        cout << "The total charge is $" << totalCharge << "." << endl;
    }
    
    else // if user enters values other than 0 or 1, displays message below
    cout << "Please enter value 1 or 0. Exit the program and try again.";
    
    return 0;
}

void inpatient (bool& patient, int& days, double& rate, double& ip_medCharge, double& ip_hsCharge, double& totalCharge)
// definition of function inpatient with all the parameters
{
    cout << "How many day(s) did the patient spend in the hospital?" << endl; // asks user to enter number of days spent at the hospital
    cin >> days; // user enters number of days
    if (days < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do 
    {
        cout << "Please enter positive day(s): ";
        cin >> days;
    } while (days < 0);
    }
    
    cout << "What is the daily rate for an in-patient stay?" << endl; // asks user to enter the daily rate
    cin >> rate; // user enters daily rate
    if (rate < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do
    {
        cout << "Please enter positive rate: ";
        cin >> rate;
    } while (rate < 0);
    }
    
    cout << "What was the medication charge(s)?" << endl; // asks user to enter medication charges
    cin >> ip_medCharge; // user enters medication charges
    if (ip_medCharge < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do
    {
        cout << "Please enter positive medication charge(s): ";
        cin >> ip_medCharge;
    } while (ip_medCharge < 0);
    }
    
    cout << "What was the hospital service charge(s)?" << endl; // asks user to enter hospital service charges
    cin >> ip_hsCharge; // user enters hospital service charges
    if (ip_hsCharge < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do
    {
        cout << "Please enter positive hospital service charge(s): ";
        cin >> ip_hsCharge;
    } while (ip_hsCharge < 0);
    }
    totalCharge = (days * rate) + ip_medCharge + ip_hsCharge; // calculates total charge based on user input
}

void outpatient (bool& patient, double& op_medCharge, double& op_hsCharge, double& totalCharge) 
// definition of function outpatient with all the parameters
{
    cout << "What was the medication charge(s)?" << endl; // asks user to enter medication charges
    cin >> op_medCharge; // user enters medication charges
    if (op_medCharge < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do
    {
        cout << "Please enter positive medication charge(s): ";
        cin >> op_medCharge;
    } while (op_medCharge < 0);
    }
    
    cout << "What was the hospital service charge(s)?" << endl; // asks user to enter hospital service charges
    cin >> op_hsCharge; // user enters hospital service charges
    if (op_hsCharge < 0) // if user enters a negative #, the program keeps asking until user enters positive number
    {
    do
    {
        cout << "Please enter positive hospital charge(s): ";
        cin >> op_hsCharge;
    } while (op_hsCharge < 0);
    }
    
    totalCharge = op_medCharge + op_hsCharge; // calculates total charge based on user input
}



