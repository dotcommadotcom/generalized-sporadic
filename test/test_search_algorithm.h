#ifndef SEARCH_ALGORITHM_TEST
#define SEARCH_ALGORITHM_TEST

#include <gtest/gtest.h>

#include "../src/search_algorithm.h"

/* TEST TIGHT D THEOREMS */

TEST(SearchAlgorithm, DemandChange) {
  int t = 1000, ts = 500;
  TaskSet random_task_set = TaskSet(0.5);

  int previous_hi_demand = sum_dbf_HI(random_task_set, t, ts);
  int previous_un_demand = sum_dbf_UN(random_task_set, t, ts);
  int previous_co_demand = sum_dbf_CO(random_task_set, t, ts);
  int previous_lo_demand = sum_dbf_LO(random_task_set, ts);
  int previous_demand = previous_hi_demand + previous_un_demand + previous_co_demand + previous_lo_demand;

  if (random_task_set.get_hi_count() > 0) {
    int id;
    for (const auto& [key, task] : random_task_set.get_task_set()) {
      if (task.L == HI) {
        id = task.ID;
        break;
      }
    }
    int previous_tight_D  = random_task_set.task_set[id].tight_D;
    random_task_set.task_set[id].tight_D = random_task_set.task_set[id].C_LO;
    
    int demand_change = sum_dbf(random_task_set, t, ts) - previous_demand;
    int co_change = sum_dbf_CO(random_task_set, t, ts) - previous_co_demand;
    int lo_change = sum_dbf_LO(random_task_set, ts) - previous_lo_demand;

    EXPECT_LT(random_task_set.task_set[id].tight_D, previous_tight_D);
    EXPECT_EQ(sum_dbf_HI(random_task_set, t, ts), previous_hi_demand);
    EXPECT_EQ(sum_dbf_UN(random_task_set, t, ts), previous_un_demand);
    EXPECT_LE(co_change, 0);
    EXPECT_GE(lo_change, 0);
    EXPECT_TRUE((demand_change >= 0 && abs(lo_change) >= abs(co_change)) 
              || (demand_change < 0 && abs(lo_change) < abs(co_change)));
  }
}

TEST(SearchAlgorithm, TightDChange) {
  Task random_hi_task = generate_task(-1, 1);
  int t = 1000, ts = 500, previous_max_request = max_requests(random_hi_task.T, t, ts);
  vector<int> expected = {}, change_list = {};
  for (int n = 0; n < floor((ts - 1) / random_hi_task.T) + 1; ++n) {
    expected.push_back(ts - n * random_hi_task.T);
  }

  for (int i = ts; i > 0; --i) {
    int current_max_request = max_requests(random_hi_task.T, ts, i);
    if (previous_max_request != current_max_request) {
      change_list.push_back(i);
      previous_max_request = current_max_request;
    }
  }

  EXPECT_EQ(change_list, expected);
}

TEST(SearchAlgorithm, MinimumDemand) {
  Task random_hi_task = generate_task(-1, 1);
  int t = 1000, ts;
  for (ts = t - 1; ts > 0; --ts) {
    if (is_demand_at_minimum(random_hi_task.T, random_hi_task.C_LO, random_hi_task.D, ts)) {
      break;
    }
  }
  int minimum_demand = demand_based_function_LO(random_hi_task, ts) + demand_based_function_CO(random_hi_task, t, ts);

  while (random_hi_task.C_LO < random_hi_task.tight_D) {
    random_hi_task.tight_D -= 1;
    EXPECT_EQ(demand_based_function_LO(random_hi_task, ts) + demand_based_function_CO(random_hi_task, t, ts), minimum_demand);
  }
}
  
/* TEST SEARCH ALGORITHM HELPER FUNCTIONS */

TEST(SearchAlgorithm, IsEligible) {
  TaskSet TaskSet1 = TaskSet({}, false, true, false);
  TaskSet TaskSet2 = TaskSet({}, false, false, true);
  TaskSet TaskSet3 = TaskSet({}, true, true, true);
  TaskSet TaskSet4 = TaskSet({}, false, true, true);

  EXPECT_FALSE(is_eligible(TaskSet1));
  EXPECT_FALSE(is_eligible(TaskSet2));
  EXPECT_FALSE(is_eligible(TaskSet3));
  EXPECT_TRUE(is_eligible(TaskSet4));
}

TEST(SearchAlgorithm, InitializeCandidates) {
  TaskSet random_task_set = TaskSet(0.6);
  int ts = 500;

  deque<int> candidates = initialize_candidates(random_task_set);
  int best_candidate = candidates[0];

  EXPECT_EQ(candidates.size(), random_task_set.get_hi_count());
  if (random_task_set.get_hi_count() > 0) {
    for (const auto& [key, task] : random_task_set.get_task_set()) {
      if (task.L == HI) {
        EXPECT_TRUE(task.C_HI - task.C_LO <= random_task_set.task_set[best_candidate].C_HI - random_task_set.task_set[best_candidate].C_LO);
        EXPECT_GE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.C_LO);
        EXPECT_LE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.D);
      }
    }
  }
}

TEST(SearchAlgorithm, HelperFunctions) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  
  TaskSet task_set = TaskSet(task_set_dict);
  deque<int> candidates = {0, 1};
  pair<int, int> failure_time = {31, 9};

  EXPECT_EQ(initialize_candidates(task_set), candidates);
  EXPECT_EQ(get_failure_time(task_set), failure_time);
}

TEST(SearchAlgorithm, GetFailureTimeDoesNotFail) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 227, 6, 6, 46, 46)};
  task_set_dict["hi"] = {Task(1, 231, 8, 30, 363, 363), Task(2, 66, 14, 36, 150, 150), Task(3, 39, 7, 21, 396, 396), Task(4, 352, 15, 55, 129, 129)};
  
  TaskSet task_set = TaskSet(task_set_dict);
  pair<int, int> failure_time = {-1, -1};

  EXPECT_EQ(get_failure_time(task_set), failure_time);
}

TEST(SearchAlgorithm, IsDemandAtMinimum) {
  Task task = Task(-1, 163, 7, 17, 21, 21);

  int ts1 = 6;
  int ts2 = 22;
  int ts3 = 21;

  EXPECT_TRUE(ts1 - floor((ts1 - 1)/task.T) * task.T <= task.D && is_demand_at_minimum(task.T, task.C_LO, task.D, ts1));
  EXPECT_TRUE(ts2 >= task.C_LO && is_demand_at_minimum(task.T, task.C_LO, task.D, ts2));
  EXPECT_FALSE(is_demand_at_minimum(task.T, task.C_LO, task.D, 21));
}

TEST(SearchAlgorithm, FindOptimalTightDWithinBounds) {
  int ts = 500;

  TaskSet random_task_set = TaskSet(0.6);

  if (random_task_set.get_hi_count() > 0) {
    for (const auto& [key, task] : random_task_set.get_task_set()) {
      if (task.L == HI) {
        EXPECT_GE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.C_LO);
        EXPECT_LE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.D);
      }
    }
  }
}

TEST(SearchAlgorithm, FindOptimalTightD) {
  int ts = 91;
  Task task = Task(-1, 10, 5, 20, 100, 100);
  int previous_tight_D = task.D;
  vector<int> tight_D_list = {};
  vector<int> expected_tight_D_list = {91, 81, 71, 61, 51, 41, 31, 21, 11};

  while (true) {
    int tight_D = find_optimal_tight_D(task.T, task.C_LO, previous_tight_D, ts);
    if (tight_D == previous_tight_D) break;
    tight_D_list.push_back(tight_D);
    previous_tight_D = tight_D;
  }

  EXPECT_EQ(tight_D_list, expected_tight_D_list);
}

/* TEST SEARCH ALGORITHM */

TEST(SearchAlgorithm, NotEligible) {
  TaskSet task_set = TaskSet({}, true, false, false);

  EXPECT_EQ(deadline_search_algorithm(task_set).first, "Not eligible for deadline-tightening");
}

TEST(SearchAlgorithm, SuccessTaskSet) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(false);
  task_set.set_thm2(true);
  task_set.set_thm3(true);

  string algorithm_result = deadline_search_algorithm(task_set).first;

  EXPECT_EQ(algorithm_result, "Success");
}

TEST(SearchAlgorithm, DemandSumDecrease) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  TaskSet task_set = TaskSet(task_set_dict);
  auto [t, ts] = get_failure_time(task_set);
  task_set.set_thm1(false);
  task_set.set_thm2(true);
  task_set.set_thm3(true);
  int best_candidate = initialize_candidates(task_set).front();
  int T = task_set.task_set[best_candidate].T;
  int C_LO = task_set.task_set[best_candidate].C_LO;
  int previous_tight_D = task_set.task_set[best_candidate].tight_D;

  int before_demand = sum_dbf(task_set, t, ts);
  task_set.task_set[best_candidate].tight_D = find_optimal_tight_D(T, C_LO, previous_tight_D, ts);

  EXPECT_LT(sum_dbf(task_set, t, ts), before_demand);
}

TEST(SearchAlgorithm, TightDDecreased) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(false);
  task_set.set_thm2(true);
  task_set.set_thm3(true);

  int best_candidate = initialize_candidates(task_set).front();
  TaskSet post_algorithm = deadline_search_algorithm(task_set).second;
  pair<int, int> failure_time = get_failure_time(post_algorithm);

  EXPECT_LT(task_set.get_task_set()[best_candidate].tight_D, task_set.get_task_set()[best_candidate].D);
  EXPECT_EQ(failure_time.first, -1);
  EXPECT_EQ(failure_time.second, -1);
}

TEST(SearchAlgorithm, NaiveGetCandidates) {
  TaskSet random_task_set = TaskSet(0.5);

   deque<int> hi_candidates = get_hi_candidates(random_task_set);

   for (size_t i = 0; i < hi_candidates.size(); i++) {
    EXPECT_EQ(random_task_set.get_task_set()[hi_candidates[i]].L, HI);
  }
}

TEST(SearchAlgorithm, NaiveTightD) {
  TaskSet random_task_set = TaskSet(0.5);

  auto [result, changed_task_set] = naive_algorithm(random_task_set);

  for (const auto& [key, task] : changed_task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(task.tight_D, task.C_LO);
      EXPECT_LE(task.tight_D, task.D);
    }
  }
}

#endif