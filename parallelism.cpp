#include <chrono>
#include <cassert>

#include "./src/search_algorithm.h"

int main(int argc, char* argv[]) {
  
  int cum_duration = 0, cum_duration2 = 0; 
  bool thm1_result_parallel, thm1_result;
  
  for (int i = 0; i < 1000; ++i) {
    TaskSet task_set = TaskSet(0.5);
    auto start_time = chrono::high_resolution_clock::now();
    thm1_result_parallel = schedulability_test_thm1_parallel(task_set);
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
    cum_duration += duration.count();


    start_time = chrono::high_resolution_clock::now();
    thm1_result = schedulability_test_thm1(task_set);
    end_time = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::milliseconds>(end_time - start_time);
    cum_duration2 += duration.count();

    assert(thm1_result_parallel == thm1_result);
  }
  
  cout << cum_duration << " " << cum_duration2 << endl;
}