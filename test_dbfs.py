import pytest
import dbfs as dbf
import generate_tasks as gt
import random as r

@pytest.fixture
def random_u_sum():
  return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def random_task_set(random_u_sum):
  return gt.generate_task_set(random_u_sum, 0.02, 0.25)

@pytest.fixture
def task_set():
  r.seed(69)

  return gt.generate_task_set(0.8, 0.02, 0.25)

@pytest.fixture
def HI_task(task_set):
  r.seed(69)

  while True:
    task = r.choice(task_set)
    if task.L == gt.Level.HI:
      break
  return task

@pytest.fixture
def LO_task(task_set):
  r.seed(69)

  while True:
    task = r.choice(task_set)
    if task.L == gt.Level.LO:
      break
  
  return task

def test_utilization_close_to_u_sum(random_u_sum, random_task_set):
  assert random_u_sum - dbf.calculate_utilization(random_task_set) < 0.05

def test_lcm_T_returns_10670913000(task_set):
  assert dbf.lcm_T(task_set) == 10670913000

def test_max_D_returns_285(task_set):
  assert dbf.max_D(task_set) == 285

def test_max_TD_returns_315(task_set):
  assert dbf.max_TD(task_set) == 315

def test_t_max_is_positive(random_task_set):
  assert dbf.calculate_t_max(random_task_set) >= 0

def test_t_max_returns_1231(task_set):
  assert dbf.calculate_t_max(task_set) == 1231

def test_max_request_returns_2():
  assert dbf.max_requests(15, 50, 30) == 2

def test_max_request_is_zero():
  assert dbf.max_requests(15, 30, 100) == 0

def test_dbf_returns_10():
  assert dbf.demand_based_function(5, 15, 50, 30) == 10

def test_dbf_is_zero():
  assert dbf.demand_based_function(5, 15, 30, 100) == 0

def test_dbf_CO_returns_112(HI_task):
  assert dbf.demand_based_function_CO(HI_task, 1000, 500) == 112

def test_dbf_CO_is_zero(HI_task):
  assert dbf.demand_based_function_CO(HI_task, 30, 50) == 0

def test_dbf_UN_returns_38(LO_task):
  assert dbf.demand_based_function_CO(LO_task, 1000, 500) == 38

def test_dbf_UN_is_zero(LO_task):
  assert dbf.demand_based_function_CO(LO_task, 30, 50) == 0

def test_sum_dbf_HI_returns_144(task_set):
  assert dbf.sum_dbf_HI(task_set, 1000, 500) == 144

def test_sum_dbf_HI_always_nonnegative(random_task_set):
  assert dbf.sum_dbf_HI(random_task_set, 1000, 500) >= 0

def test_sum_dbf_LO_returns_262(task_set):
  assert dbf.sum_dbf_LO(task_set, 500) == 262

def test_sum_dbf_LO_always_nonnegative(random_task_set):
  assert dbf.sum_dbf_LO(random_task_set, 500) >= 0

def test_sum_dbf_CO_returns_112(task_set):
  assert dbf.sum_dbf_CO(task_set, 1000, 500) == 112

def test_sum_dbf_CO_always_nonnegative(random_task_set):
  assert dbf.sum_dbf_CO(random_task_set, 1000, 500) >= 0

def test_sum_dbf_UN_returns_100(task_set):
  assert dbf.sum_dbf_UN(task_set, 1000, 500) == 100

def test_sum_dbf_UN_always_nonnegative(random_task_set):
  assert dbf.sum_dbf_UN(random_task_set, 1000, 500) >= 0

def test_sum_dbf_returns_212(task_set):
  assert dbf.sum_dbf(task_set, 1000, 500) == 618

def test_sum_dbf_always_nonnegative(random_task_set):
  assert dbf.sum_dbf(random_task_set, 1000, 500) >= 0

def test_schedulability_test_thm1(task_set):
  assert dbf.schedulability_test_thm1(task_set) is True

def test_schedulability_test_thm2(task_set):
  assert dbf.schedulability_test_thm2(task_set) is True

def test_schedulability_test_thm3(task_set):
  assert dbf.schedulability_test_thm3(task_set) is True






# def test_total_dbf_LO_with_80_seed(G):
#   r.seed(80)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_LO(ts, task_set) == 125

# def test_total_dbf_LO_with_20_seed(G):
#   r.seed(20)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_LO(ts, task_set) == 112

# def test_total_dbf_CO_with_80_seed(G):
#   r.seed(80)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_CO(t, ts, task_set) == 367

# def test_total_dbf_CO_with_20_seed(G):
#   r.seed(20)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_CO(t, ts, task_set) == 270

# def test_total_dbf_UN_with_80_seed(G):
#   r.seed(80)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_UN(t, ts, task_set) == 52

# def test_total_dbf_UN_with_20_seed(G):
#   r.seed(20)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.total_dbf_UN(t, ts, task_set) == 110

# def test_calculate_dbf_with_80_seed(G):
#   r.seed(80)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.calculate_dbf(t, ts, task_set) == 739

# def test_calculate_dbf_with_20_seed(G):
#   r.seed(20)
#   t = r.randint(300, 500)
#   ts = t//2
#   task_set = G.create_task_set(0.9, 0.02, 0.25)

#   assert dbf.calculate_dbf(t, ts, task_set) == 702

# # def test_schedulability_test_thm1_20_seed_returns_true(G):
# #   r.seed(90)

# #   assert dbf.schedulability_test_thm1(G.create_task_set(0.9, 0.02, 0.25))

# # def test_schedulability_test_thm1_80_seed_returns_false(G):
# #   r.seed(80)

# #   assert dbf.schedulability_test_thm1(G.create_task_set(0.9, 0.02, 0.25)) is False
 
# # def test_schedulability_test_thm2_50_seed_returns_true(G):
# #   r.seed(50)

# #   assert dbf.schedulability_test_thm2(G.create_task_set(0.9, 0.02, 0.25))

# # def test_schedulability_test_thm2_80_seed_returns_false(G):
# #   r.seed(40)

# #   assert dbf.schedulability_test_thm2(G.create_task_set(0.9, 0.02, 0.25)) is False
 
# # def test_schedulability_test_thm3_20_seed_returns_true(G):
# #   r.seed(20)

# #   assert dbf.schedulability_test_thm3(G.create_task_set(0.9, 0.02, 0.25))

# # def test_schedulability_test_thm3_80_seed_returns_false(G):
# #   r.seed(80)

# #   assert dbf.schedulability_test_thm3(G.create_task_set(0.9, 0.02, 0.25)) is False
 
