#include <iostream>
#include "DynamicArray.h"
#include "GroceryList.h"

int main() {
  // Initialize a list with our default constructor
  GroceryList myList;
  //Grocery myItem;

  Grocery myItem = Grocery("milk", 2.00);
  myList.addItem(myItem);
  myList.printList();

  myItem = Grocery("cheese", 5.00);
  myList.addItem(myItem);
  myList.printList();

  myItem = Grocery("eggs", 3.25);
  myList.addItem(myItem);
  myList.removeItem(3);
  myList.printList();

  // Declare variables to hold our inputs from the user
  std::string input = "";
  std::string itemName = "";
  double itemPrice = 0;


  std::cout << "\nWelcome to your grocery list tracker!\n";
  std::cout << "Type \"add\" to add a grocery item, type \"print\" to print your list, type \"remove\" to remove an item, or type \"!quit\" to quit.\n" << std::endl;
  // Loop while the user does not input quit sequence
  while (input != "!quit") {
    // Make a menu for the user
    std::cout << "What would you like to do? ";
    std::cin >> input;

    // Handle each case
    if (input == "add") {
      std::cout << "\nEnter the item's name: ";
      std::cin >> itemName;

      std::cout << "Great! Enter " << itemName << "'s price: ";
      std::cin >> itemPrice;
      myItem = Grocery(itemName, itemPrice);
      myList.addItem(myItem);
      std::cout << std::endl;
    } else if (input == "print") {
      std::cout << std::endl;
      myList.printList();
      std::cout << std::endl;
    } else if (input == "remove") {
      std::cout << "\nWrite an item's number to remove it: ";
      int removeIndex;
      std::cin >> removeIndex;
      myList.removeItem(removeIndex);
      std::cout << std::endl;
    }
  }
}