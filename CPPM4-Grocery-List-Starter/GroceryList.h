#ifndef GROCERYLIST_H
#define GROCERYLIST_H

#include "DynamicArray.h"

// Rule of Zero: member copying/moving uses DynamicArray's owning operations.
class GroceryList {
private:
    DynamicArray groceries;

public:
    GroceryList();
    void addItem(const Grocery& item);
    void printList() const;
    // One-based item numbers; invalid numbers report rejection without mutation.
    void removeItem(std::size_t itemNum);
};

#endif // GROCERYLIST_H
