#include "dbfs.h"

double ekberg_lo(const Task& task, double t) {
  return demand_based_function(task.C_LO, task.T, t, task.tight_D);
}

double ekberg_full(const Task& task, double t) {
  return demand_based_function(task.C_HI, task.T, t, task.D - task.tight_D);
}

double ekberg_done(const Task& task, double t) {
  int n = static_cast<int>(t) % static_cast<int>(task.T);

  if (n < task.D - task.tight_D || n >= task.D) { return 0; }

  return max(task.C_LO - n + task.D - task.tight_D, 0);
}

double ekberg_hi(const Task& task, double t) {
  return ekberg_full(task, t) - ekberg_done(task, t);
}

double ekberg_hi_sum(const TaskSet& task_set, double t) {
  double demand_sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.C_LO < task.C_HI) {
      demand_sum += ekberg_hi(task, t);
    } 
  }
  return demand_sum;
}

double ekberg_lo_sum(const TaskSet& task_set, double t) {
  double demand_sum = 0;
  for (const auto& [key, task] : task_set.get_task_set()) {
    demand_sum += ekberg_lo(task, t);
  }
  return demand_sum;
}

bool ekberg_thm1(TaskSet& task_set) {
  if (task_set.get_t_max() == 0) return false;

  for (int i = 0; i < task_set.get_t_max() + 1; ++i) {
    if (ekberg_lo_sum(task_set, i) > i) {
      return false;
    } 
  }
  return true;
}

bool ekberg_thm2(TaskSet& task_set) {
  if (task_set.get_t_max() == 0) return false;

  for (int i = 0; i < task_set.get_t_max() + 1; ++i) {
    if (ekberg_hi_sum(task_set, i) > i) {
      return false;
    }
  }
  return true;
}

bool ekberg_is_eligible(TaskSet& task_set) {
  return !task_set.get_thm1() || !task_set.get_thm2();
}

vector<int> get_hi_candidates_vector(TaskSet& task_set) {
  vector<int> hi_tasks;

  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      hi_tasks.push_back(task.ID);
    }
  }

  return hi_tasks;
}

int get_max_demand_candidate(vector<int>& candidates, TaskSet& task_set, int t) {
  int max_demand_difference = 0, max_candidate = -1;
  for (const auto& id : candidates) {
    int current_demand_difference = ekberg_hi(task_set.task_set[id], t) - ekberg_hi(task_set.task_set[id], t - 1);
    max_candidate = current_demand_difference > max_demand_difference ? id : max_candidate;
    max_demand_difference = current_demand_difference > max_demand_difference ? current_demand_difference : max_demand_difference;
  }
  return max_candidate;
}

pair<string, TaskSet> ekberg_algorithm(TaskSet& task_set) {
  if (!ekberg_is_eligible(task_set)) return {"Not eligible for deadline-tightening", task_set};

  vector<int> candidates = get_hi_candidates_vector(task_set);
  int best_candidate = -1;

  while (!candidates.empty()) {
    bool result = true;

    for (int i = 0; i < task_set.get_t_max() + 1; ++i) {
      if (ekberg_lo_sum(task_set, i) > i) {
        if (best_candidate == -1) return {"No more eligible candidates", task_set};
        task_set.task_set[best_candidate].tight_D += 1;
        candidates.erase(remove(candidates.begin(), candidates.end(), best_candidate), candidates.end());
        result = false;
      } else if (ekberg_hi_sum(task_set, i) > i) { 
        if (candidates.empty()) return {"No more eligible candidates", task_set};
        
        best_candidate = get_max_demand_candidate(candidates, task_set, i);

        task_set.task_set[best_candidate].tight_D--;
        if (task_set.task_set[best_candidate].tight_D == task_set.task_set[best_candidate].C_LO) {
          candidates.erase(remove(candidates.begin(), candidates.end(), best_candidate), candidates.end());
        }
        result = false;
      }
    }
    if (result) return {"Success", task_set};
  }

  return {"No more eligible candidates", task_set};
}