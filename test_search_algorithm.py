import pytest
import random as r
from collections import deque

from generate_tasks import Task, Task_Set
import schedulability as s
import dbfs as dbf
import search_algorithm as alg

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
def random_task_set():
  return Task_Set(target_u = r.choice([0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975]))

@pytest.fixture
def task_set_no_greedy():
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