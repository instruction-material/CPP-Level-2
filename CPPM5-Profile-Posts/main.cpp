#include <iostream>
#include "profile.h"

int main() {
  // Basic sample driver code that demonstrates adding a post to a profile
  Profile myProfile;
  Post firstPost{"My first post!", 30};
  myProfile.addPost(firstPost);

  // print out some stats about the current state of the profile
  std::cout << "\nMy total hearts: " << myProfile.sumHearts() << std::endl << std::endl;

  // add another post
  Post newPost;
  newPost.caption = "Incredible coders come from all backgrounds!";
  newPost.hearts = 100;
  myProfile.addPost(newPost);

  // Add another post
  newPost = Post{"A new caption", 20};
  myProfile.addPost(newPost);
  myProfile.printPosts();

  // test removing a post
  myProfile.removePost(1);
  myProfile.printPosts();
  
  // add hearts to a post
  myProfile.addHearts(0, 10);
  myProfile.printPosts();

  // add posts and then see if size manipulation is working
  newPost = Post{"On the beach!", 20};
  myProfile.addPost(newPost);
  myProfile.addPost(newPost);
  myProfile.addPost(newPost);
  myProfile.addPost(newPost);
  myProfile.addPost(newPost);

  // the dynamic array should have expanded
  myProfile.printPosts();
}
