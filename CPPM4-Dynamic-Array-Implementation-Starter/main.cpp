#include "DynamicArray.h"

#include <iostream>
#include <stdexcept>
#include <string>

int main() {
    std::cout << "DynamicArray learner project. Implement the tasks in the brief.\n";
    try {
        DynamicArray myArray;
        for (int i = 1; i <= 81; ++i) {
            myArray.addVal(i);
            std::cout << "Adding " << i << '\n';
        }
        std::cout << "\nArray: \n";
        myArray.printVals();
    } catch (const std::logic_error& error) {
        if (!std::string(error.what()).starts_with("Unfinished learner task:")) {
            throw;
        }
        std::cout << error.what() << '\n';
    }
    return 0;
}
