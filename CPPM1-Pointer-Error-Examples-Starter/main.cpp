#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

// Invalid accesses are compiled only when AddressSanitizer is enabled.
#if defined(__has_feature)
#if __has_feature(address_sanitizer)
#define POINTER_DIAGNOSTICS_ENABLED 1
#endif
#endif
#if defined(__SANITIZE_ADDRESS__)
#define POINTER_DIAGNOSTICS_ENABLED 1
#endif

/* Disabled counterexamples: classify before repairing.
1. Dangling pointer:
   int* owner = new int(10);
   int* observer = owner;
   delete owner;
   *observer = 20;
2. Dereferencing nullptr:
   int* absent = nullptr;
   *absent = 20;
3. Mixed declarators:
   int* first, second;  // Determine each declared type independently.
4. Using an uninitialized pointer:
   int* uninitialized;
   int value = *uninitialized;
5. Assigning an integer to a pointer:
   int* pointer;
   pointer = 5;
6. Reading an uninitialized target:
   int value;
   int* observer = &value;
   std::cout << *observer;
7. Mismatched target type:
   std::string text = "potatoes";
   int* pointer = &text;
*/

void repairedExamples() {
    // TODO: Classify and correct all seven disabled counterexamples.
    // Record type, lifetime, ownership, and the first invalid operation.
    throw std::logic_error("Implement repairedExamples before claiming completion");
}

int main(int argc, char* argv[]) {
    if (argc != 1) {
        const std::string_view mode = argc == 2 ? argv[1] : "";
        if (mode != "--null" && mode != "--dangling") {
            std::cerr << "Usage: ./main [--null|--dangling]\n";
            return 2;
        }
#if defined(POINTER_DIAGNOSTICS_ENABLED)
        if (mode == "--null") {
            std::cout << "Diagnostic only: null store" << std::endl;
            int* absent = nullptr;
            *absent = 20;  // Deliberately invalid; UBSan must stop this run.
        } else {
            std::cout << "Diagnostic only: dangling store" << std::endl;
            int* owner = new int(10);
            int* observer = owner;
            delete owner;
            *observer = 20;  // Deliberately invalid; ASan must stop this run.
            std::cout << *observer << '\n';
        }
        return 1;  // Reaching this point does not make the invalid access valid.
#else
        std::cerr << "Diagnostic modes require an AddressSanitizer build. "
                     "Use make main-debug.\n";
        return 2;
#endif
    }
    try {
        repairedExamples();
    } catch (const std::logic_error& error) {
        std::cout << "Learner task: " << error.what() << '\n';
    }
    return 0;
}
