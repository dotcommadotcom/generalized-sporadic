import pytest
import random as r

from generate_tasks import Task, Task_Set
import schedulability as s
import dbfs as dbf
import greedy as g

@pytest.fixture
def default_heuristic():
  return g.earliest_deadline

@pytest.fixture
def lo_task_set():
  task_set_dict = {'num_tasks': 6, 
                   't_max': 261, 
                   'utilization': 0.6964358021917052, 
                   'thm1': True, 
                   'thm2': None, 
                   'thm3': None, 
                   'lo_tasks_list': [Task(0, 414, 13, 13, 300, 300), Task(3, 115, 14, 14, 267, 267), Task(5, 94, 7, 7, 172, 172)], 
                   'hi_tasks_list': []
                   }
  
  return Task_Set(ts_dict = task_set_dict)

@pytest.fixture
def task_set_not_eligible():
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

''' TEST HEURISTICS '''
def test_max_diff_wcet(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.max_diff_wcet) == 0

def test_max_diff_wcet_wcet_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.max_diff_wcet) == -1

def test_earliest_deadline(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.earliest_deadline) == 0

def test_earliest_deadline_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.earliest_deadline) == -1

def test_smallest_sep_time(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.smallest_sep_time) == 0

def test_smallest_sep_time_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.smallest_sep_time) == -1

def test_shortest_wcet_lo(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.shortest_wcet_lo) == 0

def test_shortest_wcet_lo_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.shortest_wcet_lo) == -1

def test_longest_wcet_hi(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.longest_wcet_hi) == 1

def test_longest_wcet_hi_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.longest_wcet_hi) == -1

def test_min_diff_wcet_hi_deadline(task_set):
  candidates = g.initialize_candidates(task_set)

  assert g.find_candidate(candidates, task_set, g.min_diff_wcet_hi_deadline) == 1

def test_min_diff_wcet_hi_deadline_no_hi_tasks(lo_task_set):
  candidates = g.initialize_candidates(lo_task_set)

  assert g.find_candidate(candidates, lo_task_set, g.min_diff_wcet_hi_deadline) == -1


''' TEST GREEDY HELPER FUNCTIONS'''

def test_is_eligible_is_false(task_set_not_eligible):
  assert g.is_eligible(task_set_not_eligible) is False

def test_is_eligible_is_true(task_set):
  assert g.is_eligible(task_set) is True

def test_initialize_candidates_is_correct(task_set):
  assert g.initialize_candidates(task_set) == [True, True, False]

def test_initialize_candidates_is_equal_length(task_set):
  candidates = g.initialize_candidates(task_set)

  assert len(candidates) == len(task_set.task_set)

def test_get_failure_time_not_eligible_task_set(task_set_not_eligible):
  assert g.get_failure_time(task_set_not_eligible) == (-1, -1)

def test_get_failure_time_task_set(task_set):
  assert g.get_failure_time(task_set) == (31, 9)

''' TEST GREEDY FUNCTIONALITY'''

def test_greedy_not_eligible_task_set(task_set_not_eligible, default_heuristic):
  assert g.greedy(task_set_not_eligible, default_heuristic) ==  ("Not eligible for deadline-tightening", task_set_not_eligible)

def test_task_set_schedulable_1_is_false(task_set):
  assert task_set.thm1 is False

def test_greedy_is_True(task_set, default_heuristic):
  greedy_result, _ = g.greedy(task_set, default_heuristic)

  assert greedy_result is True

def test_greedy_decreases_sum_dbf(task_set):
  i, j = g.get_failure_time(task_set, 2, 1)
  before = dbf.sum_dbf(task_set, i, j)
  candidates = g.initialize_candidates(task_set)
  best_candidate = g.max_diff_wcet(candidates, task_set) 

  task_set.task_set[best_candidate].tight_D = task_set.task_set[best_candidate].C_LO

  assert dbf.sum_dbf(task_set, i, j) < before

def test_task_set_after_greedy_failure_time_neg(task_set, default_heuristic):
  _, task_set_post_greedy = g.greedy(task_set, default_heuristic)

  assert g.get_failure_time(task_set_post_greedy) == (-1, -1)

def test_task_set_after_greedy_decreased_tight_D(task_set, default_heuristic):
  _, task_set_post_greedy = g.greedy(task_set, default_heuristic)

  assert any(task.tight_D < task.D for task in task_set_post_greedy.task_set.values())

def test_after_greedy_decreased_tight_D_or_not_eligible(random_task_set, default_heuristic):
  eligibility, random_task_set_post_greedy = g.greedy(random_task_set, default_heuristic)

  assert eligibility == "Not eligible for deadline-tightening" or any([task.tight_D < task.D for task in random_task_set_post_greedy.task_set.values()])

def test_after_greedy_tight_D_greater_C_LO(random_task_set, default_heuristic):
  _, random_task_set_post_greedy = g.greedy(random_task_set, default_heuristic)

  assert all(task.tight_D >= task.C_LO for task in random_task_set_post_greedy.task_set.values())

# sometimes produces errors
def test_after_greedy_sched2_is_true(random_task_set, default_heuristic):
  _, random_task_set_post_greedy = g.greedy(random_task_set, default_heuristic)

  assert s.schedulability_test_thm2(random_task_set_post_greedy) is True

def test_greedy_fails_no_more_candidates(task_set_no_greedy, default_heuristic):
  greedy_result, _ = g.greedy(task_set_no_greedy, default_heuristic)

  assert greedy_result == "No more eligible candidates" 