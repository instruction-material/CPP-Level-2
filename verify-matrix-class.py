"""Independent Matrix grid, arithmetic, input, lifetime and failure acceptance."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

runtime = module("pointer_runtime", "verify-pointer-projects.py")
io_runtime = module("assembly_io", "verify-assembly-line.py")
REFERENCE = "CPPM5-Matrix-Fun-with-Matrix-Class"
STARTER = REFERENCE + "-Starter"
FILES = ["matrix.h", "matrix.cpp", "main.cpp", "Makefile", "README.md"]

CASES = r'''
#include "matrix.cpp"
#define main providedMain
#include "main.cpp"
#undef main
#include <cassert>
#include <cstdlib>
#include <new>
#include <type_traits>
#include <utility>

static int live = 0, failAfter = -1;
void* operator new(std::size_t bytes) {
    if (failAfter == 0) { failAfter = -1; throw std::bad_alloc(); }
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (!memory) throw std::bad_alloc();
    ++live; return memory;
}
void operator delete(void* memory) noexcept { if (memory) { --live; std::free(memory); } }
void operator delete(void* memory, std::size_t) noexcept { ::operator delete(memory); }
void* operator new[](std::size_t bytes) { return ::operator new(bytes); }
void operator delete[](void* memory) noexcept { ::operator delete(memory); }
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete(memory); }
using Grid = std::vector<std::vector<int>>;
class Sink : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize size) override { return size; }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};
struct Quiet {
    Sink sink;
    std::streambuf* prior;
    Quiet() : prior(std::cout.rdbuf(&sink)) {}
    ~Quiet() { std::cout.rdbuf(prior); }
};
template<class Exception, class Task> void rejected(Task task) {
    bool caught = false;
    try { task(); } catch (const Exception&) { caught = true; }
    assert(caught);
}
void expect(const Matrix& matrix, const Grid& expected) {
    assert(matrix.getNumRows() == static_cast<int>(expected.size()));
    const int cols = expected.empty() ? 0 : static_cast<int>(expected[0].size());
    assert(matrix.getNumCols() == cols);
    for (int r = 0; r < matrix.getNumRows(); ++r) {
        for (int c = 0; c < cols; ++c) {
            assert(matrix.get(r, c) == expected[static_cast<std::size_t>(r)][static_cast<std::size_t>(c)]);
        }
    }
    for (const auto& index : {std::pair{-1, 0}, std::pair{0, -1},
                             std::pair{matrix.getNumRows(), 0}, std::pair{0, cols}}) {
        rejected<std::out_of_range>([&] { (void)matrix.get(index.first, index.second); });
    }
    std::ostringstream expectedRows;
    for (const auto& row : expected) { for (int value : row) expectedRows << value << '\t'; expectedRows << '\n'; }
    expectedRows << '\n';
    std::ostringstream out; auto* prior = std::cout.rdbuf(out.rdbuf());
    matrix.display(); std::cout.rdbuf(prior);
    const auto text = out.str(); const auto newline = text.find('\n');
    assert(text.starts_with("Matrix ") && newline != std::string::npos);
    assert(text.substr(newline + 1) == expectedRows.str());
}
Matrix grid(const Grid& values) {
    Matrix result(static_cast<int>(values.size()), values.empty() ? 0 : static_cast<int>(values.front().size()));
    std::ostringstream lines;
    for (const auto& row : values) for (int value : row) lines << value << '\n';
    std::istringstream input(lines.str()); { Quiet output; result.fillMatrix(input); }
    return result;
}
class ThrowingInput : public std::streambuf {
    std::string prefix;
    int_type underflow() override { throw std::runtime_error("Read failed"); }
public:
    explicit ThrowingInput(std::string text) : prefix(std::move(text)) {
        setg(prefix.data(), prefix.data(), prefix.data() + prefix.size());
    }
};
class FailingOutput : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize) override { throw std::runtime_error("Output failed"); }
    int_type overflow(int_type) override { throw std::runtime_error("Output failed"); }
};

int main() {
    static_assert(std::is_nothrow_move_constructible_v<Matrix>);
    static_assert(std::is_nothrow_move_assignable_v<Matrix>);
    int rows = 3, cols = 4;
    for (const std::string text : {"", "1", "1 2 3", "0 2", "-1 2", "2 0", "21 2", "2 21", "2 2x", "2.0 2", "++2 2", "+-2 2", "999999999999 2"}) {
        assert(!parseDimensions(text, rows, cols) && rows == 3 && cols == 4);
    }
    assert(parseDimensions(" +2  3 \r", rows, cols) && rows == 2 && cols == 3);
    int value = 17;
    for (const std::string text : {"", " ", "nan", "1e3", "1.5", "1x", "1 2", "++1", "+-1", "99999999999999"}) {
        assert(!matrix_detail::parseElement(text, value) && value == 17);
    }
    assert(matrix_detail::parseElement(" -0 ", value) && value == 0);
    assert(matrix_detail::parseElement(std::to_string(std::numeric_limits<int>::min()), value));
    assert(value == std::numeric_limits<int>::min());
    const Grid left{{1, 2}, {3, 4}, {5, 6}}, right{{7, 8, 9}, {10, 11, 12}}, old{{-1}, {-2}};
    const Grid sum{{2, 4}, {6, 8}, {10, 12}}, product{{27, 30, 33}, {61, 68, 75}, {95, 106, 117}};
    { auto warm = grid(old); expect(warm, old); }
    const int baseline = live;
    {
        Matrix empty(0, 0); expect(empty, {});
        for (const auto& shape : {std::pair{-1, 2}, std::pair{2, -1}, std::pair{0, 2}, std::pair{2, 0}, std::pair{21, 1}, std::pair{1, 21}}) {
            rejected<std::invalid_argument>([&] { Matrix invalid(shape.first, shape.second); });
        }
        Matrix zero(20, 20); expect(zero, Grid(20, std::vector<int>(20, 0)));
        Matrix first = grid(left), second = grid(right);
        expect(first.add(first), sum); expect(first.multiply(second), product);
        { Quiet out; expect(first.add(second), {}); expect(second.multiply(second), {}); expect(empty.multiply(empty), {}); }
        expect(first, left); expect(second, right);
        Matrix copied(first); std::istringstream changed("9\n8\n7\n6\n5\n4\n");
        { Quiet out; copied.fillMatrix(changed); }
        expect(copied, {{9, 8}, {7, 6}, {5, 4}}); expect(first, left);
        Matrix assigned = grid(old); assigned = first; expect(assigned, left);
        auto* alias = &assigned; assigned = *alias; assigned = std::move(*alias);
        // Generated vector self-move guarantees validity, not unchanged contents.
        expect(assigned, {}); assigned = first; expect(assigned, left);
        failAfter = 0; Matrix moved(std::move(first)); assert(failAfter == 0); failAfter = -1;
        expect(moved, left); expect(first, {}); first = grid(old); expect(first, old);
        failAfter = 0; assigned = std::move(moved); assert(failAfter == 0); failAfter = -1;
        expect(assigned, left); expect(moved, {}); moved = grid(right); expect(moved, right);
    }
    assert(live == baseline);
    {
        const int maximum = std::numeric_limits<int>::max(), minimum = std::numeric_limits<int>::min();
        Matrix high = grid({{maximum}}), low = grid({{minimum}}), one = grid({{1}}), minus = grid({{-1}}), two = grid({{2}});
        rejected<std::overflow_error>([&] { (void)high.add(one); });
        rejected<std::overflow_error>([&] { (void)low.add(minus); });
        rejected<std::overflow_error>([&] { (void)high.multiply(two); });
        rejected<std::overflow_error>([&] { (void)low.multiply(minus); });
        expect(high.add(minus), {{maximum - 1}}); expect(low.add(one), {{minimum + 1}});
        expect(high.multiply(minus), {{-maximum}}); expect(low.multiply(one), {{minimum}});
        expect(grid({{0}}).multiply(low), {{0}}); expect(minus.multiply(minus), {{1}});
        Matrix accumulation = grid({{maximum, 1}}), ones = grid({{1}, {1}});
        rejected<std::overflow_error>([&] { (void)accumulation.multiply(ones); });
        Matrix negatives = grid({{minimum, -1}});
        rejected<std::overflow_error>([&] { (void)negatives.multiply(ones); });
        expect(high, {{maximum}}); expect(low, {{minimum}}); expect(accumulation, {{maximum, 1}});
    }
    assert(live == baseline);
    // Negative control: default nested-vector assignment can break the shape.
    bool foundRagged = false;
    for (int point = 0; point < 4; ++point) {
        Grid destination(2, std::vector<int>(1, 0)), source(2, std::vector<int>(2, 1));
        failAfter = point;
        try { destination = source; } catch (const std::bad_alloc&) {
            foundRagged = foundRagged || destination[0].size() != destination[1].size();
        }
        failAfter = -1;
    }
    assert(foundRagged && live == baseline);
    int failures[6]{}, successes[6]{};
    for (int operation = 0; operation < 6; ++operation) {
        for (int point = 0; point < 26; ++point) {
            {
                Matrix source = grid(left), target = grid(old), multiplier = grid(right);
                std::istringstream input("9\n8\n7\n6\n5\n4\n");
                const int before = live; bool failed = false;
                { Quiet out; failAfter = point;
                  try {
                    if (operation == 0) { Matrix copy(source); failAfter = -1; expect(copy, left); }
                    else if (operation == 1) target = source;
                    else if (operation == 2) source.fillMatrix(input);
                    else if (operation == 3) { Matrix result = source.add(source); failAfter = -1; expect(result, sum); }
                    else if (operation == 4) { Matrix result = source.multiply(multiplier); failAfter = -1; expect(result, product); }
                    else { Matrix result(20, 20); }
                  } catch (const std::bad_alloc&) { failed = true; }
                  failAfter = -1;
                }
                if (failed) { ++failures[operation]; assert(live == before); }
                else ++successes[operation];
                expect(source, !failed && operation == 2 ? Grid{{9, 8}, {7, 6}, {5, 4}} : left);
                expect(target, !failed && operation == 1 ? left : old); expect(multiplier, right);
            }
            assert(live == baseline);
        }
        assert(failures[operation] >= 4 && successes[operation] > 0);
    }
    for (const bool exceptions : {false, true}) {
        for (const std::string text : {"", "9\n", "9\n8\n7\n", "!quit\n", "9\n!quit\n"}) {
            Matrix matrix = grid(left); std::istringstream input(text);
            if (exceptions) input.exceptions(std::ios::badbit | std::ios::failbit);
            { Quiet out; rejected<MatrixInputStopped>([&] { matrix.fillMatrix(input); }); } expect(matrix, left);
        }
        for (const std::string prefix : {"", "9\n", "9\n8\n7\n"}) {
            Matrix matrix = grid(left); ThrowingInput buffer(prefix); std::istream input(&buffer);
            if (exceptions) input.exceptions(std::ios::badbit | std::ios::failbit);
            { Quiet out; rejected<std::runtime_error>([&] { matrix.fillMatrix(input); }); } expect(matrix, left);
        }
    }
    {
        Matrix matrix = grid(left); std::istringstream input("9\n8\n7\n6\n5\n4\n");
        FailingOutput failed; auto* prior = std::cout.rdbuf(&failed);
        std::cout.exceptions(std::ios::badbit | std::ios::failbit);
        rejected<std::exception>([&] { matrix.fillMatrix(input); });
        std::cout.exceptions(std::ios::goodbit); std::cout.clear(); std::cout.rdbuf(prior); expect(matrix, left);
    }
    const auto priorNumber = matrix_detail::numMatrices;
    matrix_detail::numMatrices = std::numeric_limits<std::size_t>::max();
    rejected<std::length_error>([] { Matrix matrix(1, 1); });
    matrix_detail::numMatrices = priorNumber;
    assert(live == baseline);
    std::cout << "Verified Matrix grids, checked arithmetic, copy/move, input and injected cleanup.\n";
}
'''


class MatrixAcceptance(unittest.TestCase):
    def test_pack_builds_and_full_line_cli(self):
        self.assertEqual((ROOT / REFERENCE / "README.md").read_bytes(), (ROOT / STARTER / "README.md").read_bytes())
        self.assertEqual((ROOT / REFERENCE / "matrix.h").read_bytes(), (ROOT / STARTER / "matrix.h").read_bytes())
        cases = [
            ("", None), ("!quit\n", None), ("add\n", None), ("add\n1 1\n", None),
            ("add\n1 1\n1 1\n", None), ("add\n1 1\n1 1\n4\n", None),
            ("multiply\n2 3\n3 2\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n", [[58, 64], [139, 154]]),
            ("add\n2 2\n2 2\n1\n-2\n0\n4\n5\n2\n-3\n6\n", [[6, 0], [-3, 10]]),
            ("unknown\nadd x\n add \n0 1\n-1 1\n1.5 1\n1 1x\n1 1 2\n21 1\n1 1\n1 1\n\n1x\n+-1\n+2\n3", [[5]]),
            ("add\n1 2\n1 1\n1 1\n1 1\n1\n2\n", [[3]]),
            ("multiply\n1 2\n1 1\n1 1\n1 1\n4\n5\n", [[20]]),
            ("add\n1 1\n1 1\n4\n!quit\n", None),
        ]
        for folder in [REFERENCE, STARTER]:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory(prefix="cppm5-matrix-pack-") as temporary:
                work = Path(temporary)
                for name in FILES: shutil.copyfile(ROOT / folder / name, work / name)
                runtime.run(["make", "main", "main-debug"], work)
                self.assertIn("matrix.cpp main.cpp", runtime.run(["make", "-n", "-W", "matrix.h", "main"], work).stdout)
                for name in ["main", "main-debug"]:
                    for text, expected in cases:
                        result = io_runtime.input_run(work / name, work, text)
                        self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                        if folder == STARTER:
                            self.assertIn("Unfinished learner task: Matrix program", result.stdout)
                        elif expected is None:
                            self.assertNotIn("Matrix ", result.stdout)
                        else:
                            final = result.stdout[result.stdout.rfind("Matrix "):].splitlines()[1:]
                            self.assertEqual([[int(v) for v in line.split()] for line in final if line.strip()], expected)
                    bad = io_runtime.input_run(work / name, work, "", ["--unknown"])
                    self.assertEqual(bad.returncode, 2); self.assertEqual(bad.stderr, "Usage: main\n")
                    if folder == REFERENCE:
                        for text in ["add\n1 1\n1 1\n2147483647\n1\n", "multiply\n1 1\n1 1\n-2147483648\n-1\n"]:
                            bad = io_runtime.input_run(work / name, work, text)
                            self.assertEqual(bad.returncode, 1); self.assertIn("int range", bad.stderr)
                runtime.run(["make", "clean"], work)
                for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                    self.assertFalse((work / name).exists())

    def test_independent_native_contracts(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-matrix-contract-") as temporary:
            work = Path(temporary)
            for name in FILES[:3]: shutil.copyfile(ROOT / REFERENCE / name, work / name)
            (work / "cases.cpp").write_text(CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", label], work)
                self.assertEqual(runtime.run([str(work / label)], work).stderr, "")

    def test_independent_cmake_targets(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-matrix-cmake-") as temporary:
            work = Path(temporary)
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(work / "build")], work)
            runtime.run(["cmake", "--build", str(work / "build"), "--target", "CPPM5_Matrix_Class_Starter", "CPPM5_Matrix_Class_Reference"], work)
            for name in ["CPPM5_Matrix_Class_Starter", "CPPM5_Matrix_Class_Reference"]:
                self.assertEqual(io_runtime.input_run(work / "build" / name, work, "!quit\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
