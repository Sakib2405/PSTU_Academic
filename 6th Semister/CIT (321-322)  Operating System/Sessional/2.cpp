#include <iostream>
#include <thread>
#include <atomic>

using namespace std;

atomic<bool> flag[2];
atomic<int> turn;

int shared_data = 0;

void process(int i) {
    int j = 1 - i;
    for (int k = 0; k < 5; k++) {
        flag[i] = true;
        turn = j;
        while (flag[j] && turn == j);

        shared_data++;
        cout << "Process " << i << " updated value to " << shared_data << endl;

        flag[i] = false;
    }
}

int main() {
    flag[0] = false;
    flag[1] = false;

    thread t1(process, 0);
    thread t2(process, 1);

    t1.join();
    t2.join();

    return 0;
}
