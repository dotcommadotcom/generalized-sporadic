#include <iostream>
#include <fstream>
#include <chrono>
#include <cassert>

#include "./src/search_algorithm.h"

void create_csv_file(string filename) {
  ifstream file_check(filename);
    
  if (!file_check.is_open()) {
    std::ofstream file_create(filename);
        
    if (file_create.is_open()) {
      file_create << "utilization,num_tasks,before_success_count,eds_success_count,eds_cum_duration,naive_success_count,naive_cum_duration" << endl;
      file_create.close();
    } else return;
  } else {
    file_check.close();
  }
}

void write_result_to_csv(const string& filename, const vector<int>& test_result) {
  ofstream file(filename, ios::app);
  if (!file.is_open()) {
    cerr << "Failed to open file: " << filename << endl;
    return;
  }

  for (const auto& cell : test_result) {
    file << cell;
    if (&cell != &test_result.back()) {
      file << ","; 
    }
  }
  file << "\n"; 
  file.close();
}

int main(int argc, char* argv[]) {
  if (argc < 3){
    std::cout << "Error: Provide count and utilization tag." << std::endl;
    return 1;
  }

  int count = stoi(argv[1]);
  double utilization = stod(argv[2]);
  int before_success = 0, after_eds_success = 0, after_naive_success = 0;
  vector<int> result;
  int cum_duration = 0, cum_duration2 = 0; 
  unsigned long long cum_eds_duration = 0, cum_naive_duration = 0;

  for (int i = 0; i < count; ++i) {
    TaskSet task_set_eds = TaskSet(utilization);
    task_set_eds.set_thm1(schedulability_test_thm1_parallel(task_set_eds));
    task_set_eds.set_thm2(schedulability_test_thm2(task_set_eds));
    task_set_eds.set_thm3(schedulability_test_thm3(task_set_eds));
    TaskSet task_set_naive = task_set_eds;
    assert(&task_set_eds != &task_set_naive);

    if (task_set_eds.get_thm1() && task_set_eds.get_thm2() && task_set_eds.get_thm3()) {
      before_success++;
    }

    // Enhanced Deadline Search Algorithm
    auto start_time = chrono::high_resolution_clock::now();
    if (!is_eligible(task_set_eds) || deadline_search_algorithm(task_set_eds).first == "Success") {
      after_eds_success++;
    } 
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
    cum_eds_duration += duration.count();

    // Naive Algorithm
    start_time = chrono::high_resolution_clock::now();
    if (!is_eligible(task_set_naive) || naive_algorithm(task_set_naive).first == "Success") {
      after_naive_success++;
    } 
    end_time = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
    assert(end_time >= start_time);
    cum_naive_duration += static_cast<unsigned long long>(duration.count());
  }

  result.push_back(static_cast<int>(utilization * 1000));
  result.push_back(count);
  result.push_back(before_success);
  result.push_back(after_eds_success);
  result.push_back(cum_eds_duration);
  result.push_back(after_naive_success);
  result.push_back(cum_naive_duration);

  string filename = "experiment_result.csv";

  create_csv_file(filename);
  write_result_to_csv(filename, result);
}