#include "DynamicArray.h"

DynamicArray::DynamicArray() : mySize(0), maxSize(0), myVals(nullptr) {
    // TODO: establish the initial owned capacity. This empty placeholder is safe.
}
DynamicArray::~DynamicArray() { delete[] myVals; }
std::size_t DynamicArray::getSize() const { return mySize; }

void DynamicArray::resize(const std::size_t newCapacity) {
    // TODO: keep a temporary owner until all potentially throwing copies succeed.
    (void)newCapacity; (void)maxSize;
    throw UnfinishedGroceryTask("Unfinished learner task: Grocery array resize");
}
void DynamicArray::addVal(const Grocery& val) {
    // TODO: validate the draft, grow safely if full, then commit the accepted item.
    (void)val;
    throw UnfinishedGroceryTask("Unfinished learner task: Grocery array append");
}
void DynamicArray::printVals() const {
    // TODO: display logical records only, including their one-based item numbers.
    throw UnfinishedGroceryTask("Unfinished learner task: Grocery array display");
}
Grocery DynamicArray::accessVal(const std::size_t index) const {
    // TODO: return an independent record or reject an out-of-range index.
    (void)index;
    throw UnfinishedGroceryTask("Unfinished learner task: Grocery array access");
}
// TODO: add the four declared copy/move definitions. Until then, drivers that
// call those operations cannot link. Do not introduce shallow pointer copies.
