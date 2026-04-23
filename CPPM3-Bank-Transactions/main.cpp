#include <iostream>
#include <string>

void print(int arr[], int m, int n);

int main() {
  int balances[4][5];
  int amountRemaining;
  std::string name;
  int numTransactions = 3;
  int startDate;
  int amount;

  std::cout << "\nEnter your name: ";
  std::cin >> name;
  std::cout << "Enter your starting balance: ";
  std::cin >> amountRemaining;
  // Enter date in MMDDYYYY format
  std::cout << "Enter your starting date(MMDDYYYY): ";
  std::cin >> startDate;

  // initialize the first row of our grid to record the information
  balances[0][0] = 0;
  balances[0][1] = startDate;
  balances[0][2] = amountRemaining;
  balances[0][3] = 0;
  balances[0][4] = amountRemaining;

  std::cout << "\nHi " + name + ", you have " + std::to_string(numTransactions) + " remaining transactions. Please enter them below: " << std::endl << std::endl << std::endl;
  
  for (int i = 1; i < (numTransactions + 1); i++) {
    balances[i][2] = amountRemaining;

    // Enter date in MMDDYYYY format
    std::cout << "Date of transaction (MMDDYYYY): ";
    std::cin >> balances[i][1];

    // Enter amoung
    std::cout << "Amount of: ";
    std::cin >> amount;
    balances[i][3] = amount;

    balances[i][0] = i;
    amountRemaining += amount;
    balances[i][4] = amountRemaining;
    
    std::cout << "You have completed " << i << " transactions. You have " << numTransactions - i << " transactions remaining." << std::endl << std::endl;
  }

  std::cout << "Thank you for entering your transactions for this pay period! Your transaction breakdown is below: " << std::endl;

  print(*balances, (numTransactions + 1),5);

}

void print(int *arr, int m, int n) {
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      if (j == 0) {
        std::cout << "\nTRANSACTION NO: " << *((arr + i*n) + j);
      } else if (j == 1) {
        std::cout << "\n DATE: " << *((arr + i*n) + j);
      } else if (j == 2) {
        std::cout << "\n STARTING BALANCE: " << *((arr + i*n) + j);
      } else if (j == 3) {
        std::cout << "\n AMOUNT: " << *((arr + i*n) + j);
      } else if (j == 4) {
        std::cout << "\n ENDING BALANCE: " << *((arr + i*n) + j);
      }
    }
    std::cout << " " << std::endl;
  }
}