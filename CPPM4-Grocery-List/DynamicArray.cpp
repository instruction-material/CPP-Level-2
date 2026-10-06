#include "DynamicArray.h"

#include <cmath>
#include <iostream>
#include <limits>
#include <memory>
#include <stdexcept>

namespace grocery_detail {
constexpr std::size_t maxElements =
    std::numeric_limits<std::size_t>::max() / sizeof(Grocery);

std::size_t nextCapacity(const std::size_t current) {
    if (current >= maxElements) throw std::length_error("Grocery array cannot grow");
    if (current == 0) return DEFAULT_SIZE;
    return current > maxElements / 2 ? maxElements : current * 2;
}

void validateRecord(const Grocery& record) {
    if (record.name.find_first_not_of(" \t\r\n\f\v") == std::string::npos ||
        !std::isfinite(record.price) || record.price < 0) {
        throw std::invalid_argument("Use a named record with a finite nonnegative price");
    }
}

std::unique_ptr<Grocery[]> copiedBuffer(const Grocery* values,
                                      const std::size_t size,
                                      const std::size_t capacity) {
    if (size > capacity || capacity > maxElements) {
        throw std::length_error("Grocery capacity is outside its storage bound");
    }
    std::unique_ptr<Grocery[]> replacement(capacity == 0 ? nullptr : new Grocery[capacity]);
    // Each string copy can throw. The temporary owner destroys every slot then.
    for (std::size_t i = 0; i < size; ++i) replacement[i] = values[i];
    return replacement;
}
} // namespace grocery_detail

DynamicArray::DynamicArray() : mySize(0), maxSize(0), myVals(nullptr) {
    resize(DEFAULT_SIZE);
}

DynamicArray::DynamicArray(const DynamicArray& other)
    : mySize(0), maxSize(0), myVals(nullptr) {
    auto replacement = grocery_detail::copiedBuffer(other.myVals, other.mySize, other.maxSize);
    myVals = replacement.release();
    mySize = other.mySize;
    maxSize = other.maxSize;
}

DynamicArray& DynamicArray::operator=(const DynamicArray& other) {
    if (this == &other) return *this;
    auto replacement = grocery_detail::copiedBuffer(other.myVals, other.mySize, other.maxSize);
    delete[] myVals;
    myVals = replacement.release();
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
    if (this == &other) return *this;
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
    if (newCapacity == 0) throw std::length_error("Resize needs positive capacity");
    auto replacement = grocery_detail::copiedBuffer(myVals, mySize, newCapacity);
    delete[] myVals;
    myVals = replacement.release();
    maxSize = newCapacity;
}

void DynamicArray::addVal(const Grocery& val) {
    grocery_detail::validateRecord(val);
    if (mySize == maxSize) {
        const auto capacity = grocery_detail::nextCapacity(maxSize);
        auto replacement = grocery_detail::copiedBuffer(myVals, mySize, capacity);
        replacement[mySize] = val; // Prepare the new record before releasing storage.
        delete[] myVals;
        myVals = replacement.release();
        maxSize = capacity;
    } else {
        myVals[mySize] = val; // Failed string assignment leaves logical size unchanged.
    }
    ++mySize;
}

void DynamicArray::printVals() const {
    for (std::size_t i = 0; i < mySize; ++i) {
        std::cout << "Item Number: " << i + 1 << '\n'
                  << " Name: " << myVals[i].name << '\n'
                  << " Price: " << myVals[i].price << '\n';
    }
}

Grocery DynamicArray::accessVal(const std::size_t index) const {
    if (index >= mySize) throw std::out_of_range("Grocery index is outside logical size");
    return myVals[index];
}

std::size_t DynamicArray::getSize() const {
    return mySize;
}
