CC = clang++
CFLAGS = -Xclang -fopenmp -std=c++17 -I/opt/homebrew/opt/libomp/include
LDFLAGS = -L/opt/homebrew/opt/libomp/lib
LIBS = -lomp

SRC = main.cpp
TARGET = main

COUNT = 100
UTILIZATION = 0.5

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(LIBS) $^ -o $@

run: $(TARGET)
	./$(TARGET) $(COUNT) $(UTILIZATION)

clean:
	rm -f $(TARGET)

run-all: all run clean

.PHONY: all clean

EK = ekberg_experiment.cpp
EK2 = ekberg_experiment

ek: $(EK2)

$(EK2): $(EK)
	$(CC) $(CFLAGS) $(LDFLAGS) $(LIBS) $^ -o $@

ekberg: $(EK2)
	./$(EK2)

ekclean:
	rm -f $(EK2)

ekrun: ek ekberg ekclean
