#include <charconv>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <locale>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>

constexpr std::size_t MAX_BATCH = 20;

std::string_view trimmed(const std::string_view text) {
    const auto first = text.find_first_not_of(" \t\r\n\f\v");
    if (first == std::string_view::npos) return {};
    const auto last = text.find_last_not_of(" \t\r\n\f\v");
    return text.substr(first, last - first + 1);
}

bool parseWeight(const std::string_view text, double& result) {
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

bool parseCount(std::string_view text, std::size_t& result) {
    text = trimmed(text);
    if (text.starts_with('+')) text.remove_prefix(1);
    if (text.empty()) return false;
    std::size_t value = 0;
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size() ||
        value == 0 || value > MAX_BATCH) return false;
    result = value;
    return true;
}

enum class LineState { ready, stopped, failed };
LineState readLine(std::istream& input, std::string& line) {
    if (std::getline(input, line)) return LineState::ready;
    return input.eof() && !input.bad() ? LineState::stopped : LineState::failed;
}

class Object {
public:
    std::string name;
    double weight;

    // The array bonus needs a safe placeholder before input initializes each slot.
    Object() : name(), weight(0) {}
    // BMI means base/member initialization here. Weight is measured in pounds.
    Object(std::string nextName, const double nextWeight)
        : name(std::move(nextName)), weight(nextWeight) {
        validate();
    }
    void validate() const {
        if (trimmed(name).empty() || !std::isfinite(weight) || weight < 0) {
            throw std::invalid_argument("Use a nonempty name and finite nonnegative weight");
        }
    }
    void print(std::ostream& output = std::cout) const {
        validate();
        constexpr double poundsPerKilogram = 2.205;
        output << "Nice! This object is named " << name << " and weighs "
               << weight << " pounds, which is " << weight / poundsPerKilogram
               << " kilograms.\n";
    }
};

LineState readObject(std::istream& input, std::ostream& output,
                     std::string& name, double& weight) {
    std::string line;
    while (true) {
        output << "\nAnother object is coming!\nWhat is its name? [!quit exits.] ";
        const auto state = readLine(input, line);
        if (state != LineState::ready) return state;
        const auto token = trimmed(line);
        if (token == "!quit") return LineState::stopped;
        if (!token.empty()) { name = std::string(token); break; }
        output << "Enter a nonempty name.\n";
    }
    while (true) {
        output << "Enter the object's weight in pounds [!quit cancels]: ";
        const auto state = readLine(input, line);
        if (state != LineState::ready) return state;
        if (trimmed(line) == "!quit") return LineState::stopped;
        if (parseWeight(line, weight)) return LineState::ready;
        output << "Enter one finite nonnegative weight.\n";
    }
}

void printDynamicObject(const std::string& name, const double weight,
                        std::ostream& output) {
    Object* nextObject = new Object(name, weight);
    try {
        nextObject->print(output);
    } catch (...) {
        delete nextObject;
        throw;
    }
    delete nextObject;
    // The released object is never dereferenced again.
}

int runAssembly(std::istream& input, std::ostream& output) {
    while (true) {
        std::string name;
        double weight = 0;
        const auto state = readObject(input, output, name, weight);
        if (state == LineState::stopped) return 0;
        if (state == LineState::failed) { output << "Input could not be read.\n"; return 1; }
        printDynamicObject(name, weight, output);
    }
}

int runBatch(std::istream& input, std::ostream& output) {
    std::size_t count = 0;
    std::string line;
    while (true) {
        output << "How many objects [1-20, !quit cancels]? ";
        const auto state = readLine(input, line);
        if (state == LineState::stopped) return 0;
        if (state == LineState::failed) { output << "Input could not be read.\n"; return 1; }
        if (trimmed(line) == "!quit") return 0;
        if (parseCount(line, count)) break;
        output << "Enter one whole count from 1 through 20.\n";
    }
    Object* objects = new Object[count];
    int status = 0;
    bool complete = true;
    try {
        for (std::size_t i = 0; i < count; ++i) {
            std::string name;
            double weight = 0;
            const auto state = readObject(input, output, name, weight);
            if (state != LineState::ready) {
                complete = false;
                status = state == LineState::failed ? 1 : 0;
                output << (status == 1 ? "Input could not be read.\n"
                                      : "Batch cancelled; no objects printed.\n");
                break;
            }
            objects[i] = Object(name, weight);
        }
        if (complete) {
            for (std::size_t i = 0; i < count; ++i) objects[i].print(output);
        }
    } catch (...) {
        delete[] objects;
        throw;
    }
    delete[] objects;
    return status;
}

int main(const int argc, char* argv[]) {
    try {
        if (argc == 1) return runAssembly(std::cin, std::cout);
        if (argc == 2 && std::string_view(argv[1]) == "--batch") {
            return runBatch(std::cin, std::cout);
        }
        std::cerr << "Usage: main [--batch]\n";
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "Assembly Line stopped: " << error.what() << '\n';
        return 1;
    }
}
