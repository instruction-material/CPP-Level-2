#include <iostream>
#include <memory>
#include <string>
#include <vector>

void printScores(const std::string& label, const int scores[], size_t size) {
  std::cout << label << ": ";
  for (size_t i = 0; i < size; ++i) {
    std::cout << scores[i] << " ";
  }
  std::cout << std::endl;
}

void manualArrayDemo() {
  const size_t size = 4;
  int* scores = new int[size]{84, 91, 76, 88};

  printScores("Manual array", scores, size);
  std::cout << "Manual responsibility: delete[] must run exactly once." << std::endl;

  delete[] scores;
  scores = nullptr;
}

void vectorDemo() {
  std::vector<int> scores{84, 91, 76, 88};

  std::cout << "Vector: ";
  for (int score : scores) {
    std::cout << score << " ";
  }
  std::cout << std::endl;
  std::cout << "Vector responsibility: the vector cleans up its own storage." << std::endl;
}

void uniquePointerDemo() {
  const size_t size = 4;
  std::unique_ptr<int[]> scores(new int[size]{84, 91, 76, 88});

  printScores("unique_ptr array", scores.get(), size);
  std::cout << "unique_ptr responsibility: ownership is still explicit, but cleanup is automatic." << std::endl;
}

int main() {
  manualArrayDemo();
  std::cout << std::endl;

  vectorDemo();
  std::cout << std::endl;

  uniquePointerDemo();

  return 0;
}
