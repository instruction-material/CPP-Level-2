#include <array>
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

void question1(const std::array<int, 20>& arr1) {
    constexpr std::size_t mySize = 20;
    // 1. How would we advance through an array at twice the speed using a pointer?
    // declare two pointers to point to arr1
    const int* p1 = arr1.data();
    const int* p2 = arr1.data();

    std::cout << "*p1 and *p2 are originally equal to: " << std::endl;
    std::cout << *p1 << " " << *p2 << std::endl;

    for (std::size_t i = 0; i < mySize / 2; ++i) {
        std::cout << "loop number: " << i << std::endl;
        std::cout << "p1 is: " << *(p1++) << std::endl;
        std::cout << "p2 is: " << *p2 << std::endl;
        p2 += 2;
    }

    // p2 is now one-past-end; forming it is valid, dereferencing it is not.

    /*
  Debug 1a for student: why would this not work?

  int *p1 = arr1;
  int *p2 = arr1;
  for (std::size_t i = 0; i < mySize / 2; ++i) {
    std::cout << "loop number: " << i << std::endl;
    std::cout << "p1 is: " << *(p1++) << std::endl;
    std::cout << "p2 is: " << *(p2 += 2) << std::endl;
  }
  */

    /*
  Debug 1b for student: why would this not work?

  int *p1, p2 = arr1;
  for (std::size_t i = 0; i < mySize / 2; ++i) {
    std::cout << "loop number: " << i << std::endl;
    std::cout << "p1 is: " << *(p1++) << std::endl;
    std::cout << "p2 is: " << *(p2 += 2) << std::endl;
  }

  // Fixed declaration for a const array observer:
  const int *p1, *p2;
  p1 = p2 = arr1.data();
  */

    /*
  Debug 1c for student: why would this not work?

  int *p1, *p2;
  p1 = p2 = arr1;
  for (std::size_t i = 0; i < mySize / 2; ++i) {
    std::cout << "loop number: " << i << std::endl;
    std::cout << "p1 is: " << *(++p1) << std::endl;
    std::cout << "p2 is: " << *(p2 += 2) << std::endl;
  }
  */
}

void question2(const std::string& startString) {
    // 2. Generate 2 pointers that point to a reference of an array, and start one at the beginning of the array and one at the end. Print out when these pointers meet!

    const std::size_t stringSize = startString.size();

    // sizeof(chrArr) measures the vector object, not its character buffer.
    // size_t chrArrLen = sizeof(chrArr);

    // declare a char array of stringSize
    std::vector<char> chrArr(startString.begin(), startString.end());
    chrArr.push_back('\0');

    if (startString.empty()) {
        std::cout << "Question 2 needs a non-empty string." << std::endl;
        return;
    }

    // The vector owns this buffer; do not resize it while these observers exist.
    // initialize our pointers
    char* chrP1 = chrArr.data();
    char* chrP2 = chrArr.data() + stringSize - 1;

    // Keep a count of the number of times that these pointers increased
    std::size_t numP1 = 0;
    std::size_t numP2 = 0;

    // Print out some starting information about our string and pointers
    std::cout << "Starting string: " << chrArr.data() << std::endl;
    std::cout << "Starting chrP1 is pointing to: " << *chrP1 << std::endl;
    std::cout << "Starting chrP2 is pointing to: " << *chrP2 << std::endl;

    // move up the pointers until we are matching
    while (chrP1 != chrP2) {
        chrP1++;
        numP1++;
        std::cout << "chrP1 is pointing to: " << *chrP1 << std::endl;

        // if we're already matching, don't iterate more times.
        if (chrP2 != chrP1) {
            chrP2--;
            numP2++;
        }
        std::cout << "chrP2 is pointing to: " << *chrP2 << std::endl;
    }

    // Final printing of some statistics
    std::cout << "\nNumber of times p1 pointer increased: " << numP1
              << std::endl;
    std::cout << "Number of times p2 pointer decreased: " << numP2 << std::endl;

    /*
  // QUESTION 2b: Debug
  // Why doesn't this work for even-numbered sized strings?

  while (chrP1 != chrP2) {
    chrP1++;
    chrP2--;
  }
  */
}

// Two cursors: the scanner visits each character once; digits move the result.
// Non-digits leave the result unchanged but do not stop the scanner. Each digit
// is separate, including zero. Stop before a result could become one-past-end.
// The borrowed string stays alive and unchanged for the duration of this call.
void question3(const std::string& inputStr) {
    if (inputStr.empty()) {
        std::cout << "Question 3 needs a non-empty string." << std::endl;
        return;
    }

    std::cout << "Now implementing question 3 on string " << inputStr
              << " using an integer as index:" << std::endl;

    // EASIER IMPLEMENTATION WITH INTEGER INDEX POINTER
    // this end index will keep track of the index where we end up
    std::size_t end = 0;

    // iterate through the string using i to look through the string, and only changing end if the character i is looking at is a digit or not
    for (std::size_t i = 0; i < inputStr.length(); ++i) {
        std::cout << "Now looking at character " << inputStr[i] << std::endl;
        // if this character is a digit, then advance end pointer
        if (inputStr[i] >= '0' && inputStr[i] <= '9') {
            std::cout << "We encountered a digit, " << inputStr[i] << std::endl;
            // converts the increment to its numeric value
            const std::size_t increment = static_cast<std::size_t>(inputStr[i] - '0');

            // only advance end if it will not surpass the end of the length of our string
            if (increment < inputStr.length() - end) {
                end += increment;
                std::cout << "We incremented end by: " << increment
                          << ", putting our end pointer pointing to: "
                          << inputStr[end] << std::endl;
            } else {
                std::cout << "The increment would reach or pass the end of the "
                             "string, we're done!"
                          << std::endl;
                break;
            }
        }
    }

    // print out information about the end location of the second pointer
    std::cout << "The final location of the end pointer was pointing to: "
              << inputStr[end] << ", after advancing " << end << " characters."
              << std::endl;

    // ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    // IMPLEMENTATION 2
    std::cout << "Now implementing question 3 on string " << inputStr
              << " using a char*:" << std::endl;

    // create a char pointer to the address of the first character in the string
    const char* specAdvPtr = inputStr.c_str();
    std::size_t pointerOffset = 0;
    std::cout << "The pointer starts at: " << *specAdvPtr << std::endl;
    for (std::size_t i = 0; i < inputStr.length(); ++i) {
        std::cout << "Now looking at character " << inputStr[i] << std::endl;
        if (inputStr[i] >= '0' && inputStr[i] <= '9') {
            // Convert this individual ASCII digit to its integer value.
            const std::size_t increment = static_cast<std::size_t>(inputStr[i] - '0');

            if (increment < inputStr.length() - pointerOffset) {
                pointerOffset += increment;
                specAdvPtr += increment;
                std::cout << "The pointer increased by " << increment
                          << " character(s)" << std::endl;
                std::cout
                    << "The value of where the pointer is pointing at now: "
                    << *specAdvPtr << std::endl;
            } else {
                std::cout << "The increment would reach or pass the end of the "
                             "string, we're done!"
                          << std::endl;
                break;
            }
        }
    }

    // print out information about the end location of the second pointer
    std::cout << "The final location of the end pointer was pointing to: "
              << *specAdvPtr << ", after advancing " << pointerOffset
              << " characters." << std::endl;
}

int main() {
    // std::size_t is an unsigned size type; zero is a valid value.
    std::array<int, 20> arr1{};
    for (std::size_t i = 0; i < arr1.size(); ++i) {
        arr1[i] = static_cast<int>(i);
    }
    std::cout << "Question 1:" << std::endl;
    question1(arr1);
    std::cout << "\nQuestion 2:" << std::endl;
    question2("JuniLearning");
    std::cout << "\nQuestion 3:" << std::endl;
    question3("1hello");
    question3("3hello");
    question3("12e4woah");
    return 0;
}
