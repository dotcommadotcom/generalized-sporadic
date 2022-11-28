import pytest
import generate_tasks as gt 
import random as r
import dbfs as dbf

@pytest.fixture
def u_min():
  return 0.02

@pytest.fixture
def u_max():
  return 0.25

@pytest.fixture
def u_sum():
  return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def seed():
  return r.seed(80)

@pytest.fixture
def task(u_sum, u_min, u_max):
  utilization = r.choice(gt.generate_kato_utilizations(u_sum, u_min, u_max))
  return gt.generate_task(utilization, "")

def test_canary():
  assert True

def test_utilizations_greater_than_0_exclusive(u_sum, u_min, u_max):
  assert min(gt.generate_kato_utilizations(u_sum, u_min, u_max)) > 0

def test_utilizations_less_than_umax_inclusive(u_sum, u_min, u_max):
  assert max(gt.generate_kato_utilizations(u_sum, u_min, u_max)) < u_max + 0.00001

def test_utilizations_sum_equal_target_sum(u_sum, u_min, u_max):
  assert sum(gt.generate_kato_utilizations(u_sum, u_min, u_max)) == pytest.approx(u_sum)

def test_level_HI_or_LO():
  assert isinstance(gt.generate_L(), gt.Level)

def test_C_LO_greater_than_5_inclusive():
  assert gt.generate_C_LO() >= 5

def test_C_LO_less_than_31_exclusive():
  assert gt.generate_C_LO() < 31

def test_C_LO_is_13(seed):
  assert gt.generate_C_LO() == 13

def test_C_HI_is_C_LO_when_L_is_LO():
  C_LO = gt.generate_C_LO()

  assert gt.generate_C_HI(C_LO, gt.Level.LO) == C_LO

def test_C_HI_greater_than_2_C_LO_inclusive():
  C_LO = gt.generate_C_LO()

  assert gt.generate_C_HI(C_LO, gt.Level.HI) >= 2 * C_LO

def test_C_HI_less_than_5_C_LO_exclusive():
  C_LO = gt.generate_C_LO()
  
  assert gt.generate_C_HI(C_LO, gt.Level.HI) < 5 * C_LO

def test_C_HI_is_90(seed):
  assert gt.generate_C_HI(30, gt.Level.HI) == 90

def test_D_greater_than_C_HI_inclusive():
  C_HI = gt.generate_C_HI(gt.generate_C_LO(), gt.Level.HI)
  
  assert gt.generate_D(C_HI) >= C_HI

def test_D_less_than_301_exclusive():
  C_HI = gt.generate_C_HI(gt.generate_C_LO(), gt.Level.HI)
  
  assert gt.generate_D(C_HI) < 301

def test_T_minimum_is_20():
  assert gt.generate_T(5, 0.25) == 20

def test_T_maximum_known_is_1500():
  assert gt.generate_T(30, 0.02) == 1500

def test_task_C_LO_less_than_C_HI_inclusive(task):
  assert task.C_LO < task.C_HI if task.L == gt.Level.HI else task.C_LO == task.C_HI

def test_task_C_HI_less_than_T_inclusive(task):
  assert task.C_HI <= task.T 

def test_task_max_C_HI_equal_min_T(task):
  task.C_HI = 4 * task.C_LO
  task.T = gt.generate_T(task.C_LO, 0.25)

  assert task.C_HI == task.T

def test_task_set_not_empty(u_sum, u_min, u_max):
  assert len(gt.generate_task_set(u_sum, u_min, u_max)) > 0

def test_task_set_utilization_approximately_u_sum(u_sum, u_min, u_max):
  task_set = gt.generate_task_set(u_sum, u_min, u_max)

  assert u_sum - sum([task.C_LO / task.T for task in task_set]) < 0.05

# TODO test tightened deadlines
