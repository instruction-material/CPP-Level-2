#include <iostream>
#include <stdexcept>
#include <string>

class UnfinishedTask final : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

// Preserve the original flat-array model: index zero is unused.
char square[10] = {'o', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
int checkwin();
void board();
bool applyMove(int choice, char mark);

// Provided input boundary: accept exactly one 1-9 digit after ASCII whitespace.
bool parseMove(const std::string& line, int& choice) {
    const auto first = line.find_first_not_of(" \t\r\f\v");
    if (first == std::string::npos || first != line.find_last_not_of(" \t\r\f\v") ||
        line[first] < '1' || line[first] > '9') return false;
    choice = line[first] - '0';
    return true;
}

int main() {
    try {
        int player = 1;
        board();
        for (;;) {
            std::cout << "Player " << player << ", enter a number: ";
            std::string line;
            if (!std::getline(std::cin, line)) {
                if (std::cin.eof()) {
                    std::cout << "\nGame ended before a result (input closed).\n";
                    return 0;
                }
                std::cerr << "Input could not be read.\n";
                return 1;
            }
            int choice = 0;
            const char mark = player == 1 ? 'X' : 'O';
            if (!parseMove(line, choice) || !applyMove(choice, mark)) {
                std::cout << "Invalid move\n";
                continue;
            }
            board();
            const int status = checkwin();
            if (status == 1) {
                std::cout << "Player " << player << " wins!\n";
                return 0;
            }
            if (status == 0) {
                std::cout << "Game draw\n";
                return 0;
            }
            player = player == 1 ? 2 : 1;
        }
    } catch (const UnfinishedTask&) {
        std::cout << "Learner tasks: complete applyMove, checkwin, and board before play.\n";
        return 0;
    }
}

// TASK applyMove
bool applyMove(const int choice, const char mark) {
    // TODO: implement the described flat-board task.
    (void)choice;
    (void)mark;
    throw UnfinishedTask("applyMove");
}
// END TASK applyMove

// TASK checkwin
int checkwin() {
    // TODO: implement the described flat-board task.
    throw UnfinishedTask("checkwin");
}
// END TASK checkwin

// TASK board
void board() {
    // TODO: implement the described flat-board task.
    throw UnfinishedTask("board");
}
// END TASK board
