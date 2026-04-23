#ifndef MATRIX_H
#define MATRIX_H

#include <vector>

class Matrix {

  private:
    int numRows;

    int numCols;

    std::vector<std::vector<int>> mat;

    int matNum;
    
  public:
    Matrix(int r, int c);

    int getNumRows() const;

    int getNumCols() const;

    int get(int r, int c) const;

    void fillMatrix();

    Matrix add(const Matrix& other) const;

    Matrix multiply(const Matrix& other) const;

    void display() const;

};

#endif // MATRIX_H
