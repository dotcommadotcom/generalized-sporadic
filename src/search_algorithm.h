#ifndef SEARCH_ALGORITHM_H
#define SEARCH_ALGORITHM_H

#include <deque>
#include <algorithm>
#include <string>

#include "schedulability.h"

bool is_eligible(TaskSet& task_set) {
  return !task_set.get_thm1() && task_set.get_thm2() && task_set.get_thm3();
}

deque<int> get_best_candidates(TaskSet& task_set) {
  vector<Task> hi_tasks;

  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      hi_tasks.push_back(task);
    }
  }

  sort(hi_tasks.begin(), hi_tasks.end(), [](const Task& a, const Task& b) {
    return (a.C_HI - a.C_LO) > (b.C_HI - b.C_LO);
  });

  deque<int> candidates;
  for (const auto& task : hi_tasks) {
    candidates.push_back(task.ID);
  }

  return candidates;
}

deque<int> get_hi_candidates(TaskSet& task_set) {
  deque<int> candidates;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      candidates.push_back(task.ID);
    }
  }
  return candidates;
}

pair<int, int> get_failure_time(TaskSet& task_set) {
  for (int i = 2; i < task_set.get_t_max() + 1; ++i) {
    for (int j = 1; j < i; ++j) {
      if (sum_dbf(task_set, i, j) > i) {
        return {i, j};
      }
    }
  }
  return {-1, -1};
}

bool is_demand_at_minimum(int T, int C_LO, int D, int ts) {
  return ts < C_LO || ts - floor((ts - 1) / T) * T > D;
}

int find_optimal_tight_D(int T, int C_LO, int previous_tight_D, int ts) {
  for (int n = 0; n <= (ts - 1) / T + 1; ++n) {
    if (C_LO <= ts - n * T && ts - n * T < previous_tight_D) {
      return ts - n * T;
    }
  }
  return previous_tight_D;
}

string deadline_search_algorithm(TaskSet& task_set) {
  if (!is_eligible(task_set)) return "Not eligible for deadline-tightening";

  deque<int> candidates = get_best_candidates(task_set);
  int best_candidate = -1;
  auto [t, ts] = get_failure_time(task_set);

  while (!candidates.empty()) {
    best_candidate = candidates.front();
    candidates.pop_front();

    int T = task_set.task_set[best_candidate].T;
    int C_LO = task_set.task_set[best_candidate].C_LO;
    int D = task_set.task_set[best_candidate].D;
    int previous_tight_D = task_set.task_set[best_candidate].tight_D;

    if (is_demand_at_minimum(T, C_LO, D, ts)) {
      continue;
    }

    task_set.task_set[best_candidate].tight_D = find_optimal_tight_D(T, C_LO, previous_tight_D, ts);
    if (task_set.task_set[best_candidate].tight_D == previous_tight_D) {
      continue;
    }

    if (!schedulability_test_thm2_3(task_set)) {
      task_set.task_set[best_candidate].tight_D = previous_tight_D;
      continue;
    }

    auto [t, ts] = get_failure_time(task_set);
    if (t == -1 && ts == -1) {
      task_set.set_thm1(true);
      return "Success";
    }

    candidates.push_front(best_candidate);
  }

  return "No more eligible candidates";
}

string naive_algorithm(TaskSet& task_set) {
  if (!is_eligible(task_set)) return "Not eligible for deadline-tightening";

  deque<int> candidates = get_hi_candidates(task_set);
  int best_candidate = -1;
  auto [t, ts] = get_failure_time(task_set);

  while (!candidates.empty()) {
    best_candidate = candidates.front();
    candidates.pop_front();

    int C_LO = task_set.task_set[best_candidate].C_LO;
    int previous_tight_D = task_set.task_set[best_candidate].tight_D;

    task_set.task_set[best_candidate].tight_D -= 1;
    
    if (task_set.task_set[best_candidate].tight_D < C_LO) {
      task_set.task_set[best_candidate].tight_D = previous_tight_D;
      continue;
    }
    
    if (!schedulability_test_thm2_3(task_set)) {
      task_set.task_set[best_candidate].tight_D = previous_tight_D;
      continue;
    }

    auto [t, ts] = get_failure_time(task_set);
    if (t == -1 && ts == -1) {
      task_set.set_thm1(true);
      return "Success";
    }

    candidates.push_front(best_candidate);
  }

  return "No more eligible candidates";
}

#endif
