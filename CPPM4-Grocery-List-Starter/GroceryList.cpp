#include "GroceryList.h"

GroceryList::GroceryList() = default;
void GroceryList::addItem(const Grocery& item) {
    // TODO: delegate validated storage to the custom array.
    (void)item;
    throw UnfinishedGroceryTask("Unfinished learner task: add grocery item");
}
void GroceryList::printList() const {
    // TODO: show the logical count and the records.
    throw UnfinishedGroceryTask("Unfinished learner task: print grocery list");
}
void GroceryList::removeItem(const std::size_t itemNum) {
    // TODO: reject invalid one-based numbers, prepare survivors, then commit.
    (void)itemNum;
    throw UnfinishedGroceryTask("Unfinished learner task: remove grocery item");
}
