#include <cstddef>
#include <iostream>

int main() {
    constexpr int mySize = 20;
    int arr1[mySize]{};
    for (int i = 0; i < mySize; ++i) arr1[i] = i;

    int* p1 = arr1;
    std::cout << "*p1 is originally equal to:\n" << *p1 << "\n";
    const int index = 4;
    std::cout << "\nPrinting out the items at index 4:\n"
              << *(p1 + index) << "\n" << arr1[index] << "\n";
    std::cout << "\nPrinting out *(++p1):\n" << *(++p1) << "\n";
    std::cout << "Now p1 is equal to:\n" << *p1 << "\n";
    const std::ptrdiff_t currentOffset = p1 - arr1;
    std::cout << "Current offset: " << currentOffset << "\n";

    // One-past belongs to the same array's arithmetic range, but is not an element.
    int* const end = arr1 + mySize;
    std::cout << "One-past offset (not dereferenced): " << end - arr1 << "\n";
    std::cout << "Values by traversal: ";
    for (int* cursor = arr1; cursor != end; ++cursor) std::cout << *cursor << " ";
    std::cout << "\n";

    /* Disabled original counterexamples. Predict the validity failure first.
       After ++p1, p1 is at offset 1. p1 + 21 would attempt offset 22:
       forming that pointer is already outside this 20-element array's range.
       std::cout << *(p1 + 21) << std::endl;
       std::cout << arr1[21] << std::endl; // Index 21 is not in [0, 20).
       Do not form or dereference either expression in an ordinary run.
    */
}
