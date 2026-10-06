cmake_minimum_required(VERSION 4.1)
project(CPP_Level_2)

set(CMAKE_CXX_STANDARD 14)

include_directories(CPPM4-Dynamic-Array-Implementation)
include_directories(CPPM4-Grocery-List)
include_directories(CPPM5-Matrix-Fun-with-Matrix-Class)
include_directories(CPPM5-Profile-Posts)

add_executable(CPP_Level_2
#        CPPM1-Pointers/main.cpp
        CPPM1-Pointer-Practice/main.cpp
#        CPPM1-Pointer-Error-Examples/main.cpp
#        CPPM2-Array-Basics-Reference/main.cpp
#        CPPM2-Array-Practice/main.cpp
#        CPPM2-Pointer-Arithmetic-Reference/main.cpp
#        CPPM2-Tic-Tac-Toe/main.cpp
#        CPPM3-Two-Dimensional-Arrays-Reference/main.cpp
#        CPPM3-2D-Array-Practice/main.cpp
#        CPPM3-Bank-Transactions/main.cpp
#        CPPM4-Dynamic-Variables-Reference/main.cpp
#        CPPM4-Assembly-Line/main.cpp
#        CPPM4-Dynamic-Array-Implementation/DynamicArray.cpp
#        CPPM4-Dynamic-Array-Implementation/main.cpp
#        CPPM4-Grocery-List/DynamicArray.cpp
#        CPPM4-Grocery-List/GroceryList.cpp
#        CPPM4-Grocery-List/main.cpp
#        CPPM5-Matrix-Fun-with-Matrix-Class/main.cpp
#        CPPM5-Matrix-Fun-with-Matrix-Class/matrix.cpp
#        CPPM5-Profile-Posts/main.cpp
#        CPPM5-Profile-Posts/profile.cpp
)

add_executable(CPPM0_Lifetime_Tracing_Warm_Up
        CPPM0-Lifetime-Tracing-Warm-Up/main.cpp
)

add_executable(CPPM0_Ownership_Boundary_Debugging
        CPPM0-Ownership-Boundary-Debugging/main.cpp
)

add_executable(CPPM5_Modern_Ownership_Reflection
        CPPM5-Modern-Ownership-Reflection/main.cpp
)

# Keep the CPPM0 learner/reference programs independent.
add_executable(CPPM0_Lifetime_Starter CPPM0-Lifetime-Tracing-Warm-Up/starter/main.cpp)
add_executable(CPPM0_Lifetime_Reference CPPM0-Lifetime-Tracing-Warm-Up/solution/main.cpp)
add_executable(CPPM0_Ownership_Starter CPPM0-Ownership-Boundary-Debugging/starter/main.cpp)
add_executable(CPPM0_Ownership_Reference CPPM0-Ownership-Boundary-Debugging/solution/main.cpp)
set_target_properties(CPPM0_Lifetime_Tracing_Warm_Up CPPM0_Ownership_Boundary_Debugging CPPM0_Lifetime_Starter CPPM0_Lifetime_Reference CPPM0_Ownership_Starter CPPM0_Ownership_Reference PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
