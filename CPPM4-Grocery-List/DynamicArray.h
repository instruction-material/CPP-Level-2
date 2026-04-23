#ifndef DYNAMICARRAY_H
#define DYNAMICARRAY_H

#include <cstddef>
#include <string>

// Grocery item that will be used as the type for the dynamic array
struct Grocery {
  std::string name;
  double price;

  // Default constructor
  Grocery() : name(""), price(0) {}

  // Overloaded constructor
  Grocery(const std::string& newName, double newPrice) : name(newName), price(newPrice) {}
};

constexpr size_t DEFAULT_SIZE = 5;

class DynamicArray {

  private:
    size_t mySize; // this keeps track of our current size
    size_t maxSize; // this is the capacity of our array
    Grocery *myVals; // keeps track of the values in a Grocery array

    void resize(size_t newCapacity);

  public:
    // default constructor
    DynamicArray();
    DynamicArray(const DynamicArray& other);
    DynamicArray& operator=(const DynamicArray& other);
    DynamicArray(DynamicArray&& other) noexcept;
    DynamicArray& operator=(DynamicArray&& other) noexcept;
 
    // the destructor
    ~DynamicArray();

    // adds a value to the current location in the dynamic array
    void addVal(const Grocery& val);

    // print out the current vals in the array
    void printVals() const;

    // access and prints out a specific value at an index, given that it's within our current bounds
    Grocery accessVal(size_t index) const;

    // Gets the current size of the array
    size_t getSize() const;
};

#endif // DYNAMICARRAY_H
