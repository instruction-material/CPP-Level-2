#include "profile.h"

#include <charconv>
#include <iostream>
#include <limits>
#include <string>
#include <string_view>

std::string_view trimmed(const std::string_view text) {
    const auto first = text.find_first_not_of(" \t\r\n\f\v");
    if (first == std::string_view::npos) return {};
    return text.substr(first, text.find_last_not_of(" \t\r\n\f\v") - first + 1);
}

bool parseHeartCount(std::string_view text, int& result, const bool signedDelta = false) {
    text = trimmed(text);
    if (text.starts_with('+')) {
        text.remove_prefix(1);
        if (text.starts_with('-')) return false;
    }
    if (text.empty()) return false;
    int value = 0;
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size() ||
        (!signedDelta && value < 0)) return false;
    result = value;
    return true;
}

bool parsePostNumber(std::string_view text, std::size_t& result) {
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
    try {
        if (std::getline(input, line)) return LineState::ready;
    } catch (const std::exception&) {
        return input.eof() && !input.bad() ? LineState::stopped : LineState::failed;
    }
    return input.eof() && !input.bad() ? LineState::stopped : LineState::failed;
}
int stopFor(const LineState state) {
    if (state == LineState::failed) { std::cerr << "Input could not be read.\n"; return 1; }
    return 0;
}

int runProfileMenu(Profile& profile, std::istream& input) {
    std::cout << "Profile Posts: fictional local records only.\n"
              << "Use add, print, view, hearts, remove, sum, fill or !quit.\n";
    std::string line;
    while (true) {
        std::cout << "Command: ";
        auto state = readLine(input, line);
        if (state != LineState::ready) return stopFor(state);
        const std::string command(trimmed(line));
        if (command == "!quit") return 0;
        if (command == "print") { profile.printPosts(); continue; }
        if (command == "sum") {
            try { const int total = profile.sumHearts(); std::cout << "Total hearts: " << total << '\n'; }
            catch (const std::overflow_error& error) { std::cout << "Rejected: " << error.what() << '\n'; }
            continue;
        }
        if (command == "fill") { profile.fillProfile(); continue; }
        if (command == "add") {
            std::string caption;
            while (true) {
                std::cout << "Caption [!quit exits]: ";
                state = readLine(input, line);
                if (state != LineState::ready) return stopFor(state);
                if (trimmed(line) == "!quit") return 0;
                if (!trimmed(line).empty()) { caption = std::string(trimmed(line)); break; }
                std::cout << "Enter a nonempty caption.\n";
            }
            int hearts = 0;
            while (true) {
                std::cout << "Initial hearts [!quit exits]: ";
                state = readLine(input, line);
                if (state != LineState::ready) return stopFor(state);
                if (trimmed(line) == "!quit") return 0;
                if (parseHeartCount(line, hearts)) break;
                std::cout << "Enter one whole heart count from 0 to " << std::numeric_limits<int>::max() << ".\n";
            }
            profile.addPost({caption, hearts});
            std::cout << "Post added.\n";
        } else if (command == "view" || command == "hearts" || command == "remove") {
            std::size_t number = 0;
            while (true) {
                std::cout << "One-based post number [!quit exits]: ";
                state = readLine(input, line);
                if (state != LineState::ready) return stopFor(state);
                if (trimmed(line) == "!quit") return 0;
                if (parsePostNumber(line, number)) break;
                std::cout << "Enter one positive whole post number.\n";
            }
            if (command == "view") profile.printPost(number - 1);
            else if (command == "remove") profile.removePost(number - 1);
            else {
                int delta = 0;
                while (true) {
                    std::cout << "Signed heart change [!quit exits]: ";
                    state = readLine(input, line);
                    if (state != LineState::ready) return stopFor(state);
                    if (trimmed(line) == "!quit") return 0;
                    if (parseHeartCount(line, delta, true)) break;
                    std::cout << "Enter one signed whole change within the int range.\n";
                }
                try { profile.addHearts(number - 1, delta); }
                catch (const std::invalid_argument& error) { std::cout << "Rejected: " << error.what() << '\n'; }
                catch (const std::overflow_error& error) { std::cout << "Rejected: " << error.what() << '\n'; }
            }
        } else {
            std::cout << "Unknown command. Use add, print, view, hearts, remove, sum, fill or !quit.\n";
        }
    }
}

void originalDemonstration(Profile& profile) {
    profile.addPost({"My first post!", 30});
    std::cout << "\nMy total hearts: " << profile.sumHearts() << "\n\n";
    profile.addPost({"Incredible coders come from all backgrounds!", 100});
    profile.addPost({"A new caption", 20});
    profile.printPosts();
    profile.removePost(1);
    profile.printPosts();
    profile.addHearts(0, 10);
    profile.printPosts();
    const Post beach{"On the beach!", 20};
    for (int i = 0; i < 5; ++i) profile.addPost(beach);
    profile.printPosts();
}

int main(const int argc, char* argv[]) {
    if (argc > 2 || (argc == 2 && std::string_view(argv[1]) != "--demo")) {
        std::cerr << "Usage: main [--demo]\n";
        return 2;
    }
    try {
        Profile profile;
        if (argc == 2) { originalDemonstration(profile); return 0; }
        return runProfileMenu(profile, std::cin);
    } catch (const UnfinishedProfileTask& error) {
        std::cout << error.what() << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Profile Posts stopped: " << error.what() << '\n';
        return 1;
    }
}
