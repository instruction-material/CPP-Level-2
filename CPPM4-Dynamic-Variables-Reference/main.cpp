#include <charconv>
#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

bool parseInteger(const std::string& line, int& value) {
    std::string_view token(line);
    while (!token.empty() && std::isspace(static_cast<unsigned char>(token.front()))) token.remove_prefix(1);
    while (!token.empty() && std::isspace(static_cast<unsigned char>(token.back()))) token.remove_suffix(1);
    if (token.empty()) return false;
    if (token.front() == '+') {
        token.remove_prefix(1);
        if (token.empty() || token.front() == '-' || token.front() == '+') return false;
    }
    int parsed = 0;
    const auto result = std::from_chars(token.data(), token.data() + token.size(), parsed);
    if (result.ec != std::errc{} || result.ptr != token.data() + token.size()) return false;
    value = parsed;
    return true;
}

void demonstrateInteger(const int value) {
    // The initialized object is live from successful new until delete.
    int* p1 = new int{value};
    try {
        std::cout << "The value of *p1 is: " << *p1 << '\n';
        std::cout << "Cleaning up p1.\n";
    } catch (...) {
        delete p1;
        throw;
    }
    delete p1;
    p1 = nullptr;
    // delete did not write zero into the destroyed object. Never read *p1 here.
    std::cout << "After deletion, p1 is nullptr: " << std::boolalpha << (p1 == nullptr) << '\n';
}

void demonstrateString() {
    std::string* strPtr = new std::string{"Dynamic input"};
    try {
        std::cout << "String pointer lifecycle\n" << *strPtr << '\n';
        std::cout << "Live string address: " << static_cast<const void*>(strPtr) << '\n';
    } catch (...) {
        delete strPtr;
        throw;
    }
    delete strPtr;
    strPtr = nullptr;
    std::cout << "After deletion, strPtr is nullptr: " << std::boolalpha << (strPtr == nullptr) << '\n';
}

int main() {
    try {
        std::cout << "Please enter an integer: ";
        std::string line;
        if (!std::getline(std::cin, line)) {
            if (std::cin.bad() || !std::cin.eof()) throw std::runtime_error("Input could not be read.");
            std::cout << "No integer entered; no dynamic object allocated.\n";
            return 0;
        }
        int value = 0;
        if (!parseInteger(line, value)) {
            std::cerr << "Expected a complete, representable integer.\n";
            return 1;
        }
        demonstrateInteger(value);
        demonstrateString();
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
