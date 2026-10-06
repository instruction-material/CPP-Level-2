#include "GroceryList.h"

#include <iostream>
#include <utility>

GroceryList::GroceryList() = default;

void GroceryList::addItem(const Grocery& item) {
    groceries.addVal(item);
}

void GroceryList::printList() const {
    std::cout << "Here are your groceries! You have " << groceries.getSize()
              << " grocery items.\n";
    groceries.printVals();
}

void GroceryList::removeItem(const std::size_t itemNum) {
    if (itemNum == 0 || itemNum > groceries.getSize()) {
        std::cout << "Sorry! That's not a valid item number to remove.\n";
        return;
    }
    DynamicArray replacement;
    for (std::size_t i = 0; i < groceries.getSize(); ++i) {
        if (i + 1 != itemNum) replacement.addVal(groceries.accessVal(i));
    }
    // All surviving string copies succeeded. Commit with allocation-free moves.
    std::swap(replacement, groceries);
    std::cout << "You have successfully removed the item number " << itemNum
              << " from your list.\n";
}
