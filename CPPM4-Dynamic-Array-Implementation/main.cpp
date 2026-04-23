#include <iostream>
#include "DynamicArray.h"

int main() {
  DynamicArray myArray;
  std::cout << std::endl;
  for (int i = 1; i <= 81; ++i) {
    myArray.addVal(i);
    std::cout << "Adding " << i << std::endl;
  }

  std::cout << "\nArray: " << std::endl;
  myArray.printVals();
}
