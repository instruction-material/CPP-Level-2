#include <iostream>
#include <string>

struct ScoreCard {
    std::string owner;
    int score;
};

void printCard(const std::string& label, const ScoreCard& card) {
    std::cout << label << " -> " << card.owner << ": " << card.score << " at "
              << static_cast<const void*>(&card) << std::endl;
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
    // Named return value optimization may construct localCard as the result.
    // Either way, the returned value remains valid in the caller.
    return localCard;
}

int main() {
    ScoreCard card{"Taylor", 70};
    printCard("Original card", card);

    std::cout << "\nPass by value creates an independent copy:" << std::endl;
    updateCopy(card);
    printCard("After updateCopy", card);

    std::cout << "\nPass by reference mutates the caller's object:"
              << std::endl;
    updateReference(card);
    printCard("After updateReference", card);

    std::cout << "\nConst reference observes without ownership or mutation:"
              << std::endl;
    observeConstReference(card);

    std::cout << "\nReturn by value gives the caller a valid result:"
              << std::endl;
    ScoreCard bonus = makeBonusCard("Morgan");
    printCard("Returned bonus card", bonus);

    return 0;
}

// TODO 1: Predict caller/copy values and alias relationships before running.
// TODO 2: Predict reference mutation and the const observer result.
// TODO 3: Draw returned-value lifetime and permitted address relationships.
// TODO 4: Explain the effect of disabling named return value optimization.
