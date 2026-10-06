#include <climits>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>

class UnfinishedTask final : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

// Provided boundary check. The caller still proves storage capacity and lifetime.
void validateRange(const void* values, const int size) {
    if (size < 0 || (size > 0 && values == nullptr)) {
        throw std::invalid_argument("Use a nonnegative size and live storage for a nonempty range");
    }
}

void fillPerfectSquares(int arr[], int size);
bool firstLast(int arr[], int size);
int sumArray(int arr[], int size);
int sumLetters(std::string words[], int size);

template<class Task>
void runTask(const char* label, Task task) {
    try {
        task();
    } catch (const UnfinishedTask&) {
        std::cout << "Learner task: " << label << " remains unfinished.\n";
    }
}

int main() {
    constexpr int count = 10;
    // Initialized storage remains defined while the four tasks are unfinished.
    int perfectSquares[count]{};
    std::string words[] = {"happy", "Juni", "computer"};
    runTask("1. perfect squares", [&] {
        fillPerfectSquares(perfectSquares, count);
        std::cout << "\nPerfect squares: ";
        for (const int value : perfectSquares) std::cout << value << " ";
        std::cout << "\n";
    });
    runTask("2. endpoint comparison", [&] {
        std::cout << "First and last are the same? " << firstLast(perfectSquares, count) << "\n";
    });
    runTask("3. integer sum", [&] {
        std::cout << "Sum: " << sumArray(perfectSquares, count) << "\n";
    });
    runTask("4. string byte count", [&] {
        std::cout << "Total letters: " << sumLetters(words, 3) << "\n";
    });
    return 0;
}

// TASK fillPerfectSquares
void fillPerfectSquares(int arr[], const int size) {
    validateRange(arr, size);
    if (size != 10) throw std::invalid_argument("The square task requires exactly 10 elements");
    for (int i = 0; i < size; ++i) arr[i] = i * i;
}
// END TASK fillPerfectSquares

// TASK firstLast
bool firstLast(int arr[], const int size) {
    validateRange(arr, size);
    return size != 0 && arr[0] == arr[size - 1];
}
// END TASK firstLast

// TASK sumArray
int sumArray(int arr[], const int size) {
    validateRange(arr, size);
    int total = 0;
    for (int i = 0; i < size; ++i) {
        if ((arr[i] > 0 && total > INT_MAX - arr[i]) ||
            (arr[i] < 0 && total < INT_MIN - arr[i])) {
            throw std::overflow_error("An ordered prefix sum cannot be represented by int");
        }
        total += arr[i];
    }
    return total;
}
// END TASK sumArray

// TASK sumLetters
int sumLetters(std::string words[], const int size) {
    validateRange(words, size);
    int total = 0;
    for (int i = 0; i < size; ++i) {
        if (words[i].size() > static_cast<std::size_t>(INT_MAX - total)) {
            throw std::overflow_error("The string byte count cannot be represented by int");
        }
        total += static_cast<int>(words[i].size());
    }
    return total;
}
// END TASK sumLetters
