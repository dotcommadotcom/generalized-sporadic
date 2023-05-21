import pytest
import random as r

from generate_tasks import Task, Task_Set
import schedulability as s

@pytest.fixture
def random_target_u(): return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def task_set_false():
  task_set_dict = { 'num_tasks': 5, 
                    't_max': 724, 
                    'utilization': 0.6963020471899597, 
                    'thm1': None, 
                    'thm2': None, 
                    'thm3': None,
                    'lo_tasks_list': [Task(2, 133, 18, 18, 399, 399), Task(4, 472, 13, 13, 315, 315)],
                    'hi_tasks_list': [Task(0, 146, 10, 40, 410, 410), Task(1, 386, 24, 59, 93, 93), Task(3, 394, 15, 42, 78, 78)]}
            
  return Task_Set(task_set_dict = task_set_dict)

@pytest.fixture
def task_set_false2():
  task_set_dict = { 'num_tasks': 15, 
                    't_max': 3210, 
                    'utilization': 0.8976534653451079, 
                    'thm1': None, 
                    'thm2': None, 
                    'thm3': None,
                    'lo_tasks_list': [Task(1, 357, 8, 8, 256, 256), Task(2, 429, 19, 19, 63, 63), Task(4, 180, 22, 22, 77, 77), Task(5, 26, 13, 13, 103, 103), Task(7, 283, 13, 13, 208, 208), Task(8, 419, 6, 6, 316, 316), Task(9, 445, 8, 8, 385, 385), Task(10, 336, 8, 8, 29, 29), Task(12, 360, 11, 11, 144, 144), Task(13, 117, 20, 20, 39, 39), Task(14, 491, 14, 14, 422, 422)],
                    'hi_tasks_list': [Task(0, 400, 24, 92, 244, 244), Task(3, 420, 20, 63, 449, 449), Task(6, 354, 17, 48, 426, 426), Task(11, 143, 17, 37, 485, 485)]}
                      
  return Task_Set(task_set_dict = task_set_dict)

@pytest.fixture
def task_set():
  task_set_dict = {'num_tasks': 6, 
                   't_max': 261, 
                   'utilization': 0.6964358021917052, 
                   'thm1': None, 
                   'thm2': None, 
                   'thm3': None, 
                   'lo_tasks_list': [Task(0, 414, 13, 13, 300, 300), Task(3, 115, 14, 14, 267, 267), Task(5, 94, 7, 7, 172, 172)], 
                   'hi_tasks_list': [Task(1, 122, 23, 46, 312, 312), Task(2, 108, 18, 37, 107, 107), Task(4, 132, 15, 50, 233, 233)]}
  
  return Task_Set(task_set_dict = task_set_dict)

''' TEST THEOREM 1 '''

def test_sched_thm1_task_set_is_false(task_set_false):
  assert s.schedulability_test_thm1(task_set_false) is False

def test_sched_thm1_task_set_is_true(task_set):
  assert s.schedulability_test_thm1(task_set) is True

''' TEST THEOREM 2 '''

def test_sched_thm2_task_set_is_false(task_set_false2):
  assert s.schedulability_test_thm1(task_set_false2) is False

def test_sched_thm2_task_set_is_true(task_set):
  assert s.schedulability_test_thm2(task_set) is True

''' TEST THEOREM 3 '''

def test_sched_thm3_task_set_is_false(task_set_false):
  assert s.schedulability_test_thm1(task_set_false) is False

def test_sched_thm3_task_set_is_true(task_set):
  assert s.schedulability_test_thm3(task_set) is True