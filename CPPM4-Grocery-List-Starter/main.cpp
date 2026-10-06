#include "GroceryList.h"

#include <charconv>
#include <cmath>
#include <iostream>
#include <locale>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>

std::string_view trimmed(const std::string_view text) {
    const auto first = text.find_first_not_of(" \t\r\n\f\v");
    if (first == std::string_view::npos) return {};
    const auto last = text.find_last_not_of(" \t\r\n\f\v");
    return text.substr(first, last - first + 1);
}

bool parsePrice(const std::string_view text, double& result) {
    const auto token = trimmed(text);
    if (token.empty()) return false;
    std::istringstream input{std::string(token)};
    input.imbue(std::locale::classic());
    double value = 0;
    input >> std::noskipws >> value;
    if (!input || !input.eof() || !std::isfinite(value) || value < 0) return false;
    result = value;
    return true;
}

bool parseItemNumber(std::string_view text, std::size_t& result) {
    text = trimmed(text);
    if (text.starts_with('+')) text.remove_prefix(1);
    if (text.empty()) return false;
    std::size_t value = 0;
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size() || value == 0) return false;
    result = value;
    return true;
}

enum class LineState { ready, stopped, failed };
LineState readLine(std::istream& input, std::string& line) {
    if (std::getline(input, line)) return LineState::ready;
    return input.eof() && !input.bad() ? LineState::stopped : LineState::failed;
}
int stopFor(const LineState state) {
    if (state == LineState::failed) { std::cerr << "Input could not be read.\n"; return 1; }
    return 0;
}

int runGroceryMenu(GroceryList& list, std::istream& input) {
    // TODO: implement add/print/remove/!quit with complete lines and validation.
    // Rejected or incomplete input must not mutate the list or reuse old values.
    (void)list; (void)input;
    throw UnfinishedGroceryTask("Unfinished learner task: Grocery menu");
}

void seedDemonstration(GroceryList& list) {
    list.addItem(Grocery("milk", 2.00));
    list.printList();
    list.addItem(Grocery("cheese", 5.00));
    list.printList();
    list.addItem(Grocery("eggs", 3.25));
    list.removeItem(3);
    list.printList();
}

int main() {
    try {
        GroceryList myList;
        seedDemonstration(myList);
        return runGroceryMenu(myList, std::cin);
    } catch (const UnfinishedGroceryTask& error) {
        std::cout << error.what() << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Grocery List stopped: " << error.what() << '\n';
        return 1;
    }
}
