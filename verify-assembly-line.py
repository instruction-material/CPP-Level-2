"""Independent input, ownership, failure and bonus acceptance for Assembly Line."""
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
spec = importlib.util.spec_from_file_location("pointer_runtime", ROOT / "verify-pointer-projects.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
REFERENCE = "CPPM4-Assembly-Line"
STARTER = REFERENCE + "-Starter"


def input_run(binary, cwd, text, arguments=()):
    command = [str(binary), *arguments]
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True,
                               env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0", "UBSAN_OPTIONS": "halt_on_error=1"})
    print(json.dumps({"event": "start", "parentTaskId": runtime.TASK, "cwd": str(cwd),
                      "command": command, "pid": process.pid, "parentPid": os.getpid(),
                      "time": datetime.now(timezone.utc).isoformat(), "timeoutSeconds": 30}), flush=True)
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
            print(json.dumps({"event": "child-process-group-cleanup", "pid": process.pid}), flush=True)
        raise
    finally:
        print(json.dumps({"event": "end", "parentTaskId": runtime.TASK, "cwd": str(cwd),
                          "command": command, "pid": process.pid, "exitCode": process.poll(),
                          "time": datetime.now(timezone.utc).isoformat()}), flush=True)
    return subprocess.CompletedProcess(command, process.returncode, output, errors)


CASES = r'''
#undef main
#include <cassert>
#include <cstdlib>
#include <limits>
#include <new>

static int live = 0;
static int failAfter = -1;
void* allocate(std::size_t bytes) {
    if (failAfter == 0) { failAfter = -1; throw std::bad_alloc(); }
    if (failAfter > 0) --failAfter;
    void* memory = std::malloc(bytes == 0 ? 1 : bytes);
    if (memory == nullptr) throw std::bad_alloc();
    ++live;
    return memory;
}
void* operator new(std::size_t bytes) { return allocate(bytes); }
void* operator new[](std::size_t bytes) { return allocate(bytes); }
void operator delete(void* memory) noexcept { if (memory) { --live; std::free(memory); } }
void operator delete[](void* memory) noexcept { ::operator delete(memory); }
void operator delete(void* memory, std::size_t) noexcept { ::operator delete(memory); }
void operator delete[](void* memory, std::size_t) noexcept { ::operator delete(memory); }
class Sink : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize size) override { return size; }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};
class FailingOutput : public std::streambuf {
    std::streamsize xsputn(const char*, std::streamsize) override { throw std::runtime_error("Output failed"); }
    int_type overflow(int_type) override { throw std::runtime_error("Output failed"); }
};
class FailingDisplay : public std::streambuf {
    std::streamsize xsputn(const char* text, std::streamsize size) override {
        if (std::string_view(text, static_cast<std::size_t>(size)).find("Nice!") != std::string_view::npos) {
            throw std::runtime_error("Display failed");
        }
        return size;
    }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};
template<class Exception, class Task>
void rejected(Task task) {
    bool caught = false;
    try { task(); } catch (const Exception&) { caught = true; }
    assert(caught);
}

int main() {
    double weight = 19;
    for (const std::string token : {"", " ", "-1", "nan", "inf", "-inf", "1e9999", "1x", "1 2", "+", "--1"}) {
        assert(!parseWeight(token, weight) && weight == 19);
    }
    for (const double value : {0.0, 0.5, 2.205, 4.41, 1e12}) {
        assert(parseWeight(" +" + std::to_string(value) + " \r", weight));
        assert(weight == value);
    }
    assert(parseWeight("-0", weight) && weight == 0);
    assert(parseWeight("1e3", weight) && weight == 1000);
    std::size_t count = 7;
    for (const std::string token : {"", "0", "-1", "21", "2x", "2 3", "2.5", "++2", "99999999999999999999999999"}) {
        assert(!parseCount(token, count) && count == 7);
    }
    assert(parseCount(" +1 ", count) && count == 1);
    assert(parseCount("20", count) && count == 20);
    for (const double value : {-1.0, std::numeric_limits<double>::infinity(),
                               std::numeric_limits<double>::quiet_NaN()}) {
        rejected<std::invalid_argument>([&] { Object bad("crate", value); });
    }
    rejected<std::invalid_argument>([] { Object bad(" \t", 1); });
    {
        Object placeholder;
        rejected<std::invalid_argument>([&] { placeholder.print(); });
        Object named("small crate", 2.205);
        std::ostringstream output;
        named.print(output);
        assert(output.str() == "Nice! This object is named small crate and weighs 2.205 pounds, which is 1 kilograms.\n");
    }
    const std::string name(90, 'x');
    Sink sink;
    std::ostream quiet(&sink);
    // Warm formatted output before measuring scoped object cleanup.
    printDynamicObject(name, 2.205, quiet);
    const int warmed = live;
    for (int i = 0; i < 5; ++i) {
        printDynamicObject(name, i, quiet);
        assert(live == warmed);
    }
    for (const int point : {0, 1}) {
        failAfter = point;
        rejected<std::bad_alloc>([&] { printDynamicObject(name, 5, quiet); });
        assert(failAfter == -1 && live == warmed);
    }
    FailingOutput failing;
    std::ostream failed(&failing);
    failed.exceptions(std::ios::badbit | std::ios::failbit);
    rejected<std::exception>([&] { printDynamicObject(name, 5, failed); });
    assert(live == warmed);
    for (const bool batch : {false, true}) {
        std::istringstream absent;
        absent.setstate(std::ios::badbit);
        std::ostringstream output;
        assert((batch ? runBatch(absent, output) : runAssembly(absent, output)) == 1);
        assert(output.str().find("Input could not be read.") != std::string::npos);
    }
    const std::string script = "3\n" + name + "\n2.205\n" + name + "\n4.41\n" + name + "\n0\n";
    int injected = 0;
    for (int point = 0; point < 40; ++point) {
        const int before = live;
        {
            std::istringstream input(script);
            std::ostream output(&sink);
            failAfter = point;
            try { (void)runBatch(input, output); } catch (const std::bad_alloc&) {}
            if (failAfter == -1) ++injected;
            failAfter = -1;
        }
        assert(live == before);
    }
    assert(injected >= 8);
    // Exercise the actual batch cleanup when display fails after collection.
    {
        std::istringstream input(script);
        FailingDisplay display;
        std::ostream output(&display);
        output.exceptions(std::ios::badbit | std::ios::failbit);
        const int before = live;
        rejected<std::exception>([&] { (void)runBatch(input, output); });
        assert(live == before);
    }
    for (const std::string text : {"2\ncrate\n1\n!quit\n", "2\ncrate\n1\n", "1\ncrate\n!quit\n"}) {
        const int before = live;
        {
            std::istringstream input(text);
            std::ostream output(&sink);
            assert(runBatch(input, output) == 0);
        }
        assert(live == before);
    }
    std::cout << "Verified parser boundaries, object conversion, scalar/array failure cleanup and read errors.\n";
}
'''


class AssemblyLineAcceptance(unittest.TestCase):
    def test_pack_build_input_and_cleanup(self):
        self.assertEqual((ROOT / REFERENCE / "README.md").read_text(), (ROOT / STARTER / "README.md").read_text())
        cases = [
            ((), "small crate\n2.205\n!quit\n", 1),
            ((), "a\n0\nb\n4.41\n!quit\n", 2),
            ((), "\n crate with spaces \n-1\nnan\n1x\n1 2\n4.41\n!quit\n", 1),
            ((), "", 0), ((), "crate\n", 0), ((), "crate\n!quit\n", 0),
            ((), "crate\n0.5", 1),
            (("--batch",), "2\none box\n2.205\ntwo boxes\n4.41\n", 2),
            (("--batch",), "0\n21\n2.5\n+1\ncrate\n0\n", 1),
            (("--batch",), "2\ncrate\n1\n!quit\n", 0),
            (("--batch",), "2\ncrate\n1\n", 0),
            (("--batch",), "!quit\n", 0), (("--batch",), "", 0),
            (("--batch",), "20\n" + "box\n0\n" * 20, 20),
        ]
        for folder in [REFERENCE, STARTER]:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory(prefix="cppm4-assembly-pack-") as temporary:
                work = Path(temporary)
                for name in ["main.cpp", "Makefile", "README.md"]:
                    shutil.copyfile(ROOT / folder / name, work / name)
                runtime.run(["make", "main", "main-debug"], work)
                for name in ["main", "main-debug"]:
                    for arguments, text, expected in cases:
                        result = input_run(work / name, work, text, arguments)
                        self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                        if folder == REFERENCE:
                            self.assertEqual(result.stdout.count("Nice! This object is named "), expected)
                            if "small crate" in text: self.assertIn("small crate and weighs 2.205 pounds, which is 1 kilograms", result.stdout)
                            if "crate with spaces" in text: self.assertIn("crate with spaces and weighs 4.41 pounds, which is 2 kilograms", result.stdout)
                        else:
                            self.assertIn("Unfinished learner task:", result.stdout)
                            self.assertNotIn("Nice!", result.stdout)
                    result = input_run(work / name, work, "", ["--unknown"])
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stderr, "Usage: main [--batch]\n")
                runtime.run(["make", "clean"], work)
                for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                    self.assertFalse((work / name).exists())

    def test_native_contracts_and_cmake_targets(self):
        with tempfile.TemporaryDirectory(prefix="cppm4-assembly-contract-") as temporary:
            work = Path(temporary)
            source = (ROOT / REFERENCE / "main.cpp").read_text()
            (work / "cases.cpp").write_text("#define main providedMain\n" + source + CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                binary = work / label
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", str(binary)], work)
                self.assertEqual(runtime.run([str(binary)], work).stderr, "")
            cmake = work / "cmake"
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(cmake)], work)
            runtime.run(["cmake", "--build", str(cmake), "--target", "CPPM4_Assembly_Line_Starter", "CPPM4_Assembly_Line_Reference"], work)
            for name in ["CPPM4_Assembly_Line_Starter", "CPPM4_Assembly_Line_Reference"]:
                self.assertEqual(input_run(cmake / name, work, "!quit\n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
