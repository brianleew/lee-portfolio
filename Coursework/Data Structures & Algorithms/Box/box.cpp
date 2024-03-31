#include <iostream>
using namespace std;

class Box {
    private:
        int *magicNumber = nullptr;
        double length;
        double width;
        double height;
    public:
        //class constructor
        Box(double l, double w, double h, int x) {
            this-> length = l;
            this-> width = w;
            this-> height = h;
            magicNumber = new int; // dynamically creating a pointer 
            *magicNumber = x; // and it points to x
        }
        
        //getters and setters
        int getInt() {
            return *magicNumber;
        }
        
        void setInt(int x) {
            *magicNumber = x;
        }
        double getLength() {
			return this->length;
		}
		double getWidth() {
			return this->width;
		}
		double getHeight() {
			return this->height;
		}
		int getMagicNumber() {
		    return *magicNumber;
		}
		
		void setLength(int length) {
			this->length = length;
		}
		void setWidth(int width) {
			this->width = width;
		}
		void setHeight(int height) {
			this->height = height;
		}
		
        // overloading the + operator // this allows the Box class to have a funtion to add box objects when using + sign (addition)
        Box operator+(Box obj) {
            Box y(length + obj.getLength(), width + obj.getWidth(), height + obj.getHeight(), *magicNumber + obj.getMagicNumber());
            return y;
        }
};



int main() {
    // instantiating box object
    Box Box1(3.3, 1.2, 1.5, 5);
    Box Box2(8.5, 6.0, 2.0, 6);
    

    //testing the overloaded + operator
    Box sum = Box1 + Box2; // adding box objects
    cout << "Sum of Length: " << sum.getLength() << endl;
    cout << "Sum of Width: " << sum.getWidth() << endl;
    cout << "Sum of Height: " << sum.getHeight() << endl;
    cout << "Sum of Magic Numbers: " << sum.getMagicNumber() << endl;
}



