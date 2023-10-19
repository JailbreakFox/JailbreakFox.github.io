cmake_minimum_required(VERSION 2.8)
project(CTest)

set(CMAKE_CXX_STANDARD 11)

add_executable(${PROJECT_NAME} CTest.cpp)
install(TARGETS CTest
	DESTINATION /usr/bin)
