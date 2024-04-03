#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>
using namespace std;

class Weapon {
    protected:
        string name;
        int attackDmg;
        int attackDecay;
        int usedWeapon = 0;
    public:
        virtual int attack(int attackSkill) {
            return attackSkill;
        }
        Weapon(string name, int attackDmg, int attackDecay) {
            this->name = name;
            this->attackDmg = attackDmg;
            this->attackDecay = attackDecay;
        }
    void incrementWeapon() {
        usedWeapon++;
    }
    string getName() {
        return name;
    }
    int getAttackDmg() {
        return attackDmg;
    }
    int getAttackDecay() {
        return attackDecay;
    }
    void setName(string name) {
        this->name = name;
    }
    void setAttackDmg(int attackDmg) {
        this->attackDmg = attackDmg;
    }
    void setAttackDecay(int attackDecay) {
        this->attackDecay = attackDecay;
    }
        
};

class Sword : public Weapon {
    public:
        Sword(int attackDmg, int attackDecay) : Weapon("Sword", attackDmg, attackDecay) {
            this->attackDmg = attackDmg;
            this->attackDecay = attackDecay;
        }
    int attack(int attackSkill) {
        int damage = attackSkill + (getAttackDmg() - (getAttackDecay()*usedWeapon));
        incrementWeapon();
        cout << "for " << damage << " damage. ";
        return damage;
    }
        
};

class Nunchucks : public Weapon {
    public:
        Nunchucks(int attackDmg) : Weapon("Nunchucks", attackDmg, attackDecay) {
            this->attackDmg = attackDmg;
        }
    int attack(int attackSkill) {
        int dam = (attackSkill * getAttackDmg())/10;
        cout << "for " << dam << " damage. ";
        return dam;
    }
};

class Ninja {
    protected:
        Weapon *wo = nullptr;
        string name;
        int health;
        int attackSkill;
    public:
        Ninja(string name, int health, int attackSkill) {
            this->name = name;
            this->health = health;
            this->attackSkill = attackSkill;
            Weapon *wo = nullptr;
        }
    string getName() {
        return name;
    }
    int getHealth() {
        return health;
    }
    int getAttackSkill() {
        return attackSkill;
    }
    void setName(string name) {
        this->name = name;
    }
    void setHealth(int health) {
        this->health = health;
    }
    void setAttackSkill(int attackSkill) {
        this->attackSkill = attackSkill;
    }
    int attack() {
        return wo->attack(attackSkill);
    }
    void pickupWeapon(Weapon *wpn) {
        this->wo = wpn;
    }
    Ninja(const Ninja &source) //copy constructor
    {
        this->name = source.name;
        this->health = source.health;
        this->attackSkill = source.attackSkill;
        if (source.wo->getName() == "Sword")
        {
            this->wo = new Sword(source.wo->getAttackDmg(), source.wo->getAttackDecay());
        }    
        if (source.wo->getName() == "Nunchucks")
        {
            this->wo = new Nunchucks(source.wo->getAttackDmg());
        }
    }
    ~Ninja(){delete wo;}
	
    Ninja& operator=(const Ninja& source) //overloading = operator
    {
	    this->name = source.name;
        this->health = source.health;
        this->attackSkill = source.attackSkill;
        if (source.wo->getName() == "Sword")
        {
            this->wo = new Sword(source.wo->getAttackDmg(), source.wo->getAttackDecay());
        }    
        if (source.wo->getName() == "Nunchucks")
        {
            this->wo = new Nunchucks(source.wo->getAttackDmg());
        }
	}
};

int main()
{
//-------------------------------------Sword------------------------------------------------
//Create a Sword
Sword *sword = new Sword(21, 2); // 21 is the attack damage and 2 is the attack decay.
   
//Create Player 1 and pickup the Sword
Ninja player1("Maximus", 100, 12); // 100 is health and 12 is the attack skill.
player1.pickupWeapon(sword);
  
//Create Player 2 from Player 1
Ninja player2 = player1;

//Rename Player 2.
player2.setName("Achilles"); 
   
//Adjust Player 1's health.
player1.setHealth(84);
   
//Write the code that lets the players fight until one of them has 0 or less health.
cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;

cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
player2.setHealth(player2.getHealth() - player1.attack());
cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;

cout << player2.getName() << " attacks " << player1.getName() << " with a Sword ";
player1.setHealth(player1.getHealth() - player2.attack());
cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;
    
cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
player2.setHealth(player2.getHealth() - player1.attack());
cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;
    
cout << player2.getName() << " attacks " << player1.getName() << " with a Sword ";
player1.setHealth(player1.getHealth() - player2.attack());
cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;

cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
player2.setHealth(player2.getHealth() - player1.attack());
cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;

cout << player2.getName() << " attacks " << player1.getName() << " with a Sword ";
player1.setHealth(player1.getHealth() - player2.attack());
cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

// //-----------------------------------Sword & Nunchuck------------------------------------------

// //Create a Sword
// Sword *sword = new Sword(21, 2); // 21 is the attack damage and 2 is the attack decay.
   
// //Create Player 1 and pickup the Sword
// Ninja player1("Maximus", 100, 12); // 100 is health and 12 is the attack skill.
// player1.pickupWeapon(sword);
  
// //Create Player 2 from Player 1
// Ninja player2 = player1;
   
// //Rename Player 2.
// player2.setName("Achilles"); 
   
// //Adjust Player 1's health.
// player1.setHealth(84);

// Nunchucks *nunchucks = new Nunchucks(21); 
// player2.pickupWeapon(nunchucks);
   
// //Write the code that lets the players fight until one of them has 0 or less health.
// cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
// cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;

// cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
// player2.setHealth(player2.getHealth() - player1.attack());
// cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;

// cout << player2.getName() << " attacks " << player1.getName() << " with a Nunchucks ";
// player1.setHealth(player1.getHealth() - player2.attack());
// cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

// cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
// cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;
    
// cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
// player2.setHealth(player2.getHealth() - player1.attack());
// cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;
    
// cout << player2.getName() << " attacks " << player1.getName() << " with a Nunchucks ";
// player1.setHealth(player1.getHealth() - player2.attack());
// cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

// cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
// cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;

// cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";
// player2.setHealth(player2.getHealth() - player1.attack());
// cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;

// cout << player2.getName() << " attacks " << player1.getName() << " with a Nunchucks ";
// player1.setHealth(player1.getHealth() - player2.attack());
// cout << player1.getName() << " has " << player1.getHealth() << " left" << endl;

// cout << player1.getName() << " has " << player1.getHealth() << " health." << endl;
// cout << player2.getName() << " has " << player2.getHealth() << " health." << endl;
// cout << player1.getName() << " attacks " << player2.getName() << " with a Sword ";

// player2.setHealth(player2.getHealth() - player1.attack());
// cout << player2.getName() << " has " << player2.getHealth() << " left" << endl;



if (player1.getHealth() > player2.getHealth())
{
    cout << player1.getName() << " wins.";
}
if (player2.getHealth() > player1.getHealth())
{
    cout << player2.getName() << " wins.";
}
return 0;
}

















