import random 
import math
from enum import Enum 

class Level(Enum):
    HI = 1
    LO = 2

class task:
    def __init__(self, ID, T, C_LO, C_HI, D, L, tight_D = -1):
        """
        Args:
                ID:         type: string. The id of the task.
                T:          type: int. The minimum separation time of the task.
                C_LO:    type: int. The WCET in low-criticality mode.
                C_HI:    type: int. The WCET in high-criticality mode.
                D:          type: int. The deadline of the task.
                L:          type: Level. The criticality level of the task. Either HI (1) or LO (2).
                tight_D:    type: int. The tightened deadline of the task. If not assigned, the same as D.
        """
        self.ID = ID
        self.T = T
        self.C_LO = C_LO
        self.C_HI = C_HI
        self.D = D
        self.L = L
        self.tight_D = D if tight_D == -1 else tight_D

class task_generation:
    def generate_kato_utilizations(self, target_value, min_value, max_value):
        '''
            This function is modified from the function gen_kato_utilizations in class simso.generator.task_generator.
            Inputs: 
                target_value:         type: float. The target sum of the utilization ratio.
                min_value:            type: float. The minimum utilization ratio.
                max_value:            type: float. The maximum utilization ratio.
            Outputs:
                values:               A set of utilization ratios whose sum is the target_val.
        '''
        values = []
        total_value = 0
        # Classic UUniFast algorithm:
        while total_value < target_value:
            val = random.uniform(min_value, max_value)
            if val + total_value> target_value:
                val = target_value - total_value
            total_value += val
            values.append(val)
        return values

    def generate_task(self, utilization, ID):
        '''
            Generates the task based on the utilization ratio
            How do we define the utilization ratio? --> WCET_LO / T based on Easwaran 2013
            Inputs:
                utilization:        type: float. The utilization ratio of the task.
            Output:    
                A task with all parameters initialized.
        '''
        C_LO = self.generate_C_LO()
        T = self.generate_T(C_LO, utilization)

        # the operations below randomly generate T and then calculates C_LO
        # this may cause the C_LO to be 0
        # T = self.generate_T()
        # C_LO = math.floor(T * utilization)

        L = self.generate_L()
        C_HI = C_LO if L == Level.LO else self.generate_C_HI(C_LO)
        D = self.generate_D(C_HI)

        return task(ID, T, C_LO, C_HI, D, L)

    def generate_C_LO(self):
        return random.randrange(5, 30)

    def generate_C_HI(self, C_LO):
      return C_LO * random.randrange(2, 5)

    def generate_T(self, C_LO, utilization):
      return math.ceil(C_LO / utilization)

    def generate_D(self, C_HI):
      # return random.randrange(C_HI, 101)
      # enlarge the random range to fit in large C_HI values
      return random.randrange(C_HI, 301)

    def generate_L(self):
      return random.choice([Level.HI, Level.LO])

    def create_task_set(self, utilization_sum, min_u, max_u):
        utilization_ratios = self.generate_kato_utilizations(utilization_sum, min_u, max_u)
        tasks = []
        counter = 0
        for u in utilization_ratios:
            t = self.generate_task(u, str(counter))
            while t.C_LO == 0:
                t = self.generate_task(u, str(counter))
            tasks.append(t)
            counter += 1
        return tasks

