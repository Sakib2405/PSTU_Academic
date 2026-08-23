#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <vector>

using namespace std;

mutex mtx;
condition_variable cv;
bool writing = false;

void writeLog(int id) {
    unique_lock<mutex> lock(mtx);
    cv.wait(lock, [] { return !writing; });
    writing = true;

    cout << "Thread " << id << " is writing log" << endl;

    writing = false;
    lock.unlock();
    cv.notify_one();
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 5; i++) {
        threads.push_back(thread(writeLog, i));
    }

    for (auto &t : threads) {
        t.join();
    }

    return 0;
}
