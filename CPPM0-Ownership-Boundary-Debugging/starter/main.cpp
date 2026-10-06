#include <cstddef>
#include <iostream>
#include <string>
#include <stdexcept>
#include <vector>

struct LogEntry {
  std::string message;
  int severity;
};

void printEntry(const std::string& label, const LogEntry& entry) {
  std::cout << label << " -> " << entry.message << " (severity " << entry.severity << ")"
            << " at " << static_cast<const void*>(&entry) << std::endl;
}

void editCopy(LogEntry entry) {
  entry.severity += 5;
  printEntry("Inside editCopy", entry);
}

void editCallerOwnedEntry(LogEntry& entry) {
  entry.severity += 5;
  printEntry("Inside editCallerOwnedEntry", entry);
}

const LogEntry& highestSeverity(const std::vector<LogEntry>& entries) {
  if (entries.empty()) {
    throw std::invalid_argument("highestSeverity requires a nonempty vector");
  }

  // TODO: Find the earliest maximum and return that vector element.
  throw std::logic_error("Implement highestSeverity before running selection");
}

int main() {
  std::vector<LogEntry> entries = {
      {"loaded configuration", 2},
      {"missing optional field", 4},
      {"failed validation", 8}
  };

  printEntry("Original first entry", entries[0]);

  std::cout << "\nA copy can change without changing the vector:" << std::endl;
  editCopy(entries[0]);
  printEntry("After editCopy", entries[0]);

  std::cout << "\nA reference changes the object owned by the vector:" << std::endl;
  editCallerOwnedEntry(entries[0]);
  printEntry("After editCallerOwnedEntry", entries[0]);

  std::cout << "\nA const reference observes an element while that element remains valid:" << std::endl;
  // Reallocation, erasure, clearing or destruction can invalidate this borrow.
  try {
    const LogEntry& worst = highestSeverity(entries);
    printEntry("Highest severity entry", worst);
  } catch (const std::logic_error& error) {
    std::cout << "Learner task: " << error.what() << std::endl;
  }

  return 0;
}

// TODO 1: Predict values before and after editing a copy.
// TODO 2: Predict the caller-owned entry after reference mutation.
// TODO 3: Name the selected entry owner and two invalidating operations.
