#include "matrix.h"

#include <iostream>
#include <locale>
#include <sstream>
#include <string>

bool parseDimensions(const std::string& line, int& rows, int& cols) {
    std::istringstream input(line);
    input.imbue(std::locale::classic());
    int r = 0, c = 0;
    if (!(input >> r >> c)) return false;
    input >> std::ws;
    if (!input.eof() || r < 1 || c < 1 || r > MAX_MATRIX_DIMENSION || c > MAX_MATRIX_DIMENSION) return false;
    rows = r; cols = c;
    return true;
}

int runMatrixProgram(std::istream& input) {
    std::string response;
    while (true) {
        std::cout << "After creating the matrices, add or multiply them? [!quit exits] ";
        response = std::string(matrix_detail::trimmed(matrix_detail::line(input)));
        if (response == "add" || response == "multiply") break;
        std::cout << "Enter add, multiply or !quit.\n";
    }
    int r1 = 0, c1 = 0, r2 = 0, c2 = 0;
    while (true) {
        while (true) {
            std::cout << "Rows and columns for first matrix [1 through 20, !quit exits]: ";
            if (parseDimensions(matrix_detail::line(input), r1, c1)) break;
            std::cout << "Enter exactly two whole dimensions from 1 through 20.\n";
        }
        while (true) {
            std::cout << "Rows and columns for second matrix [1 through 20, !quit exits]: ";
            if (parseDimensions(matrix_detail::line(input), r2, c2)) break;
            std::cout << "Enter exactly two whole dimensions from 1 through 20.\n";
        }
        if ((response == "add" && r1 == r2 && c1 == c2) || (response == "multiply" && c1 == r2)) break;
        std::cout << (response == "add" ? "Error! Addition needs matching dimensions.\n" :
                                           "Error! Multiplication needs first columns equal to second rows.\n");
    }
    Matrix first(r1, c1), second(r2, c2);
    first.fillMatrix(input); second.fillMatrix(input);
    first.display(); second.display();
    const Matrix result = response == "add" ? first.add(second) : first.multiply(second);
    result.display();
    return 0;
}

int main(const int argc, char*[]) {
    if (argc != 1) { std::cerr << "Usage: main\n"; return 2; }
    try {
        return runMatrixProgram(std::cin);
    } catch (const MatrixInputStopped&) {
        return 0;
    } catch (const UnfinishedMatrixTask& error) {
        std::cout << error.what() << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Matrix stopped: " << error.what() << '\n';
        return 1;
    }
}
