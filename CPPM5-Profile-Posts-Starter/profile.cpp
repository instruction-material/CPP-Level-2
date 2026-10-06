#include "profile.h"

Profile::Profile() : mySize(0), maxSize(0), myPosts(nullptr) {
    // TODO: establish the initial owned capacity. This placeholder is safe.
}
Profile::~Profile() { delete[] myPosts; }

void Profile::resize(const std::size_t newCapacity) {
    // TODO: retain a temporary owner until all potentially throwing copies succeed.
    (void)newCapacity; (void)maxSize;
    throw UnfinishedProfileTask("Unfinished learner task: Profile resize");
}
void Profile::addPost(const Post& newPost) {
    // TODO: validate, grow safely (including after move), then commit the record.
    (void)newPost;
    throw UnfinishedProfileTask("Unfinished learner task: Profile append");
}
void Profile::printPost(const std::size_t postIndex) const {
    // TODO: reject invalid zero-based indices; display one logical record.
    (void)postIndex;
    throw UnfinishedProfileTask("Unfinished learner task: Profile single display");
}
void Profile::printPosts() const {
    // TODO: display logical records only; an empty profile must be readable.
    throw UnfinishedProfileTask("Unfinished learner task: Profile display");
}
int Profile::sumHearts() const {
    // TODO: return a checked total without overflowing the int API.
    throw UnfinishedProfileTask("Unfinished learner task: Profile total");
}
void Profile::fillProfile() {
    // TODO: handle empty/full profiles and commit all duplicates together.
    throw UnfinishedProfileTask("Unfinished learner task: Profile duplication");
}
void Profile::removePost(const std::size_t index) {
    // TODO: retain order and preserve logical records if copying fails.
    (void)index;
    throw UnfinishedProfileTask("Unfinished learner task: Profile removal");
}
void Profile::addHearts(const std::size_t postIndex, const int numHearts) {
    // TODO: validate the index and check the final count before changing it.
    (void)postIndex; (void)numHearts;
    throw UnfinishedProfileTask("Unfinished learner task: Profile heart update");
}
bool Profile::validPostIndex(const std::size_t index) const {
    // TODO: distinguish logical size from capacity.
    (void)index; (void)mySize;
    throw UnfinishedProfileTask("Unfinished learner task: Profile index validation");
}
// TODO: define the four declared copy/move operations. Until then, drivers that
// call them cannot link. Keep moves noexcept; do not add shallow pointer copies.
