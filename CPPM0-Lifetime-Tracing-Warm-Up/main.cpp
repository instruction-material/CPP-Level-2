#include <iostream>
#include <string>

struct ScoreCard {
  std::string owner;
  int score;
};

void printCard(const std::string& label, const ScoreCard& card) {
  std::cout << label << " -> " << card.owner << ": " << card.score
            << " at " << static_cast<const void*>(&card) << std::endl;
}

void updateCopy(ScoreCard card) {
  card.score += 10;
  printCard("Inside updateCopy", card);
}

void updateReference(ScoreCard& card) {
  card.score += 10;
  printCard("Inside updateReference", card);
}

void observeConstReference(const ScoreCard& card) {
  printCard("Inside observeConstReference", card);
}

ScoreCard makeBonusCard(const std::string& owner) {
  ScoreCard localCard{owner, 100};
  printCard("Inside makeBonusCard", localCard);
  return localCard;
}

int main() {
  ScoreCard card{"Taylor", 70};
  printCard("Original card", card);

  std::cout << "\nPass by value creates an independent copy:" << std::endl;
  updateCopy(card);
  printCard("After updateCopy", card);

  std::cout << "\nPass by reference mutates the caller's object:" << std::endl;
  updateReference(card);
  printCard("After updateReference", card);

  std::cout << "\nConst reference observes without ownership or mutation:" << std::endl;
  observeConstReference(card);

  std::cout << "\nA returned value is a new object in the caller's scope:" << std::endl;
  ScoreCard bonus = makeBonusCard("Morgan");
  printCard("Returned bonus card", bonus);

  return 0;
}
