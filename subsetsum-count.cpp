#include <iostream>
#include <vector>
#include <map>

using namespace std;

int main()
{
    vector<int> X = {-962, -855, -777, -751, -669, -441, -326, -321, -314, -307,
     -168, -166, -122, -51, -39, 4, 48, 142, 155, 193, 241, 257,
     324, 333, 334, 352, 359, 493, 823, 849, 878, 996};
    
    int s = X.size();
    
    cout << "number of variables: " << s << endl;
    
    map<int, int> m; // store for every sum how often it has occurred
    
    // loop over all subsets
    for(unsigned long p = 0; p < (1ul<<s); p++)
    {
        // print every 2^20 numbers
        if ((p & 0xFFFFF) == 0) cout << (p >> 20) << "/" << (1 << (s-20)) << endl;
        
        int sum = 0;
        auto p2 = p;
        int k = 0;
        while (p2 != 0)
        {
            if (p2 & 1) sum += X[k];
            p2 >>= 1;
            k++;
        }
        
        if (m.find(sum) == m.end())
        {
            m[sum] = 1;
        }
        else m[sum]++;
    }
    
    cout << "The sums that occur only once are:" << endl;
    for (const auto& tuple: m)
    {
        if (tuple.second == 1)
        {
            cout << tuple.first << " ";
        }
    }
}