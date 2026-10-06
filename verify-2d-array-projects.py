"""Native source gates for the seven CPPM3 lesson, learner and reference packs."""
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pointer_runtime', ROOT / 'verify-pointer-projects.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
run, FLAGS, SANITIZERS = runtime.run, runtime.FLAGS, runtime.SANITIZERS
FOLDERS = ['CPPM3-Two-Dimensional-Arrays-Reference', 'CPPM3-2D-Array-Practice',
           'CPPM3-2D-Array-Practice-Starter', 'CPPM3-Bank-Transactions',
           'CPPM3-Bank-Transactions-Starter',
           'CPPM3-2D-Array-Extension', 'CPPM3-2D-Array-Extension-Starter']


def input_run(binary, cwd, text='', expected=0):
    command = [str(binary)]
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True,
                               env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=0',
                                    'UBSAN_OPTIONS': 'halt_on_error=1'})
    print(json.dumps({'event': 'start', 'parentTaskId': runtime.TASK, 'cwd': str(cwd),
                      'command': command, 'pid': process.pid, 'parentPid': os.getpid(),
                      'time': datetime.now(timezone.utc).isoformat(), 'timeoutSeconds': 30}), flush=True)
    try:
        output, errors = process.communicate(text, timeout=30)
    except BaseException:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
            print(json.dumps({'event': 'child-process-group-cleanup', 'pid': process.pid}), flush=True)
        raise
    finally:
        print(json.dumps({'event': 'end', 'parentTaskId': runtime.TASK, 'pid': process.pid,
                          'exitCode': process.poll(), 'time': datetime.now(timezone.utc).isoformat()}), flush=True)
    assert process.returncode == expected, (output, errors)
    if expected == 0:
        assert not errors, errors
    else:
        assert errors == 'Input could not be read.\n', errors
    return output


def completed_learner(reference, tasks):
    source = (ROOT / reference / 'main.cpp').read_text()
    attempt = (ROOT / (reference + '-Starter') / 'main.cpp').read_text()
    for task in tasks:
        pattern = r'// TASK ' + task + r'\n[\s\S]*?\n// END TASK ' + task
        implementation = re.search(pattern, source).group()
        attempt, count = re.subn(pattern, lambda match: implementation, attempt)
        assert count == 1
    return attempt


GRID_CASES = r'''
#undef main
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <vector>

template<class Call> void invalid(Call call) {
    bool caught = false;
    try { call(); } catch (const std::invalid_argument&) { caught = true; }
    assert(caught);
}

int main() {
    assert(sumArray(nullptr, 0, 7) == 0 && sumArray(nullptr, 4, 0) == 0);
    assert(averageArray(nullptr, 0, 7) == nullptr);
    invalid([] { (void)minArray(nullptr, 0, 7); });
    invalid([] { (void)averageArray(nullptr, 4, 0); });
    int values[9]{};
    for (const auto shape : {std::array<int, 2>{-1, 3}, {3, -1}, {-1, 0}, {0, -1}}) {
        invalid([&] { (void)sumArray(values, shape[0], shape[1]); });
        invalid([&] { (void)minArray(values, shape[0], shape[1]); });
        invalid([&] { (void)averageArray(values, shape[0], shape[1]); });
    }
    invalid([] { (void)sumArray(nullptr, 1, 1); });
    invalid([] { (void)minArray(nullptr, 1, 1); });
    invalid([] { (void)averageArray(nullptr, 1, 1); });
    std::size_t cases = 0;
    for (int rows = 1; rows <= 3; ++rows) for (int cols = 1; cols <= 3; ++cols) {
        const int count = rows * cols;
        if (count > 6) continue;
        int combinations = 1;
        for (int i = 0; i < count; ++i) combinations *= 3;
        for (int code = 0; code < combinations; ++code) {
            std::array<int, 9> grid{};
            grid.fill(77);
            int digits = code, total = 0, minimum = 1;
            for (int i = 0; i < count; ++i) {
                grid[static_cast<std::size_t>(i)] = digits % 3 - 1;
                digits /= 3;
                total += grid[static_cast<std::size_t>(i)];
                minimum = std::min(minimum, grid[static_cast<std::size_t>(i)]);
            }
            const auto before = grid;
            assert(sumArray(grid.data(), rows, cols) == total);
            assert(minArray(grid.data(), rows, cols) == minimum);
            double* averages = averageArray(grid.data(), rows, cols);
            for (int row = 0; row < rows; ++row) {
                int expected = 0;
                for (int col = 0; col < cols; ++col) expected += grid[static_cast<std::size_t>(row * cols + col)];
                assert(std::abs(averages[row] - static_cast<double>(expected) / cols) < 1e-12);
            }
            delete[] averages;
            assert(grid == before);
            ++cases;
        }
    }
    const std::vector<std::vector<int>> boundaries = {
        {INT_MAX}, {INT_MIN}, {INT_MAX, 0}, {INT_MIN, 0},
        {INT_MAX, 1}, {INT_MIN, -1}, {INT_MAX, 1, -1}, {INT_MIN, -1, 1},
        {INT_MAX, -INT_MAX}, {INT_MIN, INT_MAX}, {INT_MAX, INT_MIN},
        {0, INT_MAX, -1, 1}, {0, INT_MIN, 1, -1}
    };
    for (auto grid : boundaries) {
        const auto before = grid;
        long long prefix = 0, total = 0;
        bool exceeds = false, caught = false;
        for (const int value : grid) {
            prefix += value;
            if (prefix > INT_MAX || prefix < INT_MIN) exceeds = true;
            total += value;
        }
        try {
            const int result = sumArray(grid.data(), 1, static_cast<int>(grid.size()));
            assert(!exceeds && result == total);
        } catch (const std::overflow_error&) { caught = true; }
        assert(caught == exceeds);
        assert(minArray(grid.data(), 1, static_cast<int>(grid.size())) == *std::min_element(grid.begin(), grid.end()));
        double* averages = averageArray(grid.data(), 1, static_cast<int>(grid.size()));
        const double expected = static_cast<double>(total) / static_cast<double>(grid.size());
        assert(std::abs(averages[0] - expected) <= 1e-12 * std::max(1.0, std::abs(expected)));
        delete[] averages;
        assert(grid == before);
    }
    int fractional[] = {1, 2};
    double* result = averageArray(fractional, 1, 2);
    assert(result[0] == 1.5);
    delete[] result;
    assert(multTable(0) == nullptr);
    invalid([] { (void)multTable(-1); });
    for (const int size : {46341, INT_MAX}) {
        bool caught = false;
        try { (void)multTable(size); } catch (const std::overflow_error&) { caught = true; }
        assert(caught);
    }
    for (int size = 1; size <= 12; ++size) {
        int** table = multTable(size);
        for (int row = 0; row < size; ++row) for (int col = 0; col < size; ++col) assert(table[row][col] == (row + 1) * (col + 1));
        deleteTable(table, size);
    }
    assert(cases == 1614);
    std::cout << "Verified " << cases << " rectangular grids, 13 integer boundaries, fractional averages and input preservation.\n";
}
'''

ALLOCATION_CASES = r'''
#undef main
#include <cassert>
#include <cstdlib>
#include <new>
int failAfter = -1;
int liveArrays = 0;
void* operator new[](const std::size_t bytes) {
    if (failAfter == 0) throw std::bad_alloc();
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++liveArrays;
    return memory;
}
void operator delete[](void* memory) noexcept {
    if (memory != nullptr) { --liveArrays; std::free(memory); }
}
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete[](memory); }
int main() {
    const int baseline = liveArrays;
    for (int failure = 0; failure <= 4; ++failure) {
        failAfter = failure;
        bool caught = false;
        try { (void)multTable(4); } catch (const std::bad_alloc&) { caught = true; }
        assert(caught && liveArrays == baseline);
    }
    failAfter = 5;
    int** table = multTable(4);
    assert(liveArrays == baseline + 5);
    deleteTable(table, 4);
    assert(liveArrays == baseline);
    int grid[] = {1, 2};
    failAfter = 0;
    bool caught = false;
    try { (void)averageArray(grid, 1, 2); } catch (const std::bad_alloc&) { caught = true; }
    assert(caught && liveArrays == baseline);
    failAfter = -1;
    assert(providedMain() == 0 && liveArrays == baseline);
    std::cout << "Verified five table allocation failures, average allocation failure, and driver cleanup.\n";
}
'''

BANK_CASES = r'''
#undef main
#include <array>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <chrono>
int main() {
    int grid[4][5];
    for (auto& row : grid) std::fill(row, row + 5, 77);
    std::array<std::array<int, 5>, 4> original{};
    auto snapshot = [&] {
        std::array<std::array<int, 5>, 4> result{};
        for (int row = 0; row < 4; ++row) for (int col = 0; col < 5; ++col) result[static_cast<std::size_t>(row)][static_cast<std::size_t>(col)] = grid[row][col];
        return result;
    };
    original = snapshot();
    assert(!initializeLedger(nullptr, 1012025, 100));
    assert(!initializeLedger(grid, 2292025, 100) && snapshot() == original);
    assert(initializeLedger(grid, 1012025, 100));
    assert(grid[0][0] == 0 && grid[0][1] == 1012025 && grid[0][2] == 100 && grid[0][3] == 0 && grid[0][4] == 100);
    for (int row = 1; row < 4; ++row) for (const int value : grid[row]) assert(value == 77);
    for (const int number : {-1, 0, 4, INT_MAX}) {
        const auto before = snapshot();
        assert(!recordTransaction(grid, number, 1022025, 1) && snapshot() == before);
    }
    assert(!recordTransaction(nullptr, 1, 1022025, 1));
    const auto before = snapshot();
    assert(!recordTransaction(grid, 1, 4312025, 1) && snapshot() == before);
    for (const auto boundary : {std::array<int, 2>{INT_MAX, 1}, {INT_MIN, -1}, {INT_MAX, INT_MAX}, {INT_MIN, INT_MIN}}) {
        assert(initializeLedger(grid, 1012025, boundary[0]));
        const auto saved = snapshot();
        assert(!recordTransaction(grid, 1, 1022025, boundary[1]) && snapshot() == saved);
    }
    assert(initializeLedger(grid, 1012025, 100));
    int ending = 100;
    const int amounts[] = {20, -30, 0};
    for (int number = 1; number <= 3; ++number) {
        const auto saved = snapshot();
        assert(recordTransaction(grid, number, 1022025 + number * 10000, amounts[number - 1]));
        assert(grid[number][0] == number && grid[number][2] == ending && grid[number][3] == amounts[number - 1]);
        ending += amounts[number - 1];
        assert(grid[number][4] == ending);
        const auto changed = snapshot();
        for (int row = 0; row < 4; ++row) if (row != number) assert(changed[static_cast<std::size_t>(row)] == saved[static_cast<std::size_t>(row)]);
    }
    std::ostringstream output;
    auto* previous = std::cout.rdbuf(output.rdbuf());
    const auto saved = snapshot();
    print(grid, 4, 5);
    print(nullptr, 0, 5);
    assert(snapshot() == saved);
    std::cout.rdbuf(previous);
    assert(output.str().find(" DATE: 01012025") != std::string::npos);
    for (const auto shape : {std::array<int, 2>{-1, 5}, {5, 5}, {4, 4}}) {
        bool caught = false;
        try { print(grid, shape[0], shape[1]); } catch (const std::invalid_argument&) { caught = true; }
        assert(caught && snapshot() == saved);
    }
    bool caught = false;
    try { print(nullptr, 1, 5); } catch (const std::invalid_argument&) { caught = true; }
    assert(caught);
    int parsed = 17;
    for (const auto text : {"", " ", "2.5", "7 8", "1x", "--1", "+-1", "2147483648", "-2147483649"}) assert(!parseInteger(text, parsed) && parsed == 17);
    assert(parseInteger(" \t+20\r", parsed) && parsed == 20);
    assert(parseInteger("-2147483648", parsed) && parsed == INT_MIN);
    parsed = 17;
    for (const auto text : {"0101202", "010120250", "1x012025", "02292025", "04312025", "13012025", "01010000"}) assert(!parseDate(text, parsed) && parsed == 17);
    assert(parseDate(" 01012025 ", parsed) && parsed == 1012025);
    std::size_t dates = 0;
    for (const int year : {1, 4, 100, 400, 1900, 2000, 2024, 2025, 9999}) for (int month = 1; month <= 13; ++month) for (int day = 0; day <= 32; ++day) {
        const auto date = std::chrono::year_month_day(std::chrono::year(year), std::chrono::month(static_cast<unsigned>(month)), std::chrono::day(static_cast<unsigned>(day)));
        assert(isValidDate(month * 1000000 + day * 10000 + year) == date.ok());
        ++dates;
    }
    assert(!isValidDate(-1) && !isValidDate(INT_MAX));
    std::cout << "Verified ledger mutation boundaries, input preservation, integer limits and " << dates << " calendar cases.\n";
}
'''


EXTENSION_CASES = r'''
#undef main
#include <array>
#include <cassert>
#include <cmath>
#include <climits>
template<class Exception, class Call> void rejected(Call call) {
    bool caught = false;
    try { call(); } catch (const Exception&) { caught = true; }
    assert(caught);
}
int main() {
    assert(columnAverages(nullptr, 3, 0) == nullptr);
    assert(columnAverages(nullptr, 0, 0) == nullptr);
    rejected<std::invalid_argument>([] { (void)columnAverages(nullptr, 0, 3); });
    rejected<std::out_of_range>([] { (void)checkedCell(nullptr, 0, 3, 0, 0); });
    rejected<std::invalid_argument>([] { (void)checkedCell(nullptr, 1, 1, 0, 0); });
    rejected<std::invalid_argument>([] { (void)columnAverages(nullptr, 1, 1); });
    int storage[9]{};
    for (const auto shape : {std::array<int, 2>{-1, 3}, {3, -1}, {-1, 0}, {0, -1}}) {
        rejected<std::invalid_argument>([&] { (void)columnAverages(storage, shape[0], shape[1]); });
        rejected<std::invalid_argument>([&] { (void)checkedCell(storage, shape[0], shape[1], 0, 0); });
    }
    std::size_t cases = 0, coordinates = 0;
    for (int rows = 1; rows <= 3; ++rows) for (int cols = 1; cols <= 3; ++cols) {
        const int count = rows * cols;
        if (count > 6) continue;
        int combinations = 1;
        for (int i = 0; i < count; ++i) combinations *= 3;
        for (int code = 0; code < combinations; ++code) {
            std::array<int, 9> grid{};
            grid.fill(77);
            int digits = code;
            for (int i = 0; i < count; ++i) { grid[static_cast<std::size_t>(i)] = digits % 3 - 1; digits /= 3; }
            const auto before = grid;
            int cursor = 0;
            for (int row = 0; row < rows; ++row) for (int col = 0; col < cols; ++col) {
                assert(checkedCell(grid.data(), rows, cols, row, col) == before[static_cast<std::size_t>(cursor++)]);
                ++coordinates;
            }
            for (const auto coordinate : {std::array<int, 2>{-1, 0}, {0, -1}, {rows, 0}, {0, cols}, {INT_MAX, INT_MAX}}) {
                rejected<std::out_of_range>([&] { (void)checkedCell(grid.data(), rows, cols, coordinate[0], coordinate[1]); });
            }
            double* averages = columnAverages(grid.data(), rows, cols);
            for (int col = 0; col < cols; ++col) {
                int expected = 0;
                for (int index = col; index < count; index += cols) expected += before[static_cast<std::size_t>(index)];
                assert(std::abs(averages[col] - static_cast<double>(expected) / rows) < 1e-12);
            }
            delete[] averages;
            assert(grid == before);
            ++cases;
        }
    }
    assert(cases == 1614);
    int fractional[] = {1, 2};
    double* result = columnAverages(fractional, 2, 1);
    assert(result[0] == 1.5);
    delete[] result;
    int limits[] = {INT_MAX, INT_MIN};
    result = columnAverages(limits, 2, 1);
    assert(result[0] == -0.5);
    delete[] result;
    std::cout << "Verified " << cases << " extension rectangles, " << coordinates << " valid coordinates, rejected boundaries and preserved inputs.\n";
}
'''

EXTENSION_ALLOCATION_CASES = r'''
#undef main
#include <cassert>
#include <cstdlib>
#include <new>
int failAfter = -1;
int liveArrays = 0;
void* operator new[](const std::size_t bytes) {
    if (failAfter == 0) throw std::bad_alloc();
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++liveArrays;
    return memory;
}
void operator delete[](void* memory) noexcept {
    if (memory != nullptr) { --liveArrays; std::free(memory); }
}
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete[](memory); }
int main() {
    const int baseline = liveArrays;
    const int grid[] = {2, -1, 8, 4, 5, 10};
    failAfter = 0;
    bool caught = false;
    try { (void)columnAverages(grid, 2, 3); } catch (const std::bad_alloc&) { caught = true; }
    assert(caught && liveArrays == baseline);
    assert(columnAverages(nullptr, 3, 0) == nullptr && liveArrays == baseline);
    failAfter = -1;
    double* result = columnAverages(grid, 2, 3);
    assert(liveArrays == baseline + 1);
    delete[] result;
    assert(liveArrays == baseline);
    assert(providedMain() == 0 && liveArrays == baseline);
    std::cout << "Verified column-result allocation failure and extension driver cleanup.\n";
}
'''

class TwoDimensionalArrays(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='cppm3-native-')
        cls.work = Path(cls.temporary.name)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def compile(self, source, label):
        folder = self.work / label
        folder.mkdir(exist_ok=True)
        (folder / 'main.cpp').write_text(source)
        binary = folder / 'program'
        run(['clang++', *FLAGS, *SANITIZERS, 'main.cpp', '-o', str(binary)], folder)
        return binary, folder

    def test_roles_and_seven_make_workflows(self):
        for reference, count in [(FOLDERS[1], 4), (FOLDERS[3], 3), (FOLDERS[5], 2)]:
            starter = reference + '-Starter'
            self.assertEqual((ROOT / reference / 'README.md').read_bytes(), (ROOT / starter / 'README.md').read_bytes())
            self.assertTrue((ROOT / reference / 'REFLECTION.md').is_file())
            self.assertFalse((ROOT / starter / 'REFLECTION.md').exists())
            self.assertEqual((ROOT / starter / 'main.cpp').read_text().count('throw UnfinishedTask'), count)
        for folder in FOLDERS:
            target = self.work / folder
            target.mkdir()
            for name in ['main.cpp', 'Makefile']:
                shutil.copyfile(ROOT / folder / name, target / name)
            self.assertEqual([path.name for path in target.glob('*.cpp')], ['main.cpp'])
            self.assertIn('## Native workflow', (ROOT / folder / 'README.md').read_text())
            run(['make', 'main', 'main-debug'], target)
            normal = input_run(target / 'main', target)
            debug = input_run(target / 'main-debug', target)
            self.assertEqual(normal, debug)
            if folder.endswith('Starter'):
                self.assertEqual(normal.count('Learner task:'), 4 if 'Practice' in folder else (2 if 'Extension' in folder else 3))
                self.assertNotIn('Enter a fictional name:', normal)
            elif 'Practice' in folder:
                self.assertIn('Sum: 36\nMin: 0\n', normal)
                self.assertIn('Row averages: 2 5 5 ', normal)
            elif 'Bank' in folder:
                self.assertEqual(normal.count('Input ended;'), 1)
                self.assertNotIn('TRANSACTION NO:', normal)
            elif 'Extension' in folder:
                self.assertEqual(normal, 'Cell (1, 2): 10\nColumn averages: 3 2 9 \n')
            else:
                self.assertIn('Number of rows: 10\nNumber of cols: 10\nNumber of elements: 100\nExample value from arr2: 5\n42\n', normal)
                self.assertTrue(normal.endswith('A real flat rectangular grid:\n1 2 3 \n4 5 6 \n'))
            run(['make', 'clean'], target)
            self.assertFalse((target / 'main').exists())
            self.assertFalse((target / 'main-debug').exists())
            self.assertFalse(list(target.glob('*.dSYM')))

    def test_reference_and_completed_practice_contracts(self):
        tasks = ['sumArray', 'minArray', 'multTable', 'averageArray']
        for role, source in [('reference', (ROOT / FOLDERS[1] / 'main.cpp').read_text()), ('completed-learner', completed_learner(FOLDERS[1], tasks))]:
            for name, cases in [('grid', GRID_CASES), ('allocations', ALLOCATION_CASES)]:
                binary, cwd = self.compile('#define main providedMain\n' + source + cases, role + '-' + name)
                output = input_run(binary, cwd)
                self.assertIn('Verified', output)
                print(json.dumps({'event': 'verified-cppm3-practice', 'role': role, 'kind': name, 'result': output.splitlines()[-1]}), flush=True)

    def test_reference_and_completed_bank_contracts(self):
        tasks = ['initializeLedger', 'recordTransaction', 'print']
        for role, source in [('reference', (ROOT / FOLDERS[3] / 'main.cpp').read_text()), ('completed-learner', completed_learner(FOLDERS[3], tasks))]:
            binary, cwd = self.compile('#define main providedMain\n' + source + BANK_CASES, role + '-ledger')
            output = input_run(binary, cwd)
            self.assertIn('3861 calendar cases', output)
            print(json.dumps({'event': 'verified-cppm3-bank', 'role': role, 'result': output.strip()}), flush=True)

    def test_bank_input_retries_eof_and_stream_failure(self):
        tasks = ['initializeLedger', 'recordTransaction', 'print']
        fixture = ['Pat Example', '100', '01012025', '01022025', '20', '01032025', '-30', '01042025', '0']
        for role, source in [('reference', (ROOT / FOLDERS[3] / 'main.cpp').read_text()), ('completed-learner', completed_learner(FOLDERS[3], tasks))]:
            binary, cwd = self.compile(source, role + '-input')
            full = input_run(binary, cwd, '\n'.join(fixture) + '\n')
            self.assertIn('Hi Pat Example,', full)
            self.assertEqual(full.count('TRANSACTION NO:'), 4)
            self.assertEqual(full.count('ENDING BALANCE: 90'), 2)
            self.assertNotIn('Input ended;', full)
            for prefix in range(len(fixture)):
                output = input_run(binary, cwd, '\n'.join(fixture[:prefix]) + ('\n' if prefix else ''))
                self.assertEqual(output.count('Input ended;'), 1)
                self.assertEqual(output.count('TRANSACTION NO:'), 0 if prefix < 3 else 1 + (prefix - 3) // 2)
            bad = ['', 'Pat Example', '2.5', '7 8', '2147483648', '100', '02292025', '04312025', '01012025', *fixture[3:]]
            output = input_run(binary, cwd, '\n'.join(bad) + '\n')
            self.assertEqual(output.count('Enter one whole number'), 3)
            self.assertEqual(output.count('Enter a valid eight-digit date'), 2)
            self.assertEqual(output.count('TRANSACTION NO:'), 4)
            for start, rejected, accepted in [(str(2147483647), '1', '-1'), (str(-2147483648), '-1', '1')]:
                text = ['Pat Example', start, '01012025', '01022025', rejected, accepted, '01032025', '0', '01042025', '0']
                output = input_run(binary, cwd, '\n'.join(text) + '\n')
                self.assertEqual(output.count('would exceed the int balance range'), 1)
                self.assertEqual(output.count('TRANSACTION NO:'), 4)
                self.assertIn(' AMOUNT: ' + accepted + '\n', output)
            failure = '#define main providedMain\n' + source + '\n#undef main\nint main() { std::cin.setstate(std::ios::badbit); return providedMain(); }\n'
            failed, failed_cwd = self.compile(failure, role + '-read-error')
            input_run(failed, failed_cwd, expected=1)

    def test_extension_coordinate_and_column_contracts(self):
        tasks = ['checkedCell', 'columnAverages']
        for role, source in [('reference', (ROOT / FOLDERS[5] / 'main.cpp').read_text()), ('completed-learner', completed_learner(FOLDERS[5], tasks))]:
            binary, cwd = self.compile('#define main providedMain\n' + source + EXTENSION_CASES, role + '-extension-cases')
            output = input_run(binary, cwd)
            self.assertIn('1614 extension rectangles', output)
            print(json.dumps({'event': 'verified-cppm3-extension', 'role': role, 'kind': 'coordinates', 'result': output.strip()}), flush=True)

    def test_extension_allocation_failure_and_cleanup(self):
        tasks = ['checkedCell', 'columnAverages']
        for role, source in [('reference', (ROOT / FOLDERS[5] / 'main.cpp').read_text()), ('completed-learner', completed_learner(FOLDERS[5], tasks))]:
            binary, cwd = self.compile('#define main providedMain\n' + source + EXTENSION_ALLOCATION_CASES, role + '-extension-allocation')
            output = input_run(binary, cwd)
            self.assertIn('Verified column-result allocation failure', output)
            print(json.dumps({'event': 'verified-cppm3-extension', 'role': role, 'kind': 'allocations', 'result': output.splitlines()[-1]}), flush=True)

    def test_seven_independent_cmake_targets(self):
        build = self.work / 'cmake'
        run(['cmake', '-S', str(ROOT), '-B', str(build), '-DCMAKE_CXX_COMPILER=clang++'], self.work)
        targets = ['CPPM3_Two_Dimensional_Arrays', 'CPPM3_Array_Practice_Starter', 'CPPM3_Array_Practice_Reference', 'CPPM3_Bank_Starter', 'CPPM3_Bank_Reference', 'CPPM3_Extension_Starter', 'CPPM3_Extension_Reference']
        run(['cmake', '--build', str(build), '--target', *targets, '--parallel', '1'], self.work, timeout=120)
        for target in targets:
            input_run(build / target, self.work)


if __name__ == '__main__':
    unittest.main(verbosity=2)
