from greedy import *
from generate_tasks import task, task_generation
import copy
def print_task_set(task_set):
  for t in task_set:
    print("ID:{}, WCET_LO:{}, WCET_HI:{}, T:{}, D:{}, L:{}".format(t.ID, t.WCET_LO, t.WCET_HI, t.T, t.D, t.L))

def cal_real_u_sum(task_set):
  sum = 0
  for t in task_set:
    sum += t.WCET_LO/t.T
  return sum
if __name__ == '__main__':
	G = task_generation()
	for u_sum in [0.5, 0.6, 0.7, 0.8, 0.9]:
		task_set = G.create_task_set(u_sum, 0.02, 0.25)
		print("------- Current utilization sum: {}---------".format(u_sum))
		print_task_set(task_set)
		print("Real utilization sum: {}".format(cal_real_u_sum(task_set)))
		temp_tasks = copy.deepcopy(task_set)
		result = greedy(temp_tasks)
		print("Greedy's result is: {}".format(result))
