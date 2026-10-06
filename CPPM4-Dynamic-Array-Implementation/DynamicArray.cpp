#include "DynamicArray.h"

#include <iostream>
#include <limits>
#include <stdexcept>

namespace cppm4_array_detail {
// This arithmetic bound does not promise that the machine has this much memory.
constexpr std::size_t maxElements =
    std::numeric_limits<std::size_t>::max() / sizeof(int);

std::size_t nextCapacity(const std::size_t current) {
    if (current >= maxElements) {
        throw std::length_error("DynamicArray capacity cannot grow");
    }
    if (current == 0) {
        return DEFAULT_SIZE;
    }
    // Clamp before multiplying, so doubling cannot wrap or exceed the byte bound.
    return current > maxElements / 2 ? maxElements : current * 2;
}
} // namespace cppm4_array_detail

DynamicArray::DynamicArray()
    : mySize(0), maxSize(DEFAULT_SIZE), myVals(new int[DEFAULT_SIZE]) {}

DynamicArray::DynamicArray(const DynamicArray& other)
    : mySize(other.mySize), maxSize(other.maxSize),
      myVals(other.maxSize == 0 ? nullptr : new int[other.maxSize]) {
    // Copy only initialized elements; int assignment cannot throw.
    for (std::size_t i = 0; i < mySize; ++i) {
        myVals[i] = other.myVals[i];
    }
}

DynamicArray& DynamicArray::operator=(const DynamicArray& other) {
    if (this == &other) {
        return *this;
    }
    // Allocate and copy before releasing the existing owner.
    int* newVals = other.maxSize == 0 ? nullptr : new int[other.maxSize];
    for (std::size_t i = 0; i < other.mySize; ++i) {
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

DynamicArray::~DynamicArray() {
    delete[] myVals;
}

void DynamicArray::resize(const std::size_t newCapacity) {
    if (newCapacity == 0 || newCapacity < mySize ||
        newCapacity > cppm4_array_detail::maxElements) {
        throw std::length_error("DynamicArray capacity is outside its storage bound");
    }
    int* newVals = new int[newCapacity];
    for (std::size_t i = 0; i < mySize; ++i) {
        newVals[i] = myVals[i];
    }
    delete[] myVals;
    myVals = newVals;
    maxSize = newCapacity;
}

void DynamicArray::addVal(const int val) {
    if (mySize == maxSize) {
        resize(cppm4_array_detail::nextCapacity(maxSize));
    }
    myVals[mySize] = val;
    ++mySize;
}

void DynamicArray::printVals() const {
    for (std::size_t i = 0; i < mySize; ++i) {
        std::cout << myVals[i] << " ";
    }
    std::cout << '\n';
}

int DynamicArray::get(const std::size_t index) const {
    if (index >= mySize) {
        throw std::out_of_range("DynamicArray index is outside its logical size");
    }
    return myVals[index];
}
