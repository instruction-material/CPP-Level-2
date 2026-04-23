#include <iostream>
#include <string>

int main() {
  // creates a new pointer p1
  auto p1 = new int;

  // sets p1 to point to an anonymous variable with whatever integer value comes in from the console
  std::cout << "Please enter an integer: " << std::endl;
  std::cin >> *p1;

  // prints out the value of p1 to demonstrate the storage of the value
  std::cout << "The value of *p1 is: " << *p1 << std::endl;

  // deletes that new information!
  std::cout << "Cleaning up p1: " << std::endl;
  delete p1;

  // the below line will now show that *p1 is 0, which is also nullptr
  std::cout << "After deletion, *p1 is now equal to: " << *p1 << std::endl;

  // sets p1 to nullptr
  p1 = nullptr;

  // Further example code using dynamic variables
  std::cout << "\n\n–––––– String pointer lifecycle ––––––" << std::endl;

  // Create a new string ptr
  auto strPtr = new std::string;

  // Assign the value that the strptr points to
  *strPtr = "Dynamic input";
  std::cout << *strPtr << std::endl;
  std::cout << strPtr << std::endl;

  // delete the old strPtr, cleaning it up
  delete strPtr;

  // reset the strPtr to nullptr
  strPtr = nullptr;
}
