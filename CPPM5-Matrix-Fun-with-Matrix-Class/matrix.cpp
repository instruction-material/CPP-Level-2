#include "matrix.h"

#include <charconv>
#include <iostream>
#include <limits>
#include <string>
#include <string_view>
#include <utility>

namespace matrix_detail {
std::size_t numMatrices = 0;
std::size_t nextNumber() {
    if (numMatrices == std::numeric_limits<std::size_t>::max()) {
        throw std::length_error("Matrix display numbers exhausted");
    }
    return ++numMatrices;
}

std::vector<std::vector<int>> storage(const int rows, const int cols) {
    if (rows == 0 && cols == 0) return {};
    if (rows < 1 || cols < 1 || rows > MAX_MATRIX_DIMENSION || cols > MAX_MATRIX_DIMENSION) {
        throw std::invalid_argument("Matrix dimensions must both be 1 through 20, or both zero");
    }
    return std::vector<std::vector<int>>(static_cast<std::size_t>(rows),
                                        std::vector<int>(static_cast<std::size_t>(cols), 0));
}

std::string_view trimmed(const std::string_view text) {
    const auto first = text.find_first_not_of(" \t\r\n\f\v");
    if (first == std::string_view::npos) return {};
    return text.substr(first, text.find_last_not_of(" \t\r\n\f\v") - first + 1);
}

bool parseElement(std::string_view text, int& result) {
    text = trimmed(text);
    if (text.starts_with('+')) {
        text.remove_prefix(1);
        if (text.starts_with('-')) return false;
    }
    if (text.empty()) return false;
    int value = 0;
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size()) return false;
    result = value;
    return true;
}

std::string line(std::istream& input) {
    std::string value;
    try {
        if (std::getline(input, value)) {
            if (trimmed(value) == "!quit") throw MatrixInputStopped();
            return value;
        }
    } catch (const MatrixInputStopped&) {
        throw;
    } catch (const std::exception&) {
        if (input.eof() && !input.bad()) throw MatrixInputStopped();
        throw std::runtime_error("Input could not be read.");
    }
    if (input.eof() && !input.bad()) throw MatrixInputStopped();
    throw std::runtime_error("Input could not be read.");
}

int checkedAdd(const int first, const int second) {
    const int maximum = std::numeric_limits<int>::max(), minimum = std::numeric_limits<int>::min();
    if ((second > 0 && first > maximum - second) || (second < 0 && first < minimum - second)) {
        throw std::overflow_error("Matrix addition exceeds the int range");
    }
    return first + second;
}

int checkedMultiply(const int first, const int second) {
    const int maximum = std::numeric_limits<int>::max(), minimum = std::numeric_limits<int>::min();
    if ((first > 0 && ((second > 0 && first > maximum / second) ||
                      (second < 0 && second < minimum / first))) ||
        (first < 0 && ((second > 0 && first < minimum / second) ||
                      (second < 0 && first < maximum / second)))) {
        throw std::overflow_error("Matrix product exceeds the int range");
    }
    return first * second;
}
} // namespace matrix_detail

Matrix::Matrix(const int r, const int c) : mat(matrix_detail::storage(r, c)), matNum(matrix_detail::nextNumber()) {}
Matrix& Matrix::operator=(const Matrix& other) {
    if (this == &other) return *this;
    // Nested vector assignment could otherwise change some rows before throwing.
    auto replacement = other.mat;
    mat.swap(replacement);
    matNum = other.matNum;
    return *this;
}
int Matrix::getNumRows() const { return static_cast<int>(mat.size()); }
int Matrix::getNumCols() const { return mat.empty() ? 0 : static_cast<int>(mat.front().size()); }
int Matrix::get(const int r, const int c) const {
    return mat.at(static_cast<std::size_t>(r)).at(static_cast<std::size_t>(c));
}

void Matrix::fillMatrix() { fillMatrix(std::cin); }
void Matrix::fillMatrix(std::istream& input) {
    auto replacement = mat;
    std::cout << "\nEnter elements of matrix " << matNum << ":\n";
    for (std::size_t i = 0; i < replacement.size(); ++i) {
        for (std::size_t j = 0; j < replacement[i].size(); ++j) {
            int value = 0;
            while (true) {
                std::cout << "Enter element (" << i + 1 << ", " << j + 1 << ") [!quit exits]: ";
                if (matrix_detail::parseElement(matrix_detail::line(input), value)) break;
                std::cout << "Enter one whole value within the int range.\n";
            }
            replacement[i][j] = value;
        }
    }
    mat = std::move(replacement);
}

Matrix Matrix::add(const Matrix& other) const {
    if (getNumRows() != other.getNumRows() || getNumCols() != other.getNumCols()) {
        std::cout << "Incompatible matrices (dimensions do not match)\n";
        return Matrix(0, 0);
    }
    Matrix result(getNumRows(), getNumCols());
    for (int i = 0; i < getNumRows(); ++i) {
        for (int j = 0; j < getNumCols(); ++j) {
            result.mat[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] =
                matrix_detail::checkedAdd(get(i, j), other.get(i, j));
        }
    }
    return result;
}

Matrix Matrix::multiply(const Matrix& other) const {
    if (getNumCols() != other.getNumRows() || getNumRows() == 0 || other.getNumCols() == 0) {
        std::cout << "Incompatible matrices (number of columns of first matrix "
                     "does not match number of rows of second matrix)\n";
        return Matrix(0, 0);
    }
    Matrix result(getNumRows(), other.getNumCols());
    for (int i = 0; i < getNumRows(); ++i) {
        for (int j = 0; j < other.getNumCols(); ++j) {
            int total = 0;
            for (int k = 0; k < getNumCols(); ++k) {
                total = matrix_detail::checkedAdd(total, matrix_detail::checkedMultiply(get(i, k), other.get(k, j)));
            }
            result.mat[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] = total;
        }
    }
    return result;
}

void Matrix::display() const {
    std::cout << "Matrix " << matNum << ":\n";
    for (const auto& row : mat) {
        for (const int value : row) std::cout << value << '\t';
        std::cout << '\n';
    }
    std::cout << '\n';
}
