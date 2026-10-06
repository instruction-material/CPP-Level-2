#include <array>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

void question1(const std::array<int, 20>& arr1) {
    (void)arr1;
    // TODO: Trace two observers reading ten values, advancing by one and two.
    throw std::logic_error("Implement question1");
}

void question2(const std::string& startString) {
    (void)startString;
    // TODO: Meet observers safely for empty, single, odd, and even strings.
    throw std::logic_error("Implement question2");
}

void question3(const std::string& inputStr) {
    (void)inputStr;
    // TODO: Implement the separate scanner/result index and pointer versions.
    // Each ASCII digit is separate; stop before a move could reach the end.
    throw std::logic_error("Implement question3");
}

template <typename Function>
void attempt(Function function) {
    try {
        function();
    } catch (const std::logic_error& error) {
        std::cout << "Learner task: " << error.what() << '\n';
    }
}

int main() {
    std::array<int, 20> values{};
    for (std::size_t index = 0; index < values.size(); ++index) {
        values[index] = static_cast<int>(index);
    }
    attempt([&values] { question1(values); });
    attempt([] { question2("JuniLearning"); });
    attempt([] { question3("1hello"); question3("3hello"); question3("12e4woah"); });
    return 0;
}
