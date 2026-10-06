#include "DynamicArray.h"

#include <stdexcept>

DynamicArray::DynamicArray() : mySize(0), maxSize(0), myVals(nullptr) {
    // TODO: establish the initial owned capacity. This empty placeholder is safe.
}

// Provided cleanup also handles the empty placeholder. Keep one owner per buffer.
DynamicArray::~DynamicArray() {
    delete[] myVals;
}

void DynamicArray::resize(const std::size_t newCapacity) {
    // TODO: validate capacity, prepare a replacement, then commit without data loss.
    (void)newCapacity;
    throw std::logic_error("Unfinished learner task: resize");
}

void DynamicArray::addVal(const int val) {
    // TODO: grow safely when full, including after a move, then initialize one slot.
    (void)val;
    throw std::logic_error("Unfinished learner task: addVal");
}

void DynamicArray::printVals() const {
    // TODO: print logical elements only, followed by one newline.
    throw std::logic_error("Unfinished learner task: printVals");
}

int DynamicArray::get(const std::size_t index) const {
    // TODO: return valid data; reject an invalid index with std::out_of_range.
    (void)index;
    throw std::logic_error("Unfinished learner task: get");
}

// TODO: add the four declared copy/move definitions. They are intentionally
// absent; a driver that calls them cannot link until those tasks are implemented.
