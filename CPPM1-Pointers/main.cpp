#include <iostream>

int main() {  
  int val = 5;
  int* p1 = &val;

  // Assume we have a pointer named p1 that points to int val = 5. What happens when we print out *p1?
  std::cout << "\n" << *p1 << std::endl;

  // What happens when we print out p1 without dereferencing it?
  std::cout << p1 << std::endl;

  // What happens when we change the value of *p1?
  *p1 = 10;
  std::cout << *p1 << std::endl;
  std::cout << val << std::endl;

  // If we set a new pointer equal to an existing one, what value does the new pointer store?
  int *p2 = p1;
  std::cout << p1 << std::endl;
  std::cout << p2 << std::endl;

  // Assume we have two pointers named p1 and p2, where p2 = p1. What happens when we change *p2?
  *p2 = 20;
  std::cout << "\nval1 is now changed because we modified p2:" << std::endl;
  std::cout << "Printing val with the pointer: " << *p1 << std::endl;
  std::cout << "Directly printing val1: " << val << std::endl;

  // What happens when we try to dereference an uninitialized pointer?
  int *p3;
  std::cout << "This is p3: " << p3 << std::endl;
  // Dereferencing an uninitialized pointer causes an error
  // std::cout << "This is *p3: " << *p3 << std::endl;

  // What happens when we try to dereference a pointer that is nullptr?
  int *p4 = nullptr;
  std::cout << "This is p4: " << p4 << std::endl;
  // Dereferencing a nullptr causes an error 
  // std::cout << "This is p4: " << *p4 << std::endl;

  // Would *p1 = &val1 work?
  // Would *p1 = val1 work?
  // Would p1 = val1 work?
}
