#include <iostream>
#include <stdio.h> 

int sumArray(int *arr, int m, int n);
int minArray(int *arr, int m, int n);
int** multTable(int N);
float* averageArray(int *arr, int m, int n);
  
int main() 
{ 
  int arr[][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}; 
  int m = 3, n = 3; 

  std::cout << "\n2D array:\n";
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      std::cout << arr[i][j] << " ";
    }
    std::cout << " " << std::endl;
  }
  
  std::cout << "\nSum: " << sumArray((int *)arr, m, n) << std::endl;
  std::cout << "Min: " << minArray((int *)arr, m, n) << std::endl;

  std::cout << "\n5x5 multiplication table:\n";
  int** result = multTable(5);
  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
      std::cout << result[i][j] << " ";
    }
    std::cout << " " << std::endl;
  }

  std::cout << "\nRow averages: ";
  float* result2 = averageArray((int *)arr, m, n);
  for (int i = 0; i < m; i++) {
    std::cout << result2[i] << " ";
  }
}

// 1. Write a method that takes in a 2D array of integers and returns the sum of all of the integers in the array.
int sumArray(int *arr, int m, int n) {
  int sum = 0;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      sum += *((arr+i*n) + j);
    }
  }
  return sum;
}

// 2. Write a method that takes in a 2D array of integers and returns the minimum of all of the integers in the array.
int minArray(int *arr, int m, int n) {
  int min = *(arr);
  int i, j;
  for (i = 0; i < m; i++) {
    for (j = 0; j < n; j++) {
      if (*((arr+i*n) + j) < min) {
        min = *((arr+i*n) + j);
      }
    }
  }
  return min;
}

// 3. Write a method that takes in an integer N and returns a 2D array of the NxN multiplication table. Then, print out the array in grid format.
int** multTable(int N) {
  int** result = 0;
  result = new int*[N];
  int i,j;

  for (i = 0; i < N; i++) {
    result[i] = new int[N];
    for (j = 0; j < N; j++) {
        result[i][j] = (i+1) * (j+1);
      }
    }
  return result;
} 
  
// 4. Write a method that takes in a 2D array of integers and returns an array (one-dimensional) of the averages of the integers in each row. Make sure the averages are returned as doubles!
float* averageArray(int *arr, int m, int n) {
  float* result = 0;
  result = new float[m];
  int i,j,sum;
  float mean;

  for (i = 0; i < m; i++) {
    sum = 0;
    for (j = 0; j < n; j++) {
      sum += *((arr+i*n) + j);
    }
    mean = sum/n;
    result[i] = mean;
  }

  return result;
}