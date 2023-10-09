#ifndef SCHEDULABILITY_H
#define SCHEDULABILITY_H

#include "/opt/homebrew/Cellar/libomp/17.0.2/include/omp.h"

#include "dbfs.h"

bool schedulability_test_thm1_parallel(TaskSet& task_set) {
  int t_max = task_set.get_t_max(); 

  if (t_max == 0) return false;

  bool is_schedulable = true;

  #pragma omp parallel for
  for (int i = 2; i < t_max + 1; ++i) {
    bool local_is_schedulable = true;
    for (int j = 1; j < i; ++j) {
      if (sum_dbf(task_set, i, j) > i) {
        local_is_schedulable = false;
        break;
      }
    }

    #pragma omp critical
    {
      if (!local_is_schedulable) is_schedulable = false;
    }
  }

  return is_schedulable;
}

bool schedulability_test_thm1(TaskSet& task_set) {
  if (task_set.get_t_max() == 0) return false;

  for (int i = 2; i < task_set.get_t_max() + 1; ++i) {
    for (int j = 1; j < i; ++j) {
      if (sum_dbf(task_set, i, j) > i) {
        return false;
      }
    }
  }
  return true;
}

bool schedulability_test_thm2(TaskSet& task_set) {
  if (task_set.get_t_max() == 0) return false;

  for (int i = 1; i < task_set.get_t_max() + 1; ++i) {
    if (sum_dbf_LO(task_set, i) > i) {
      return false;
    }
  }
  return true;
}

bool schedulability_test_thm3(TaskSet& task_set) {
  if (task_set.get_t_max() == 0) return false;

  for (int i = 1; i < task_set.get_t_max() + 1; ++i) {
    if (sum_dbf_HI(task_set, i, 0) > i) {
      return false;
    }
  }
  return true;
}

#endif