#ifndef GENERATE_TASKS_H
#define GENERATE_TASKS_H

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <random>
#include <cmath>
#include <map>

using namespace std;

constexpr int MIN_CLO = 5;
constexpr int MAX_CLO = 25;
constexpr int MAX_D = 500;
constexpr int MAX_T = 500;

enum Level { LO, HI };

struct Task {
  int ID, T, C_LO, C_HI, D, tight_D;
  Level L;

  Task() {
    ID = -1;
    T = 0;
    C_LO = 0;
    C_HI = 0;
    D = 0;
    tight_D = -1;
    L = Level::LO;
  }

  Task(int ID, int T, int C_LO, int C_HI, int D, int tight_D = -1, Level L = LO)
    : ID(ID), T(T), C_LO(C_LO), C_HI(C_HI), D(D), tight_D(tight_D == -1 ? D : tight_D), L(C_LO == C_HI ? LO : HI) {}

  Task(const Task& other)
    : ID(other.ID), T(other.T), C_LO(other.C_LO), C_HI(other.C_HI), D(other.D), tight_D(other.tight_D), L(other.L) {}

  Task& operator=(const Task& other) {
    if (this != &other) { 
      this->ID = other.ID;
      this->T = other.T;
      this->C_LO = other.C_LO;
      this->C_HI = other.C_HI;
      this->D = other.D;
      this->tight_D = other.tight_D;
      this->L = other.L;
    }
    return *this;
  }

  bool operator==(const Task& other) const {
    return this->ID == other.ID &&
           this->T == other.T &&
           this->C_LO == other.C_LO &&
           this->C_HI == other.C_HI &&
           this->D == other.D &&
           this->tight_D == other.tight_D &&
           this->L == other.L;
  }

  string task_to_string() const {
    return "Task(" + to_string(ID) + "," + to_string(T) + "," + to_string(C_LO) + "," + to_string(C_HI) + "," + to_string(D) + "," + to_string(tight_D) + ")";
  }
};

mt19937 get_generator(unsigned int seed = 0) {
  if (seed > 0) {
    return mt19937(seed);
  } else {
    random_device rand_device;
    return mt19937(rand_device());
  }
}

int generate_C_LO(unsigned int seed = 0) {
  mt19937 generator = get_generator(seed);
  uniform_int_distribution<> distribution(MIN_CLO, MAX_CLO);
  return distribution(generator);
}

Level generate_L(double hi_probability = 0.5, unsigned int seed = 0) {
  mt19937 generator = get_generator(seed);
  bernoulli_distribution distribution(hi_probability);
  return distribution(generator) ? HI : LO;
}

int generate_C_HI(int C_LO, Level L, int wcet_ratio = 4, unsigned int seed = 0) {
  if (L == LO) return C_LO;

  mt19937 generator = get_generator(seed);
  uniform_int_distribution<> distribution(C_LO * 2, C_LO * wcet_ratio);

  return distribution(generator);
}

int generate_D(int C_HI, unsigned int seed = 0) {
  mt19937 generator = get_generator(seed);
  uniform_int_distribution<> distribution(C_HI, MAX_D);
  return distribution(generator);
}

int generate_T(int C_HI, unsigned int seed = 0) {
  mt19937 generator = get_generator(seed);
  uniform_int_distribution<> distribution(C_HI, MAX_T);
  return distribution(generator);
}

Task generate_task(int ID = -1, double hi_probability = 0.5, double wcet_ratio = 4) {
  auto L = generate_L(hi_probability);
  auto C_LO = generate_C_LO();
  auto C_HI = generate_C_HI(C_LO, L, wcet_ratio);
  auto D = generate_D(C_HI);
  auto T = generate_T(C_HI);

  return Task(ID, T, C_LO, C_HI, D, -1, L);
}

#endif
