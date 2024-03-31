#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>
using namespace std;

class SportsStats
{
    protected:
        string name;
        int age;
        double salary;
  
    public:
        SportsStats(string name, int age, double salary) {
            this->name = name;
            this->age = age;
            this->salary = salary;
        }
    
    const string toString() const
        {
            ostringstream buffer;
            buffer<<fixed<<showpoint<<setprecision(2)
            <<"Player Name: "<<name<<endl
            <<"Player Age: "<<age<<endl
            <<"Player Salary: $"<<salary<<endl;
            return buffer.str();
        }

    string getName() {
        return name;
    }
    int getAge() {
        return age;
    }
    double getSalary() {
        return salary;
    }
    void setName(string name) {
        this->name = name;
    }
    void setAge(int age) {
        this->age = age;
    }
    void setSalary(double salary) {
        this->salary = salary;
    }
};

class BasketballPlayer : public SportsStats 
{
    protected:
        double freeThrowAverage;
        int freeThrowShots;
        int threePointShots;
        int twoPointShots;
    public:
        BasketballPlayer(string name, int age, double salary, double freeThrowAverage, int freeThrowShots, int threePointShots, int twoPointShots) : 
        SportsStats(name, age, salary) {
            this->freeThrowAverage = freeThrowAverage;
            this->freeThrowShots = freeThrowShots;
            this->threePointShots = threePointShots;
            this->twoPointShots = twoPointShots;
        }
    const string toString() const
        {
            ostringstream buffer;
            buffer<<fixed<<showpoint<<setprecision(2)
            <<"Player Name: "<<name<<endl
            <<"Player Age: "<<age<<endl
            <<"Player Salary: $"<<salary<<endl
            <<"Free Throw Average: "<<freeThrowAverage<<endl
            <<"Free Throw Shots: "<<freeThrowShots<<endl
            <<"Three Point Shots: "<<threePointShots<<endl
            <<"Two Point Shots: "<<twoPointShots<<endl;
            return buffer.str();
        }

    double getFreeThrowAverage() {
        return this->freeThrowAverage;
    }
    int getFreeThrowShots() {
        return this->freeThrowShots;
    }
    int getThreePointShots() {
        return this->threePointShots;
    }
    int getTwoPointShots() {
        return this->twoPointShots;
    }
    void setFreeThrowAverage(double fta){
        this->freeThrowAverage = fta;
    }
    void setFreeThrowShots(int fts) {
        this->freeThrowShots = fts;
    }
    void setThreePointShots(int tttps) {
        this->threePointShots = tttps;
    }
    void setTwoPointShots(int ttps) {
        this->twoPointShots = ttps;
    }
};

class BaseballPlayer : public SportsStats
{
    protected:
        double battingAverage;
        int homoRuns;
        int errors;
    public:
        BaseballPlayer(string name, int age, double salary, double battingAverage, int homoRuns, int errors) : 
        SportsStats(name, age, salary) {
            this->battingAverage = battingAverage;
            this->homoRuns = homoRuns;
            this->errors = errors;
        }
    const string toString() const
        {
            ostringstream buffer;
            buffer<<fixed<<showpoint<<setprecision(2)
            <<"Player Name: "<<name<<endl
            <<"Player Age: "<<age<<endl
            <<"Player Salary: $"<<salary<<endl
            <<"Batting Average: "<<battingAverage<<endl
            <<"Home Runs: "<<homoRuns<<endl
            <<"Field Errors: "<<errors<<endl;
            return buffer.str();
        }
    
    double getBattingAverage() {
        return this->battingAverage;
    }
    int getHomoRuns() {
        return this->homoRuns;
    }
    int getErrors() {
        return this->errors;
    }
    void setBattingAverage(double ba){
        this->battingAverage = ba;
    }
    void setHomoRuns(int hr) {
        this->homoRuns = hr;
    }
    void setErrors(int e) {
        this->errors = e;
    }
};

int main()
{
    SportsStats player("Brian Lee", 25, 150000.99);
    cout << player.toString() << endl;
    
    BasketballPlayer player2("Lebron James", 28, 250000.69, 55.5, 25, 62, 57);
    cout << player2.toString() << endl;
    
    BaseballPlayer player3("Chan Ho Park", 34, 200004.20, 46.4, 18, 2);
    cout << player3.toString() << endl;
    
    return 0;
}



