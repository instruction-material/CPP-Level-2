"""Independent Profile Posts record, ownership, failure, arithmetic and menu gates."""
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
REFERENCE = "CPPM5-Profile-Posts"
STARTER = REFERENCE + "-Starter"
FILES = ["profile.h", "profile.cpp", "main.cpp", "Makefile", "README.md"]

OBSERVER = r'''
#define main providedMain
#include "main.cpp"
#undef main
int main() {
    try {
        Profile profile;
        const int status = runProfileMenu(profile, std::cin);
        profile.printPosts();
        return status;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
'''

CASES = r'''
#include "profile.cpp"
#define main providedMain
#include "main.cpp"
#undef main
#include <cassert>
#include <cstdlib>
#include <new>
#include <sstream>
#include <type_traits>
#include <utility>
#include <vector>

static int live = 0, liveArrays = 0, failAfter = -1;
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
struct Quiet {
    Sink sink;
    std::streambuf* prior;
    Quiet() : prior(std::cout.rdbuf(&sink)) {}
    ~Quiet() { std::cout.rdbuf(prior); }
};
template<class Exception, class Task>
void rejected(Task task) {
    bool caught = false;
    try { task(); } catch (const Exception&) { caught = true; }
    assert(caught);
}
std::string rows(const std::vector<Post>& values) {
    std::ostringstream out;
    for (std::size_t i = 0; i < values.size(); ++i) {
        out << "Post number: " << i + 1 << '\n'
            << "Post caption: " << values[i].caption << '\n'
            << "Post hearts: " << values[i].hearts << "\n\n";
    }
    return out.str();
}
void expect(const Profile& profile, const std::vector<Post>& values) {
    { Capture out; profile.printPosts();
      assert(out.text.str() == "Now printing out the current profile: \n" + rows(values) + "\n\n"); }
    for (std::size_t i = 0; i < values.size(); ++i) {
        Capture out; profile.printPost(i);
        // Numbering is part of the public output, not a private storage oracle.
        auto expected = rows({values[i]});
        expected.replace(13, 1, std::to_string(i + 1));
        assert(out.text.str() == expected);
    }
    for (const auto index : {values.size(), std::numeric_limits<std::size_t>::max()}) {
        Capture out; profile.printPost(index);
        assert(out.text.str() == "Error! This would have attempted to print a post that doesn't exist in the array.\n");
    }
    long long total = 0;
    for (const auto& value : values) total += value.hearts;
    if (total <= std::numeric_limits<int>::max()) assert(profile.sumHearts() == total);
    else rejected<std::overflow_error>([&] { (void)profile.sumHearts(); });
}
void fill(Profile& profile, const std::vector<Post>& values) {
    for (const auto& value : values) profile.addPost(value);
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
        if (std::string_view(data, static_cast<std::size_t>(size)).find("Filled remaining") != std::string_view::npos) {
            throw std::runtime_error("Acknowledgement failed");
        }
        return size;
    }
    int_type overflow(int_type value) override { return traits_type::not_eof(value); }
};

int main() {
    static_assert(std::is_nothrow_move_constructible_v<Profile>);
    static_assert(std::is_nothrow_move_assignable_v<Profile>);
    assert(Post{}.hearts == 0);
    int count = 17;
    for (const std::string token : {"", " ", "-1", "nan", "inf", "1e3", "1.0", "1x", "1 2", "++1", "+-1", "999999999999999999999"}) {
        assert(!parseHeartCount(token, count) && count == 17);
    }
    assert(parseHeartCount(" +0 \r", count) && count == 0);
    assert(parseHeartCount(std::to_string(std::numeric_limits<int>::max()), count));
    assert(parseHeartCount(std::to_string(std::numeric_limits<int>::min()), count, true));
    assert(count == std::numeric_limits<int>::min());
    for (const std::string token : {"+-1", "++1", "-+1", "--1", "1.5", "2x"}) {
        assert(!parseHeartCount(token, count, true) && count == std::numeric_limits<int>::min());
    }
    std::size_t number = 7;
    for (const std::string token : {"", "0", "-1", "1.5", "1x", "1 2", "++1", "+-1", "99999999999999999999999999999"}) {
        assert(!parsePostNumber(token, number) && number == 7);
    }
    assert(parsePostNumber(" +1 ", number) && number == 1);
    assert(parsePostNumber(std::to_string(std::numeric_limits<std::size_t>::max()), number));

    std::vector<Post> values;
    for (int i = 0; i < 5; ++i) values.push_back({std::string(90, 'a' + i), i * 3});
    const Post extra{std::string(90, 'x'), 9};
    const std::vector<Post> old{{std::string(90, 'z'), 42}};
    { Profile warm; fill(warm, old); expect(warm, old); }
    const int baseline = live, baselineArrays = liveArrays;
    {
        Profile profile; expect(profile, {});
        { Capture out; profile.fillProfile(); assert(out.text.str() == "There was no last post to duplicate!\n"); }
        std::vector<Post> many;
        for (int i = 0; i < 201; ++i) {
            many.push_back({"post " + std::to_string(i), i});
            profile.addPost(many.back());
        }
        expect(profile, many);
        for (const Post& invalid : {Post{}, Post{" \t", 1}, Post{"bad", -1}}) {
            rejected<std::invalid_argument>([&] { profile.addPost(invalid); }); expect(profile, many);
        }
        Profile copied(profile); copied.addPost(extra); expect(profile, many);
        auto changed = many; changed.push_back(extra); expect(copied, changed);
        copied.addHearts(0, 1); changed[0].hearts += 1; expect(copied, changed); expect(profile, many);
        Profile assigned; fill(assigned, old); assigned = profile; expect(assigned, many);
        auto* alias = &assigned;
        assigned = *alias; assigned = std::move(*alias); expect(assigned, many);
        failAfter = 0; Profile moved(std::move(profile));
        assert(failAfter == 0); failAfter = -1;
        expect(moved, many); expect(profile, {});
        Profile emptyCopy(profile); emptyCopy.addPost(extra); expect(emptyCopy, {extra});
        assigned = profile; expect(assigned, {}); assigned.addPost(old[0]); expect(assigned, old);
        profile.addPost(extra); expect(profile, {extra});
        Profile destination; fill(destination, old);
        failAfter = 0; destination = std::move(moved);
        assert(failAfter == 0); failAfter = -1;
        expect(destination, many); expect(moved, {});
        fill(moved, values); moved.addPost(extra);
        auto reused = values; reused.push_back(extra); expect(moved, reused);
    }
    assert(live == baseline && liveArrays == baselineArrays);
    {
        Profile profile; profile.addPost({"maximum", std::numeric_limits<int>::max()});
        rejected<std::overflow_error>([&] { profile.addHearts(0, 1); });
        rejected<std::invalid_argument>([&] { profile.addHearts(0, std::numeric_limits<int>::min()); });
        expect(profile, {{"maximum", std::numeric_limits<int>::max()}});
        profile.addPost({"one", 1}); expect(profile, {{"maximum", std::numeric_limits<int>::max()}, {"one", 1}});
        profile.addHearts(0, -std::numeric_limits<int>::max()); expect(profile, {{"maximum", 0}, {"one", 1}});
        rejected<std::invalid_argument>([&] { profile.addHearts(0, -1); });
        profile.addHearts(0, std::numeric_limits<int>::max());
        rejected<std::overflow_error>([&] { profile.addHearts(1, std::numeric_limits<int>::max()); });
        { Capture out;
          profile.addHearts(2, std::numeric_limits<int>::min());
          profile.removePost(std::numeric_limits<std::size_t>::max()); }
        expect(profile, {{"maximum", std::numeric_limits<int>::max()}, {"one", 1}});
    }
    const std::vector<Post> shortValues{{"a", 1}, {"b", 2}, {"c", 3}};
    for (std::size_t removed = 0; removed < 3; ++removed) {
        Profile profile; fill(profile, shortValues); profile.removePost(removed);
        auto after = shortValues; after.erase(after.begin() + static_cast<std::ptrdiff_t>(removed));
        expect(profile, after);
    }
    {
        Profile profile; profile.addPost(extra); profile.removePost(0); expect(profile, {});
        profile.addPost(extra); expect(profile, {extra});
        Profile partial; fill(partial, shortValues);
        { Capture out; partial.fillProfile(); }
        auto after = shortValues; after.push_back(shortValues.back()); after.push_back(shortValues.back());
        expect(partial, after);
        failAfter = 0; { Quiet out; partial.fillProfile(); }
        assert(failAfter == 0); failAfter = -1; expect(partial, after);
        partial.addPost(extra); after.push_back(extra);
        { Capture out; partial.fillProfile(); }
        while (after.size() < 10) after.push_back(extra);
        expect(partial, after);
    }
    assert(live == baseline && liveArrays == baselineArrays);
    // Each operation reaches array acquisition and later string allocations.
    int failures[6]{}, successes[6]{};
    for (int operation = 0; operation < 6; ++operation) {
        for (int point = 0; point < 14; ++point) {
            {
                Profile source; Profile destination; fill(destination, old);
                auto beforeValues = values;
                if (operation == 3) beforeValues = {values[0]};
                if (operation == 5) beforeValues = {values[0], values[1]};
                fill(source, beforeValues);
                const int before = live, beforeArrays = liveArrays;
                bool failed = false;
                { Quiet out;
                  failAfter = point;
                  try {
                    if (operation == 0) { Profile copy(source); failAfter = -1; expect(copy, beforeValues); }
                    else if (operation == 1) destination = source;
                    else if (operation == 2 || operation == 3) source.addPost(extra);
                    else if (operation == 4) source.removePost(1);
                    else source.fillProfile();
                  } catch (const std::bad_alloc&) { failed = true; }
                  failAfter = -1;
                }
                if (failed) {
                    ++failures[operation];
                    assert(live == before && liveArrays == beforeArrays);
                    expect(source, beforeValues); expect(destination, old);
                } else {
                    ++successes[operation];
                    auto after = beforeValues;
                    if (operation == 1) expect(destination, beforeValues);
                    else expect(destination, old);
                    if (operation == 2 || operation == 3) after.push_back(extra);
                    else if (operation == 4) after.erase(after.begin() + 1);
                    else if (operation == 5) while (after.size() < 5) after.push_back(beforeValues.back());
                    expect(source, after);
                }
            }
            assert(live == baseline && liveArrays == baselineArrays);
        }
    }
    for (int operation = 0; operation < 6; ++operation) {
        assert(failures[operation] >= (operation == 3 ? 1 : 5));
        assert(successes[operation] > 0);
    }
    failAfter = 0; rejected<std::bad_alloc>([] { Profile profile; }); failAfter = -1;
    assert(live == baseline && liveArrays == baselineArrays);
    {
        Profile profile; fill(profile, shortValues);
        FailingAcknowledgement failed;
        auto* prior = std::cout.rdbuf(&failed);
        std::cout.exceptions(std::ios::badbit | std::ios::failbit);
        rejected<std::exception>([&] { profile.fillProfile(); });
        std::cout.exceptions(std::ios::goodbit); std::cout.clear(); std::cout.rdbuf(prior);
        auto after = shortValues; after.push_back(shortValues.back()); after.push_back(shortValues.back());
        expect(profile, after);
    }
    for (const std::string text : {"", "add\n", "add\nnew caption\n", "remove\n", "view\n",
                                  "hearts\n", "hearts\n1\n", "add\n!quit\n", "add\nnew\n!quit\n",
                                  "remove\n!quit\n", "view\n!quit\n", "hearts\n1\n!quit\n"}) {
        Profile profile; fill(profile, shortValues); std::istringstream input(text);
        { Capture out; assert(runProfileMenu(profile, input) == 0); } expect(profile, shortValues);
    }
    for (const bool exceptions : {false, true}) {
        for (const std::string prefix : {"", "add\n", "add\nnew caption\n", "remove\n", "view\n", "hearts\n1\n"}) {
            Profile profile; fill(profile, shortValues); ThrowingInput buffer(prefix); std::istream input(&buffer);
            if (exceptions) input.exceptions(std::ios::badbit | std::ios::failbit);
            Capture errors(std::cerr);
            { Capture out; assert(runProfileMenu(profile, input) == 1); }
            assert(errors.text.str() == "Input could not be read.\n"); expect(profile, shortValues);
        }
        Profile profile; fill(profile, shortValues); std::istringstream input("add\nnew\n");
        if (exceptions) input.exceptions(std::ios::badbit | std::ios::failbit);
        { Capture out; assert(runProfileMenu(profile, input) == 0); } expect(profile, shortValues);
    }
    const auto bound = std::numeric_limits<std::size_t>::max() / sizeof(Post);
    assert(profile_detail::nextCapacity(0) == DEFAULT_SIZE);
    for (const auto value : {std::size_t{5}, bound / 2, bound / 2 + 1, bound - 1}) {
        const auto grown = profile_detail::nextCapacity(value); assert(grown > value && grown <= bound);
    }
    rejected<std::length_error>([&] { (void)profile_detail::nextCapacity(bound); });
    rejected<std::length_error>([&] { (void)profile_detail::nextCapacity(bound + 1); });
    std::cout << "Verified Profile records, both copies/moves, growth, heart bounds, removal, fill, input and injected cleanup.\n";
}
'''


class ProfileAcceptance(unittest.TestCase):
    def test_pack_roles_builds_and_menu(self):
        self.assertEqual((ROOT / REFERENCE / "README.md").read_bytes(), (ROOT / STARTER / "README.md").read_bytes())
        self.assertEqual((ROOT / REFERENCE / "profile.h").read_bytes(), (ROOT / STARTER / "profile.h").read_bytes())
        self.assertIn("TODO", (ROOT / STARTER / "profile.cpp").read_text())
        self.assertNotEqual((ROOT / REFERENCE / "profile.cpp").read_bytes(), (ROOT / STARTER / "profile.cpp").read_bytes())
        cases = [
            ("", []), ("!quit\n", []), ("print\n!quit\n", []),
            ("add\nhello world\n30\nprint\n!quit\n", [("hello world", 30)]),
            ("add\n\n hello world \n-1\nnan\n1.5\n1x\n1 2\n2147483648\n+0\nprint\n!quit\n", [("hello world", 0)]),
            ("add\na\n30\nadd\nb\n10\nremove\n1\nprint\n!quit\n", [("b", 10)]),
            ("add\na\n30\nremove\n1\nprint\n!quit\n", []),
            ("add\na\n30\nhearts\n1\n-30\nprint\n!quit\n", [("a", 0)]),
            ("add\na\n0\nhearts\n1\n-2147483648\nhearts\n1\n2147483647\nhearts\n1\n1\nprint\n!quit\n", [("a", 2147483647)]),
            ("add\na\n2147483647\nadd\nb\n1\nsum\nprint\n!quit\n", [("a", 2147483647), ("b", 1)]),
            ("add\na\n30\nremove\n0\n-1\n1.5\n1x\n99999999999999999999999\n999\nprint\n!quit\n", [("a", 30)]),
            ("unknown\nadd words\nview\n1\nfill\nprint\n!quit\n", []),
            ("add\n", []), ("add\nnew caption\n", []), ("remove\n", []), ("hearts\n", []),
            ("add\n!quit\n", []), ("add\nnew\n!quit\n", []),
            ("add\na\n30\nhearts\n1\n!quit\nprint\n", [("a", 30)]),
            ("add\na\n3\nfill\nprint\n!quit\n", [("a", 3)] * 5),
            ("add\na\n3\nview\n+1\nprint", [("a", 3)]),
        ]
        for folder in [REFERENCE, STARTER]:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory(prefix="cppm5-profile-pack-") as temporary:
                work = Path(temporary)
                for name in FILES: shutil.copyfile(ROOT / folder / name, work / name)
                runtime.run(["make", "main", "main-debug"], work)
                rebuild = runtime.run(["make", "-n", "-W", "profile.h", "main"], work)
                self.assertIn("profile.cpp main.cpp", rebuild.stdout)
                if folder == REFERENCE:
                    (work / "observer.cpp").write_text(OBSERVER)
                    for label, flags in [("main", []), ("main-debug", runtime.SANITIZERS)]:
                        runtime.run(["clang++", *runtime.FLAGS, *flags, "profile.cpp", "observer.cpp", "-o", label + "-observer"], work)
                for name in ["main", "main-debug"]:
                    for text, expected in cases:
                        result = io_runtime.input_run(work / name, work, text)
                        self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")
                        if folder == REFERENCE:
                            # The independent observer prints after the exact menu returns,
                            # including EOF/quit before any ordinary print command.
                            observed = io_runtime.input_run(work / (name + "-observer"), work, text)
                            self.assertEqual(observed.returncode, 0); self.assertEqual(observed.stderr, "")
                            marker = observed.stdout.rfind("Now printing out the current profile:")
                            self.assertGreaterEqual(marker, 0)
                            lines = observed.stdout[marker:].splitlines()
                            captions = [line.removeprefix("Post caption: ") for line in lines if line.startswith("Post caption: ")]
                            hearts = [int(line.removeprefix("Post hearts: ")) for line in lines if line.startswith("Post hearts: ")]
                            self.assertEqual(list(zip(captions, hearts)), expected)
                            if "2147483647\nadd\nb\n1\nsum" in text:
                                self.assertIn("Rejected: Total hearts exceed the int range", result.stdout)
                        else:
                            self.assertIn("Unfinished learner task: Profile menu", result.stdout)
                            self.assertNotIn("Profile Posts:", result.stdout)
                    demo = io_runtime.input_run(work / name, work, "", ["--demo"])
                    self.assertEqual(demo.returncode, 0); self.assertEqual(demo.stderr, "")
                    if folder == REFERENCE:
                        final = demo.stdout[demo.stdout.rfind("Now printing out the current profile:"):]
                        self.assertEqual(final.count("Post number:"), 7)
                        self.assertEqual([int(line[13:]) for line in final.splitlines() if line.startswith("Post hearts: ")], [40, 20, 20, 20, 20, 20, 20])
                        self.assertIn("Incredible coders come from all backgrounds!", demo.stdout)
                    else:
                        self.assertIn("Unfinished learner task: Profile append", demo.stdout)
                    for arguments in [["--unknown"], ["--demo", "--demo"]]:
                        bad = io_runtime.input_run(work / name, work, "", arguments)
                        self.assertEqual(bad.returncode, 2); self.assertEqual(bad.stderr, "Usage: main [--demo]\n")
                runtime.run(["make", "clean"], work)
                for name in ["main", "main-debug", "main.dSYM", "main-debug.dSYM"]:
                    self.assertFalse((work / name).exists())

    def test_independent_native_contracts(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-profile-contract-") as temporary:
            work = Path(temporary)
            for name in FILES[:3]: shutil.copyfile(ROOT / REFERENCE / name, work / name)
            (work / "cases.cpp").write_text(CASES)
            for label, flags in [("ordinary", []), ("debug", runtime.SANITIZERS)]:
                binary = work / label
                runtime.run(["clang++", *runtime.FLAGS, *flags, "cases.cpp", "-o", str(binary)], work)
                result = runtime.run([str(binary)], work)
                self.assertEqual(result.stderr, "")
                self.assertIn("Verified Profile records", result.stdout)

    def test_independent_cmake_targets(self):
        with tempfile.TemporaryDirectory(prefix="cppm5-profile-cmake-") as temporary:
            work = Path(temporary)
            cmake = work / "build"
            runtime.run(["cmake", "-S", str(ROOT), "-B", str(cmake)], work)
            runtime.run(["cmake", "--build", str(cmake), "--target", "CPPM5_Profile_Posts_Starter", "CPPM5_Profile_Posts_Reference"], work)
            for name in ["CPPM5_Profile_Posts_Starter", "CPPM5_Profile_Posts_Reference"]:
                result = io_runtime.input_run(cmake / name, work, "!quit\n")
                self.assertEqual(result.returncode, 0); self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
