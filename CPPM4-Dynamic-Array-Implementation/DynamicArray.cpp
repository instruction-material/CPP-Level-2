#include "DynamicArray.h"
#include <iostream>

// our default constructor
DynamicArray::DynamicArray() : mySize(0), maxSize(DEFAULT_SIZE), myVals(new int[DEFAULT_SIZE]) {}

DynamicArray::DynamicArray(const DynamicArray& other)
    : mySize(other.mySize), maxSize(other.maxSize), myVals(new int[other.maxSize]) {
  for (size_t i = 0; i < mySize; ++i) {
    myVals[i] = other.myVals[i];
  }
}

DynamicArray& DynamicArray::operator=(const DynamicArray& other) {
  if (this == &other) {
    return *this;
  }

  int* newVals = new int[other.maxSize];
  for (size_t i = 0; i < other.mySize; ++i) {
    newVals[i] = other.myVals[i];
  }

  delete[] myVals;
  myVals = newVals;
  mySize = other.mySize;
  maxSize = other.maxSize;
  return *this;
}

DynamicArray::DynamicArray(DynamicArray&& other) noexcept
    : mySize(other.mySize), maxSize(other.maxSize), myVals(other.myVals) {
  other.mySize = 0;
  other.maxSize = 0;
  other.myVals = nullptr;
}

DynamicArray& DynamicArray::operator=(DynamicArray&& other) noexcept {
  if (this == &other) {
    return *this;
  }

  delete[] myVals;
  myVals = other.myVals;
  mySize = other.mySize;
  maxSize = other.maxSize;

  other.mySize = 0;
  other.maxSize = 0;
  other.myVals = nullptr;
  return *this;
}

// our destructor
DynamicArray::~DynamicArray() {
  delete[] myVals;
}

void DynamicArray::resize(size_t newCapacity) {
  int* newVals = new int[newCapacity];
  for (size_t i = 0; i < mySize; ++i) {
    newVals[i] = myVals[i];
  }

  delete[] myVals;
  myVals = newVals;
  maxSize = newCapacity;
}

// adds a value to the next available spot in the array
void DynamicArray::addVal(int val) {
  // doubles in size, dynamically, if we're out of space. creates a new array and swaps the values
  if (mySize == maxSize) {
    resize(maxSize * 2);
  }
  myVals[mySize] = val;
  ++mySize;
}

// print out all the values that we are holding on to right now
void DynamicArray::printVals() const {
  for (size_t i = 0; i < mySize; ++i) {
    std::cout << myVals[i] << " ";
  }
  std::cout << std::endl;
}

// access and prints out a specific value at an index, given that it's within our current bounds
int DynamicArray::get(size_t index) const {
  if (index < mySize) {
    return myVals[index];
  } else {
    std::cout << "Error! This was not a valid index." << std::endl;
    return -1;
  }
}
