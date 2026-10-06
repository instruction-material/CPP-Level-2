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

  // Borrow the earliest maximum; do not mutate the vector.
  std::size_t highestIndex = 0;

  for (std::size_t i = 1; i < entries.size(); ++i) {
    if (entries[i].severity > entries[highestIndex].severity) {
      highestIndex = i;
    }
  }

  return entries[highestIndex];
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
  const LogEntry& worst = highestSeverity(entries);
  printEntry("Highest severity entry", worst);

  return 0;
}
