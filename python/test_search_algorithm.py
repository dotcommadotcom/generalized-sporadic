import pytest
import random as r
from collections import deque
import copy

from generate_tasks import Task, Task_Set, generate_task, Level
import schedulability as s
import dbfs as dbf
import search_algorithm as alg

@pytest.fixture
def random_task_set():
  return Task_Set(target_u = 0.6)

@pytest.fixture
def random_hi_task():
  while True:
    task = generate_task(r.uniform(0.02, 0.5))
    if task.L == Level.HI:
      return task

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
  
  return Task_Set(task_set_dict = task_set_dict)

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

def test_demand_at_minimum_under_ts_conditions(random_hi_task):
  t = 1000
  while True:
    ts = r.randrange(1, t)
    if ts < random_hi_task.C_LO or ts - ((ts - 1)//random_hi_task.T) * random_hi_task.T > random_hi_task.D:
      break
  previous_task_demand = dbf.demand_based_function_LO(random_hi_task, ts) + dbf.demand_based_function_CO(random_hi_task, t, ts)
  demand_change_list = []
  previous_tight_D = random_hi_task.tight_D

  while random_hi_task.C_LO < previous_tight_D <= random_hi_task.D:
    tight_task = copy.deepcopy(random_hi_task)
    tight_task.tight_D = previous_tight_D - 1
    demand_change_list.append(dbf.demand_based_function_LO(tight_task, ts) + dbf.demand_based_function_CO(tight_task, t, ts) - previous_task_demand)
    previous_tight_D = tight_task.tight_D 

  assert sum(demand_change_list) == 0
  
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

# ''' TEST MAX DIFFERENCE WCET HEURISTIC '''

# def test_find_max_wcet_difference_is_zero(task_set):
#   assert alg.find_max_wcet_difference(task_set) == 0

# def test_find_max_wcet_difference_no_candidates(task_set):
#   task_set.hi_tasks_list = []

#   assert alg.find_max_wcet_difference(task_set) == -1

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

''' TEST GET FAILURE TIME '''

def test_get_failure_time_neg_thm1_true():
  task_set_dict = {'num_tasks': 5, 
                   't_max': 218, 
                   'utilization': 0.4952857806657366, 
                   'thm1': True, 
                   'thm2': True, 
                   'thm3': True, 
                   'lo_tasks_list': [Task(0, 227, 6, 6, 46, 46)], 
                   'hi_tasks_list': [Task(1, 231, 8, 30, 363, 363), Task(2, 66, 14, 36, 150, 150), Task(3, 39, 7, 21, 396, 396), Task(4, 352, 15, 55, 129, 129)]
                   }
  
  task_set = Task_Set(task_set_dict = task_set_dict)
  
  assert alg.get_failure_time(task_set) == (-1, -1)

def test_get_failure_time_pos_task_set(task_set):
  assert alg.get_failure_time(task_set) == (31, 9)

''' TEST IS DEMAND AT MINIMUM '''

def test_is_demand_at_minimum_true_ts_less_CLO():
  ts = 6
  task = Task(-1, 49, 7, 17, 162, 162)

  assert ts - ((ts - 1)//task.T) * task.T <= task.D and \
    alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is True

def test_is_demand_at_minimum_true_ts_greater_D():
  ts = 1000
  task = Task(-1, 163, 7, 17, 21, 21)

  assert ts >= task.C_LO and alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is True

def test_is_demand_at_minimum_false(task_set):
  ts = 9
  task = task_set.task_set[0]

  assert alg.is_demand_at_minimum(task.T, task.C_LO, task.D, ts) is False

''' TEST FIND OPTIMAL TIGHT D '''

def test_find_optimal_tight_D_is_between_C_LO_and_D(random_task_set):
  ts = r.randrange(1, 1000)
  id = random_task_set.hi_tasks_list[0].ID if len(random_task_set.hi_tasks_list) > 0 else random_task_set.lo_tasks_list[0].ID 
  task = random_task_set.task_set[id]

  assert task.C_LO <= alg.find_optimal_tight_D(task.T, task.C_LO, task.tight_D, ts) <= task.D

def test_find_optimal_tight_D_is_ts_nT():
  ts, task = 91, Task(-1, 10, 5, 20, 100, 100)
  previous_tight_D = 100
  tight_D_list = []

  while True:
    tight_D = alg.find_optimal_tight_D(task.T, task.C_LO, previous_tight_D, ts)
    if tight_D == previous_tight_D:
      break
    tight_D_list.append(tight_D)
    previous_tight_D = tight_D

  assert tight_D_list == [91, 81, 71, 61, 51, 41, 31, 21, 11]

''' TEST SEARCH ALGORITHM '''

def test_search_not_eligible_task_set_thm2_false(random_task_set):
  random_task_set.thm1 = True
  random_task_set.thm2 = False
  random_task_set.thm3 = False
  
  assert alg.tighten_deadline(random_task_set)[0] == "Not eligible for deadline-tightening"

def test_search_is_True(task_set):
  search_result, _ = alg.tighten_deadline(task_set)

  assert search_result is True

def test_search_no_more_eligible_candidates(random_task_set):
  random_task_set.thm1 = False
  random_task_set.thm2 = True
  random_task_set.thm3 = True
  random_task_set.hi_tasks_list = []

  search_result, _ = alg.tighten_deadline(random_task_set)

  assert search_result == "No more eligible candidates"

def test_search_success_decreases_sum_dbf(task_set):
  t, ts = alg.get_failure_time(task_set)
  before = dbf.sum_dbf(task_set, t, ts)
  best_candidate = alg.initialize_candidates(task_set)[0]
  T, C_LO, previous_tight_D = task_set.task_set[best_candidate].T, task_set.task_set[best_candidate].C_LO, task_set.task_set[best_candidate].tight_D

  task_set.task_set[best_candidate].tight_D = alg.find_optimal_tight_D(T, C_LO, previous_tight_D, ts)

  assert dbf.sum_dbf(task_set, t, ts) < before

def test_search_decreases_tight_D(task_set):
  _, task_set_post_search = alg.tighten_deadline(task_set)

  assert any(task.tight_D < task.D for task in task_set_post_search.task_set.values())

def test_search_success_failure_time_neg(task_set):
  _, task_set_post_search = alg.tighten_deadline(task_set)

  assert alg.get_failure_time(task_set_post_search) == (-1, -1)

def test_search_tight_D_between_C_LO_D(random_task_set):
  _, random_task_set_post_search = alg.tighten_deadline(random_task_set)

  assert all(task.C_LO <= task.tight_D <= task.D for task in random_task_set_post_search.task_set.values())

def test_search_thm2_still_true(random_task_set):
  before_search_thm2 = s.schedulability_test_thm2(random_task_set)
  _, random_task_set_post_search = alg.tighten_deadline(random_task_set)

  assert before_search_thm2 is False or s.schedulability_test_thm2(random_task_set_post_search) is True

def test_search_thm3_still_true(random_task_set):
  before_search_thm3 = s.schedulability_test_thm3(random_task_set)
  _, random_task_set_post_search = alg.tighten_deadline(random_task_set)

  assert before_search_thm3 is False or s.schedulability_test_thm3(random_task_set_post_search) is True