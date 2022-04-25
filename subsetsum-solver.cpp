#include <iostream>
#include <vector>
#include <mutex>
#include <queue>
#include <thread>
#include <cassert>

using namespace std;

struct JobDesc
{
    unsigned long start, end; // start/end index for the brute force search
    vector<unsigned long> solutions; // list of solutions
    
    // list of numbers and target sum
    vector<int> X;
    int T;
    
    JobDesc(unsigned long s, unsigned long e, vector<int> _X, int _T)
    {
        start = s;
        end = e;
        X = _X;
        T = _T;
    }
};

// implementation of a thread-safe queue containing jobs
template<typename T, typename U> // T = type that describes the job (contains inputs and outputs), U = class that takes the jobs and executes them
class SafeQueue
{
public:
    queue<T*> q;
    mutex m;

    void enqueue(T* t)
    {
        lock_guard<mutex> lock(m);
        q.push(t);
    }

    T* dequeue()
    {
        unique_lock<mutex> lock(m);
        if (q.empty())
        {
            // done
            return nullptr;
        }
        T* val = q.front();
        q.pop();
        cout << "popped. left in queue: " << q.size() << endl;
        return val;
    }

    void start(int workers)
    {
        // create worker threads
        vector<thread> worker_threads;
        for (int i = 0; i < workers; i++)
        {
            worker_threads.push_back(thread(U(this)));
        }

        // wait for each thread to finish
        for (int i = 0; i < workers; i++)
        {
            worker_threads[i].join();
        }
    }
};


// Class that takes job descriptions, runs it, and puts the result back in the job struct
class Worker
{
public:
    SafeQueue<JobDesc, Worker>* q;
    explicit Worker(SafeQueue<JobDesc, Worker>* q2)
    {
        q = q2;
    }

    void operator()()
    {
        JobDesc* job = nullptr;
        while (job = q->dequeue()) // as long as the queue is not returning nullptr
        {
            unsigned long start = job->start;
            unsigned long end = job->end;
            
            // further optimizations are possible but this is simple enough
            for(unsigned long p = start; p < end; p++)
            {
                int sum = 0;
                auto p2 = p;
                int k = 0;
                while (p2 != 0)
                {
                    if (p2 & 1) sum += job->X[k];
                    p2 >>= 1;
                    k++;
                }
                
                if (sum == job->T)
                {
                    job->solutions.push_back(p);
                }
            }
        }
    }
};


// format a given solution p
void prettyprint(const vector<int>& X, unsigned long p, int T)
{
    bool first = true;
    int k = 0;
    while (p != 0)
    {
        if (p & 1)
        {
            if (!first)
            {
                cout << " + ";
            }
            else first = false;
            
            int num = X[k];
            if (num < 0)
            {
                cout << "(" << num << ")";
            }
            else cout << num;
        }
        p >>= 1;
        k++;
    }
    
    cout << " = " << T << endl;
}

int main()
{
    vector<int> X = {-962, -855, -777, -751, -669, -441, -326, -321, -314, -307,
     -168, -166, -122, -51, -39, 4, 48, 142, 155, 193, 241, 257,
     324, 333, 334, 352, 359, 493, 823, 849, 878, 996};
     
    int T = 6411;
    int s = X.size();
    cout << "number of variables: " << s << endl;
    int threads = thread::hardware_concurrency();
    if (threads < 1) threads = 1;
    cout << "thread count: " << threads << endl;
    
    
    if ((threads == 1) || (s <= 10)) // don't use multiple threads if there's only 10 variables or less
    {
        // loop over all subsets in one thread
        for(unsigned long p = 0; p < (1ul<<s); p++)
        {
            if (s > 24)
            {
                // print some progress every 2^24 numbers
                if ((p & 0xFFFFFF) == 0) cout << (p >> 24) << "/" << (1 << (s-24)) << endl;
            }
            
            int sum = 0;
            auto p2 = p;
            int k = 0;
            while (p2 != 0)
            {
                if (p2 & 1) sum += X[k];
                p2 >>= 1;
                k++;
            }
            
            if (sum == T)
            {
                prettyprint(X, p, T);
            }
        }
    }
    else
    {
        int top_bits = 6; // amount of fixed bits, higher -> more smaller jobs
        assert(s > top_bits);
        
        SafeQueue<JobDesc, Worker> safequeue;
        vector<JobDesc> jobs;
        // make 2^n jobs each fixing the top n bits, looping over every bit below it
        for(unsigned long i = 0; i < (1ul << top_bits); i++)
        {
            jobs.push_back(JobDesc(i << (s-top_bits), (i+1) << (s-top_bits), X, T));
        }
        // add the jobs to the safequeue (have to do this after the previous loop so std::vector doesn't move its data and invalidate our pointers!)
        for(size_t i = 0; i < jobs.size(); i++)
        {
            safequeue.enqueue(&jobs[i]);
        }
        safequeue.start(threads);
        
        // loop over every job's solutions
        for(size_t i = 0; i < jobs.size(); i++)
        {
            for(unsigned long p: jobs[i].solutions)
            {
                prettyprint(X, p, T);
            }
        }
    }
}