#ifndef SCHEDULABILITY_TEST
#define SCHEDULABILITY_TEST

#include <gtest/gtest.h>

#include "../src/schedulability.h"

/* TEST SCHEDULABILITY FUNCTIONS */

TEST(Schedulability, TrueTaskSet) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 414, 13, 13, 300, 300), Task(3, 115, 14, 14, 267, 267), Task(5, 94, 7, 7, 172, 172)};
  task_set_dict["hi"] = {Task(1, 122, 23, 46, 312, 312), Task(2, 108, 18, 37, 107, 107), Task(4, 132, 15, 50, 233, 233)};
  TaskSet task_set = TaskSet(task_set_dict);
  
  EXPECT_TRUE(schedulability_test_thm1(task_set));
  EXPECT_TRUE(schedulability_test_thm2(task_set));
  EXPECT_TRUE(schedulability_test_thm3(task_set));
}

TEST(Schedulability, FalseTaskSet) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 133, 18, 18, 399, 399), Task(4, 472, 13, 13, 315, 315)};
  task_set_dict["hi"] = {Task(0, 146, 10, 40, 410, 410), Task(1, 386, 24, 59, 93, 93), Task(3, 394, 15, 42, 78, 78)};
  TaskSet task_set = TaskSet(task_set_dict);
  
  EXPECT_FALSE(schedulability_test_thm1(task_set));
  EXPECT_FALSE(schedulability_test_thm3(task_set));
  EXPECT_FALSE(schedulability_test_thm2_3(task_set));
}

TEST(Schedulability, FalseTaskSet2) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(1, 357, 8, 8, 256, 256), Task(2, 429, 19, 19, 63, 63), Task(4, 180, 22, 22, 77, 77), Task(5, 26, 13, 13, 103, 103), Task(7, 283, 13, 13, 208, 208), Task(8, 419, 6, 6, 316, 316), Task(9, 445, 8, 8, 385, 385), Task(10, 336, 8, 8, 29, 29), Task(12, 360, 11, 11, 144, 144), Task(13, 117, 20, 20, 39, 39), Task(14, 491, 14, 14, 422, 422)};
  task_set_dict["hi"] = {Task(0, 400, 24, 92, 244, 244), Task(3, 420, 20, 63, 449, 449), Task(6, 354, 17, 48, 426, 426), Task(11, 143, 17, 37, 485, 485)};
  TaskSet task_set = TaskSet(task_set_dict);
  
  EXPECT_FALSE(schedulability_test_thm2(task_set));
  EXPECT_FALSE(schedulability_test_thm2_3(task_set));
}

TEST(Schedulability, Sched23) {
  TaskSet task_set = TaskSet(0.5);
  
  EXPECT_EQ(schedulability_test_thm2(task_set) || schedulability_test_thm3(task_set), schedulability_test_thm2_3(task_set));
}
#endif
