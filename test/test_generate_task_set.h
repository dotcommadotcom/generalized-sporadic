#ifndef GENERATE_TASK_SET_TEST
#define GENERATE_TASK_SET_TEST

#include <gtest/gtest.h>

#include "../src/generate_task_set.h"
#include "../src/schedulability.h"

/* TEST TASK SET */ 

TEST(GenerateTaskSet, GenerateRandomTaskSet) {
  random_device random_device;
  mt19937 generator(random_device());
  uniform_real_distribution<double> distribution(0.1, 0.9);
  
  double random_target_u = distribution(generator);
  TaskSet random_task_set = TaskSet(random_target_u, 0.5, 4);
  
  EXPECT_LT(random_target_u - random_task_set.get_utilization(), 0.05);
  EXPECT_GT(random_task_set.calculate_t_max(), 0);
  EXPECT_GT(random_task_set.get_num_tasks(), 0);
  EXPECT_EQ(random_task_set.get_num_tasks(), random_task_set.get_task_set().size());
}

TEST(GenerateTaskSet, TaskSetTMax) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 414, 13, 13, 300, 300), Task(3, 115, 14, 14, 267, 267), Task(5, 94, 7, 7, 172, 172)};
  task_set_dict["hi"] = {Task(1, 122, 23, 46, 312, 312), Task(2, 108, 18, 37, 107, 107), Task(4, 132, 15, 50, 233, 233)};
  TaskSet task_set = TaskSet(task_set_dict);
  
  EXPECT_EQ(task_set.calculate_t_max(), 224);
}

TEST(GenerateTaskSet, ConstrainDeadlines) {
  TaskSet random_task_set = TaskSet(0.5);

  TaskSet random_task_set_copy = random_task_set;
  random_task_set_copy.constrain_deadlines();

  EXPECT_NE(&random_task_set, &random_task_set_copy);
  for (auto& [key, task] : random_task_set_copy.get_task_set()) {
    EXPECT_LE(task.D, task.T);
  }
}

/* TEST OVERLOADED OPERATOR */ 

TEST(GenerateTaskSet, AssignmentAndEqualOperator) {
  TaskSet random_task_set = TaskSet(0.5);
  random_task_set.set_thm1(schedulability_test_thm1_parallel(random_task_set));
  random_task_set.set_thm2(schedulability_test_thm2(random_task_set));
  random_task_set.set_thm3(schedulability_test_thm3(random_task_set));

  TaskSet copy_task_set = random_task_set;

  EXPECT_NE(&random_task_set, &copy_task_set);
  EXPECT_EQ(random_task_set.get_num_tasks(), copy_task_set.get_num_tasks());
  EXPECT_LT(random_task_set.get_utilization() - copy_task_set.get_utilization(), 0.05);
  EXPECT_EQ(random_task_set.get_t_max(), copy_task_set.get_t_max());
  EXPECT_EQ(random_task_set.get_thm1(), copy_task_set.get_thm1());
  EXPECT_EQ(random_task_set.get_thm2(), copy_task_set.get_thm2());
  EXPECT_EQ(random_task_set.get_thm3(), copy_task_set.get_thm3());
  for (int i = 0; i < random_task_set.get_num_tasks(); ++i) {
    EXPECT_EQ(random_task_set.get_task_set()[i], copy_task_set.get_task_set()[i]);
  }

  EXPECT_TRUE(random_task_set == random_task_set);
  EXPECT_TRUE(random_task_set == copy_task_set);
}

#endif