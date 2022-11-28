import random as r
import math as m
from enum import Enum 
import dbfs as dbf

class Level(Enum):
    HI = 1
    LO = 2

class task:
    def __init__(self, ID, T, C_LO, C_HI, D, L, tight_D = -1):
        """
        Args:
                ID:         type: int. ID of task.
                T:          type: int. Minimum inter-arrival separation time of task.
                C_LO:       type: int. WCET in low-criticality mode.
                C_HI:       type: int. WCET in high-criticality mode. If L == LO, the same as C_LO
                D:          type: int. Relative deadline of task.
                L:          type: Level. Criticality level of task. Either HI or LO.
                tight_D:    type: int. Tightened deadline of the task. If not assigned, the same as D.
        """
        self.ID = ID
        self.T = T
        self.C_LO = C_LO
        self.C_HI = C_HI
        self.D = D
        self.L = L
        self.tight_D = D if tight_D == -1 else tight_D

def generate_kato_utilizations(target_u, min_u, max_u):
    '''
        This function is modified from the function gen_kato_utilizations in class simso.generator.task_generator.
        Inputs: 
            target_u:               type: float. Target sum of the utilization ratio.
            min_u:                  type: float. Minimum utilization ratio.
            max_u:                  type: float. Maximum utilization ratio.
        Outputs:
            A set of utilization ratios whose sum is the target_u.
    '''
    utilizations = []
    total_u = 0
    # Classic UUniFast algorithm:
    while total_u < target_u:
        current_u = r.uniform(min_u, max_u)
        if current_u + total_u > target_u:
            current_u = target_u - total_u
        total_u += current_u
        utilizations.append(current_u)
    return utilizations

def generate_L():
    return r.choice([Level.HI, Level.LO])

def generate_C_LO():
    return r.randrange(5, 31)

def generate_C_HI(C_LO, L):
    return C_LO if L == Level.LO else C_LO * r.randrange(2, 5)

def generate_D(C_HI):
    return r.randrange(C_HI, 301)

def generate_T(C_LO, utilization):
    return m.ceil(C_LO / utilization) # TODO should it be less C_HI?

def generate_task(utilization, ID):
    '''
        Generates the task based on the utilization ratio
        How do we define the utilization ratio? --> WCET_LO / T based on Easwaran 2013
        Inputs:
            utilization:        type: float. The utilization ratio of the task.
        Output:    
            A task with all parameters initialized.
    '''
    L = generate_L()
    C_LO = generate_C_LO()
    C_HI = generate_C_HI(C_LO, L)
    D = generate_D(C_HI)
    T = generate_T(C_LO, utilization)

    return task(ID, T, C_LO, C_HI, D, L)

def generate_task_set(utilization_sum, min_u, max_u):
    utilizations = generate_kato_utilizations(utilization_sum, min_u, max_u)
    return [generate_task(u, i) for u, i in zip(utilizations, range(len(utilizations)))]





def print_task_set(task_set):
  for t in task_set:
    print("ID: {}, C_LO: {}, C_HI: {}, T: {}, D: {}, L: {}".format(t.ID, t.C_LO, t.C_HI, t.T, t.D, t.L))

if __name__ == '__main__':
  for u_sum in [0.5, 0.6, 0.7, 0.8, 0.9]:
    task_set = generate_task_set(u_sum, 0.02, 0.25)
    print("------- Current utilization sum: {}---------".format(u_sum))
    print_task_set(task_set)
    print("Real utilization sum: {}".format(sum([task.C_LO / task.T for task in task_set])))
    print("t_max: {}".format(dbf.calculate_t_max(task_set)))