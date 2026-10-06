#include "profile.h"

#include <iostream>
#include <limits>
#include <memory>

namespace profile_detail {
constexpr auto maxElements = std::numeric_limits<std::size_t>::max() / sizeof(Post);

std::size_t nextCapacity(const std::size_t current) {
    if (current >= maxElements) throw std::length_error("Profile capacity exhausted");
    if (current == 0) return DEFAULT_SIZE;
    return current > maxElements / 2 ? maxElements : current * 2;
}

void validate(const Post& value) {
    if (value.caption.find_first_not_of(" \t\r\n\f\v") == std::string::npos) {
        throw std::invalid_argument("A post needs a nonempty caption");
    }
    if (value.hearts < 0) throw std::invalid_argument("Hearts must be nonnegative");
}

std::unique_ptr<Post[]> copiedBuffer(const Post* source, const std::size_t size,
                                     const std::size_t capacity) {
    if (size > capacity || capacity > maxElements) {
        throw std::length_error("Invalid Profile capacity");
    }
    std::unique_ptr<Post[]> result(capacity == 0 ? nullptr : new Post[capacity]);
    for (std::size_t i = 0; i < size; ++i) result[i] = source[i];
    return result;
}
} // namespace profile_detail

Profile::Profile() : mySize(0), maxSize(0), myPosts(nullptr) { resize(DEFAULT_SIZE); }

Profile::Profile(const Profile& other) : mySize(0), maxSize(0), myPosts(nullptr) {
    auto replacement = profile_detail::copiedBuffer(other.myPosts, other.mySize, other.maxSize);
    myPosts = replacement.release();
    mySize = other.mySize;
    maxSize = other.maxSize;
}

Profile& Profile::operator=(const Profile& other) {
    if (this == &other) return *this;
    auto replacement = profile_detail::copiedBuffer(other.myPosts, other.mySize, other.maxSize);
    delete[] myPosts;
    myPosts = replacement.release();
    mySize = other.mySize;
    maxSize = other.maxSize;
    return *this;
}

Profile::Profile(Profile&& other) noexcept
    : mySize(other.mySize), maxSize(other.maxSize), myPosts(other.myPosts) {
    other.mySize = other.maxSize = 0;
    other.myPosts = nullptr;
}

Profile& Profile::operator=(Profile&& other) noexcept {
    if (this == &other) return *this;
    delete[] myPosts;
    myPosts = other.myPosts;
    mySize = other.mySize;
    maxSize = other.maxSize;
    other.mySize = other.maxSize = 0;
    other.myPosts = nullptr;
    return *this;
}

Profile::~Profile() { delete[] myPosts; }

void Profile::resize(const std::size_t newCapacity) {
    if (newCapacity == 0) throw std::length_error("Profile capacity must be positive");
    auto replacement = profile_detail::copiedBuffer(myPosts, mySize, newCapacity);
    delete[] myPosts;
    myPosts = replacement.release();
    maxSize = newCapacity;
}

void Profile::addPost(const Post& newPost) {
    profile_detail::validate(newPost);
    if (mySize == maxSize) {
        const auto capacity = profile_detail::nextCapacity(maxSize);
        auto replacement = profile_detail::copiedBuffer(myPosts, mySize, capacity);
        // The new record can throw too. Commit only after all copies succeed.
        replacement[mySize] = newPost;
        delete[] myPosts;
        myPosts = replacement.release();
        maxSize = capacity;
    } else {
        // A failed assignment into an unused slot cannot change logical posts.
        myPosts[mySize] = newPost;
    }
    ++mySize;
}

void Profile::printPost(const std::size_t postIndex) const {
    if (!validPostIndex(postIndex)) {
        std::cout << "Error! This would have attempted to print a post that "
                     "doesn't exist in the array.\n";
        return;
    }
    const Post* observer = &myPosts[postIndex];
    std::cout << "Post number: " << postIndex + 1 << '\n'
              << "Post caption: " << observer->caption << '\n'
              << "Post hearts: " << observer->hearts << "\n\n";
}

void Profile::printPosts() const {
    std::cout << "Now printing out the current profile: \n";
    for (std::size_t i = 0; i < mySize; ++i) printPost(i);
    std::cout << "\n\n";
}

int Profile::sumHearts() const {
    int total = 0;
    for (std::size_t i = 0; i < mySize; ++i) {
        if (myPosts[i].hearts > std::numeric_limits<int>::max() - total) {
            throw std::overflow_error("Total hearts exceed the int range");
        }
        total += myPosts[i].hearts;
    }
    return total;
}

void Profile::fillProfile() {
    if (mySize == 0) {
        std::cout << "There was no last post to duplicate!\n";
        return;
    }
    if (mySize < maxSize) {
        auto replacement = profile_detail::copiedBuffer(myPosts, mySize, maxSize);
        for (std::size_t i = mySize; i < maxSize; ++i) replacement[i] = myPosts[mySize - 1];
        delete[] myPosts;
        myPosts = replacement.release();
        mySize = maxSize;
    }
    // Output happens after the mutation commits. An output failure is not rollback.
    const Post& lastPost = myPosts[mySize - 1];
    std::cout << "Filled remaining posts with a post that contained:\nCaption: "
              << lastPost.caption << "\nHearts: " << lastPost.hearts << '\n'
              << "Your profile now contains: " << mySize << " posts!\n";
    printPosts();
}

void Profile::removePost(const std::size_t index) {
    if (!validPostIndex(index)) {
        std::cout << "Error! This would have attempted to remove a post that "
                     "doesn't exist in the array.\n";
        return;
    }
    auto replacement = profile_detail::copiedBuffer(nullptr, 0, maxSize);
    for (std::size_t from = 0, to = 0; from < mySize; ++from) {
        if (from != index) replacement[to++] = myPosts[from];
    }
    delete[] myPosts;
    myPosts = replacement.release();
    --mySize;
}

void Profile::addHearts(const std::size_t postIndex, const int numHearts) {
    if (!validPostIndex(postIndex)) {
        std::cout << "Error! This would have attempted to add hearts to a post "
                     "that doesn't exist in the array.\n";
        return;
    }
    const int current = myPosts[postIndex].hearts;
    if (numHearts < -current) throw std::invalid_argument("Hearts cannot become negative");
    if (numHearts > 0 && current > std::numeric_limits<int>::max() - numHearts) {
        throw std::overflow_error("Post hearts exceed the int range");
    }
    myPosts[postIndex].hearts += numHearts;
}

bool Profile::validPostIndex(const std::size_t index) const { return index < mySize; }
