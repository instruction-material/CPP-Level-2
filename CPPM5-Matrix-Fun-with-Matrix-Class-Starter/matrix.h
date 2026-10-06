#ifndef MATRIX_H
#define MATRIX_H

#include <cstddef>
#include <exception>
#include <istream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

constexpr int MAX_MATRIX_DIMENSION = 20;

class MatrixInputStopped : public std::exception {
public:
    const char* what() const noexcept override { return "Matrix input stopped"; }
};
class UnfinishedMatrixTask : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

namespace matrix_detail {
std::string_view trimmed(std::string_view text);
std::string line(std::istream& input);
bool parseElement(std::string_view text, int& result);
} // namespace matrix_detail

class Matrix {
private:
    // Dimensions are derived from storage, including after generated moves.
    std::vector<std::vector<int>> mat;
    std::size_t matNum;
public:
    Matrix(int r, int c);
    Matrix(const Matrix& other) = default;
    Matrix(Matrix&& other) noexcept = default;
    Matrix& operator=(const Matrix& other);
    Matrix& operator=(Matrix&& other) noexcept = default;
    int getNumRows() const;
    int getNumCols() const;
    int get(int r, int c) const;
    void fillMatrix();
    void fillMatrix(std::istream& input);
    Matrix add(const Matrix& other) const;
    Matrix multiply(const Matrix& other) const;
    void display() const;
};

#endif // MATRIX_H
