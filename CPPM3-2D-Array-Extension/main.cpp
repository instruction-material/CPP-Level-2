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

int checkedCell(const int* grid, int rows, int columns, int row, int column);
double* columnAverages(const int* grid, int rows, int columns);

template<class Task> void runTask(const char* label, Task task) {
    try { task(); }
    catch (const UnfinishedTask&) {
        std::cout << "Learner task: " << label << " remains unfinished.\n";
    }
}

int main() {
    constexpr int rows = 2, columns = 3;
    const int grid[] = {2, -1, 8, 4, 5, 10};
    runTask("1. checked coordinate", [&] {
        std::cout << "Cell (1, 2): " << checkedCell(grid, rows, columns, 1, 2) << "\n";
    });
    runTask("2. column averages", [&] {
        double* averages = columnAverages(grid, rows, columns);
        std::cout << "Column averages: ";
        for (int column = 0; column < columns; ++column) std::cout << averages[column] << " ";
        std::cout << "\n";
        delete[] averages;
    });
    return 0;
}

// TASK checkedCell
int checkedCell(const int* grid, const int rows, const int columns, const int row, const int column) {
    (void)validateGrid(grid, rows, columns);
    if (row < 0 || column < 0 || row >= rows || column >= columns) {
        throw std::out_of_range("The coordinate must select a cell inside the logical rectangle");
    }
    const auto index = static_cast<std::size_t>(row) * static_cast<std::size_t>(columns) + static_cast<std::size_t>(column);
    return grid[index];
}
// END TASK checkedCell

// TASK columnAverages
double* columnAverages(const int* grid, const int rows, const int columns) {
    (void)validateGrid(grid, rows, columns);
    if (columns == 0) return nullptr;
    if (rows == 0) throw std::invalid_argument("A nonempty set of columns needs at least one row");
    double* result = new double[columns];
    for (int column = 0; column < columns; ++column) {
        long double total = 0;
        for (int row = 0; row < rows; ++row) {
            const auto index = static_cast<std::size_t>(row) * static_cast<std::size_t>(columns) + static_cast<std::size_t>(column);
            total += static_cast<long double>(grid[index]);
        }
        result[column] = static_cast<double>(total / static_cast<long double>(rows));
    }
    return result;
}
// END TASK columnAverages
