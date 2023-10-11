#ifndef GENERATE_TASK_SET_H
#define GENERATE_TASK_SET_H
 
#include "generate_tasks.h"

class TaskSet {
public:
  map<int, Task> task_set;
  int num_tasks;
  double utilization, t_max;
  bool thm1, thm2, thm3;

  TaskSet(double target_u = 0, double hi_probability = 0.5, int wcet_ratio = 4) {
    this->task_set = {};
    this->num_tasks = 0;
    this->lo_tasks_list = {};
    this->hi_tasks_list = {};
    this->thm1 = false;
    this->thm2 = false;
    this->thm3 = false;

    while (true) {
      Task task = generate_task(this->num_tasks, hi_probability, wcet_ratio);

      this->task_set[this->num_tasks] = task;
      this->num_tasks = this->task_set.size();
      this->utilization = this->calculate_utilization();

      if (task.L == Level::LO) {
        this->lo_tasks_list.push_back(task);
      }

      if (task.L == Level::HI) {
        this->hi_tasks_list.push_back(task);
      }

      if ((target_u - 0.005 <= this->utilization && this->utilization <= target_u + 0.005)
        && !this->lo_tasks_list.empty() && !this->hi_tasks_list.empty() && this->calculate_t_max() > 0) {
        break;
      }

      else if (this->utilization > target_u + 0.005) {
        this->task_set.clear();
        this->num_tasks = this->task_set.size();
        this->lo_tasks_list.clear();
        this->hi_tasks_list.clear();
      }
    }

    this->t_max = calculate_t_max();
  } 

  TaskSet(map<string, vector<Task>> TaskSet_dict = {}, bool thm1 = false, bool thm2 = false, bool thm3 = false) {
    this->thm1 = thm1;
    this->thm2 = thm2;
    this->thm3 = thm3;
    this->lo_tasks_list = TaskSet_dict["lo"];
    this->hi_tasks_list = TaskSet_dict["hi"]; 
    
    for (Task task : this->lo_tasks_list) {
      this->task_set[task.ID] = task;
    }

    for (Task task : this->hi_tasks_list) {
      this->task_set[task.ID] = task;
    }

    this->num_tasks = this->task_set.size();
    this->utilization = calculate_utilization();
    this->t_max = calculate_t_max();
  }

  TaskSet& operator=(const TaskSet& other) {
    if (this != &other) {
      this->num_tasks = other.num_tasks;
      this->utilization = other.utilization;
      this->t_max = other.t_max;
      this->thm1 = other.thm1;
      this->thm2 = other.thm2;
      this->thm3 = other.thm3;

      for (const auto& [key, task] : other.get_task_set()) {
        Task copied_task = task;
        this->task_set[key] = copied_task;
      }
    }
    return *this;
  }

  double calculate_t_max() {
    double lcm = lcmT_maxD();
    double u = U_maxTD();

    return u >= 0 ? min(lcm, u) : 0;
  }

  double calculate_utilization() {
    double lo_utilization = 0;
    double hi_utilization = 0;

    for(auto const&[key, task]: task_set) {
      
      if (task.L == Level::LO) { // Calculate the sum of C_LO / T for all tasks with level LO
        lo_utilization += task.C_LO / static_cast<double>(task.T);
      }

      
      if (task.L == Level::HI) { // Calculate the sum of C_HI / T for all tasks with level HI
        hi_utilization += task.C_HI / static_cast<double>(task.T);
      }
    }

    return (lo_utilization + hi_utilization) / 2;
  }

  void constrain_deadlines() {
    for (auto& [key, task] : task_set) {
      if (task.T > task.D) task.T = task.D;
    }
  }

  string task_set_to_string() {
    string task_set_string = "Task set: " + to_string(num_tasks) + " tasks, t_max = " + to_string(t_max) + ", utilization = " + to_string(utilization) + "\n";
    task_set_string += "Thm 1, 2, 3 -- " + thm_to_string(thm1) + ", " + thm_to_string(thm2) + ", " + thm_to_string(thm3) + "\n";

    for(auto &[key, task]: task_set) {
      task_set_string += task.task_to_string() + "\n";
    }

    return task_set_string;
  }

  void set_utilization(double utilization) { this->utilization = utilization; }
  void set_t_max(double t_max) { this->t_max = t_max; }
  void set_hi_probability(double hi_probability) { this->hi_probability = hi_probability; }
  void set_num_tasks(int num_tasks) { this->num_tasks = num_tasks; }
  void set_thm1(bool thm1) { this->thm1 = thm1; }
  void set_thm2(bool thm2) { this->thm2 = thm2; }
  void set_thm3(bool thm3) { this->thm3 = thm3; }
  void set_task_set(map<int, Task> task_set) { this->task_set = task_set; }

  double get_utilization() const { return utilization; }
  double get_t_max() const { return t_max; }
  double get_hi_probability() const { return hi_probability; }
  int get_num_tasks() const { return num_tasks; }
  bool get_thm1() const { return thm1; }
  bool get_thm2() const { return thm2; }
  bool get_thm3() const { return thm3; }
  int get_lo_count() const { return this->lo_tasks_list.size(); }
  int get_hi_count() const { return this->hi_tasks_list.size(); }
  map<int, Task> get_task_set() const { return task_set; }

private:
  vector<Task> lo_tasks_list;
  vector<Task> hi_tasks_list;
  double target_u;
  double hi_probability;
  int wcet_ratio;

  int gcd(int a, int b) {
    while (b != 0) {
      int t = b;
      b = a % b;
      a = t;
    }
    return a;
  }

  int lcm(int a, int b) {
    return abs(a * b) / gcd(a, b);
  }

  double lcmT_maxD() {
    int l = 1;
    int maxD = 0;

    for(auto const&[key, task]: task_set) {
      l = lcm(l, task.T); // Calculate the LCM of all T values

      if (task.D > maxD) maxD = task.D; // Find the maximum D value
    }

    return static_cast<double>(l + maxD);
  }

  double U_maxTD() {
    double maxTD = 0;

    for(auto const&[key, task]: task_set) { // Calculate the maximum T - D value
      double currentTD = static_cast<double>(task.T - task.D); 
      if (currentTD > maxTD) maxTD = currentTD; 
    }

    return floor(utilization / (1 - utilization) * maxTD);
  }

  string thm_to_string(bool thm_result) {
    return thm_result ? "True" : "False";
  }

};

#endif
