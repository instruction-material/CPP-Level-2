"""Scoped native acceptance gates for the four CPPM2 array lesson/project packs."""
from pathlib import Path
import importlib.util,json,re,shutil,tempfile,unittest

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pointer_command_runtime',ROOT/'verify-pointer-projects.py')
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
run=runtime.run;FLAGS=runtime.FLAGS;SANITIZERS=runtime.SANITIZERS
FOLDERS=['CPPM2-Array-Basics-Reference','CPPM2-Pointer-Arithmetic-Reference','CPPM2-Array-Practice','CPPM2-Array-Practice-Starter']
TASKS=['fillPerfectSquares','firstLast','sumArray','sumLetters']
SAMPLE='\nPerfect squares: 0 1 4 9 16 25 36 49 64 81 \nFirst and last are the same? 0\nSum: 285\nTotal letters: 17\n'
CASES=r'''
#undef main
#include <array>
#include <vector>
#include <cassert>
#include <limits>
#include <algorithm>

template<class Call>
void invalid(Call call) {
    bool caught = false;
    try { call(); } catch (const std::invalid_argument&) { caught = true; }
    assert(caught);
}

int main() {
    assert(!firstLast(nullptr, 0));
    assert(sumArray(nullptr, 0) == 0);
    assert(sumLetters(nullptr, 0) == 0);
    int storage[12]{};
    storage[10] = -11; storage[11] = -12;
    fillPerfectSquares(storage, 10);
    const int squares[10] = {0, 1, 4, 9, 16, 25, 36, 49, 64, 81};
    assert(std::equal(storage, storage + 10, squares));
    assert(storage[10] == -11 && storage[11] == -12);
    assert(!firstLast(storage, 10) && sumArray(storage, 10) == 285);
    for (const int size : {-1, -2}) {
        invalid([&] { (void)firstLast(storage, size); });
        invalid([&] { (void)sumArray(storage, size); });
        invalid([&] { (void)sumLetters(nullptr, size); });
        invalid([&] { fillPerfectSquares(storage, size); });
    }
    invalid([] { (void)firstLast(nullptr, 1); });
    invalid([] { (void)sumArray(nullptr, 1); });
    invalid([] { (void)sumLetters(nullptr, 1); });
    invalid([] { fillPerfectSquares(nullptr, 10); });
    for (const int size : {0, 9, 11}) invalid([&] { fillPerfectSquares(storage, size); });
    std::size_t checked = 0;
    const std::array<int, 5> domain = {-2, -1, 0, 1, 2};
    for (int length = 0; length <= 5; ++length) {
        int combinations = 1;
        for (int i = 0; i < length; ++i) combinations *= 5;
        for (int code = 0; code < combinations; ++code) {
            std::array<int, 5> values{};
            values.fill(77);
            int digits = code;
            long long expected = 0;
            for (int i = 0; i < length; ++i) {
                values[static_cast<std::size_t>(i)] = domain[static_cast<std::size_t>(digits % 5)];
                digits /= 5;
                expected += values[static_cast<std::size_t>(i)];
            }
            const auto before = values;
            const bool endpoints = length != 0 && values[0] == values[static_cast<std::size_t>(length - 1)];
            assert(firstLast(values.data(), length) == endpoints);
            assert(sumArray(values.data(), length) == expected);
            assert(values == before);
            ++checked;
        }
    }
    assert(checked == 3906);
    const std::vector<std::vector<int>> boundaries = {
        {INT_MAX}, {INT_MIN}, {INT_MAX, 0}, {INT_MIN, 0},
        {INT_MAX, 1}, {INT_MIN, -1}, {INT_MAX, 1, -1}, {INT_MIN, -1, 1},
        {INT_MAX, -INT_MAX}, {INT_MIN, INT_MAX}, {INT_MAX, INT_MIN},
        {0, INT_MAX, -1, 1}, {0, INT_MIN, 1, -1}
    };
    for (auto values : boundaries) {
        const auto before = values;
        long long expected = 0;
        bool overflow = false;
        for (const int value : values) {
            expected += value;
            if (expected > INT_MAX || expected < INT_MIN) { overflow = true; break; }
        }
        bool caught = false;
        try {
            const int actual = sumArray(values.data(), static_cast<int>(values.size()));
            assert(!overflow && actual == expected);
        } catch (const std::overflow_error&) { caught = true; }
        assert(caught == overflow && values == before);
    }
    std::vector<std::string> words = {"happy", "Juni", "computer", "", "\xc3\xa9", std::string("a\0b", 3), "\x80"};
    const auto before = words;
    std::size_t expectedBytes = 0;
    for (int length = 0; length <= static_cast<int>(words.size()); ++length) {
        assert(sumLetters(words.data(), length) == static_cast<int>(expectedBytes));
        if (length < static_cast<int>(words.size())) expectedBytes += words[static_cast<std::size_t>(length)].size();
    }
    assert(sumLetters(words.data(), 3) == 17 && words == before);
    invalid([&] { (void)sumLetters(words.data(), -1); });
    std::cout << "Verified 3906 logical ranges, 13 integer boundaries, string byte prefixes, and input preservation.\n";
    return 0;
}
'''

def completedLearner():
    reference=(ROOT/FOLDERS[2]/'main.cpp').read_text()
    learner=(ROOT/FOLDERS[3]/'main.cpp').read_text()
    for task in TASKS:
        pattern=r'// TASK '+task+r'\n[\s\S]*?\n// END TASK '+task
        implementation=re.search(pattern,reference).group()
        learner,count=re.subn(pattern,lambda match:implementation,learner)
        assert count==1
    return learner

class ArrayProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary=tempfile.TemporaryDirectory(prefix='cpp-level2-array-gate-');cls.work=Path(cls.temporary.name)
    @classmethod
    def tearDownClass(cls):cls.temporary.cleanup()
    def compile(self,source,label,flags=()):
        folder=self.work/label;folder.mkdir(exist_ok=True);(folder/'main.cpp').write_text(source)
        binary=folder/'program';run(['clang++',*FLAGS,*flags,'main.cpp','-o',str(binary)],folder)
        return binary,folder
    def test_roles_briefs_and_single_entrypoints(self):
        reference=ROOT/FOLDERS[2];learner=ROOT/FOLDERS[3]
        self.assertEqual((reference/'README.md').read_bytes(),(learner/'README.md').read_bytes())
        self.assertTrue((reference/'REFLECTION.md').is_file());self.assertFalse((learner/'REFLECTION.md').exists())
        for folder in FOLDERS:
            path=ROOT/folder;self.assertEqual([p.name for p in path.glob('*.cpp')],['main.cpp'])
            self.assertIn('## Native workflow',(path/'README.md').read_text())
        text=(learner/'main.cpp').read_text();self.assertEqual(text.count('throw UnfinishedTask'),4)
        for task in TASKS:self.assertIn('// TASK '+task,text)
    def test_four_strict_make_workflows_and_safe_defaults(self):
        for folder in FOLDERS:
            target=self.work/folder;target.mkdir()
            for name in ['main.cpp','Makefile']:shutil.copyfile(ROOT/folder/name,target/name)
            run(['make','main','main-debug'],target)
            normal=run([str(target/'main')],target);debug=run([str(target/'main-debug')],target)
            self.assertEqual(normal.stderr,'');self.assertEqual(debug.stderr,'');self.assertEqual(normal.stdout,debug.stdout)
            if folder.endswith('-Starter'):self.assertEqual(normal.stdout.count('Learner task:'),4)
            elif folder==FOLDERS[2]:self.assertEqual(normal.stdout,SAMPLE)
            elif folder==FOLDERS[0]:self.assertEqual(normal.stdout,'0\n42\n1\n10\n'+''.join(str(i)+'\n' for i in range(10)))
            else:
                self.assertIn('Current offset: 1\n',normal.stdout)
                self.assertIn('One-past offset (not dereferenced): 20\n',normal.stdout)
                self.assertIn('Values by traversal: '+''.join(str(i)+' ' for i in range(20))+'\n',normal.stdout)
                self.assertTrue(normal.stdout.startswith('*p1 is originally equal to:\n0\n'))
            run(['make','clean'],target);self.assertFalse((target/'main').exists());self.assertFalse((target/'main-debug').exists());self.assertFalse(list(target.glob('*.dSYM')))
    def test_reference_and_completed_learner_contracts(self):
        for label,source in [('reference',(ROOT/FOLDERS[2]/'main.cpp').read_text()),('completed-learner',completedLearner())]:
            binary,cwd=self.compile(source,label+'-default',SANITIZERS);result=run([str(binary)],cwd)
            self.assertEqual(result.stdout,SAMPLE);self.assertEqual(result.stderr,'')
            binary,cwd=self.compile('#define main providedMain\n'+source+CASES,label+'-contracts',SANITIZERS);result=run([str(binary)],cwd)
            self.assertEqual(result.stderr,'');self.assertIn('3906 logical ranges, 13 integer boundaries',result.stdout)
    def test_four_independent_cmake_targets(self):
        build=self.work/'cmake';run(['cmake','-S',str(ROOT),'-B',str(build),'-DCMAKE_CXX_COMPILER=clang++'],self.work)
        targets=['CPPM2_Array_Basics','CPPM2_Pointer_Arithmetic','CPPM2_Array_Practice_Starter','CPPM2_Array_Practice_Reference']
        run(['cmake','--build',str(build),'--target',*targets,'--parallel','1'],self.work,timeout=120)
        for target in targets:self.assertEqual(run([str(build/target)],self.work).stderr,'')

if __name__=='__main__':unittest.main(verbosity=2)
