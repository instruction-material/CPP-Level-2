#include <iostream>

int main() {
  // Different ways of creating arrays
  int nums[10] = {};
  const int arr[3] = {1, 2, 3};

  // Printing and updating an element in nums
  std::cout << nums[3] << std::endl;
  nums[3] = 42;
  std::cout << nums[3] << std::endl;
  std::cout << arr[0] << std::endl;

  // Calculating the size of an array
  const size_t numCount = sizeof(nums) / sizeof(nums[0]);
  std::cout << numCount << std::endl;

  // Looping through and updating the elements of an array
  for (size_t i = 0; i < numCount; ++i) {
    nums[i] = i;
  }

  // Printing the elements in an array by looping through it
  for (size_t i = 0; i < numCount; ++i) {
    std::cout << nums[i] << std::endl;
  }
}
