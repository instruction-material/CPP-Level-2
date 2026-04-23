#include <iostream>
#include <string>

bool firstLast(int arr[], int size);
int sumArray(int arr[], int size);
int sumLetters(std::string words[], int size);

int main() {
  // 1. Create and print an array containing the first 10 perfect squares (0, 1, 4, ...).

  // create array
  int perfectSquares[10];
  for (int i = 0; i < 10; i++) {
    perfectSquares[i] = i*i;
  }

  // print array
  std::cout << "\nPerfect squares: ";
  for (const int n : perfectSquares) {
    std::cout << n << " ";
  }

  std::cout << "\nFirst and last are the same? " << firstLast(perfectSquares, 10) << std::endl;
  std::cout << "Sum: " << sumArray(perfectSquares, 10) << std::endl;

  std::string words[] = {"happy", "Juni", "computer"};
  std::cout << "Total letters: " << sumLetters(words, 3) << std::endl;
}

// 2. Write a method that takes in an array of integers and its size, and returns true if the first and last elements in the array are the same, and otherwise returns false.
bool firstLast(int arr[], const int size) {
  return arr[0] == arr[size - 1];

  // if (arr[0] == arr[size - 1]) {
  //   return true;
  // }
  // return false;
}

// 3. Write a method that takes in an array of integers and its size and returns the sum of the integers in the array.
int sumArray(int arr[], const int size) {
  int total = 0;
  for (int i = 0; i < size; i++) {
    total += arr[i];
  }
  return total;
}

// 4. Write a method that takes in an array of strings and returns the total number of letters of all the strings.
int sumLetters(std::string words[], const int size) {
  int total = 0;
  for (int i = 0; i < size; i++) {
    total += words[i].size();
  }
  return total;
}
