"""Native acceptance gates for the optional CPPM2 flat-array game."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,os,re,shutil,signal,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('native_runtime',ROOT/'verify-pointer-projects.py');runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
run=runtime.run;FLAGS=runtime.FLAGS;SANITIZERS=runtime.SANITIZERS
FOLDERS=['CPPM2-Tic-Tac-Toe','CPPM2-Tic-Tac-Toe-Starter'];TASKS=['applyMove','checkwin','board']

def inputRun(binary,cwd,text=''):
 command=[str(binary)];process=subprocess.Popen(command,cwd=cwd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1'})
 print(json.dumps({'event':'start','parentTaskId':'cpp-level2-tictactoe-source','cwd':str(cwd),'command':command,'pid':process.pid,'parentPid':os.getpid(),'time':datetime.now(timezone.utc).isoformat(),'timeoutSeconds':5}),flush=True)
 try:output,errors=process.communicate(text,timeout=5)
 except BaseException:
  if process.poll() is None:
   os.killpg(process.pid,signal.SIGTERM)
   try:process.communicate(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.communicate()
   print(json.dumps({'event':'child-process-group-cleanup','parentTaskId':'cpp-level2-tictactoe-source','pid':process.pid}),flush=True)
  raise
 finally:print(json.dumps({'event':'end','parentTaskId':'cpp-level2-tictactoe-source','cwd':str(cwd),'command':command,'pid':process.pid,'time':datetime.now(timezone.utc).isoformat(),'exitCode':process.poll()}),flush=True)
 assert process.returncode==0 and not errors,(process.returncode,output,errors)
 return output

CASES=r'''
#undef main
#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <climits>
#include <queue>
#include <set>
#include <sstream>
#include <utility>
const unsigned lines[8] = {7, 56, 448, 73, 146, 292, 273, 84};
int classify(unsigned x, unsigned o) {
    for (const unsigned mask : lines) if ((x & mask) == mask || (o & mask) == mask) return 1;
    return (x | o) == 511 ? 0 : -1;
}
void restore(unsigned x, unsigned o) {
    square[0] = 'o';
    for (int bit = 0; bit < 9; ++bit) {
        const unsigned mask = 1u << bit;
        square[bit + 1] = x & mask ? 'X' : o & mask ? 'O' : static_cast<char>('1' + bit);
    }
}
std::array<char, 10> snapshot() {
    std::array<char, 10> result{};
    std::copy(square, square + 10, result.begin());
    return result;
}
int main() {
    std::queue<std::pair<unsigned, unsigned>> pending;
    std::set<unsigned> visited;
    std::array<unsigned, 8> xWins{}, oWins{};
    std::size_t draws = 0;
    pending.push({0, 0});
    while (!pending.empty()) {
        const auto [x, o] = pending.front(); pending.pop();
        if (!visited.insert(x | (o << 9)).second) continue;
        restore(x, o);
        const auto before = snapshot();
        const int status = classify(x, o);
        assert(checkwin() == status && snapshot() == before);
        std::ostringstream rendered;
        auto* prior = std::cout.rdbuf(rendered.rdbuf());
        board();
        std::cout.rdbuf(prior);
        assert(snapshot() == before && !rendered.str().empty());
        if (status == 0) ++draws;
        for (std::size_t line = 0; line < 8; ++line) {
            if ((x & lines[line]) == lines[line]) ++xWins[line];
            if ((o & lines[line]) == lines[line]) ++oWins[line];
        }
        for (const int choice : {INT_MIN, -1, 0, 10, INT_MAX}) {
            assert(!applyMove(choice, 'X') && snapshot() == before);
        }
        for (const char mark : {'?', '\0'}) assert(!applyMove(1, mark) && snapshot() == before);
        const bool xTurn = std::popcount(x) == std::popcount(o);
        for (int bit = 0; bit < 9; ++bit) {
            restore(x, o);
            const unsigned mask = 1u << bit;
            const bool accepted = status == -1 && ((x | o) & mask) == 0;
            assert(applyMove(bit + 1, xTurn ? 'X' : 'O') == accepted);
            auto after = before;
            if (accepted) {
                after[static_cast<std::size_t>(bit + 1)] = xTurn ? 'X' : 'O';
                pending.push({xTurn ? x | mask : x, xTurn ? o : o | mask});
            }
            assert(snapshot() == after);
        }
    }
    assert(visited.size() > 5000 && draws > 0);
    for (std::size_t line = 0; line < 8; ++line) assert(xWins[line] > 0 && oWins[line] > 0);
    std::cout << "Verified " << visited.size() << " reachable boards, all eight lines for both players, terminal rejection and single-cell mutation.\n";
    return 0;
}
'''

def completedLearner():
 reference=(ROOT/FOLDERS[0]/'main.cpp').read_text();learner=(ROOT/FOLDERS[1]/'main.cpp').read_text()
 for task in TASKS:
  pattern=r'// TASK '+task+r'\n[\s\S]*?\n// END TASK '+task
  learner,count=re.subn(pattern,lambda match:re.search(pattern,reference).group(),learner);assert count==1
 return learner

class TicTacToe(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.temporary=tempfile.TemporaryDirectory(prefix='cpp-tictactoe-gate-');cls.work=Path(cls.temporary.name)
 @classmethod
 def tearDownClass(cls):cls.temporary.cleanup()
 def compile(self,source,label,flags=()):
  folder=self.work/label;folder.mkdir(exist_ok=True);(folder/'main.cpp').write_text(source);binary=folder/'program'
  run(['clang++',*FLAGS,*flags,'main.cpp','-o',str(binary)],folder);return binary,folder
 def test_roles_briefs_and_two_make_workflows(self):
  reference=ROOT/FOLDERS[0];starter=ROOT/FOLDERS[1]
  self.assertEqual((reference/'README.md').read_bytes(),(starter/'README.md').read_bytes());self.assertTrue((reference/'REFLECTION.md').is_file());self.assertFalse((starter/'REFLECTION.md').exists());self.assertEqual((starter/'main.cpp').read_text().count('throw UnfinishedTask'),3)
  for folder in FOLDERS:
   target=self.work/folder;target.mkdir()
   for name in ['main.cpp','Makefile']:shutil.copyfile(ROOT/folder/name,target/name)
   self.assertEqual([p.name for p in target.glob('*.cpp')],['main.cpp']);run(['make','main','main-debug'],target)
   normal=inputRun(target/'main',target);debug=inputRun(target/'main-debug',target);self.assertEqual(normal,debug)
   self.assertEqual(normal.count('Learner tasks:'),1 if folder.endswith('-Starter') else 0)
   if not folder.endswith('-Starter'):self.assertEqual(normal.count('input closed'),1)
   run(['make','clean'],target);self.assertFalse((target/'main').exists());self.assertFalse((target/'main-debug').exists());self.assertFalse(list(target.glob('*.dSYM')))
 def test_reference_and_completed_learner_input_contracts(self):
  for role,source in [('reference',(ROOT/FOLDERS[0]/'main.cpp').read_text()),('completed-learner',completedLearner())]:
   binary,cwd=self.compile(source,role+'-input',SANITIZERS)
   for text in ['', '1\n']:
    out=inputRun(binary,cwd,text);self.assertEqual(out.count('input closed'),1);self.assertNotIn('Invalid move',out);self.assertNotIn('wins!',out);self.assertNotIn('Game draw',out)
   for moves,winner in [([1,4,2,5,3],1),([1,4,2,5,9,6],2),([1,2,5,3,9],1)]:
    out=inputRun(binary,cwd,'\n'.join(map(str,moves+[1,2]))+'\n');self.assertEqual(out.count(f'Player {winner} wins!'),1);self.assertEqual(len(re.findall(r'Player [12], enter a number:',out)),len(moves));self.assertNotIn('input closed',out)
   out=inputRun(binary,cwd,'1\n2\n3\n5\n4\n6\n8\n7\n9\n1\n');self.assertEqual(out.count('Game draw'),1);self.assertEqual(len(re.findall(r'Player [12], enter a number:',out)),9);self.assertNotIn('wins!',out)
   bad=['','cat','0','10','-1','1x','1 2','+1','01','1.0'];out=inputRun(binary,cwd,'\n'.join(bad+[' \t1 \r','1','4','2','5','3'])+'\n')
   self.assertEqual(out.count('Invalid move'),len(bad)+1);self.assertIn('Player 1 wins!',out)
   self.assertEqual(re.findall(r'Player ([12]), enter a number:',out),['1']*(len(bad)+1)+['2','2','1','2','1'])
 def test_all_reachable_states_against_independent_bitmasks(self):
  for role,source in [('reference',(ROOT/FOLDERS[0]/'main.cpp').read_text()),('completed-learner',completedLearner())]:
   binary,cwd=self.compile('#define main providedMain\n'+source+CASES,role+'-states',SANITIZERS);out=inputRun(binary,cwd);self.assertRegex(out,r'Verified \d+ reachable boards, all eight lines')
   print(json.dumps({'event':'verified-game-state-space','role':role,'result':out.strip()}),flush=True)
 def test_two_independent_cmake_targets(self):
  build=self.work/'cmake';run(['cmake','-S',str(ROOT),'-B',str(build),'-DCMAKE_CXX_COMPILER=clang++'],self.work)
  targets=['CPPM2_Tic_Tac_Toe_Starter','CPPM2_Tic_Tac_Toe_Reference'];run(['cmake','--build',str(build),'--target',*targets,'--parallel','1'],self.work,timeout=120)
  for target in targets:inputRun(build/target,self.work)

if __name__=='__main__':unittest.main(verbosity=2)
