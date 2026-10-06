#include "DynamicArray.h"

#include <exception>
#include <iostream>

int main() {
    try {
        DynamicArray myArray;
        std::cout << '\n';
        for (int i = 1; i <= 81; ++i) {
            myArray.addVal(i);
            std::cout << "Adding " << i << '\n';
        }
        std::cout << "\nArray: \n";
        myArray.printVals();
    } catch (const std::exception& error) {
        std::cerr << "Dynamic array demonstration failed: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
