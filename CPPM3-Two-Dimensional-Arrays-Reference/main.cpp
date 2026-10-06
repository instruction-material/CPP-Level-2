#include <cstddef>
#include <iostream>

// A row pointer retains the three-column nested-array shape.
void printRows(const int rows[][3], const std::size_t count) {
    for (std::size_t row = 0; row < count; ++row) {
        for (std::size_t column = 0; column < 3; ++column) std::cout << rows[row][column] << " ";
        std::cout << "\n";
    }
}

int main() {
    int arr[10][10]{};
    const int arr2[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    const auto numRows = sizeof(arr) / sizeof(arr[0]);
    const auto numCols = sizeof(arr[0]) / sizeof(arr[0][0]);
    std::cout << "Number of rows: " << numRows << "\n";
    std::cout << "Number of cols: " << numCols << "\n";
    std::cout << "Number of elements: " << numRows * numCols << "\n";
    std::cout << "Example value from arr2: " << arr2[1][1] << "\n";
    arr[4][2] = 42;
    std::cout << arr[4][2] << "\n";
    for (std::size_t row = 0; row < numRows; ++row) {
        for (std::size_t column = 0; column < numCols; ++column) {
            arr[row][column] = static_cast<int>(row + column);
            std::cout << arr[row][column] << "\t";
        }
        std::cout << "\n";
    }
    std::cout << "Nested rows through a typed function boundary:\n";
    printRows(arr2, 3);
    // A separate flat six-element object can use row * columns + column.
    constexpr std::size_t rows = 2, columns = 3;
    const int flat[rows * columns] = {1, 2, 3, 4, 5, 6};
    std::cout << "A real flat rectangular grid:\n";
    for (std::size_t row = 0; row < rows; ++row) {
        for (std::size_t column = 0; column < columns; ++column) std::cout << flat[row * columns + column] << " ";
        std::cout << "\n";
    }
    return 0;
}
