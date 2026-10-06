#include <climits>
#include <cstddef>
#include <iostream>
#include <limits>
#include <stdexcept>

class UnfinishedTask final : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

// Provided check: capacity, object shape, initialization and lifetime remain
// caller preconditions. This pointer describes one real flat int array.
std::size_t validateGrid(const int* arr, const int m, const int n) {
    if (m < 0 || n < 0) throw std::invalid_argument("Dimensions cannot be negative");
    const auto rows = static_cast<std::size_t>(m);
    const auto columns = static_cast<std::size_t>(n);
    if (columns != 0 && rows > std::numeric_limits<std::size_t>::max() / columns) {
        throw std::overflow_error("The grid element count is not representable");
    }
    const auto count = rows * columns;
    if (count > static_cast<std::size_t>(std::numeric_limits<std::ptrdiff_t>::max()) ||
        count > std::numeric_limits<std::size_t>::max() / sizeof(int)) {
        throw std::overflow_error("The grid storage extent is not representable");
    }
    if (count != 0 && arr == nullptr) throw std::invalid_argument("A nonempty grid needs live storage");
    return count;
}

// Provided cleanup for a table produced by multTable with its original N.
void deleteTable(int** table, const int rows) noexcept {
    if (table == nullptr) return;
    for (int row = 0; row < rows; ++row) delete[] table[row];
    delete[] table;
}

int sumArray(int* arr, int m, int n);
int minArray(int* arr, int m, int n);
int** multTable(int N);
double* averageArray(int* arr, int m, int n);

template<class Task>
void runTask(const char* label, Task task) {
    try { task(); }
    catch (const UnfinishedTask&) {
        std::cout << "Learner task: " << label << " remains unfinished.\n";
    }
}

int main() {
    constexpr int m = 3, n = 3;
    // Same original grid values, stored as one real nine-element array.
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 0};
    std::cout << "\n2D array:\n";
    for (int row = 0; row < m; ++row) {
        for (int column = 0; column < n; ++column) std::cout << arr[row * n + column] << " ";
        std::cout << "\n";
    }
    runTask("1. sum", [&] { std::cout << "\nSum: " << sumArray(arr, m, n) << "\n"; });
    runTask("2. minimum", [&] { std::cout << "Min: " << minArray(arr, m, n) << "\n"; });
    runTask("3. multiplication table", [] {
        std::cout << "\n5x5 multiplication table:\n";
        int** result = multTable(5);
        for (int row = 0; row < 5; ++row) {
            for (int column = 0; column < 5; ++column) std::cout << result[row][column] << " ";
            std::cout << "\n";
        }
        deleteTable(result, 5);
    });
    runTask("4. double row averages", [&] {
        double* result = averageArray(arr, m, n);
        std::cout << "\nRow averages: ";
        for (int row = 0; row < m; ++row) std::cout << result[row] << " ";
        std::cout << "\n";
        delete[] result;
    });
    return 0;
}

// 1. Write a method that takes in a 2D array of integers and returns the sum of all of the integers in the array.
// TASK sumArray
int sumArray(int* arr, const int m, const int n) {
    // TODO: implement this task after reading README.md.
    (void)arr;
    (void)m;
    (void)n;
    throw UnfinishedTask("sumArray");
}
// END TASK sumArray

// 2. Write a method that takes in a 2D array of integers and returns the minimum of all of the integers in the array.
// TASK minArray
int minArray(int* arr, const int m, const int n) {
    // TODO: implement this task after reading README.md.
    (void)arr;
    (void)m;
    (void)n;
    throw UnfinishedTask("minArray");
}
// END TASK minArray

// 3. Write a method that takes in an integer N and returns a 2D array of the NxN multiplication table. Then, print out the array in grid format.
// TASK multTable
int** multTable(const int N) {
    // TODO: implement this task after reading README.md.
    (void)N;
    throw UnfinishedTask("multTable");
}
// END TASK multTable

// 4. Write a method that takes in a 2D array of integers and returns an array (one-dimensional) of the averages of the integers in each row. Make sure the averages are returned as doubles!
// TASK averageArray
double* averageArray(int* arr, const int m, const int n) {
    // TODO: implement this task after reading README.md.
    (void)arr;
    (void)m;
    (void)n;
    throw UnfinishedTask("averageArray");
}
// END TASK averageArray
