#include "matrix.h"
#include <iostream>

namespace {
int numMatrices = 0;
}

Matrix::Matrix(int r, int c)
    : numRows(r > 0 ? r : 0),
      numCols(c > 0 ? c : 0),
      mat(static_cast<size_t>(numRows), std::vector<int>(static_cast<size_t>(numCols), 0)),
      matNum(++numMatrices) {}

int Matrix::getNumRows() const {
  return numRows;
}

int Matrix::getNumCols() const {
  return numCols;
}

int Matrix::get(int r, int c) const {
  return mat.at(static_cast<size_t>(r)).at(static_cast<size_t>(c));
}

void Matrix::fillMatrix() {
  std::cout << std::endl << "Enter elements of matrix " << matNum << ":" << std::endl;
  for (int i = 0; i < numRows; ++i) {
    for (int j = 0; j < numCols; ++j) {
      std::cout << "Enter element (" << i + 1 << ", " << j + 1 << "): ";
      std::cin >> mat[static_cast<size_t>(i)][static_cast<size_t>(j)];
    }
  }
}

Matrix Matrix::add(const Matrix& other) const {
  if (numRows != other.getNumRows() || numCols != other.getNumCols()) {
    std::cout << "Incompatible matrices (dimensions do not match)" << std::endl;
    return Matrix(0, 0);
  }

  Matrix result(numRows, numCols);

  for (int i = 0; i < numRows; ++i) {
    for (int j = 0; j < numCols; ++j) {
      result.mat[static_cast<size_t>(i)][static_cast<size_t>(j)] =
          mat[static_cast<size_t>(i)][static_cast<size_t>(j)] + other.get(i, j);
    }
  }

  return result;
}

Matrix Matrix::multiply(const Matrix& other) const {
  if (numCols != other.getNumRows()) {
    std::cout << "Incompatible matrices (number of columns of first matrix does not match number of rows of second matrix)" << std::endl;
    return Matrix(0, 0);
  }

  Matrix result(numRows, other.getNumCols());

  for (int i = 0; i < numRows; ++i) {
    for (int j = 0; j < other.getNumCols(); ++j) {
      for (int k = 0; k < numCols; ++k) {
        result.mat[static_cast<size_t>(i)][static_cast<size_t>(j)] +=
            mat[static_cast<size_t>(i)][static_cast<size_t>(k)] * other.get(k, j);
      }
    }
  }

  return result;
}

void Matrix::display() const {
  std::cout << "Matrix " << matNum << ":" << std::endl;
  for (int i = 0; i < numRows; ++i) {
    for (int j = 0; j < numCols; ++j) {
      std::cout << mat[static_cast<size_t>(i)][static_cast<size_t>(j)] << "\t";
    }
    std::cout << std::endl;
  }
  std::cout << std::endl;
}
