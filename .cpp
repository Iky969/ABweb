#include <iostream>
using namespace std;

int main() {
    int total = 0;
    for (int i = 1; i <= 5; i++) {
        total += i;
        cout << "Menambahkan " << i << ", total: " << total << endl;
    }
    return 0;
}
