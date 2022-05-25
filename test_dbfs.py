import pytest
import dbfs as dbf
import generate_tasks as gt
import random as r

G = None

@pytest.fixture()
def G():
    yield gt.task_generation()

def test_canary():
  assert True

def test_lcm():
  assert dbf.lcm([4,5,12,15,30]) == 60

def test_calculate_t_max_returns_132(G):
  r.seed(80)

  assert dbf.calculate_t_max(G.create_task_set(0.5, 0.02, 0.25)) == 132

def test_calculate_t_max_always_returns_nonnegative(G):
  assert dbf.calculate_t_max(G.create_task_set(0.5, 0.02, 0.25)) > 0

def test_demand_based_function():
  assert dbf.demand_based_function(7, 4, 6, 4) == 4

def test_demand_based_function_always_nonnegative(G):
  C = G.generate_WCET_LO()
  T = G.generate_T(C, 0.8)
  D = G.generate_D(G.generate_WCET_HI(C))

  assert dbf.demand_based_function(r.randrange(5, 101), C, D, T) >= 0

def test_max_num_requests():
  assert dbf.max_num_requests(75,63,15,4) == 3

def test_dbf_CO():
  assert dbf.demand_based_function_CO(117, 58, 3, 6, 51, 21) == 18

def test_dbf_UN():
  assert dbf.demand_based_function_UN(117, 58, 1, 86, 75) == 1

def test_total_dbf_HI_with_80_seed(G):
  r.seed(80)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_HI(t, ts, task_set) == 195

def test_total_dbf_HI_with_20_seed(G):
  r.seed(20)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_HI(t, ts, task_set) == 210

def test_total_dbf_LO_with_80_seed(G):
  r.seed(80)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_LO(ts, task_set) == 125

def test_total_dbf_LO_with_20_seed(G):
  r.seed(20)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_LO(ts, task_set) == 112

def test_total_dbf_CO_with_80_seed(G):
  r.seed(80)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_CO(t, ts, task_set) == 367

def test_total_dbf_CO_with_20_seed(G):
  r.seed(20)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_CO(t, ts, task_set) == 270

def test_total_dbf_UN_with_80_seed(G):
  r.seed(80)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_UN(t, ts, task_set) == 52

def test_total_dbf_UN_with_20_seed(G):
  r.seed(20)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.total_dbf_UN(t, ts, task_set) == 110

def test_calculate_dbf_with_80_seed(G):
  r.seed(80)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.calculate_dbf(t, ts, task_set) == 739

def test_calculate_dbf_with_20_seed(G):
  r.seed(20)
  t = r.randint(300, 500)
  ts = t//2
  task_set = G.create_task_set(0.9, 0.02, 0.25)

  assert dbf.calculate_dbf(t, ts, task_set) == 702

# def test_schedulability_test_thm1_20_seed_returns_true(G):
#   r.seed(90)

#   assert dbf.schedulability_test_thm1(G.create_task_set(0.9, 0.02, 0.25))

# def test_schedulability_test_thm1_80_seed_returns_false(G):
#   r.seed(80)

#   assert dbf.schedulability_test_thm1(G.create_task_set(0.9, 0.02, 0.25)) is False
 
# def test_schedulability_test_thm2_50_seed_returns_true(G):
#   r.seed(50)

#   assert dbf.schedulability_test_thm2(G.create_task_set(0.9, 0.02, 0.25))

# def test_schedulability_test_thm2_80_seed_returns_false(G):
#   r.seed(40)

#   assert dbf.schedulability_test_thm2(G.create_task_set(0.9, 0.02, 0.25)) is False
 
# def test_schedulability_test_thm3_20_seed_returns_true(G):
#   r.seed(20)

#   assert dbf.schedulability_test_thm3(G.create_task_set(0.9, 0.02, 0.25))

# def test_schedulability_test_thm3_80_seed_returns_false(G):
#   r.seed(80)

#   assert dbf.schedulability_test_thm3(G.create_task_set(0.9, 0.02, 0.25)) is False
 
