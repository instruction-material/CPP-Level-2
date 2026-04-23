#include <iostream>

int main() {
  constexpr int mySize = 20;
  int arr1[mySize];

  // load values into arr1
  for (int i = 0; i < mySize; ++i) {
    arr1[i] = i;
  }

  // –––– demonstrate pointer arithmetic ––– 
  // Setting a pointer equal to arr1 so that we can play around
  int *p1 = arr1;

  std::cout << "*p1 is originally equal to: " << std::endl;
  std::cout << *p1 << std::endl;

  // This prints out the location at index 4: both of these do the same thing
  int index = 4;
  std::cout << "\nPrinting out the items at index 4: " << std::endl;
  std::cout << *(p1 + index) << std::endl;
  std::cout << arr1[index] << std::endl;

  // preincrements the value, then dereferences the value at the incremented place
  std::cout << "\nPrinting out *(++p1):" << std::endl;
  std::cout << *(++p1) << std::endl;
  std::cout << "Now p1 is equal to:" << std::endl;
  std::cout << *(p1) << std::endl;

  // This prints out the location at index 21: THIS IS A BAD THING! We don't know what memory exists out there past what we allocated ...
  std::cout << "\nUh oh! We're trying to access some index that doesn't belong to us!" << std::endl;
  index = 21;
  std::cout << *(p1 + index) << std::endl;
  std::cout << arr1[index] << std::endl;
}
