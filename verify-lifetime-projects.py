"""Verify the two CPPM0 learner/reference contracts using native tools."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
FOLDERS = ['CPPM0-Lifetime-Tracing-Warm-Up', 'CPPM0-Ownership-Boundary-Debugging']
TASK = os.environ.get('CLASSES_AUDIT_PARENT_TASK_ID', 'cpp-level2-lifetime-source')

def interrupted(signum, frame):
    raise KeyboardInterrupt

for signum in (signal.SIGINT, signal.SIGTERM):
    signal.signal(signum, interrupted)

def run(command, cwd, timeout=60):
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True,
                               env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=0'})
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
            print(json.dumps({'event': 'child-process-group-cleanup', 'parentTaskId': TASK, 'pid': process.pid}), flush=True)
        raise
    finally:
        print(json.dumps({'event': 'end', 'parentTaskId': TASK, 'cwd': str(cwd),
                         'command': command, 'pid': process.pid, 'exitCode': process.poll(),
                         'time': datetime.now(timezone.utc).isoformat()}), flush=True)
    if process.returncode:
        raise AssertionError(str(command) + '\n' + output + '\n' + errors)
    return output

class LifetimeProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='cpp-level2-lifetime-gate-')
        cls.work = Path(cls.temporary.name)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def compile(self, text, label, flags=()):
        folder = self.work/label
        folder.mkdir(exist_ok=True)
        source = folder/'main.cpp'
        source.write_text(text)
        binary = folder/'program'
        run(['clang++', '-std=c++20', '-Wall', '-Wextra', '-Wpedantic', '-Werror', *flags, str(source), '-o', str(binary)], folder)
        return run([str(binary)], folder)

    def test_brief_and_role_contracts(self):
        for folder in FOLDERS:
            learner = ROOT/folder/'starter'
            reference = ROOT/folder/'solution'
            self.assertEqual((learner/'README.md').read_bytes(), (reference/'README.md').read_bytes())
            self.assertEqual((ROOT/folder/'main.cpp').read_bytes(), (reference/'main.cpp').read_bytes())
            self.assertIn('TODO', (learner/'main.cpp').read_text())
            self.assertTrue((reference/'REFLECTION.md').is_file())
            self.assertNotIn('REFLECTION.md', [p.name for p in learner.iterdir()])
        starter = (ROOT/FOLDERS[1]/'starter/main.cpp').read_text()
        self.assertIn('throw std::logic_error', starter)
        self.assertNotIn('highestIndex', starter)

    def test_six_independent_make_workflows(self):
        for number, folder in enumerate(FOLDERS):
            for role in ['', 'starter', 'solution']:
                target = self.work/('make-' + str(number) + '-' + (role or 'parent'))
                target.mkdir()
                original = ROOT/folder/role
                for name in ['main.cpp', 'Makefile']:
                    (target/name).write_bytes((original/name).read_bytes())
                run(['make', 'main', 'main-debug'], target)
                for binary in ['main', 'main-debug']:
                    output = run([str(target/binary)], target)
                    if number == 0:
                        self.assertIn('After updateCopy -> Taylor: 70', output)
                        self.assertIn('After updateReference -> Taylor: 80', output)
                        self.assertIn('Returned bonus card -> Morgan: 100', output)
                    else:
                        self.assertIn('After editCopy -> loaded configuration (severity 2)', output)
                        self.assertIn('After editCallerOwnedEntry -> loaded configuration (severity 7)', output)
                        if role == 'starter':
                            self.assertIn('Learner task: Implement highestSeverity', output)
                        else:
                            self.assertIn('Highest severity entry -> failed validation (severity 8)', output)
                run(['make', 'clean'], target)
                self.assertFalse((target/'main').exists())

    def test_return_value_and_alias_traces(self):
        source = (ROOT/FOLDERS[0]/'solution/main.cpp').read_text()
        for label, flags in [('ordinary', ()), ('no-elision', ('-fno-elide-constructors',)), ('sanitized', ('-fsanitize=address,undefined', '-fno-sanitize-recover=all'))]:
            output = self.compile(source, label, flags)
            rows = {match[1]: (int(match[3]), match[4]) for line in output.splitlines()
                    if (match := re.match(r'^(.+) -> (Taylor|Morgan): (\d+) at (\S+)$', line))}
            self.assertEqual(len(rows), 8)
            address = rows['Original card'][1]
            for key in ['After updateCopy', 'Inside updateReference', 'After updateReference', 'Inside observeConstReference']:
                self.assertEqual(rows[key][1], address)
            self.assertNotEqual(rows['Inside updateCopy'][1], address)
            self.assertEqual(rows['After updateCopy'][0], 70)
            self.assertEqual(rows['After updateReference'][0], 80)
            self.assertEqual(rows['Returned bonus card'][0], 100)
            if label == 'no-elision':
                self.assertNotEqual(rows['Inside makeBonusCard'][1], rows['Returned bonus card'][1])

    def test_selection_and_completed_learner(self):
        reference = (ROOT/FOLDERS[1]/'solution/main.cpp').read_text()
        learner = (ROOT/FOLDERS[1]/'starter/main.cpp').read_text()
        pattern = r'const LogEntry& highestSeverity\(.*?\n}\n'
        implementation = re.search(pattern, reference, re.S).group()
        completed = re.sub(pattern, lambda match: implementation, learner, flags=re.S)
        cases = '''
#undef main
#include <cassert>
#include <limits>
int main() {
  std::vector<LogEntry> empty;
  bool rejected = false;
  try { (void)highestSeverity(empty); }
  catch (const std::invalid_argument&) { rejected = true; }
  assert(rejected);
  std::vector<LogEntry> one{{"only", -9}};
  assert(&highestSeverity(one) == &one[0]);
  std::vector<LogEntry> tied{{"low", -10}, {"first", -2}, {"later", -2}};
  assert(&highestSeverity(tied) == &tied[1]);
  assert(tied[0].severity == -10 && tied[1].severity == -2 && tied[2].severity == -2);
  std::vector<LogEntry> extremes{{"min", std::numeric_limits<int>::min()}, {"max", std::numeric_limits<int>::max()}};
  assert(&highestSeverity(extremes) == &extremes[1]);
  assert(extremes[0].message == "min" && extremes[1].message == "max");
}
'''
        for name, code in [('reference', reference), ('completed-learner', completed)]:
            harness = '#define main providedDemoMain\n' + code + cases
            self.compile(harness, name, ('-fsanitize=address,undefined', '-fno-sanitize-recover=all'))

    def test_six_cmake_targets(self):
        build = self.work/'cmake'
        run(['cmake', '-S', str(ROOT), '-B', str(build), '-DCMAKE_CXX_COMPILER=clang++', '-DCMAKE_CXX_FLAGS=-Wall -Wextra -Wpedantic -Werror'], self.work)
        targets = ['CPPM0_Lifetime_Tracing_Warm_Up', 'CPPM0_Ownership_Boundary_Debugging',
                   'CPPM0_Lifetime_Starter', 'CPPM0_Lifetime_Reference',
                   'CPPM0_Ownership_Starter', 'CPPM0_Ownership_Reference']
        run(['cmake', '--build', str(build), '--target', *targets, '--parallel', '1'], self.work, 120)
        for target in targets:
            run([str(build/target)], self.work)

if __name__ == '__main__':
    unittest.main()
