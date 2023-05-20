import pytest
import random as r
from collections import deque
import copy

from generate_tasks import Task, Task_Set, generate_task, Level
import schedulability as s
import dbfs as dbf
import search_algorithm as alg

@pytest.fixture
def random_hi_task():
  while True:
    task = generate_task(r.uniform(0.02, 0.5))
    if task.L == Level.HI:
      return task

@pytest.fixture
def random_task_set():
  return Task_Set(target_u = 0.6)

@pytest.fixture
def task_set_thm1_true():
  task_set_dict = {'num_tasks': 5, 
                   't_max': 218, 
                   'utilization': 0.4952857806657366, 
                   'thm1': True, 
                   'thm2': True, 
                   'thm3': True, 
                   'lo_tasks_list': [Task(0, 227, 6, 6, 46, 46)], 
                   'hi_tasks_list': [Task(1, 231, 8, 30, 363, 363), Task(2, 66, 14, 36, 150, 150), Task(3, 39, 7, 21, 396, 396), Task(4, 352, 15, 55, 129, 129)]
                   }
  
  return Task_Set(ts_dict = task_set_dict)

@pytest.fixture
def task_set2():
  task_set_dict = {'num_tasks': 4, 
                  't_max': 77, 
                  'utilization': 0.49624662388746893, 
                  'thm1': False, 
                  'thm2': True, 
                  'thm3': True, 
                  'lo_tasks_list': [Task(0, 142, 17, 17, 63, 63)],
                  'hi_tasks_list': [Task(1, 111, 19, 52, 58, 58), Task(2, 224, 14, 48, 284, 284), Task(3, 49, 7, 17, 162, 162)]
                  }
  
  return Task_Set(ts_dict = task_set_dict)

@pytest.fixture
def task_set():
  task_set_dict = {'num_tasks': 3, 
                   't_max': 61, 
                   'utilization': 0.5900067674261222, 
                   'thm1': False, 
                   'thm2': True, 
                   'thm3': True, 
                   'lo_tasks_list': [Task(2, 62, 11, 11, 19, 19)],
                   'hi_tasks_list': [Task(0, 26, 5, 23, 31, 31), Task(1, 55, 10, 27, 356, 356)]
                   }
  
  return Task_Set(ts_dict = task_set_dict)

''' TEST TIGHT D THEOREMS '''

def test_tight_D_reduced(random_task_set):
  id = r.choice(range(random_task_set.num_tasks))
  tight_task_set = copy.deepcopy(random_task_set)

  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO

  assert tight_task_set.task_set[id].tight_D != random_task_set.task_set[id].tight_D

def test_hi_demand_change_is_zero(random_task_set):
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  t, ts = 1000, 500
  previous_hi_demand = dbf.sum_dbf_HI(random_task_set, t, ts)
  tight_task_set = copy.deepcopy(random_task_set)
  
  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO

  assert previous_hi_demand == dbf.sum_dbf_HI(tight_task_set, t, ts)

def test_un_demand_change_is_zero(random_task_set):
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  t, ts = 1000, 500
  previous_un_demand = dbf.sum_dbf_UN(random_task_set, t, ts)
  tight_task_set = copy.deepcopy(random_task_set)
  
  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO

  assert previous_un_demand == dbf.sum_dbf_UN(tight_task_set, t, ts)

def test_co_demand_change_leq_zero(random_task_set):
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  t, ts = 1000, 500
  previous_co_demand = dbf.sum_dbf_CO(random_task_set, t, ts)
  tight_task_set = copy.deepcopy(random_task_set)
  
  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO

  assert 0 >= dbf.sum_dbf_CO(tight_task_set, t, ts) - previous_co_demand

def test_co_demand_change_geq_zero(random_task_set):
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  ts = 500
  previous_lo_demand = dbf.sum_dbf_LO(random_task_set, ts)
  tight_task_set = copy.deepcopy(random_task_set)
  
  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO

  assert 0 <= dbf.sum_dbf_LO(tight_task_set, ts) - previous_lo_demand

def test_demand_change_decrease_iff_lo_less_co(random_task_set):
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  t, ts = 1000, 500
  previous_demand = dbf.sum_dbf(random_task_set, t, ts)
  previous_demand_lo = dbf.sum_dbf_LO(random_task_set, ts)
  previous_demand_co = dbf.sum_dbf_CO(random_task_set, t, ts)
  tight_task_set = copy.deepcopy(random_task_set)

  tight_task_set.task_set[id].tight_D = tight_task_set.task_set[id].C_LO
  demand_change = dbf.sum_dbf(tight_task_set, t, ts) - previous_demand
  lo_change = dbf.sum_dbf_LO(tight_task_set, ts) - previous_demand_lo
  co_change = dbf.sum_dbf_CO(tight_task_set, t, ts) - previous_demand_co
  
  assert (demand_change < 0 and abs(lo_change) < abs(co_change)) \
        or (demand_change >= 0 and abs(lo_change) >= abs(co_change))
  
def test_dbf_lo_is_0_ts_less_tight_D(random_hi_task):
  random_hi_task.tight_D = r.choice([random_hi_task.C_LO, random_hi_task.D])
  ts = random_hi_task.tight_D - 1

  assert dbf.demand_based_function_LO(random_hi_task, ts) == 0

def test_lower_is_0_ts_less_tight_D(random_hi_task):
  random_hi_task.tight_D = r.choice([random_hi_task.C_LO, random_hi_task.D])
  ts = random_hi_task.tight_D - 1

  assert dbf.lower(random_hi_task, ts) == 0

def test_tight_D_changes_at_ts_nT(random_hi_task):
  t = 1000
  ts = r.randrange(random_hi_task.D, t)
  tight_D_list = [ts - n * random_hi_task.T for n in range((ts - 1)//random_hi_task.T + 1)]
  previous_max_request = dbf.max_requests(random_hi_task.T, ts, ts)

  change_list = [ts]
  for i in range(ts, 0, -1):
    current_max_request = dbf.max_requests(random_hi_task.T, ts, i)
    if previous_max_request != current_max_request:
      change_list.append(i)
      previous_max_request = current_max_request

  assert tight_D_list == change_list

def test_demand_no_change_with_tight_D_under_conditions(random_hi_task):
  t = 1000
  while True:
    ts = r.randrange(1, t)
    if ts < random_hi_task.C_LO or ts - ((ts - 1)//random_hi_task.T) * random_hi_task.T > random_hi_task.D:
      break
  previous_task_demand = dbf.demand_based_function_LO(random_hi_task, ts) + dbf.demand_based_function_CO(random_hi_task, t, ts)
  tight_task = copy.deepcopy(random_hi_task)
  tight_task.tight_D = r.randrange(tight_task.C_LO, tight_task.D + 1)

  demand_change = dbf.demand_based_function_LO(tight_task, ts) + dbf.demand_based_function_CO(tight_task, t, ts) - previous_task_demand

  assert demand_change == 0








# ''' TEST EXAMPLE '''

# def test_task_set_greedy_sched_tight_D_is_9(task_set):
#   task_set.task_set[0].tight_D = 9

#   assert all([s.schedulability_test_thm1(task_set), s.schedulability_test_thm2(task_set), s.schedulability_test_thm3(task_set)])
  
# def test_task_set2_greedy_sched_tight_D_is_9(task_set2):
#   assert alg.initialize_candidates(task_set2) == deque([2, 1, 3])
#   assert alg.get_failure_time(task_set2) == (63, 12)

#   task_set2.task_set[3].tight_D = 12
#   assert alg.get_failure_time(task_set2) == (58, 12)
#   assert alg.is_demand_at_minimum(task_set2.task_set[3].T, task_set2.task_set[3].C_LO, task_set2.task_set[3].D, 12) is True

#   task_set2.task_set[3].tight_D = 7

#   assert all([s.schedulability_test_thm1(task_set2), s.schedulability_test_thm2(task_set2), s.schedulability_test_thm3(task_set2)])


  
''' TEST IS ELIGIBLE '''

def test_is_eligible_is_false_thm2_is_false(task_set):
  task_set.thm1, task_set.thm2, task_set.thm3= False, True, False

  assert alg.is_eligible(task_set) is False

def test_is_eligible_is_false_thm3_is_false(task_set):
  task_set.thm1, task_set.thm2, task_set.thm3= False, False, True

  assert alg.is_eligible(task_set) is False

def test_is_eligible_is_false_thm1_is_true(task_set):
  task_set.thm1, task_set.thm2, task_set.thm3= True, True, True

  assert alg.is_eligible(task_set) is False

def test_is_eligible_is_true(task_set):
  task_set.thm1, task_set.thm2, task_set.thm3= False, True, True

  assert alg.is_eligible(task_set) is True

''' TEST MAX DIFFERENCE WCET HEURISTIC '''

def test_find_max_wcet_difference_is_zero(task_set):
  assert alg.find_max_wcet_difference(task_set) == 0

def test_find_max_wcet_difference_no_candidates(task_set):
  task_set.hi_tasks_list = []

  assert alg.find_max_wcet_difference(task_set) == -1

''' TEST INITIALIZE CANDIDATES '''

def test_initialize_candidates_is_correct(task_set):
  assert alg.initialize_candidates(task_set) == deque([0, 1])

def test_initialize_candidates_is_equal_length_hi_tasks(random_task_set):
  candidates = alg.initialize_candidates(random_task_set)

  assert len(candidates) == len(random_task_set.hi_tasks_list)

def test_initialize_candidates_top_max_wcet_difference(random_task_set):
  candidates = alg.initialize_candidates(random_task_set)

  assert len(random_task_set.hi_tasks_list) == 0 or \
    all(task.C_HI - task.C_LO <= random_task_set.task_set[candidates[0]].C_HI - random_task_set.task_set[candidates[0]].C_LO for task in random_task_set.hi_tasks_list)

''' TEST GET FAILURE TIME  '''

def test_get_failure_time_thm1_true(task_set_thm1_true):
  assert alg.get_failure_time(task_set_thm1_true) == (-1, -1)

def test_get_failure_time_task_set(task_set):
  assert alg.get_failure_time(task_set) == (31, 9)

''' TEST IS DEMAND AT MINIMUM  '''

def test_is_demand_at_minimum_true_ts_less_CLO():
  ts = 6
  task = Task(-1, 49, 7, 17, 162, 162)

  assert ts - ((ts - 1)//task.T) * task.T <= task.D
  assert alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is True

def test_is_demand_at_minimum_true_ts_greater_D():
  ts = 1000
  task = Task(-1, 163, 7, 17, 21, 21)

  assert ts >= task.C_LO
  assert alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is True

def test_is_demand_at_minimum_false(task_set):
  ts = 9
  task = task_set.task_set[0]

  assert alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is False



# def test_get_failure_time_task_set(task_set):
#   assert alg.get_failure_time(task_set) == (31, 9)

# ''' TEST GREEDY FUNCTIONALITY'''

# def test_greedy_not_eligible_task_set(task_set_not_eligible, default_heuristic):
#   assert alg.greedy_search(task_set_not_eligible, default_heuristic) ==  ("Not eligible for deadline-tightening", task_set_not_eligible)

# def test_task_set_schedulable_1_is_false(task_set):
#   assert task_set.thm1 is False

# def test_greedy_is_True(task_set, default_heuristic):
#   greedy_result, _ = alg.greedy_search(task_set, default_heuristic)

#   assert greedy_result is True

# def test_greedy_decreases_sum_dbf(task_set):
#   i, j = alg.get_failure_time(task_set, 2, 1)
#   before = dbf.sum_dbf(task_set, i, j)
#   candidates = alg.initialize_candidates(task_set)
#   best_candidate = alg.find_max_wcet_difference(candidates, task_set) 

#   task_set.task_set[best_candidate].tight_D = task_set.task_set[best_candidate].C_LO

#   assert dbf.sum_dbf(task_set, i, j) < before

# def test_task_set_after_greedy_failure_time_neg(task_set, default_heuristic):
#   _, task_set_post_greedy = alg.greedy_search(task_set, default_heuristic)

#   assert alg.get_failure_time(task_set_post_greedy) == (-1, -1)

# def test_task_set_after_greedy_decreased_tight_D(task_set, default_heuristic):
#   _, task_set_post_greedy = alg.greedy_search(task_set, default_heuristic)

#   assert any(task.tight_D < task.D for task in task_set_post_greedy.task_set.values())

# def test_after_greedy_decreased_tight_D_or_not_eligible(random_task_set, default_heuristic):
#   eligibility, random_task_set_post_greedy = alg.greedy_search(random_task_set, default_heuristic)

#   assert eligibility == "Not eligible for deadline-tightening" or any([task.tight_D < task.D for task in random_task_set_post_greedy.task_set.values()])

# def test_after_greedy_tight_D_greater_C_LO(random_task_set, default_heuristic):
#   _, random_task_set_post_greedy = alg.greedy_search(random_task_set, default_heuristic)

#   assert all(task.tight_D >= task.C_LO for task in random_task_set_post_greedy.task_set.values())

# # sometimes produces errors
# def test_after_greedy_sched2_is_true(random_task_set, default_heuristic):
#   _, random_task_set_post_greedy = alg.greedy_search(random_task_set, default_heuristic)

#   assert s.schedulability_test_thm2(random_task_set_post_greedy) is True

# def test_greedy_fails_no_more_candidates(task_set_no_greedy, default_heuristic):
#   greedy_result, _ = alg.greedy_search(task_set_no_greedy, default_heuristic)

#   assert greedy_result == "No more eligible candidates" 