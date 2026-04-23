#include <iostream>

int main() {

  std::cout << "\n";
  
  // ----- dangling pointer -----
  const auto val1 = new int;
  int* p1 = val1;
  *val1 = 10;
  delete p1;
  // error! 
  // *p1 = 20;

  // ----- dererencing a nullptr -----
  int val2 = 10;
  int* p2 = &val2;
  p1 = nullptr;
  // error!
  *p1 = 20;

  // ----- improper initialization -----
  // this line will initialize p1 to be int*, and p2 to be an int
  // int* p1, p2;

  // ----- attempting to use uninitialized pointers -----
  // int* p1;
  // int val1 = *p1;

  // ----- assigning values to pointer variables -----
  // int *p1; 
  // p1 = 5;

  // ----- assigning a pointer to an uninitialized variables -----
  // int val1;
  // int *p1 = &val1;
  // std::cout << *p1 << std::endl;

  // ----- pointer data type mismatch -----
  // std::string str = "potatoes";
  // int *p1 = &str;

}
