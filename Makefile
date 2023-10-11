CC = clang++
CFLAGS = -Xclang -fopenmp -std=c++17 -I/opt/homebrew/opt/libomp/include
LDFLAGS = -L/opt/homebrew/opt/libomp/lib
LIBS = -lomp

SRC = main.cpp
TARGET = main

COUNT = 10000
UTILIZATION = 0.5

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(LIBS) $^ -o $@

run: $(TARGET)
	./$(TARGET) $(COUNT) $(UTILIZATION)

clean:
	rm -f $(OBJS) $(TARGET)

run-all: all run clean

.PHONY: all clean
