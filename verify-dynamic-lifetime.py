"""Scoped native checks for the complete dynamic-variable lifetime lesson."""
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pointer_runtime", ROOT/"verify-pointer-projects.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
FOLDER = "CPPM4-Dynamic-Variables-Reference"

def input_run(binary, cwd, text):
    command = [str(binary)]
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0", "UBSAN_OPTIONS": "halt_on_error=1"})
    print(json.dumps({"event":"start", "parentTaskId":runtime.TASK, "cwd":str(cwd), "command":command, "pid":process.pid, "parentPid":os.getpid(), "time":datetime.now(timezone.utc).isoformat(), "timeoutSeconds":30}), flush=True)
    try:
        output, errors = process.communicate(text, timeout=30)
    except BaseException:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL); process.communicate()
            print(json.dumps({"event":"child-process-group-cleanup", "pid":process.pid}), flush=True)
        raise
    finally:
        print(json.dumps({"event":"end", "parentTaskId":runtime.TASK, "cwd":str(cwd), "pid":process.pid, "exitCode":process.poll(), "time":datetime.now(timezone.utc).isoformat()}), flush=True)
    return subprocess.CompletedProcess(command, process.returncode, output, errors)

CASES = r"""
#undef main
#include <cassert>
#include <climits>
#include <cstdlib>
#include <new>
#include <sstream>

static int live = 0;
static bool failNext = false;
void* operator new(std::size_t bytes) {
    if (failNext) { failNext = false; throw std::bad_alloc(); }
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++live; return memory;
}
void operator delete(void* memory) noexcept { if (memory) { --live; std::free(memory); } }
void operator delete(void* memory, std::size_t) noexcept { ::operator delete(memory); }
class FailingOutput : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize) override { throw std::runtime_error("Output failed"); }
    int_type overflow(int_type) override { throw std::runtime_error("Output failed"); }
};
int main() {
    int value = 77;
    for (const std::string token : {"", " ", "+", "-", "--1", "+-1", "1.2", "1x", "1 2", "9999999999999999999999999999999999"}) {
        assert(!parseInteger(token, value) && value == 77);
    }
    for (const int expected : {INT_MIN, -1, 0, 1, INT_MAX}) {
        const std::string token = std::to_string(expected);
        assert(parseInteger(" \t" + token + "\r ", value) && value == expected);
        if (expected >= 0) assert(parseInteger("+" + token, value) && value == expected);
        const int before = value;
        if (expected == INT_MIN || expected == INT_MAX) {
            assert(!parseInteger(token + "0", value) && value == before);
        } else {
            assert(parseInteger(token + "0", value) && value == expected * 10);
        }
    }
    // Warm the same stream formats before checking scoped live allocations.
    std::cout << std::boolalpha << true << static_cast<const void*>(&value) << value << '\n';
    for (int attempt = 0; attempt < 5; ++attempt) {
        const int baseline = live;
        demonstrateInteger(attempt); demonstrateString();
        assert(live == baseline);
    }
    for (const bool stringExample : {false, true}) {
        const int baseline = live;
        failNext = true; bool caught = false;
        try { if (stringExample) demonstrateString(); else demonstrateInteger(5); }
        catch (const std::bad_alloc&) { caught = true; }
        assert(caught && !failNext && live == baseline);
        FailingOutput failed;
        auto* original = std::cout.rdbuf(&failed);
        std::cout.exceptions(std::ios::badbit | std::ios::failbit);
        caught = false;
        try { if (stringExample) demonstrateString(); else demonstrateInteger(5); }
        catch (...) { caught = true; }
        std::cout.exceptions(std::ios::goodbit);
        std::cout.clear(); std::cout.rdbuf(original);
        assert(caught && live == baseline);
    }
    std::istringstream absent("");
    auto* originalInput = std::cin.rdbuf(absent.rdbuf());
    std::cin.setstate(std::ios::badbit);
    std::ostringstream errors;
    auto* originalErrors = std::cerr.rdbuf(errors.rdbuf());
    assert(providedMain() == 1);
    std::cin.clear(); std::cin.rdbuf(originalInput); std::cerr.rdbuf(originalErrors);
    assert(errors.str() == "Input could not be read.\n");
    std::cout << "Verified parser boundaries, repeated scalar/string cleanup, allocation/output failures and failed input.\n";
}
"""

class DynamicLifetime(unittest.TestCase):
    def test_make_input_and_cleanup(self):
        with tempfile.TemporaryDirectory(prefix="cppm4-lifetime-gate-") as temporary:
            work = Path(temporary)
            for name in ["main.cpp", "Makefile"]:
                shutil.copyfile(ROOT/FOLDER/name, work/name)
            runtime.run(["make", "main", "main-debug"], work)
            for name in ["main", "main-debug"]:
                for text, value in [("5\n", 5), (" -1 \n", -1), ("+0\n", 0), ("42", 42)]:
                    result = input_run(work/name, work, text)
                    self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                    self.assertIn(f"The value of *p1 is: {value}\n", result.stdout)
                    self.assertIn("p1 is nullptr: true\n", result.stdout)
                    self.assertIn("Dynamic input\n", result.stdout)
                    self.assertIn("strPtr is nullptr: true\n", result.stdout)
                for text in ["\n", "no\n", "5x\n", "5 6\n", "1.5\n", "+-5\n", "99999999999999999999999\n"]:
                    result = input_run(work/name, work, text)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stderr, "Expected a complete, representable integer.\n")
                    self.assertNotIn("The value of", result.stdout)
                result = input_run(work/name, work, "")
                self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                self.assertIn("no dynamic object allocated", result.stdout)
            runtime.run(["make", "clean"], work)
            for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                self.assertFalse((work/name).exists())
    def test_native_lifetime_contracts(self):
        with tempfile.TemporaryDirectory(prefix="cppm4-lifetime-contract-") as temporary:
            work = Path(temporary)
            source = (ROOT/FOLDER/"main.cpp").read_text()
            (work/"cases.cpp").write_text("#define main providedMain\n" + source + CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                binary = work/label
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", str(binary)], work)
                result = runtime.run([str(binary)], work)
                self.assertEqual(result.stderr, "")
                self.assertIn("Verified parser boundaries", result.stdout)
            cmake = work/"cmake"
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(cmake)], work)
            runtime.run(["cmake", "--build", str(cmake), "--target", "CPPM4_Dynamic_Variables"], work)
            result = input_run(cmake/"CPPM4_Dynamic_Variables", work, "5\n")
            self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")

if __name__ == "__main__":
    unittest.main()
