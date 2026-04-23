#include "profile.h"
#include <iostream>

// our default constructor
Profile::Profile() : mySize(0), maxSize(DEFAULT_SIZE), myPosts(new Post[DEFAULT_SIZE]) {}

Profile::Profile(const Profile& other)
    : mySize(other.mySize), maxSize(other.maxSize), myPosts(new Post[other.maxSize]) {
  for (size_t i = 0; i < mySize; ++i) {
    myPosts[i] = other.myPosts[i];
  }
}

Profile& Profile::operator=(const Profile& other) {
  if (this == &other) {
    return *this;
  }

  Post* newPosts = new Post[other.maxSize];
  for (size_t i = 0; i < other.mySize; ++i) {
    newPosts[i] = other.myPosts[i];
  }

  delete[] myPosts;
  myPosts = newPosts;
  mySize = other.mySize;
  maxSize = other.maxSize;
  return *this;
}

Profile::Profile(Profile&& other) noexcept
    : mySize(other.mySize), maxSize(other.maxSize), myPosts(other.myPosts) {
  other.mySize = 0;
  other.maxSize = 0;
  other.myPosts = nullptr;
}

Profile& Profile::operator=(Profile&& other) noexcept {
  if (this == &other) {
    return *this;
  }

  delete[] myPosts;
  myPosts = other.myPosts;
  mySize = other.mySize;
  maxSize = other.maxSize;

  other.mySize = 0;
  other.maxSize = 0;
  other.myPosts = nullptr;
  return *this;
}

Profile::~Profile() {
  delete[] myPosts;
}

void Profile::resize(size_t newCapacity) {
  Post* newPosts = new Post[newCapacity];
  for (size_t i = 0; i < mySize; ++i) {
    newPosts[i] = myPosts[i];
  }

  delete[] myPosts;
  myPosts = newPosts;
  maxSize = newCapacity;
}

// adds a post to the next available spot in the array
void Profile::addPost(const Post& newPost) {
  // doubles in size, dynamically, if we're out of space. creates a new array and swaps the values
  if (mySize == maxSize) {
    resize(maxSize * 2);
  }
  myPosts[mySize] = newPost;
  ++mySize;
}

// prints a specific post given an index
void Profile::printPost(size_t postIndex) const {
  if (validPostIndex(postIndex)) {
    // create a temp just for prettier printing and another demonstration of pointers; the print statements could be achieved with myPosts[i].field
    const Post* temp = &myPosts[postIndex];
    std::cout << "Post number: " << postIndex + 1 << std::endl;
    std::cout << "Post caption: " << temp->caption << std::endl;
    std::cout << "Post hearts: " << temp->hearts << std::endl;
    std::cout << "\n";
  } else {
    std::cout << "Error! This would have attempted to print a post that doesn't exist in the array." << std::endl;
  }
}


// print out all the values that we are holding on to right now
void Profile::printPosts() const {
  std::cout << "Now printing out the current profile: " << std::endl;
  for (size_t i = 0; i < mySize; ++i) {
    // use our helper function to print out posts rather than iterating through it again
    printPost(i);
  }
  std::cout << "\n" << std::endl;
}

// bonus: add a statistic calculator
int Profile::sumHearts() const {
  int total = 0;
  for (size_t i = 0; i < mySize; ++i) {
    total += myPosts[i].hearts;
  }
  return total;
}

// fills all empty slots in the array with the last entry until we have filled our current capacity.
void Profile::fillProfile() {
  // if there was no last post, then we shouldn't continue execution of code.
  if (mySize == 0) {
    std::cout << "There was no last post to duplicate!" << std::endl; 
    return;
  }

  // make a copy of our last post
  Post lastPost(myPosts[mySize - 1]);

  // iterate through all empty positions in the our array 
  for (; mySize < maxSize; ++mySize) {
    myPosts[mySize] = lastPost;
  }
  
  // print out some statements for the user to get feedback on what actions are occurring
  std::cout << "Filled remaining posts with a post that contained:\nCaption: " << lastPost.caption << "\nHearts: " << lastPost.hearts << std::endl;
  std::cout << "Your profile now contains: " << mySize << " posts!" << std::endl;
  printPosts();
}

// removes a post at a certain index
void Profile::removePost(size_t index) {
  if (validPostIndex(index)) {
    for (size_t i = index + 1; i < mySize; ++i) {
      myPosts[i - 1] = myPosts[i];
    }
    --mySize;
    myPosts[mySize] = Post{};

  } else {
    std::cout << "Error! This would have attempted to remove a post that doesn't exist in the array." << std::endl;
  }
}

// add hearts to a specific post
void Profile::addHearts(size_t postIndex, int numHearts) {
  if (validPostIndex(postIndex)) {
    myPosts[postIndex].hearts += numHearts;
  } else {
    std::cout << "Error! This would have attempted to add hearts to a post that doesn't exist in the array." << std::endl;
  }
}

// helper function that checks to see if a post index is correct or not
bool Profile::validPostIndex(size_t index) const {
  return index < mySize;
}
