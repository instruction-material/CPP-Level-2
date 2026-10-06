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
    // TODO: collect compatible dimensions, fill both drafts and display a result.
    // EOF/quit stop promptly; rejected or incomplete data must not reuse old values.
    (void)input;
    throw UnfinishedMatrixTask("Unfinished learner task: Matrix program");
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
