#ifndef PROFILE_H
#define PROFILE_H

#include <cstddef>
#include <stdexcept>
#include <string>

struct Post {
    std::string caption;
    int hearts = 0;
};

constexpr std::size_t DEFAULT_SIZE = 5;

class UnfinishedProfileTask : public std::logic_error {
public:
    using std::logic_error::logic_error;
};

class Profile {
private:
    std::size_t mySize;
    std::size_t maxSize;
    Post* myPosts;
    bool validPostIndex(std::size_t index) const;
    void resize(std::size_t newCapacity);
public:
    Profile();
    Profile(const Profile& other);
    Profile& operator=(const Profile& other);
    Profile(Profile&& other) noexcept;
    Profile& operator=(Profile&& other) noexcept;
    ~Profile();

    void addPost(const Post& newPost);
    void printPost(std::size_t postIndex) const;
    void printPosts() const;
    int sumHearts() const;
    void fillProfile();
    void removePost(std::size_t index);
    void addHearts(std::size_t postIndex, int numHearts);
};

#endif // PROFILE_H
