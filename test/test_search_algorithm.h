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
  TaskSet TaskSet1 = TaskSet({}, true, true, true);
  TaskSet TaskSet2 = TaskSet({}, true, true, false);
  TaskSet TaskSet3 = TaskSet({}, true, false, true);
  TaskSet TaskSet4 = TaskSet({}, true, false, false);
  TaskSet TaskSet5 = TaskSet({}, false, true, false);
  TaskSet TaskSet6 = TaskSet({}, false, false, true);
  TaskSet TaskSet7 = TaskSet({}, false, false, false);
  TaskSet TaskSetEligible = TaskSet({}, false, true, true);

  EXPECT_FALSE(is_eligible(TaskSet1));
  EXPECT_FALSE(is_eligible(TaskSet2));
  EXPECT_FALSE(is_eligible(TaskSet3));
  EXPECT_FALSE(is_eligible(TaskSet4));
  EXPECT_FALSE(is_eligible(TaskSet5));
  EXPECT_FALSE(is_eligible(TaskSet6));
  EXPECT_FALSE(is_eligible(TaskSet7));
  EXPECT_TRUE(is_eligible(TaskSetEligible));
}

TEST(SearchAlgorithm, GetBestCandidates) {
  TaskSet random_task_set = TaskSet(0.6);
  int ts = 500;

  deque<int> candidates = get_best_candidates(random_task_set);
  int best_candidate = candidates.front();

  EXPECT_EQ(candidates.size(), random_task_set.get_hi_count());
  for (const auto& [key, task] : random_task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_TRUE(task.C_HI - task.C_LO <= random_task_set.task_set[best_candidate].C_HI - random_task_set.task_set[best_candidate].C_LO);
    }
  }
}

TEST(SearchAlgorithm, NaiveGetHiCandidates) {
  TaskSet random_task_set = TaskSet(0.5);

  deque<int> hi_candidates = get_hi_candidates(random_task_set);

  EXPECT_EQ(hi_candidates.size(), random_task_set.get_hi_count());
  for (size_t i = 0; i < hi_candidates.size(); i++) {
    EXPECT_EQ(random_task_set.get_task_set()[hi_candidates[i]].L, HI);
  }
}

TEST(SearchAlgorithm, FailureTimeExists) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  
  TaskSet task_set = TaskSet(task_set_dict);
  deque<int> expected_candidates = {0, 1};
  pair<int, int> expected_failure_time = {31, 9};

  EXPECT_EQ(get_best_candidates(task_set), expected_candidates);
  EXPECT_EQ(get_failure_time(task_set), expected_failure_time);
}

TEST(SearchAlgorithm, FailureTimeDoesNotExist) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0, 227, 6, 6, 46, 46)};
  task_set_dict["hi"] = {Task(1, 231, 8, 30, 363, 363), Task(2, 66, 14, 36, 150, 150), Task(3, 39, 7, 21, 396, 396), Task(4, 352, 15, 55, 129, 129)};
  
  TaskSet task_set = TaskSet(task_set_dict);
  deque<int> expected_candidates = {4, 1, 2, 3};
  pair<int, int> expected_failure_time = {-1, -1};

  EXPECT_EQ(get_best_candidates(task_set), expected_candidates);
  EXPECT_EQ(get_failure_time(task_set), expected_failure_time);
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

  for (const auto& [key, task] : random_task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.C_LO);
      EXPECT_LE(find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts), task.D);
    }
  }
}

TEST(SearchAlgorithm, FindOptimalTightDTask) {
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

TEST(SearchAlgorithm, DemandSumDecreasesWithTightenedDeadlines) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(2, 62, 11, 11, 19, 19)};
  task_set_dict["hi"] = {Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)};
  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
  task_set.set_thm2(schedulability_test_thm2(task_set));
  task_set.set_thm3(schedulability_test_thm3(task_set));
  auto [t, ts] = get_failure_time(task_set);
  int best_candidate = get_best_candidates(task_set).front();

  int before_demand = sum_dbf(task_set, t, ts);
  task_set.task_set[best_candidate].tight_D = find_optimal_tight_D(task_set.task_set[best_candidate].T, task_set.task_set[best_candidate].C_LO, task_set.task_set[best_candidate].tight_D, ts);
  pair<int, int> expected_failure_time = {-1, -1};

  EXPECT_LT(task_set.get_task_set()[best_candidate].tight_D, task_set.get_task_set()[best_candidate].D);
  EXPECT_LT(sum_dbf(task_set, t, ts), before_demand);
  EXPECT_EQ(get_failure_time(task_set), expected_failure_time);
}

/* TEST DEADLINE SEARCH ALGORITHM */

TEST(SearchAlgorithm, EDSNotEligible) {
  TaskSet task_set = TaskSet({}, true, false, false);

  EXPECT_FALSE(is_eligible(task_set));
  EXPECT_EQ(deadline_search_algorithm(task_set), "Not eligible for deadline-tightening");
}

TEST(SearchAlgorithm, EDSTightDWithinBounds) {
  TaskSet task_set = TaskSet(0.5);

  deadline_search_algorithm(task_set); 
  
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(task.tight_D, task.C_LO);
      EXPECT_LE(task.tight_D, task.D);
    }
  }
}

TEST(SearchAlgorithm, EDSNoMoreEligible) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = { Task(0,18,5,5,7,7), \
                          Task(2,197,24,24,473,473), \
                          Task(4,118,16,16,315,315), \
                          Task(5,157,22,22,277,277)};
  task_set_dict["hi"] = { Task(1,360,24,94,377,377), \
                          Task(3,480,12,29,33,33)};

  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
  task_set.set_thm2(schedulability_test_thm2(task_set));
  task_set.set_thm3(schedulability_test_thm3(task_set));

  EXPECT_TRUE(is_eligible(task_set));
  EXPECT_EQ(deadline_search_algorithm(task_set), "No more eligible candidates");
}

TEST(SearchAlgorithm, EDSSuccess) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0,230,16,16,158,158), \
                         Task(6,427,23,23,202,202), \
                         Task(7,124,11,11,467,467), \
                         Task(9,397,21,21,82,82)};
  task_set_dict["hi"] = {Task(1,353,25,78,497,497), \
                         Task(2,473,19,45,314,314), \
                         Task(3,293,16,34,87,87), \
                         Task(4,394,11,31,59,59), \
                         Task(5,492,24,90,232,232), \
                         Task(8,473,7,16,255,255)};
                          
  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
  task_set.set_thm2(schedulability_test_thm2(task_set));
  task_set.set_thm3(schedulability_test_thm3(task_set));

  pair<int, int> expected_failure_time = {-1, -1};

  EXPECT_TRUE(is_eligible(task_set));
  EXPECT_EQ(deadline_search_algorithm(task_set), "Success");
  EXPECT_EQ(task_set.get_num_tasks(), 10);
  EXPECT_EQ(get_failure_time(task_set), expected_failure_time);
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(task.tight_D, task.C_LO);
      EXPECT_LE(task.tight_D, task.D);
    }
  }
}

/* TEST NAIVE SEARCH ALGORITHM */

TEST(SearchAlgorithm, NaiveNotEligible) {
  TaskSet task_set = TaskSet({}, true, false, false);

  EXPECT_FALSE(is_eligible(task_set));
  EXPECT_EQ(naive_algorithm(task_set), "Not eligible for deadline-tightening");
}

TEST(SearchAlgorithm, NaiveTightDWithinBounds) {
  TaskSet task_set = TaskSet(0.1);

  naive_algorithm(task_set); 
  
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(task.tight_D, task.C_LO);
      EXPECT_LE(task.tight_D, task.D);
    }
  }
}

TEST(SearchAlgorithm, NaiveNoMoreEligible) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = { Task(0,18,5,5,7,7), \
                          Task(2,197,24,24,473,473), \
                          Task(4,118,16,16,315,315), \
                          Task(5,157,22,22,277,277)};
  task_set_dict["hi"] = { Task(1,360,24,94,377,377), \
                          Task(3,480,12,29,33,33)};

  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
  task_set.set_thm2(schedulability_test_thm2(task_set));
  task_set.set_thm3(schedulability_test_thm3(task_set));

  EXPECT_TRUE(is_eligible(task_set));
  EXPECT_EQ(naive_algorithm(task_set), "No more eligible candidates");
}

TEST(SearchAlgorithm, NaiveSuccess) {
  map<string, vector<Task>> task_set_dict = {};
  task_set_dict["lo"] = {Task(0,230,16,16,158,158), \
                         Task(6,427,23,23,202,202), \
                         Task(7,124,11,11,467,467), \
                         Task(9,397,21,21,82,82)};
  task_set_dict["hi"] = {Task(1,353,25,78,497,497), \
                         Task(2,473,19,45,314,314), \
                         Task(3,293,16,34,87,87), \
                         Task(4,394,11,31,59,59), \
                         Task(5,492,24,90,232,232), \
                         Task(8,473,7,16,255,255)};
                          
  TaskSet task_set = TaskSet(task_set_dict);
  task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
  task_set.set_thm2(schedulability_test_thm2(task_set));
  task_set.set_thm3(schedulability_test_thm3(task_set));
  pair<int, int> expected_failure_time = {-1, -1};

  EXPECT_TRUE(is_eligible(task_set));
  EXPECT_EQ(deadline_search_algorithm(task_set), "Success");
  EXPECT_EQ(task_set.get_num_tasks(), 10);
  EXPECT_EQ(get_failure_time(task_set), expected_failure_time);
  for (const auto& [key, task] : task_set.get_task_set()) {
    if (task.L == HI) {
      EXPECT_GE(task.tight_D, task.C_LO);
      EXPECT_LE(task.tight_D, task.D);
    }
  }
}

/* TEST SEARCH ALGORITHM OTHER */

// TEST(SearchAlgorithm, EDSFailsNaiveSucceeds) {
//   map<string, vector<Task>> task_set_dict = {};
//   task_set_dict["lo"] = {Task(0,456,25,25,140,140), \
//                          Task(4,493,23,23,35,35)};
//   task_set_dict["hi"] = {Task(1,395,9,34,50,50), \
//                          Task(2,154,17,36,275,275), \
//                          Task(3,321,11,43,273,273), \
//                          Task(5,197,12,29,409,409)};
                          
//   TaskSet task_set = TaskSet(task_set_dict);
//   task_set.set_thm1(schedulability_test_thm1_parallel(task_set));
//   task_set.set_thm2(schedulability_test_thm2(task_set));
//   task_set.set_thm3(schedulability_test_thm3(task_set));
//   TaskSet naive_task_set = task_set;
//   deque<int> expected_candidates = {3, 1, 2, 5};
//   deque<int> expected_hi_candidates = {1, 2, 3, 5};


//   EXPECT_TRUE(is_eligible(task_set));
//   EXPECT_NE(&task_set, &naive_task_set);
//   EXPECT_EQ(get_best_candidates(task_set), expected_candidates);
//   EXPECT_EQ(get_hi_candidates(naive_task_set), expected_hi_candidates);
//   EXPECT_EQ(deadline_search_algorithm(task_set), "No more eligible candidates");
//   cout << task_set.task_set_to_string() << endl;
//   EXPECT_EQ(naive_algorithm(naive_task_set), "Success");
// }

// TEST(SearchAlgorithm, CopiedTaskSets) {
//   for (int i = 0; i < 100; ++i) {
//     TaskSet eds_task_set = TaskSet(0.35);
//     eds_task_set.set_thm1(schedulability_test_thm1_parallel(eds_task_set));
//     eds_task_set.set_thm2(schedulability_test_thm2(eds_task_set));
//     eds_task_set.set_thm3(schedulability_test_thm3(eds_task_set));
//     if (!is_eligible(eds_task_set)) continue;
//     TaskSet naive_task_set = eds_task_set;

//     string eds_result = deadline_search_algorithm(eds_task_set);
//     string naive_result = naive_algorithm(naive_task_set);

//     EXPECT_NE(&eds_task_set, &naive_task_set);
//     EXPECT_EQ(eds_task_set.get_num_tasks(), naive_task_set.get_num_tasks());
//     EXPECT_EQ(eds_task_set.get_t_max(), naive_task_set.get_t_max());
//     EXPECT_LT(eds_task_set.get_utilization() - naive_task_set.get_utilization(), 0.05);
//     EXPECT_EQ(eds_task_set.get_thm2(), naive_task_set.get_thm2());
//     EXPECT_EQ(eds_task_set.get_thm3(), naive_task_set.get_thm3());

//     if (eds_result != naive_result) {
//       EXPECT_NE(eds_task_set.get_thm1(), naive_task_set.get_thm1());
//       cout << "EDS -- " << eds_result << " -- " << eds_task_set.task_set_to_string() << endl;
//       cout << "NAIVE -- " << naive_result << " -- " << naive_task_set.task_set_to_string() << endl;
//     } else {
//       EXPECT_EQ(eds_task_set.get_thm1(), naive_task_set.get_thm1());
//     }
//   }
// }

#endif