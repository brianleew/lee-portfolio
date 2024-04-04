#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <sstream>
#include <vector>
using namespace std;

class AbstractRecord {
    
    protected:
        string name;
    
    public:
        AbstractRecord(string name) {
            this->name = name;
        }
};

class StockStatRecord : public AbstractRecord {
    
    protected:
        string ticker;
        string company_name;
        double price;
    
    public:
        StockStatRecord(string name, string ticker, string company_name, double price) : AbstractRecord(name)
        {
            this->ticker = name;
            this->company_name = company_name;
            this->price = price;
        }
        const string toString() const
        {
            //StockStatRecord(1, CK HUTCHISON HOLDINGS LTD, $price=1.404816984)
            ostringstream buffer;
            buffer<<fixed<<showpoint
            <<"StockStatRecord("<<name<<", "<<company_name<<", "<<"$price="<<price<<")"<<endl;
            return buffer.str();
        }
};

class BaseBallStatRecord : public AbstractRecord {
    protected:
        string playerName;
        double salary;
        int G;
        double AVG;
    public:
        BaseBallStatRecord(string name, string playerName, double salary, int G, double AVG) : AbstractRecord(name)
        {
            this->playerName = name;
            this->salary = salary;
            this->G = G;
            this->AVG = AVG;
        }
        const string toString() const
        {
            //BaseballStatRecord(Ivan Rodriguez, 12379883, 111, 0.276)
            ostringstream buffer;
            buffer<<fixed<<showpoint
            <<"BaseballStatRecord("<<name<<", "<<salary<<", "<<G<<", "<<AVG<<")"<<endl;
            return buffer.str();
        }
};

class AbstractCSVReader {
    protected:
        string row;
    public:
        void rowToVector(string row) {
            stringstream ss(row);
        } 
        void load() {
            ifstream stockFile;
            ifstream baseballFile;
            stockFile.open("StockValuations.csv");
            baseballFile.open("MLB2008");
            getline(stockFile, row);
            getline(baseballFile, row);
            
            while (getline(stockFile, row)&&getline(baseballFile, row)) {
                ss << row;
                getline(stockFile, row);
                getline(baseballFile, row);
            }
        }

    vector<string> lineVector;
    while (getline(ss, row, ',')) {
        lineVector.push_back(row);
        vector<lineVector<string>> vectorOfLines;
    }
};

class StocksCSVReader : AbstractCSVReader {
    void createRecord() {
        StockStatRecord stockobj;
        stockobj.
    }
};

class BaseballCSVReader : AbstractCSVReader {
    void createRecord() {
        BaseballStatRecord baseballobj;
    }
};


int main() {
    StocksCSVReader stock("StockValuations.csv");
    BaseballCSVReader base("MLB2008.csv");
    cout << stock.toString() << endl;
    cout << base.toString() << endl;
}



















