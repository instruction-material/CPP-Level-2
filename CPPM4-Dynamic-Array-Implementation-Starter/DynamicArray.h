#ifndef DYNAMICARRAY_H
#define DYNAMICARRAY_H

#include <cstddef>

constexpr std::size_t DEFAULT_SIZE = 5;

class DynamicArray {
private:
    std::size_t mySize;
    std::size_t maxSize;
    int* myVals;
    void resize(std::size_t newCapacity);

public:
    DynamicArray();
    // TODO: define independent copying and allocation-free, noexcept moving.
    DynamicArray(const DynamicArray& other);
    DynamicArray& operator=(const DynamicArray& other);
    DynamicArray(DynamicArray&& other) noexcept;
    DynamicArray& operator=(DynamicArray&& other) noexcept;
    ~DynamicArray();
    void addVal(int val);
    void printVals() const;
    int get(std::size_t index) const;
};

#endif // DYNAMICARRAY_H
