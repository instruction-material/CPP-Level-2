#include <iostream>

int main() {
  int arr[10][10];
  const int arr2[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

  // Getting the number of rows and cols, and then printing the results
  int numRows = sizeof(arr) / sizeof(arr[0]);
  int numCols = sizeof(arr[0]) / sizeof(arr[0][0]);
  std::cout << "Number of rows: " << numRows << std::endl;
  std::cout << "Number of cols: " << numCols << std::endl;
  std::cout << "Number of elements: " << numRows * numCols << std::endl;
  std::cout << "Example value from arr2: " << arr2[1][1] << std::endl;

  // Accessing and changing values in a 2D array
  arr[4][2] = 42;
  std::cout << arr[4][2] << std::endl;

  // Looping through and printing the elements in a 2D array
  for (int i = 0; i < numRows; i++) {
    for (int j = 0; j < numCols; j++) {
      arr[i][j] = i + j;
      std::cout << arr[i][j] << "\t";
    }
    std::cout << std::endl;
  }
}
