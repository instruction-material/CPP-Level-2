#ifndef DYNAMICARRAY_H
#define DYNAMICARRAY_H

#include <cstddef>
#include <stdexcept>
#include <string>

class UnfinishedGroceryTask final : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

struct Grocery {
    std::string name;
    double price;
    // Provided initialized placeholder for unused array slots.
    Grocery() : name(), price(0) {}
    Grocery(const std::string& newName, const double newPrice) : name(), price(0) {
        // TODO: initialize the real record from both arguments.
        (void)newName; (void)newPrice;
        throw UnfinishedGroceryTask("Unfinished learner task: Grocery record constructor");
    }
};

constexpr std::size_t DEFAULT_SIZE = 5;
class DynamicArray {
private:
    std::size_t mySize;
    std::size_t maxSize;
    Grocery* myVals;
    void resize(std::size_t newCapacity);

public:
    DynamicArray();
    // TODO: define independent copies and allocation-free noexcept moves.
    DynamicArray(const DynamicArray& other);
    DynamicArray& operator=(const DynamicArray& other);
    DynamicArray(DynamicArray&& other) noexcept;
    DynamicArray& operator=(DynamicArray&& other) noexcept;
    ~DynamicArray();
    void addVal(const Grocery& val);
    void printVals() const;
    Grocery accessVal(std::size_t index) const;
    std::size_t getSize() const;
};

#endif // DYNAMICARRAY_H
