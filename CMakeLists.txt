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

# CPPM1 learner and reference packs each have exactly one entry point.
add_executable(CPPM1_Error_Starter CPPM1-Pointer-Error-Examples-Starter/main.cpp)
add_executable(CPPM1_Error_Reference CPPM1-Pointer-Error-Examples/main.cpp)
add_executable(CPPM1_Practice_Starter CPPM1-Pointer-Practice-Starter/main.cpp)
add_executable(CPPM1_Practice_Reference CPPM1-Pointer-Practice/main.cpp)
set_target_properties(CPP_Level_2 CPPM1_Error_Starter CPPM1_Error_Reference CPPM1_Practice_Starter CPPM1_Practice_Reference PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)

# CPPM2 lesson and practice packs each have one independent entry point.
add_executable(CPPM2_Array_Basics CPPM2-Array-Basics-Reference/main.cpp)
add_executable(CPPM2_Pointer_Arithmetic CPPM2-Pointer-Arithmetic-Reference/main.cpp)
add_executable(CPPM2_Array_Practice_Starter CPPM2-Array-Practice-Starter/main.cpp)
add_executable(CPPM2_Array_Practice_Reference CPPM2-Array-Practice/main.cpp)
set(CPPM2_TARGETS CPPM2_Array_Basics CPPM2_Pointer_Arithmetic CPPM2_Array_Practice_Starter CPPM2_Array_Practice_Reference)
set_target_properties(${CPPM2_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM2_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# Optional CPPM2 integration game: independent learner and reference targets.
add_executable(CPPM2_Tic_Tac_Toe_Starter CPPM2-Tic-Tac-Toe-Starter/main.cpp)
add_executable(CPPM2_Tic_Tac_Toe_Reference CPPM2-Tic-Tac-Toe/main.cpp)
set_target_properties(CPPM2_Tic_Tac_Toe_Starter CPPM2_Tic_Tac_Toe_Reference PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(CPPM2_Tic_Tac_Toe_Starter PRIVATE -Wall -Wextra -Wpedantic -Werror)
    target_compile_options(CPPM2_Tic_Tac_Toe_Reference PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

# CPPM3 worked lesson, required practice, and optional applied grid stay separate.
add_executable(CPPM3_Two_Dimensional_Arrays CPPM3-Two-Dimensional-Arrays-Reference/main.cpp)
add_executable(CPPM3_Array_Practice_Starter CPPM3-2D-Array-Practice-Starter/main.cpp)
add_executable(CPPM3_Array_Practice_Reference CPPM3-2D-Array-Practice/main.cpp)
add_executable(CPPM3_Bank_Starter CPPM3-Bank-Transactions-Starter/main.cpp)
add_executable(CPPM3_Bank_Reference CPPM3-Bank-Transactions/main.cpp)
set(CPPM3_TARGETS CPPM3_Two_Dimensional_Arrays CPPM3_Array_Practice_Starter CPPM3_Array_Practice_Reference CPPM3_Bank_Starter CPPM3_Bank_Reference)
set_target_properties(${CPPM3_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM3_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# Optional coordinate/column extension has its own learner and reference packs.
add_executable(CPPM3_Extension_Starter CPPM3-2D-Array-Extension-Starter/main.cpp)
add_executable(CPPM3_Extension_Reference CPPM3-2D-Array-Extension/main.cpp)
set_target_properties(CPPM3_Extension_Starter CPPM3_Extension_Reference PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(CPPM3_Extension_Starter PRIVATE -Wall -Wextra -Wpedantic -Werror)
    target_compile_options(CPPM3_Extension_Reference PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

# Complete CPPM4 lifetime lesson: independent, warning-clean C++20 target.
add_executable(CPPM4_Dynamic_Variables CPPM4-Dynamic-Variables-Reference/main.cpp)
set_target_properties(CPPM4_Dynamic_Variables PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(CPPM4_Dynamic_Variables PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

# CPPM4 integer-array learner/reference keep independent entry points and owners.
add_executable(CPPM4_Dynamic_Array_Starter CPPM4-Dynamic-Array-Implementation-Starter/DynamicArray.cpp CPPM4-Dynamic-Array-Implementation-Starter/main.cpp)
add_executable(CPPM4_Dynamic_Array_Reference CPPM4-Dynamic-Array-Implementation/DynamicArray.cpp CPPM4-Dynamic-Array-Implementation/main.cpp)
set(CPPM4_ARRAY_TARGETS CPPM4_Dynamic_Array_Starter CPPM4_Dynamic_Array_Reference)
set_target_properties(${CPPM4_ARRAY_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM4_ARRAY_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# CPPM4 Assembly Line remains separate from the required custom-array exercise.
add_executable(CPPM4_Assembly_Line_Starter CPPM4-Assembly-Line-Starter/main.cpp)
add_executable(CPPM4_Assembly_Line_Reference CPPM4-Assembly-Line/main.cpp)
set(CPPM4_ASSEMBLY_TARGETS CPPM4_Assembly_Line_Starter CPPM4_Assembly_Line_Reference)
set_target_properties(${CPPM4_ASSEMBLY_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM4_ASSEMBLY_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# Optional Grocery transfer keeps each multi-file learner/reference independent.
add_executable(CPPM4_Grocery_List_Starter CPPM4-Grocery-List-Starter/DynamicArray.cpp CPPM4-Grocery-List-Starter/GroceryList.cpp CPPM4-Grocery-List-Starter/main.cpp)
add_executable(CPPM4_Grocery_List_Reference CPPM4-Grocery-List/DynamicArray.cpp CPPM4-Grocery-List/GroceryList.cpp CPPM4-Grocery-List/main.cpp)
set(CPPM4_GROCERY_TARGETS CPPM4_Grocery_List_Starter CPPM4_Grocery_List_Reference)
set_target_properties(${CPPM4_GROCERY_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM4_GROCERY_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# Principal CPPM5 manual-memory capstone has independent learner/reference targets.
add_executable(CPPM5_Profile_Posts_Starter CPPM5-Profile-Posts-Starter/profile.cpp CPPM5-Profile-Posts-Starter/main.cpp)
add_executable(CPPM5_Profile_Posts_Reference CPPM5-Profile-Posts/profile.cpp CPPM5-Profile-Posts/main.cpp)
set(CPPM5_PROFILE_TARGETS CPPM5_Profile_Posts_Starter CPPM5_Profile_Posts_Reference)
set_target_properties(${CPPM5_PROFILE_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM5_PROFILE_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# Optional CPPM5 matrix class keeps automatic vector storage and separate programs.
add_executable(CPPM5_Matrix_Class_Starter CPPM5-Matrix-Fun-with-Matrix-Class-Starter/matrix.cpp CPPM5-Matrix-Fun-with-Matrix-Class-Starter/main.cpp)
add_executable(CPPM5_Matrix_Class_Reference CPPM5-Matrix-Fun-with-Matrix-Class/matrix.cpp CPPM5-Matrix-Fun-with-Matrix-Class/main.cpp)
set(CPPM5_MATRIX_TARGETS CPPM5_Matrix_Class_Starter CPPM5_Matrix_Class_Reference)
set_target_properties(${CPPM5_MATRIX_TARGETS} PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    foreach(target IN LISTS CPPM5_MATRIX_TARGETS)
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
    endforeach()
endif()

# The ownership reflection is a worked comparison, with strict C++20 compilation.
set_target_properties(CPPM5_Modern_Ownership_Reflection PROPERTIES CXX_STANDARD 20 CXX_STANDARD_REQUIRED YES CXX_EXTENSIONS NO)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(CPPM5_Modern_Ownership_Reflection PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()
