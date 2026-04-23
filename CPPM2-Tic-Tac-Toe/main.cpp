#include <iostream> 

char square[10] = {'o','1','2','3','4','5','6','7','8','9'};

int checkwin();
void board();

int main() {
	int player = 1, i = -1, choice;
  char mark;
  board();
  while (i == -1) {
    
    if (player % 2 == 1) {
      player = 1;
    } else {
      player = 2;
    }

    std::cout << "Player " << player << ", enter a number:  ";
    std::cin >> choice;

    if (player == 1) {
      mark = 'X';
    } else {
      mark = 'O';
    }

    if (choice == 1 && square[1] == '1') {
      square[1] = mark;
    } else if (choice == 2 && square[2] == '2') {
      square[2] = mark;
    } else if (choice == 3 && square[3] == '3') {
      square[3] = mark;
    } else if (choice == 4 && square[4] == '4') {
      square[4] = mark;
    } else if (choice == 5 && square[5] == '5') {
      square[5] = mark;
    } else if (choice == 6 && square[6] == '6') {
      square[6] = mark;
    } else if (choice == 7 && square[7] == '7') {
      square[7] = mark;
    } else if (choice == 8 && square[8] == '8') {
      square[8] = mark;
    } else if (choice == 9 && square[9] == '9') {
      square[9] = mark;
    } else {
      std::cout << "Invalid move\n";
      std::cin.ignore();
      //std::cin.get();
      continue;
    }

    board();
    i = checkwin();
    player++;
  }

  board();
  
  if (i == 1) {
    std::cout << "==>\a Player " << --player << " wins!";
  } else {
    std::cout << "==>\a Game draw";
  }

  std::cin.ignore();
  std::cin.get();
  return 0;
}

int checkwin() {
  if (square[1] == square[2] && square[2] == square[3]) return 1;
  else if (square[4] == square[5] && square[5] == square[6]) return 1;
  else if (square[7] == square[8] && square[8] == square[9]) return 1;
  else if (square[1] == square[4] && square[4] == square[7]) return 1;
  else if (square[2] == square[5] && square[5] == square[8]) return 1;
  else if (square[3] == square[6] && square[6] == square[9]) return 1;
  else if (square[1] == square[5] && square[5] == square[9]) return 1;
  else if (square[3] == square[5] && square[5] == square[7]) return 1;
  else if (square[1] != '1' && square[2] != '2' && square[3] != '3' && square[4] != '4' && square[5] != '5' && square[6] != '6' && square[7] != '7' && square[8] != '8' && square[9] != '9') return 0;
  else return -1;
}

// function for drawing the board
void board() {
  std::cout << "\n\n\tTic Tac Toe\n\n";

  std::cout << "Player 1 (X)  -  Player 2 (O)" << std::endl << std::endl;
  std::cout << std::endl;

  std::cout << "     |     |     " << std::endl;
  std::cout << "  " << square[1] << "  |  " << square[2] << "  |  " << square[3] << std::endl;

  std::cout << "_____|_____|_____" << std::endl;
  std::cout << "     |     |     " << std::endl;

  std::cout << "  " << square[4] << "  |  " << square[5] << "  |  " << square[6] << std::endl;

  std::cout << "_____|_____|_____" << std::endl;
  std::cout << "     |     |     " << std::endl;

  std::cout << "  " << square[7] << "  |  " << square[8] << "  |  " << square[9] << std::endl;

  std::cout << "     |     |     " << std::endl << std::endl;
}