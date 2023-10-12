CC = clang++
CFLAGS = -Xclang -fopenmp -std=c++17 -I/opt/homebrew/opt/libomp/include
LDFLAGS = -L/opt/homebrew/opt/libomp/lib
LIBS = -lomp

SRC = main.cpp
TARGET = main

COUNT = 10
# UTILIZATION = 500

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) $(LIBS) $^ -o $@

run: $(TARGET)
	./$(TARGET) $(COUNT) $(UTILIZATION)

clean:
	rm -f $(TARGET)

run-all:
	for UTILIZATION in $$(seq 100 50 950); do \
		make run UTILIZATION=$$UTILIZATION; \
	done
	make clean

.PHONY: all clean

ptarget = parallelism

$(ptarget): parallelism.cpp
	$(CC) $(CFLAGS) $(LDFLAGS) $(LIBS) $^ -o $@

prun: $(ptarget)
	./$(ptarget)

pclean:
	rm -f $(ptarget)

prunall: $(ptarget) prun pclean
