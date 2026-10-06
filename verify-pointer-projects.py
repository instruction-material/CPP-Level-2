"""Native acceptance gates for the four CPPM1 pointer learner/reference packs."""
from datetime import datetime, timezone
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
TASK = os.environ.get('CLASSES_AUDIT_PARENT_TASK_ID', 'cpp-level2-pointer-source')
FOLDERS = ['CPPM1-Pointer-Error-Examples', 'CPPM1-Pointer-Error-Examples-Starter',
           'CPPM1-Pointer-Practice', 'CPPM1-Pointer-Practice-Starter']
FLAGS = ['-std=c++20', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
SANITIZERS = ['-g', '-O0', '-fsanitize=address,undefined', '-fno-sanitize-recover=all']

def interrupted(signum, frame):
    raise KeyboardInterrupt

for signum in (signal.SIGINT, signal.SIGTERM):
    signal.signal(signum, interrupted)

def run(command, cwd, expected_success=True, timeout=60):
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True,
                               env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=0',
                                    'UBSAN_OPTIONS': 'halt_on_error=1'})
    print(json.dumps({'event': 'start', 'parentTaskId': TASK, 'cwd': str(cwd),
                     'command': command, 'pid': process.pid, 'parentPid': os.getpid(),
                     'time': datetime.now(timezone.utc).isoformat(), 'timeoutSeconds': timeout}), flush=True)
    try:
        output, errors = process.communicate(timeout=timeout)
    except BaseException:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
            print(json.dumps({'event': 'child-process-group-cleanup', 'parentTaskId': TASK,
                              'pid': process.pid}), flush=True)
        raise
    finally:
        print(json.dumps({'event': 'end', 'parentTaskId': TASK, 'cwd': str(cwd),
                         'command': command, 'pid': process.pid, 'exitCode': process.poll(),
                         'time': datetime.now(timezone.utc).isoformat()}), flush=True)
    if (process.returncode == 0) != expected_success:
        raise AssertionError(str(command) + '\n' + output + '\n' + errors)
    return subprocess.CompletedProcess(command, process.returncode, output, errors)

class PointerProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='cpp-level2-pointer-gate-')
        cls.work = Path(cls.temporary.name)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def compile(self, source, label, flags=()):
        folder = self.work/label
        folder.mkdir(exist_ok=True)
        (folder/'main.cpp').write_text(source)
        binary = folder/'program'
        run(['clang++', *FLAGS, *flags, 'main.cpp', '-o', str(binary)], folder)
        return binary, folder

    def test_pack_roles_and_brief_parity(self):
        for reference in [FOLDERS[0], FOLDERS[2]]:
            starter = ROOT/(reference+'-Starter')
            self.assertEqual((ROOT/reference/'README.md').read_bytes(), (starter/'README.md').read_bytes())
            self.assertTrue((ROOT/reference/'REFLECTION.md').is_file())
            self.assertFalse((starter/'REFLECTION.md').exists())
            self.assertEqual([p.name for p in starter.glob('*.cpp')], ['main.cpp'])
            self.assertIn('TODO', (starter/'main.cpp').read_text())
            self.assertIn('throw std::logic_error', (starter/'main.cpp').read_text())
        reference = (ROOT/FOLDERS[2]/'main.cpp').read_text()
        self.assertIn('p1 = p2 = arr1.data();', reference)
        self.assertIn('Debug 1a', reference)
        self.assertIn('Debug 1b', reference)
        self.assertIn('Debug 1c', reference)

    def test_four_make_workflows_and_safe_arguments(self):
        expected = ('Live observer value: 20\nAbsent observer: no dereference\n'
                    'Two pointer aliases: 1\nInitialized pointer value: 10\n'
                    'Assigned target value: 5\nInitialized target value: 7\nMatched target type: potatoes\n')
        for folder in FOLDERS:
            target = self.work/folder
            target.mkdir()
            for name in ['main.cpp', 'Makefile']:
                shutil.copyfile(ROOT/folder/name, target/name)
            run(['make', 'main', 'main-debug'], target)
            for binary in ['main', 'main-debug']:
                result = run([str(target/binary)], target)
                self.assertEqual(result.stderr, '')
                if folder.endswith('-Starter'):
                    self.assertEqual(result.stdout.count('Learner task:'), 3 if 'Practice' in folder else 1)
                elif 'Error' in folder:
                    self.assertEqual(result.stdout, expected)
                else:
                    self.assertNotIn('Learner task:', result.stdout)
            if 'Error' in folder:
                for mode in ['--null', '--dangling']:
                    result = run([str(target/'main'), mode], target, False)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn('require an AddressSanitizer build', result.stderr)
                    self.assertNotIn('runtime error', result.stderr)
                    self.assertEqual(result.stdout, '')
                for args in [['--unknown'], ['--null', '--dangling']]:
                    for binary in ['main', 'main-debug']:
                        result = run([str(target/binary), *args], target, False)
                        self.assertEqual(result.returncode, 2)
                        self.assertIn('Usage:', result.stderr)
            run(['make', 'clean'], target)
            self.assertFalse((target/'main').exists())
            self.assertFalse((target/'main-debug').exists())
            self.assertFalse(list(target.glob('*.dSYM')))

    def test_explicit_null_and_dangling_diagnostics(self):
        for folder in FOLDERS[:2]:
            binary, cwd = self.compile((ROOT/folder/'main.cpp').read_text(), folder+'-diagnostics', SANITIZERS)
            null = run([str(binary), '--null'], cwd, False)
            self.assertIn('Diagnostic only: null store', null.stdout)
            self.assertRegex(null.stderr, r'runtime error: store to null pointer')
            dangling = run([str(binary), '--dangling'], cwd, False)
            self.assertIn('Diagnostic only: dangling store', dangling.stdout)
            self.assertIn('heap-use-after-free', dangling.stderr)

    def test_disabled_type_errors_remain_compile_failures(self):
        snippets = {
            'mixed-declarators': 'int value = 10; int* first = &value, second = &value; (void)first; (void)second;',
            'integer-assignment': 'int* pointer = nullptr; pointer = 5; (void)pointer;',
            'mismatched-target': 'std::string text = "potatoes"; int* pointer = &text; (void)pointer;',
            'array-object': 'std::array<int, 20> values{}; int* pointer = values; (void)pointer;'
        }
        for label, snippet in snippets.items():
            folder = self.work/label
            folder.mkdir()
            (folder/'example.cpp').write_text('#include <array>\n#include <string>\nint main() { '+snippet+' }\n')
            result = run(['clang++', *FLAGS, '-fsyntax-only', 'example.cpp'], folder, False)
            self.assertIn('error:', result.stderr)

    def test_practice_contract_and_completed_learner(self):
        reference = (ROOT/FOLDERS[2]/'main.cpp').read_text()
        completed = (ROOT/FOLDERS[3]/'main.cpp').read_text()
        for name in ['question1', 'question2', 'question3']:
            pattern = r'void '+name+r'\([^\n]*\) \{.*?\n}'
            implementation = re.search(pattern, reference, re.S).group()
            completed, count = re.subn(pattern, lambda match: implementation, completed, flags=re.S)
            self.assertEqual(count, 1)
        cases = r'''
#undef main
#include <cassert>
#include <functional>
#include <sstream>
#include <utility>

std::string capture(const std::function<void()>& call) {
    std::ostringstream output;
    auto* previous = std::cout.rdbuf(output.rdbuf());
    call();
    std::cout.rdbuf(previous);
    return output.str();
}
int main() {
    std::array<int, 20> values{};
    for (std::size_t i = 0; i < values.size(); ++i) values[i] = static_cast<int>(i);
    const auto first = capture([&] { question1(values); });
    std::istringstream rows(first);
    std::string line;
    int left = 0, right = 0;
    while (std::getline(rows, line)) {
        if (line.starts_with("p1 is: ")) assert(std::stoi(line.substr(7)) == left++);
        if (line.starts_with("p2 is: ")) { assert(std::stoi(line.substr(7)) == right); right += 2; }
    }
    assert(left == 10 && right == 20);
    for (const auto& text : std::vector<std::string>{"", "x", "ab", "abc", "abcd", "JuniLearning", "abcdefg"}) {
        const auto output = capture([&] { question2(text); });
        if (text.empty()) {
            assert(output == "Question 2 needs a non-empty string.\n");
        } else {
            assert(output.find("Number of times p1 pointer increased: " + std::to_string(text.size()/2)) != std::string::npos);
            assert(output.find("Number of times p2 pointer decreased: " + std::to_string((text.size()-1)/2)) != std::string::npos);
        }
    }
    std::vector<std::pair<std::string, std::size_t>> fixed{
        {"1hello", 1}, {"3hello", 3}, {"12e4woah", 7}, {"1a2bc", 3},
        {"0a1b", 1}, {"4abc1", 4}, {"4abc", 0}, {"9a1bc", 0},
        {"abc", 0}, {"0", 0}, {"9", 0}, {"000", 0}, {"2abc1", 3}, {"2a3b", 2}
    };
    fixed.push_back({std::string("1") + static_cast<char>(0x80) + "2bc", 3});
    auto check = [](const std::string& text, std::size_t offset) {
        const std::string before = text;
        const auto output = capture([&] { question3(text); });
        assert(text == before);
        if (text.empty()) { assert(output == "Question 3 needs a non-empty string.\n"); return; }
        const std::string summary = "The final location of the end pointer was pointing to: " + std::string(1, text[offset]) + ", after advancing " + std::to_string(offset) + " characters.";
        const auto first = output.find(summary);
        assert(first != std::string::npos);
        assert(output.find(summary, first+summary.size()) != std::string::npos);
        assert(output.find(summary, output.find(summary, first+summary.size())+summary.size()) == std::string::npos);
    };
    check("", 0);
    for (const auto& [text, offset] : fixed) check(text, offset);
    // Independent bounded integer oracle: include letters, zero, a valid step,
    // and an oversized step. Exhaust all strings through four characters.
    const std::string alphabet = "ab0129";
    for (int length = 1; length <= 4; ++length) {
        int combinations = 1;
        for (int i = 0; i < length; ++i) combinations *= static_cast<int>(alphabet.size());
        for (int code = 0; code < combinations; ++code) {
            int rest = code;
            std::string text;
            for (int i = 0; i < length; ++i) {
                text += alphabet[static_cast<std::size_t>(rest)%alphabet.size()];
                rest /= static_cast<int>(alphabet.size());
            }
            int position = 0;
            for (char character : text) {
                if (character >= '0' && character <= '9') {
                    const int next = position + (character-'0');
                    if (next >= length) break;
                    position = next;
                }
            }
            check(text, static_cast<std::size_t>(position));
        }
    }
}
'''
        for label, code in [('reference-cases', reference), ('completed-learner-cases', completed)]:
            binary, cwd = self.compile('#define main providedMain\n'+code+cases, label, SANITIZERS)
            result = run([str(binary)], cwd)
            self.assertEqual(result.stderr, '')
        error_reference = (ROOT/FOLDERS[0]/'main.cpp').read_text()
        error_learner = (ROOT/FOLDERS[1]/'main.cpp').read_text()
        pattern = r'void repairedExamples\(\) \{.*?\n}'
        implementation = re.search(pattern, error_reference, re.S).group()
        error_completed = re.sub(pattern, lambda match: implementation, error_learner, flags=re.S)
        binary, cwd = self.compile(error_completed, 'completed-error-learner', SANITIZERS)
        result = run([str(binary)], cwd)
        self.assertNotIn('Learner task:', result.stdout)
        self.assertEqual(result.stderr, '')

    def test_five_independent_cmake_targets(self):
        build = self.work/'cmake'
        run(['cmake', '-S', str(ROOT), '-B', str(build), '-DCMAKE_CXX_COMPILER=clang++',
             '-DCMAKE_CXX_FLAGS=-Wall -Wextra -Wpedantic -Werror'], self.work)
        targets = ['CPP_Level_2', 'CPPM1_Error_Starter', 'CPPM1_Error_Reference',
                   'CPPM1_Practice_Starter', 'CPPM1_Practice_Reference']
        run(['cmake', '--build', str(build), '--target', *targets, '--parallel', '1'], self.work, timeout=120)
        for target in targets:
            result = run([str(build/target)], self.work)
            self.assertEqual(result.stderr, '')

if __name__ == '__main__':
    unittest.main(verbosity=2)
