"""Native ownership, bounds and failure acceptance for the CPPM4 integer array."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pointer_runtime", ROOT / "verify-pointer-projects.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
REFERENCE = "CPPM4-Dynamic-Array-Implementation"
STARTER = REFERENCE + "-Starter"
FILES = ["DynamicArray.h", "DynamicArray.cpp", "main.cpp", "Makefile", "README.md"]

CASES = r'''
#include "DynamicArray.cpp"
#include <cassert>
#include <climits>
#include <cstdlib>
#include <limits>
#include <new>
#include <sstream>
#include <type_traits>
#include <utility>
#include <vector>

static int liveArrays = 0;
static bool failNextArray = false;
void* operator new[](const std::size_t bytes) {
    if (failNextArray) { failNextArray = false; throw std::bad_alloc(); }
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++liveArrays;
    return memory;
}
void operator delete[](void* memory) noexcept {
    if (memory != nullptr) { --liveArrays; std::free(memory); }
}
void operator delete[](void* memory, std::size_t) noexcept {
    ::operator delete[](memory);
}

template<class Exception, class Task>
void rejected(Task task) {
    bool caught = false;
    try { task(); } catch (const Exception&) { caught = true; }
    assert(caught);
}

void expect(const DynamicArray& array, const std::vector<int>& values) {
    std::ostringstream output;
    auto* prior = std::cout.rdbuf(output.rdbuf());
    for (std::size_t i = 0; i < values.size(); ++i) {
        assert(array.get(i) == values[i]);
    }
    rejected<std::out_of_range>([&] { (void)array.get(values.size()); });
    rejected<std::out_of_range>([&] {
        (void)array.get(std::numeric_limits<std::size_t>::max());
    });
    assert(output.str().empty()); // Bounds failures are silent observers.
    array.printVals();
    std::cout.rdbuf(prior);
    std::ostringstream expected;
    for (const int value : values) expected << value << ' ';
    expected << '\n';
    assert(output.str() == expected.str());
}

int main() {
    static_assert(std::is_nothrow_move_constructible_v<DynamicArray>);
    static_assert(std::is_nothrow_move_assignable_v<DynamicArray>);
    assert(liveArrays == 0);
    rejected<std::bad_alloc>([] { failNextArray = true; DynamicArray failed; });
    assert(!failNextArray && liveArrays == 0);
    {
        DynamicArray array;
        expect(array, {});
        std::vector<int> values;
        for (int i = 0; i < 1301; ++i) {
            const int value = i % 2 == 0 ? i * 17 : -i * 13;
            values.push_back(value); array.addVal(value);
        }
        expect(array, values);
        DynamicArray extremes;
        for (const int value : {INT_MIN, -1, 0, INT_MAX}) extremes.addVal(value);
        expect(extremes, {INT_MIN, -1, 0, INT_MAX});
    }
    assert(liveArrays == 0);
    {
        DynamicArray original;
        original.addVal(7); original.addVal(-1); original.addVal(9);
        {
            DynamicArray copied(original);
            original.addVal(11); copied.addVal(33);
            expect(original, {7, -1, 9, 11}); expect(copied, {7, -1, 9, 33});
            for (int i = 0; i < 40; ++i) copied.addVal(i);
            expect(original, {7, -1, 9, 11});
            DynamicArray assigned;
            assigned.addVal(99); assigned = original;
            assigned.addVal(-55); original.addVal(22);
            expect(assigned, {7, -1, 9, 11, -55});
            expect(original, {7, -1, 9, 11, 22});
            auto* alias = &assigned;
            assigned = *alias; expect(assigned, {7, -1, 9, 11, -55});
            assigned = std::move(*alias); expect(assigned, {7, -1, 9, 11, -55});
        }
        expect(original, {7, -1, 9, 11, 22});
    }
    assert(liveArrays == 0);
    {
        DynamicArray source;
        for (int i = 0; i < 81; ++i) source.addVal(i + 1);
        std::vector<int> values;
        for (int i = 1; i <= 81; ++i) values.push_back(i);
        const int before = liveArrays;
        failNextArray = true;
        DynamicArray moved(std::move(source));
        assert(failNextArray && liveArrays == before); // The move did not allocate.
        failNextArray = false;
        expect(moved, values); expect(source, {});
        DynamicArray emptyCopy(source);
        DynamicArray emptyAssigned;
        emptyAssigned.addVal(999); emptyAssigned = source;
        expect(emptyCopy, {}); expect(emptyAssigned, {});
        source.addVal(-1); emptyCopy.addVal(-2); emptyAssigned.addVal(-3);
        expect(source, {-1}); expect(emptyCopy, {-2}); expect(emptyAssigned, {-3});
        DynamicArray destination;
        destination.addVal(42);
        const int beforeAssign = liveArrays;
        failNextArray = true;
        destination = std::move(moved);
        assert(failNextArray && liveArrays == beforeAssign - 1);
        failNextArray = false;
        expect(destination, values); expect(moved, {});
        for (int i = 0; i < 12; ++i) moved.addVal(-i);
        std::vector<int> reused;
        for (int i = 0; i < 12; ++i) reused.push_back(-i);
        expect(moved, reused); expect(destination, values);
    }
    assert(liveArrays == 0);
    {
        DynamicArray full;
        for (int i = 1; i <= 5; ++i) full.addVal(i);
        const int before = liveArrays;
        failNextArray = true;
        rejected<std::bad_alloc>([&] { full.addVal(6); });
        assert(!failNextArray && liveArrays == before);
        expect(full, {1, 2, 3, 4, 5});
        full.addVal(6); expect(full, {1, 2, 3, 4, 5, 6});
        const int beforeCopy = liveArrays;
        failNextArray = true;
        rejected<std::bad_alloc>([&] { DynamicArray failed(full); });
        assert(!failNextArray && liveArrays == beforeCopy);
        expect(full, {1, 2, 3, 4, 5, 6});
        DynamicArray destination;
        destination.addVal(-8);
        const int beforeAssign = liveArrays;
        failNextArray = true;
        rejected<std::bad_alloc>([&] { destination = full; });
        assert(!failNextArray && liveArrays == beforeAssign);
        expect(destination, {-8}); expect(full, {1, 2, 3, 4, 5, 6});
        destination = full;
        expect(destination, {1, 2, 3, 4, 5, 6});
    }
    assert(liveArrays == 0);
    // Arithmetic boundaries require no enormous allocation or forged object state.
    const std::size_t bound = std::numeric_limits<std::size_t>::max() / sizeof(int);
    assert(cppm4_array_detail::nextCapacity(0) == DEFAULT_SIZE);
    for (const std::size_t current : {std::size_t{1}, std::size_t{5}, bound / 2,
                                    bound / 2 + 1, bound - 1}) {
        const auto grown = cppm4_array_detail::nextCapacity(current);
        assert(grown > current && grown <= bound);
        if (current > bound / 2) assert(grown == bound);
    }
    rejected<std::length_error>([&] { (void)cppm4_array_detail::nextCapacity(bound); });
    rejected<std::length_error>([&] { (void)cppm4_array_detail::nextCapacity(bound + 1); });
    std::cout << "Verified independent copies, allocation-free moves, reuse, bounds, growth and failure cleanup.\n";
}
'''


class DynamicArrayAcceptance(unittest.TestCase):
    def test_pack_builds_and_original_driver(self):
        self.assertEqual((ROOT / REFERENCE / "README.md").read_text(),
                         (ROOT / STARTER / "README.md").read_text())
        for folder in [REFERENCE, STARTER]:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory(prefix="cppm4-array-pack-") as temporary:
                work = Path(temporary)
                for name in FILES:
                    shutil.copyfile(ROOT / folder / name, work / name)
                runtime.run(["make", "main", "main-debug"], work)
                for name in ["main", "main-debug"]:
                    result = runtime.run([str(work / name)], work)
                    self.assertEqual(result.stderr, "")
                    if folder == REFERENCE:
                        lines = result.stdout.splitlines()
                        self.assertEqual([line for line in lines if line.startswith("Adding ")],
                                         [f"Adding {i}" for i in range(1, 82)])
                        self.assertEqual([int(token) for token in lines[-1].split()], list(range(1, 82)))
                    else:
                        self.assertIn("Unfinished learner task: addVal", result.stdout)
                        self.assertNotIn("Adding 1\n", result.stdout)
                runtime.run(["make", "clean"], work)
                for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                    self.assertFalse((work / name).exists())

    def test_native_contracts_and_cmake_targets(self):
        with tempfile.TemporaryDirectory(prefix="cppm4-array-contract-") as temporary:
            work = Path(temporary)
            for name in ["DynamicArray.h", "DynamicArray.cpp"]:
                shutil.copyfile(ROOT / REFERENCE / name, work / name)
            (work / "cases.cpp").write_text(CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                binary = work / label
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", str(binary)], work)
                result = runtime.run([str(binary)], work)
                self.assertEqual(result.stderr, "")
                self.assertIn("Verified independent copies", result.stdout)
            cmake = work / "cmake"
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(cmake)], work)
            runtime.run(["cmake", "--build", str(cmake), "--target",
                         "CPPM4_Dynamic_Array_Starter", "CPPM4_Dynamic_Array_Reference"], work)
            for name in ["CPPM4_Dynamic_Array_Starter", "CPPM4_Dynamic_Array_Reference"]:
                self.assertEqual(runtime.run([str(cmake / name)], work).stderr, "")


if __name__ == "__main__":
    unittest.main()
