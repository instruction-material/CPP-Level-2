#include <iostream>
#include <string>

// Basic object class that has name and weight properties
class Object {
  public: 
    std::string name;
    double weight;

    // Basic constructor using the BMI
    Object(std::string nextName, double nextWeight) 
    : name(nextName), weight(nextWeight) {}

    // Function that prints out information about the current object
    void print() {
      double kiloConversionRate = 2.205;
      double kilograms = weight / kiloConversionRate;
      std::cout << "Nice! This object is named " << name << " and weighs " << weight << " pounds, which is " << kilograms << " kilograms.\n" << std::endl;
    }
};


int main() {
  std::string nextName = "";
  double nextWeight;

  // Loop while the quit command isn't reached
  while (nextName != "!quit") {
    std::cout << "\nAnother object is coming!\nWhat is its name? [Type !quit to exit.] ";
    std::cin >> nextName;
    if (nextName != "!quit") {
      std::cout << "Enter the object's weight in pounds: ";
      std::cin >> nextWeight;

      // Create a new object based on the new information
      Object* nextObject = new Object(nextName, nextWeight);
      (*nextObject).print();
      delete nextObject;
    }
  }
}