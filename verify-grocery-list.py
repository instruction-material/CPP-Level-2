"""Independent record, ownership, failure and menu acceptance for Grocery List."""
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
REFERENCE = "CPPM4-Grocery-List"
STARTER = REFERENCE + "-Starter"
FILES = ["DynamicArray.h", "DynamicArray.cpp", "GroceryList.h", "GroceryList.cpp", "main.cpp", "Makefile", "README.md"]

CASES = r'''
#include "DynamicArray.cpp"
#include "GroceryList.cpp"
#define main providedMain
#include "main.cpp"
#undef main
#include <cassert>
#include <cstdlib>
#include <limits>
#include <new>
#include <type_traits>
#include <utility>
#include <vector>

static int live = 0;
static int liveArrays = 0;
static int failAfter = -1;
void* allocate(std::size_t bytes, bool array) {
    if (failAfter == 0) { failAfter = -1; throw std::bad_alloc(); }
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++live;
    if (array) ++liveArrays;
    return memory;
}
void* operator new(std::size_t bytes) { return allocate(bytes, false); }
void* operator new[](std::size_t bytes) { return allocate(bytes, true); }
void operator delete(void* memory) noexcept { if (memory) { --live; std::free(memory); } }
void operator delete[](void* memory) noexcept { if (memory) { --liveArrays; ::operator delete(memory); } }
void operator delete(void* memory, std::size_t) noexcept { ::operator delete(memory); }
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete[](memory); }

struct Capture {
    std::ostringstream text;
    std::ostream& stream;
    std::streambuf* prior;
    explicit Capture(std::ostream& output = std::cout) : stream(output), prior(stream.rdbuf(text.rdbuf())) {}
    ~Capture() { stream.rdbuf(prior); }
};
class Sink : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize size) override { return size; }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};
struct QuietOutput {
    Sink sink;
    std::streambuf* prior;
    QuietOutput() : prior(std::cout.rdbuf(&sink)) {}
    ~QuietOutput() { std::cout.rdbuf(prior); }
};
template<class Exception, class Task>
void rejected(Task task) {
    bool caught = false;
    try { task(); } catch (const Exception&) { caught = true; }
    assert(caught);
}
std::string rows(const std::vector<Grocery>& values) {
    std::ostringstream output;
    for (std::size_t i = 0; i < values.size(); ++i) {
        output << "Item Number: " << i + 1 << '\n'
               << " Name: " << values[i].name << '\n'
               << " Price: " << values[i].price << '\n';
    }
    return output.str();
}
void expect(const DynamicArray& array, const std::vector<Grocery>& values) {
    assert(array.getSize() == values.size());
    Capture output;
    for (std::size_t i = 0; i < values.size(); ++i) {
        auto copy = array.accessVal(i);
        assert(copy.name == values[i].name && copy.price == values[i].price);
        copy.name = "edited returned copy";
        assert(array.accessVal(i).name == values[i].name);
    }
    rejected<std::out_of_range>([&] { (void)array.accessVal(values.size()); });
    rejected<std::out_of_range>([&] { (void)array.accessVal(std::numeric_limits<std::size_t>::max()); });
    assert(output.text.str().empty());
    array.printVals();
    assert(output.text.str() == rows(values));
}
void expect(const GroceryList& list, const std::vector<Grocery>& values) {
    Capture output;
    list.printList();
    assert(output.text.str() == "Here are your groceries! You have " +
           std::to_string(values.size()) + " grocery items.\n" + rows(values));
}
void fill(DynamicArray& array, const std::vector<Grocery>& values) {
    for (const auto& value : values) array.addVal(value);
}
void fill(GroceryList& list, const std::vector<Grocery>& values) {
    for (const auto& value : values) list.addItem(value);
}
class ThrowingInput : public std::streambuf {
    std::string prefix;
    int_type underflow() override { throw std::runtime_error("Read failed"); }
public:
    explicit ThrowingInput(std::string text) : prefix(std::move(text)) {
        setg(prefix.data(), prefix.data(), prefix.data() + prefix.size());
    }
};
class FailingAcknowledgement : public std::streambuf {
    std::streamsize xsputn(const char* data, std::streamsize size) override {
        if (std::string_view(data, static_cast<std::size_t>(size)).find("successfully") != std::string_view::npos) {
            throw std::runtime_error("Acknowledgement failed");
        }
        return size;
    }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};

int main() {
    static_assert(std::is_nothrow_move_constructible_v<DynamicArray>);
    static_assert(std::is_nothrow_move_assignable_v<DynamicArray>);
    static_assert(std::is_nothrow_move_constructible_v<GroceryList>);
    static_assert(std::is_nothrow_move_assignable_v<GroceryList>);
    double price = 17;
    for (const std::string token : {"", " ", "-1", "nan", "inf", "1e9999", "1x", "1 2", "++1"}) {
        assert(!parsePrice(token, price) && price == 17);
    }
    assert(parsePrice(" +0.5 \r", price) && price == 0.5);
    assert(parsePrice("-0", price) && price == 0);
    assert(parsePrice("1e3", price) && price == 1000);
    std::size_t number = 7;
    for (const std::string token : {"", "0", "-1", "1.5", "1x", "1 2", "++1", "99999999999999999999999999999"}) {
        assert(!parseItemNumber(token, number) && number == 7);
    }
    assert(parseItemNumber(" +1 ", number) && number == 1);
    assert(parseItemNumber(std::to_string(std::numeric_limits<std::size_t>::max()), number));
    std::vector<Grocery> values;
    for (int i = 0; i < 5; ++i) values.emplace_back(std::string(90, 'a' + i), i * 0.5);
    const Grocery extra(std::string(90, 'x'), 9);
    const std::vector<Grocery> old{Grocery(std::string(90, 'z'), 42)};
    // Warm output formatting before measuring scoped allocation cleanup.
    { GroceryList warm; fill(warm, old); expect(warm, old); }
    const int baseline = live;
    const int baselineArrays = liveArrays;
    {
        DynamicArray array; expect(array, {});
        std::vector<Grocery> many;
        for (int i = 0; i < 201; ++i) {
            many.emplace_back("item " + std::to_string(i), i * 0.25);
            array.addVal(many.back());
        }
        expect(array, many);
        for (const Grocery& invalid : {Grocery(), Grocery(" \t", 1), Grocery("bad", -1),
             Grocery("bad", std::numeric_limits<double>::infinity()),
             Grocery("bad", std::numeric_limits<double>::quiet_NaN())}) {
            rejected<std::invalid_argument>([&] { array.addVal(invalid); });
            expect(array, many);
        }
        DynamicArray copied(array);
        copied.addVal(extra); expect(array, many);
        auto changed = many; changed.push_back(extra); expect(copied, changed);
        DynamicArray assigned; fill(assigned, old); assigned = array; expect(assigned, many);
        auto* alias = &assigned;
        assigned = *alias; assigned = std::move(*alias); expect(assigned, many);
        failAfter = 0;
        DynamicArray moved(std::move(array));
        assert(failAfter == 0); failAfter = -1;
        expect(moved, many); expect(array, {});
        DynamicArray emptyCopy(array); emptyCopy.addVal(extra); expect(emptyCopy, {extra});
        assigned = array; expect(assigned, {}); assigned.addVal(old[0]); expect(assigned, old);
        array.addVal(extra); expect(array, {extra});
        DynamicArray destination; fill(destination, old);
        failAfter = 0; destination = std::move(moved);
        assert(failAfter == 0); failAfter = -1;
        expect(destination, many); expect(moved, {});
        fill(moved, values); moved.addVal(extra);
        auto reused = values; reused.push_back(extra); expect(moved, reused);
    }
    assert(live == baseline && liveArrays == baselineArrays);
    int copyFailures = 0, appendFailures = 0, removeFailures = 0;
    for (int operation = 0; operation < 4; ++operation) {
        for (int point = 0; point < 12; ++point) {
            {
                DynamicArray source; fill(source, values);
                DynamicArray destination; fill(destination, old);
                if (operation == 3) { source = DynamicArray(); source.addVal(values[0]); }
                const auto beforeValues = operation == 3 ? std::vector<Grocery>{values[0]} : values;
                const int before = live, beforeArrays = liveArrays;
                failAfter = point;
                bool failed = false;
                try {
                    if (operation == 0) { DynamicArray copy(source); }
                    else if (operation == 1) destination = source;
                    else source.addVal(extra);
                } catch (const std::bad_alloc&) { failed = true; }
                failAfter = -1;
                if (failed) {
                    assert(live == before && liveArrays == beforeArrays);
                    expect(source, beforeValues); expect(destination, old);
                    if (operation < 2) ++copyFailures; else ++appendFailures;
                } else if (operation >= 2) {
                    auto after = beforeValues; after.push_back(extra); expect(source, after);
                }
            }
            assert(live == baseline && liveArrays == baselineArrays);
        }
    }
    assert(copyFailures >= 12 && appendFailures >= 8);
    const std::vector<Grocery> shortValues{Grocery("a", 1), Grocery("b", 2), Grocery("c", 3)};
    for (const std::size_t removed : {std::size_t{1}, std::size_t{2}, std::size_t{3}}) {
        GroceryList list; fill(list, shortValues);
        { Capture output; list.removeItem(removed); }
        auto after = shortValues; after.erase(after.begin() + static_cast<std::ptrdiff_t>(removed - 1));
        expect(list, after);
    }
    {
        GroceryList list; fill(list, old);
        { Capture output; list.removeItem(0); list.removeItem(2); } expect(list, old);
        { Capture output; list.removeItem(1); } expect(list, {});
        list.addItem(extra); expect(list, {extra});
        GroceryList copied(list); copied.addItem(old[0]); expect(list, {extra});
        GroceryList moved(std::move(list)); expect(moved, {extra}); expect(list, {});
        list.addItem(old[0]); expect(list, old);
        GroceryList assigned; assigned = copied; expect(assigned, {extra, old[0]});
        auto* alias = &assigned; assigned = *alias; assigned = std::move(*alias);
        expect(assigned, {extra, old[0]});
        GroceryList target; fill(target, old);
        target = std::move(copied); expect(target, {extra, old[0]}); expect(copied, {});
        copied.addItem(extra); expect(copied, {extra});
    }
    std::vector<Grocery> longList;
    for (int i = 0; i < 21; ++i) longList.emplace_back(std::string(90, 'a') + std::to_string(i), i);
    const int listBaseline = live, listArrays = liveArrays;
    for (int point = 0; point < 90; ++point) {
        {
            GroceryList list; fill(list, longList);
            const int before = live, beforeArrays = liveArrays;
            bool failed = false;
            { QuietOutput output;
                failAfter = point;
                try { list.removeItem(3); } catch (const std::bad_alloc&) { failed = true; }
                failAfter = -1;
            }
            if (failed) { ++removeFailures; expect(list, longList); }
            else { auto after = longList; after.erase(after.begin() + 2); expect(list, after); }
            if (failed) assert(live == before && liveArrays == beforeArrays);
        }
        assert(live == listBaseline && liveArrays == listArrays);
    }
    assert(removeFailures >= 30);
    {
        GroceryList list; fill(list, shortValues);
        FailingAcknowledgement failed;
        auto* prior = std::cout.rdbuf(&failed);
        std::cout.exceptions(std::ios::badbit | std::ios::failbit);
        rejected<std::exception>([&] { list.removeItem(2); });
        std::cout.exceptions(std::ios::goodbit); std::cout.clear(); std::cout.rdbuf(prior);
        expect(list, {shortValues[0], shortValues[2]});
    }
    for (const std::string text : {"", "add\n", "add\nnew name\n", "remove\n",
                                   "add\n!quit\n", "add\nnew\n!quit\n", "remove\n!quit\n"}) {
        GroceryList list; fill(list, shortValues);
        std::istringstream input(text);
        { Capture output; assert(runGroceryMenu(list, input) == 0); }
        expect(list, shortValues);
    }
    for (const std::string prefix : {"", "add\n", "add\nnew name\n", "remove\n"}) {
        GroceryList list; fill(list, shortValues);
        ThrowingInput buffer(prefix); std::istream input(&buffer);
        Capture errors(std::cerr);
        { Capture output; assert(runGroceryMenu(list, input) == 1); }
        assert(errors.text.str() == "Input could not be read.\n"); expect(list, shortValues);
    }
    const auto bound = std::numeric_limits<std::size_t>::max() / sizeof(Grocery);
    assert(grocery_detail::nextCapacity(0) == DEFAULT_SIZE);
    for (const auto value : {std::size_t{5}, bound / 2, bound / 2 + 1, bound - 1}) {
        const auto grown = grocery_detail::nextCapacity(value); assert(grown > value && grown <= bound);
    }
    rejected<std::length_error>([&] { (void)grocery_detail::nextCapacity(bound); });
    rejected<std::length_error>([&] { (void)grocery_detail::nextCapacity(bound + 1); });
    std::cout << "Verified Grocery copies, moves, growth, removal, input boundaries and injected cleanup.\n";
}
'''


class GroceryAcceptance(unittest.TestCase):
    def test_pack_builds_menu_and_cleanup(self):
        self.assertEqual((ROOT / REFERENCE / "README.md").read_text(), (ROOT / STARTER / "README.md").read_text())
        seed = [("milk", 2.0), ("cheese", 5.0)]
        cases = [
            ("", seed), ("!quit\n", seed), ("print\n!quit\n", seed),
            ("add\nwhole milk\n2.5\nprint\n!quit\n", seed + [("whole milk", 2.5)]),
            ("add\n\n whole milk \n-1\nnan\ninf\n1x\n1 2\n1e9999\n0\nprint\n!quit\n", seed + [("whole milk", 0.0)]),
            ("remove\n1\nprint\n!quit\n", [("cheese", 5.0)]),
            ("remove\n2\nprint\n!quit\n", [("milk", 2.0)]),
            ("remove\n0\n-1\n1.5\n1x\n99999999999999999999999999\n999\nprint\n!quit\n", seed),
            ("add words\nunknown\nprint\n!quit\n", seed),
            ("add\n", seed), ("add\nnew name\n", seed), ("remove\n", seed),
            ("add\n!quit\n", seed), ("add\nnew\n!quit\n", seed), ("remove\n!quit\n", seed),
            ("remove\n+1\nprint", [("cheese", 5.0)]),
        ]
        for folder in [REFERENCE, STARTER]:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory(prefix="cppm4-grocery-pack-") as temporary:
                work = Path(temporary)
                for name in FILES: shutil.copyfile(ROOT / folder / name, work / name)
                runtime.run(["make", "main", "main-debug"], work)
                for header in ["DynamicArray.h", "GroceryList.h"]:
                    rebuild = runtime.run(["make", "-n", "-W", header, "main"], work)
                    self.assertIn("DynamicArray.cpp GroceryList.cpp main.cpp", rebuild.stdout)
                for name in ["main", "main-debug"]:
                    for text, expected in cases:
                        result = io_runtime.input_run(work / name, work, text)
                        self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                        if folder == REFERENCE:
                            marker = result.stdout.rfind("Here are your groceries!")
                            self.assertGreaterEqual(marker, 0)
                            lines = result.stdout[marker:].splitlines()
                            names = [line.removeprefix(" Name: ") for line in lines if line.startswith(" Name: ")]
                            prices = [float(line.removeprefix(" Price: ")) for line in lines if line.startswith(" Price: ")]
                            self.assertEqual(list(zip(names, prices)), expected)
                            self.assertIn("You have successfully removed the item number 3", result.stdout)
                        else:
                            self.assertIn("Unfinished learner task: Grocery record constructor", result.stdout)
                            self.assertNotIn("Welcome", result.stdout)
                runtime.run(["make", "clean"], work)
                for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                    self.assertFalse((work / name).exists())

    def test_native_contracts_and_cmake_targets(self):
        with tempfile.TemporaryDirectory(prefix="cppm4-grocery-contract-") as temporary:
            work = Path(temporary)
            for name in FILES[:5]: shutil.copyfile(ROOT / REFERENCE / name, work / name)
            (work / "cases.cpp").write_text(CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                binary = work / label
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", str(binary)], work)
                self.assertEqual(runtime.run([str(binary)], work).stderr, "")
            cmake = work / "cmake"
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(cmake)], work)
            runtime.run(["cmake", "--build", str(cmake), "--target", "CPPM4_Grocery_List_Starter", "CPPM4_Grocery_List_Reference"], work)
            for name in ["CPPM4_Grocery_List_Starter", "CPPM4_Grocery_List_Reference"]:
                self.assertEqual(io_runtime.input_run(cmake / name, work, "!quit\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
