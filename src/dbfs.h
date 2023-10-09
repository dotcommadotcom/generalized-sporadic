#ifndef DBFS_H
#define DBFS_H

#include <algorithm>
#include <cmath>

#include "generate_task_set.h"

int max_requests(double T, double upper, double lower) {
  auto floor_fraction = floor((upper - lower) / T);
  
  return max(0, static_cast<int>(floor_fraction) + 1);
}

double lower(const Task& task, double ts) {
  return task.T * max_requests(task.T, ts, task.tight_D);
}

double upper_CO(const Task& task, double t, double ts) {
  return t - task.D - task.T * max_requests(task.T, t - ts, task.D);
}

double upper_UN(const Task& task, double t, double ts) {
  return min(ts, t - task.tight_D);
}

double demand_based_function(double C, double T, double upper, double lower) {
  return C * max_requests(T, upper, lower);
}

double demand_based_function_LO(const Task& task, double ts) {
  return demand_based_function(task.C_LO, task.T, ts, task.tight_D);
}

double demand_based_function_HI(const Task& task, double t, double ts) {
  return demand_based_function(task.C_HI, task.T, t - task.D, ts);
}

double demand_based_function_CO(const Task& task, double t, double ts) {
  return demand_based_function(task.C_HI, task.T, upper_CO(task, t, ts), lower(task, ts));
}

double demand_based_function_UN(const Task& task, double t, double ts) {
  int k = max_requests(task.T, upper_UN(task, t, ts), lower(task, ts));
  return min(static_cast<double>(task.C_LO), ts - lower(task, ts) - (k - 1) * task.T / (double)2) * k;
}

double sum_dbf_LO(const TaskSet& task_set, double ts) {
  double sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    sum += demand_based_function_LO(task, ts);
  }
  return sum;
}

double sum_dbf_HI(const TaskSet& task_set, double t, double ts) {
  double sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      sum += demand_based_function_HI(task, t, ts);
    }
  }
  return sum;
}

double sum_dbf_CO(const TaskSet& task_set, double t, double ts) {
  double sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      sum += demand_based_function_CO(task, t, ts);
    }
  }
  return sum;
}

double sum_dbf_UN(const TaskSet& task_set, double t, double ts) {
  double sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == LO) {
      sum += demand_based_function_UN(task, t, ts);
    }
  }
  return sum;
}

double sum_dbf(const TaskSet& task_set, double t, double ts) {
  double demand_sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.C_LO < task.C_HI) {
      demand_sum += demand_based_function_HI(task, t, ts) + demand_based_function_CO(task, t, ts);
    } else {
      demand_sum += demand_based_function_UN(task, t, ts);
    }
    demand_sum += demand_based_function_LO(task, ts);
  }
  return demand_sum;
}

#endif
