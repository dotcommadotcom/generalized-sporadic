#ifndef EKBERG_TEST
#define EKBERG_TEST

#include <gtest/gtest.h>

#include "../src/ekberg.h"

TEST(Ekberg, Task1) {
  Task task1 = Task(0, 5, 2, 2, 4);

  for (int i = task1.tight_D, j = 1; i < 30; i = i + task1.T, ++j) {
    EXPECT_EQ(ekberg_lo(task1, i), task1.C_LO * j);
  }
}

TEST(Ekberg, Task2) {
  Task task2 = Task(1, 7, 1, 2, 6);

  for (int i = 0, j = 0; i < 30; i = i + task2.T, ++j) {
    for (int k = 0; k < 2; ++k) {
      EXPECT_EQ(ekberg_hi(task2, i + k), task2.C_HI * j + k + 1);
    }
  }

  for (int i = 1, j = 1; i < 30; i = i + task2.T, ++j) {
    EXPECT_EQ(ekberg_hi(task2, i), task2.C_HI * j);
  }

  for (int i = task2.tight_D, j = 1; i < 30; i = i + task2.T, ++j) {
    EXPECT_EQ(ekberg_lo(task2, i), task2.C_LO * j);
  }
}

TEST(Ekberg, Task2TightD) {
  Task task2 = Task(1, 7, 1, 2, 6, 5);

  for (int i = 1, j = 0; i < 30; i = i + task2.T, ++j) {
    for (int k = 0; k < 1; ++k) {
      EXPECT_EQ(ekberg_hi(task2, i + k), task2.C_HI * j + k + 1);
    }
  }

  for (int i = 2, j = 1; i < 30; i = i + task2.T, ++j) {
    EXPECT_EQ(ekberg_hi(task2, i), task2.C_HI * j);
  }

  for (int i = task2.tight_D, j = 1; i < 30; i = i + task2.T, ++j) {
    EXPECT_EQ(ekberg_lo(task2, i), task2.C_LO * j);
  }
}

TEST(Ekberg, Task3) {
  Task task3 = Task(2, 6, 2, 4, 6);

  for (int i = 0, j = 0; i < 30; i = i + task3.T, ++j) {
    for (int k = 0; k < 3; ++k) {
      EXPECT_EQ(ekberg_hi(task3, i + k), task3.C_HI * j + k + 2);
    }
  }

  for (int i = 2, j = 1; i < 30; i = i + task3.T, ++j) {
    EXPECT_EQ(ekberg_hi(task3, i), task3.C_HI * j);
  }

  for (int i = task3.tight_D, j = 1; i < 30; i = i + task3.T, ++j) {
    EXPECT_EQ(ekberg_lo(task3, i), task3.C_LO * j);
  }
}

TEST(Ekberg, Task3TightD) {
  Task task3 = Task(2, 6, 2, 4, 6, 4);

  for (int i = 2, j = 0; i < 30; i = i + task3.T, ++j) {
    for (int k = 0; k < 3; ++k) {
      EXPECT_EQ(ekberg_hi(task3, i + k), task3.C_HI * j + k + 2);
    }
  }

  for (int i = 4, j = 1; i < 30; i = i + task3.T, ++j) {
    EXPECT_EQ(ekberg_hi(task3, i), task3.C_HI * j);
  }

  for (int i = task3.tight_D, j = 1; i < 30; i = i + task3.T, ++j) {
    EXPECT_EQ(ekberg_lo(task3, i), task3.C_LO * j);
  }
}

TEST(Ekberg, TaskSetHiSum) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6), Task(2, 6, 2, 4, 6)};
  TaskSet task_set = TaskSet(task_set_dict);

  vector<double> expected_hi_sum = {3, 6, 12, 18, 22, 27};

  for (int i = 0; i < 30; i = i + 5) {
    EXPECT_EQ(ekberg_hi_sum(task_set, i), expected_hi_sum[static_cast<int>(i/5)]);
  }
  EXPECT_FALSE(ekberg_thm2(task_set));
}

TEST(Ekberg, TaskSetLoSum) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6), Task(2, 6, 2, 4, 6)};
  TaskSet task_set = TaskSet(task_set_dict);

  vector<double> expected_lo_sum = {0, 2, 7, 12, 17, 21};

  for (int i = 0; i < 30; i = i + 5) {
    EXPECT_EQ(ekberg_lo_sum(task_set, i), expected_lo_sum[static_cast<int>(i/5)]);
  }
  EXPECT_TRUE(ekberg_thm1(task_set));
}

TEST(Ekberg, TaskSetHiSumTightD) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6, 5), Task(2, 6, 2, 4, 6, 2)};
  TaskSet task_set = TaskSet(task_set_dict);

  vector<double> expected_hi_sum = {0, 5, 10, 13, 18, 24};

  for (int i = 0; i < 30; i = i + 5) {
    EXPECT_EQ(ekberg_hi_sum(task_set, i), expected_hi_sum[static_cast<int>(i/5)]);
  }
  EXPECT_TRUE(ekberg_thm2(task_set));
}

TEST(Ekberg, TaskSetLoSumTightD) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6, 5), Task(2, 6, 2, 4, 6, 2)};
  TaskSet task_set = TaskSet(task_set_dict);

  vector<double> expected_lo_sum = {0, 5, 9, 14, 19, 21};

  for (int i = 0; i < 30; i = i + 5) {
    EXPECT_EQ(ekberg_lo_sum(task_set, i), expected_lo_sum[static_cast<int>(i/5)]);
  }
  EXPECT_TRUE(ekberg_thm1(task_set));
}

TEST(Ekberg, IsEligibleOrNot) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6), Task(2, 6, 2, 4, 6)};
  TaskSet eligible_task_set = TaskSet(task_set_dict);

  task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6, 5), Task(2, 6, 2, 4, 6, 2)};
  TaskSet not_eligible_task_set = TaskSet(task_set_dict);

  eligible_task_set.set_thm1(ekberg_thm1(eligible_task_set));
  eligible_task_set.set_thm2(ekberg_thm2(eligible_task_set));
  not_eligible_task_set.set_thm1(ekberg_thm1(not_eligible_task_set));
  not_eligible_task_set.set_thm2(ekberg_thm2(not_eligible_task_set));

  EXPECT_TRUE(ekberg_is_eligible(eligible_task_set));
  EXPECT_FALSE(ekberg_is_eligible(not_eligible_task_set));
}

TEST(Ekberg, GetHiCandidates) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 5, 2, 2, 4)};
  task_set_dict["hi"] = {Task(1, 7, 1, 2, 6), Task(2, 6, 2, 4, 6)};
  TaskSet task_set = TaskSet(0.5);

  vector<int> candidates = get_hi_candidates_vector(task_set);

  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_NE(find(candidates.begin(), candidates.end(), task.ID), candidates.end());
    } else {
      EXPECT_EQ(task.L, LO);
    }
  }
}
#endif
