#ifndef GENERATE_TASKS_TEST
#define GENERATE_TASKS_TEST

#include <gtest/gtest.h>

#include "../src/generate_tasks.h"

TEST(GenerateTasks, CanaryTest) {
  EXPECT_TRUE(true) << "Canary test failed.";
}

/* TEST TASK ATTRIBUTES AND ASSUMPTIONS */ 

TEST(GenerateTasks, LevelHiOrLo) {
  Level level = generate_L();

  EXPECT_TRUE(level == LO || level == HI);
}

TEST(GenerateTasks, GenerateCLo) {
  int C_LO = generate_C_LO();

  EXPECT_GE(C_LO, 5);
  EXPECT_LE(C_LO, 25);
}

TEST(GenerateTasks, GenerateCHi) {
  int C_LO = generate_C_LO();

  int C_HI_LO = generate_C_HI(C_LO, LO);
  int C_HI_HI = generate_C_HI(C_LO, HI, 4);

  EXPECT_EQ(C_HI_LO, C_LO);
  EXPECT_GE(C_HI_HI, 10);
  EXPECT_LE(C_HI_HI, C_LO * 4);
}

TEST(GenerateTasks, GenerateD) {
  int C_LO = generate_C_LO();
  int C_HI = generate_C_HI(C_LO, HI);

  int D = generate_D(C_HI);

  EXPECT_GE(D, C_HI);
  EXPECT_LE(D, 500);
}

TEST(GenerateTasks, GenerateT) {
  int C_LO = generate_C_LO();
  int C_HI = generate_C_HI(C_LO, HI);

  int T = generate_T(C_HI);

  EXPECT_GE(T, C_HI);
  EXPECT_LE(T, 500);
}

TEST(GenerateTasks, GenerateWithSeed) {
  unsigned int seed = 123;

  int C_LO = generate_C_LO(seed);
  int C_HI = generate_C_HI(C_LO, HI, 4, seed);
  int D = generate_D(C_HI, seed);
  int T = generate_T(C_HI, seed);

  EXPECT_EQ(C_LO, 18);
  EXPECT_EQ(C_HI, 38);
  EXPECT_EQ(D, 403);
  EXPECT_EQ(T, 403);
}

TEST(GenerateTasks, GenerateRandomTask) {
  Task random_task = generate_task();

  EXPECT_TRUE(random_task.L == HI ? random_task.C_LO < random_task.C_HI : random_task.C_LO == random_task.C_HI);
  EXPECT_LE(random_task.C_HI, random_task.D);
  EXPECT_LE(random_task.C_HI, random_task.T);
}

/* TEST OVERLOADED OPERATOR */ 

TEST(GenerateTasks, AssignmentAndEqualOperator) {
  Task task = generate_task(-1);

  Task copy = task;

  EXPECT_NE(&task, &copy);
  EXPECT_EQ(task.ID, copy.ID);
  EXPECT_EQ(task.T, copy.T);
  EXPECT_EQ(task.C_LO, copy.C_LO);
  EXPECT_EQ(task.C_HI, copy.C_HI);
  EXPECT_EQ(task.D, copy.D);
  EXPECT_EQ(task.tight_D, copy.tight_D);
  EXPECT_EQ(task.L, copy.L);

  EXPECT_TRUE(task == copy);
  EXPECT_TRUE(task == task);
}

#endif