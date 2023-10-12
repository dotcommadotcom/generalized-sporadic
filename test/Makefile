CXX = g++
CXXFLAGS = -std=c++17
LIBS = -lgtest -lgtest_main

SRCS = main_test.cpp
TARGET = main_test

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LIBS)

test: $(TARGET)
	./$(TARGET) 

clean:
	rm -f $(TARGET)

run-all: all test clean

.PHONY: all test clean run-all

// --gtest_filter=SearchAlgorithm.NaiveTightD
