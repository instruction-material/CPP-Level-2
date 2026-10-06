"""Independent normal, allocation and throwing-output ownership comparison gates."""
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
FOLDER = "CPPM5-Modern-Ownership-Reflection"
EXPECTED = ("Manual array: 84 91 76 88 \n"
            "Manual responsibility: delete[] must run exactly once.\n\n"
            "Vector: 84 91 76 88 \n"
            "Vector responsibility: the vector cleans up its own storage.\n\n"
            "unique_ptr array: 84 91 76 88 \n"
            "unique_ptr responsibility: ownership is still explicit, but cleanup is automatic.\n")

CASES = r'''
#define main providedMain
#include "main.cpp"
#undef main
#include <cassert>
#include <cstdlib>
#include <new>
#include <sstream>
#include <string_view>
#include <type_traits>
#include <utility>

static int live = 0, arrays = 0, failAfter = -1;
void* allocate(std::size_t bytes, bool array) {
    if (failAfter == 0) { failAfter = -1; throw std::bad_alloc(); }
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (!memory) throw std::bad_alloc();
    ++live; if (array) ++arrays; return memory;
}
void* operator new(std::size_t bytes) { return allocate(bytes, false); }
void* operator new[](std::size_t bytes) { return allocate(bytes, true); }
void operator delete(void* memory) noexcept { if (memory) { --live; std::free(memory); } }
void operator delete[](void* memory) noexcept { if (memory) { --arrays; ::operator delete(memory); } }
void operator delete(void* memory, std::size_t) noexcept { ::operator delete(memory); }
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete[](memory); }

class Sink : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize size) override { return size; }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};
class FailingOutput : public std::streambuf {
    bool late;
    std::streamsize xsputn(const char* data, std::streamsize size) override {
        if (!late || std::string_view(data, static_cast<std::size_t>(size)).find("responsibility") != std::string_view::npos) {
            throw std::runtime_error("Output failed");
        }
        return size;
    }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
public:
    explicit FailingOutput(bool afterScores) : late(afterScores) {}
};
struct Quiet {
    Sink sink;
    std::streambuf* prior;
    Quiet() : prior(std::cout.rdbuf(&sink)) {}
    ~Quiet() { std::cout.rdbuf(prior); }
};

int main() {
    static_assert(!std::is_copy_constructible_v<std::unique_ptr<int[]>>);
    static_assert(std::is_nothrow_move_constructible_v<std::unique_ptr<int[]>>);
    const std::string expected[] = {
        "Manual array: 84 91 76 88 \nManual responsibility: delete[] must run exactly once.\n",
        "Vector: 84 91 76 88 \nVector responsibility: the vector cleans up its own storage.\n",
        "unique_ptr array: 84 91 76 88 \nunique_ptr responsibility: ownership is still explicit, but cleanup is automatic.\n"
    };
    const auto tasks = {manualArrayDemo, vectorDemo, uniquePointerDemo};
    { Quiet out; for (auto task : tasks) task(); }
    const int baseline = live, baselineArrays = arrays;
    int index = 0;
    for (auto task : tasks) {
        {
            std::ostringstream captured; auto* prior = std::cout.rdbuf(captured.rdbuf());
            task(); std::cout.rdbuf(prior); assert(captured.str() == expected[index]);
        }
        assert(live == baseline && arrays == baselineArrays);
        int failures = 0, successes = 0;
        for (int point = 0; point < 6; ++point) {
            bool failed = false;
            { Quiet out; failAfter = point;
              try { task(); } catch (const std::bad_alloc&) { failed = true; }
              failAfter = -1;
            }
            if (failed) ++failures; else ++successes;
            assert(live == baseline && arrays == baselineArrays);
        }
        assert(failures >= 1 && successes > 0);
        for (const bool late : {false, true}) {
            for (const bool exceptions : {false, true}) {
                FailingOutput output(late); auto* prior = std::cout.rdbuf(&output);
                std::cout.exceptions(exceptions ? std::ios::badbit | std::ios::failbit : std::ios::goodbit);
                bool caught = false;
                try { task(); } catch (const std::exception&) { caught = true; }
                std::cout.exceptions(std::ios::goodbit); std::cout.clear(); std::cout.rdbuf(prior);
                assert(caught == exceptions);
                assert(live == baseline && arrays == baselineArrays);
            }
        }
        ++index;
    }
    {
        const std::vector<int> original{84, 91, 76, 88};
        auto copied = original; copied[0] = 0; assert(original[0] == 84);
        std::unique_ptr<int[]> owner(new int[4]{84, 91, 76, 88});
        int* observer = owner.get();
        auto moved = std::move(owner); assert(!owner && moved.get() == observer);
        assert(observer[0] == 84 && observer[3] == 88);
    }
    assert(live == baseline && arrays == baselineArrays);
    std::cout << "Verified all three ownership paths, exact scores, allocation failures and throwing-output cleanup.\n";
}
'''


class OwnershipAcceptance(unittest.TestCase):
    def test_make_output_and_cleanup(self):
        source = (ROOT / FOLDER / "main.cpp").read_text()
        brief = (ROOT / FOLDER / "README.md").read_text()
        self.assertIn("```cpp\n" + source + "```", brief)
        self.assertIn("saved capstone", brief)
        self.assertIn("worked comparison", brief)
        with tempfile.TemporaryDirectory(prefix="cppm5-ownership-pack-") as temporary:
            work = Path(temporary)
            for name in ["main.cpp", "Makefile"]: shutil.copyfile(ROOT / FOLDER / name, work / name)
            runtime.run(["make", "main", "main-debug"], work)
            for name in ["main", "main-debug"]:
                result = runtime.run([str(work / name)], work)
                self.assertEqual(result.stdout, EXPECTED); self.assertEqual(result.stderr, "")
                bad = io_runtime.input_run(work / name, work, "", ["--unknown"])
                self.assertEqual(bad.returncode, 2); self.assertEqual(bad.stderr, "Usage: main\n")
            runtime.run(["make", "clean"], work)
            for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                self.assertFalse((work / name).exists())

    def test_native_failure_and_value_contracts(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-ownership-contract-") as temporary:
            work = Path(temporary)
            shutil.copyfile(ROOT / FOLDER / "main.cpp", work / "main.cpp")
            (work / "cases.cpp").write_text(CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", label], work)
                result = runtime.run([str(work / label)], work)
                self.assertEqual(result.stderr, ""); self.assertIn("Verified all three ownership paths", result.stdout)

    def test_independent_cmake_target(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-ownership-cmake-") as temporary:
            work = Path(temporary)
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(work / "build")], work)
            runtime.run(["cmake", "--build", str(work / "build"), "--target", "CPPM5_Modern_Ownership_Reflection"], work)
            result = runtime.run([str(work / "build/CPPM5_Modern_Ownership_Reflection")], work)
            self.assertEqual(result.stdout, EXPECTED); self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
