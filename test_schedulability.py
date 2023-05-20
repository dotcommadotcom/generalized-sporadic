import pytest
import random as r

import generate_tasks as gt
import schedulability as s

@pytest.fixture
def random_target_u(): return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def unconstrained_task_set(random_target_u):
  while True:
    unconstrained_task_set = gt.Task_Set(random_target_u)
    if all([task.D > task.T for task in unconstrained_task_set.task_set.values()]):
      break

  return unconstrained_task_set

@pytest.fixture
def task_set():
  task_set_dict = {'num_tasks': 6, 
                   't_max': 261, 
                   'utilization': 0.6964358021917052, 
                   'thm1': None, 
                   'thm2': None, 
                   'thm3': None, 
                   'lo_tasks_list': [gt.Task(0, 414, 13, 13, 300, 300), gt.Task(3, 115, 14, 14, 267, 267), gt.Task(5, 94, 7, 7, 172, 172)], 
                   'hi_tasks_list': [gt.Task(1, 122, 23, 46, 312, 312), gt.Task(2, 108, 18, 37, 107, 107), gt.Task(4, 132, 15, 50, 233, 233)]}
  
  return gt.Task_Set(task_set_dict = task_set_dict)

''' TEST THEOREM 1 '''

def test_sched_thm1_unconstrained_task_set_is_false(unconstrained_task_set):
  assert s.schedulability_test_thm1(unconstrained_task_set) is False

def test_sched_thm1_task_set_is_true(task_set):
  assert s.schedulability_test_thm1(task_set) is True

''' TEST THEOREM 2 '''

def test_sched_thm2_unconstrained_task_set_is_false(unconstrained_task_set):
  assert s.schedulability_test_thm1(unconstrained_task_set) is False

def test_sched_thm2_task_set_is_true(task_set):
  assert s.schedulability_test_thm2(task_set) is True

''' TEST THEOREM 3 '''

def test_sched_thm3_unconstrained_task_set_is_false(unconstrained_task_set):
  assert s.schedulability_test_thm3(unconstrained_task_set) is False

def test_sched_thm3_task_set_is_true(task_set):
  assert s.schedulability_test_thm3(task_set) is True