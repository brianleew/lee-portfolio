#include <iostream>
#include <string>
using namespace std;
// inheritance
class Product {
    protected:
        string name; // only inheritance and this class can access
    private:
        double price;
        int discountPercent;
    public:
        Product(string name, double price, int discountPercent) {
            this->name = name;
            this->price = price;
            this->discountPercent = discountPercent;
        }
    double getPrice() {
        return price;
    }
    
};
class Book : public Product {
    protected:
        string author;
    private:
        string ISBN;
    public:
        Book(string name, double price, int discountPercent, string author, string ISBN) : Product(name, price, discountedPercent) {
        
        }
};
class Movie : public Product {
    protected:
        string director;
    private:
        string IMDB;
    public:
        Movie(string name, double price, int discountPercent, string director, string IMDB) : Product(name, price, discountedPercent) {
            
        }

};
int main()
{
    Book goneWithTheWind("Gone with the Wind", 14.99, 10, "Margaret Mitchell", "329032-32923");
    cout << goneWithTheWind.getAuthor() << endl;
    cout << goneWithTheWind.getISBN() << endl;
    
}


