#ifndef DBFS_TEST
#define DBFS_TEST

#include <gtest/gtest.h>

#include "../src/dbfs.h"

/* TEST MAX_REQUESTS FUNCTIONS */

TEST(DBF, MaxRequests) {
  double upper = 100;

  // upper > lower --> k > 0
  EXPECT_GT(max_requests(1, upper, upper - 1), 0);

  // upper == lower --> k == 1
  EXPECT_EQ(max_requests(1, upper, upper), 1);

  // upper < lower --> k == 0
  EXPECT_EQ(max_requests(1, upper, upper + 1), 0);
}

TEST(DBF, MaxRequestsIsN) {
  int t = 1000;
  random_device random_device;
  mt19937 generator(random_device());

  uniform_int_distribution<> upper_distribution(0, t * t);
  double upper = upper_distribution(generator);
  uniform_int_distribution<> lower_distribution(0, upper);
  double lower = lower_distribution(generator);
  uniform_int_distribution<> T_distribution(0, t);
  int T = T_distribution(generator);
  int n = static_cast<int>(floor((upper - lower) / T));
  double lower1 = upper - n * T + 1;
  double lower2 = upper - n * T;
  double lower3 = upper - (n + 1) * T + 1;

  // upper >= lower --> k == n + 1
  EXPECT_EQ(max_requests(T, upper, lower), n + 1);

  // b - a >= T --> k_i != k_j
  EXPECT_NE(max_requests(T, upper, lower1), max_requests(T, upper, lower2));

  // b - a < T --> k_i == k_j 
  EXPECT_EQ(max_requests(T, upper, lower2), max_requests(T, upper, lower3));
}

/* TEST LOWER AND UPPER FUNCTION */

TEST(DBF, LowerUpperTaskSet) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 115, 14, 14, 267, 267), Task(3, 94, 7, 7, 172, 172), Task(5, 414, 13, 13, 300, 300)};
  task_set_dict["hi"] = {Task(1, 108, 18, 37, 107, 107), Task(2, 132, 15, 50, 233, 233), Task(4, 122, 23, 46, 312, 312)};
  TaskSet task_set = TaskSet(task_set_dict);

  int t = 1000;

  Task HI_task, LO_task;

  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) HI_task = task;
    if (task.L == LO) LO_task = task;
  }

  EXPECT_EQ(lower(HI_task, t), 732);
  EXPECT_EQ(upper_CO(HI_task, t, t/2), 444);
  EXPECT_EQ(upper_UN(LO_task, t, t/2), 500);
}

Task generate_task_level(Level level) {
  Task random_task; 
  while (true) { 
    random_task = generate_task();
    if (random_task.L == level) {
      return random_task;
    }
  }
}

TEST(DBF, LowerUpperRandomTaskSet) {
  int t = 1000;
  Task random_task = generate_task();
  Task random_HI_task = generate_task_level(HI);
  Task random_LO_task = generate_task_level(LO);

  // ts >= D --> lower > 0
  EXPECT_GT(lower(random_task, random_task.tight_D), 0);

  // ts < D --> lower == 0
  EXPECT_EQ(lower(random_task, random_task.tight_D - 1), 0);

  // ∀ 0 < ts < t, upper_co < ts 
  for (int ts = 1; ts < t; ++ts) {
    EXPECT_LT(upper_CO(random_HI_task, t, ts), ts);
  }

  // t > D --> upper_un > 0
  EXPECT_GT(upper_UN(random_LO_task, random_LO_task.tight_D + 1, 1), 0);
}

/* TEST DBF FUNCTIONS */

TEST(DBF, DemandBasedFunction) {
  double upper = 100;

  // upper > lower --> dbf == C * k
  EXPECT_EQ(demand_based_function(5, 15, upper, 0), 35);

  // upper == lower --> dbf == C
  EXPECT_EQ(demand_based_function(5, 15, upper, upper), 5);

  // upper < lower --> dbf == 0 
  EXPECT_EQ(demand_based_function(5, 15, upper, upper + 1), 0);
}

TEST(DBF, DemandBasedFunctionTask) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 115, 14, 14, 267, 267), Task(3, 94, 7, 7, 172, 172), Task(5, 414, 13, 13, 300, 300)};
  task_set_dict["hi"] = {Task(1, 108, 18, 37, 107, 107), Task(2, 132, 15, 50, 233, 233), Task(4, 122, 23, 46, 312, 312)};
  TaskSet task_set = TaskSet(task_set_dict);
  
  int t = 1000;
  Task HI_task, LO_task;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) HI_task = task;
    if (task.L == LO) LO_task = task;
  }

  EXPECT_EQ(demand_based_function_LO(LO_task, t), 26);
  EXPECT_EQ(demand_based_function_HI(HI_task, t, t/2), 92);
  EXPECT_EQ(demand_based_function_CO(HI_task, t, t/2), 92);
  EXPECT_EQ(demand_based_function_UN(LO_task, t, t/2), 13);
}

TEST(DBF, DemandBasedFunctionRandomTaskSet) {
  int t = 1000;
  Task random_task = generate_task();
  Task random_HI_task = generate_task_level(HI);
  random_HI_task.tight_D = floor(random_HI_task.D / 2);
  Task random_LO_task = generate_task_level(LO);

  // ts < tight_D --> dbf_LO == 0
  EXPECT_EQ(demand_based_function_LO(random_task, random_task.tight_D - 1), 0);

  // t - ts - D < 0 --> dbf_HI == 0
  EXPECT_EQ(demand_based_function_HI(random_HI_task, t, t - random_HI_task.D + 1), 0);

  // t < D --> upper < 0 --> dbf_CO == 0 
  EXPECT_EQ(demand_based_function_CO(random_HI_task, random_HI_task.D - 1, random_HI_task.D - 2), 0);

  // t > D and ts <= t - D - (t-D)//T * T --> upper < 0 --> dbf_CO == 0
  EXPECT_LT(upper_CO(random_HI_task, random_HI_task.D + 100, random_HI_task.D + 100 - random_HI_task.D - floor((random_HI_task.D + 100 - random_HI_task.D)/random_HI_task.T) * random_HI_task.T), 0);
  EXPECT_EQ(demand_based_function_CO(random_HI_task, random_HI_task.D + 100, random_HI_task.D + 100 - random_HI_task.D - floor((random_HI_task.D + 100 - random_HI_task.D)/random_HI_task.T) * random_HI_task.T), 0);

  // t == D and ts >= tight_D --> upper == 0 and lower > 0 --> dbf_CO == 0
  EXPECT_EQ(demand_based_function_CO(random_HI_task, random_HI_task.D, random_HI_task.D / 2), 0);

  // t > D and ts <= t - D - (t-D)//T * T --> upper < 0 --> dbf_CO == 0
  EXPECT_EQ(demand_based_function_CO(random_HI_task, random_HI_task.D + 100, floor((t - random_HI_task.D)/random_HI_task.T) * random_HI_task.T + random_HI_task.tight_D), 0);

  // upper > 0 and lower == 0 --> dbf_UN > 0 
  EXPECT_GT(demand_based_function_UN(random_LO_task, random_LO_task.D + 1, random_LO_task.tight_D - 1), 0);

  // upper == 0 and lower == 0 --> dbf_UN == C_LO
  EXPECT_EQ(upper_UN(random_LO_task, random_LO_task.D, random_LO_task.tight_D - 1), 0);
  EXPECT_EQ(demand_based_function_UN(random_LO_task, random_LO_task.D, random_LO_task.tight_D - 1), random_LO_task.C_LO);

  // upper < 0 --> dbf_UN == 0
  EXPECT_EQ(demand_based_function_UN(random_LO_task, random_LO_task.D - 1, 1), 0);

  // upper == 0 and lower > 0 --> dbf_UN == C_LO
  EXPECT_EQ(demand_based_function_UN(random_LO_task, random_LO_task.D, random_LO_task.tight_D), 0);
}

/* TEST SUM_DBF FUNCTION */

TEST(DBF, SumDBFTaskSet) {
  int t = 1000;
  TaskSet task_set = TaskSet(0.7);

  EXPECT_EQ(sum_dbf(task_set, t, t / 2), sum_dbf_LO(task_set, t / 2) + sum_dbf_HI(task_set, t, t / 2) + sum_dbf_CO(task_set, t, t / 2) + sum_dbf_UN(task_set, t, t / 2));
}

#endif