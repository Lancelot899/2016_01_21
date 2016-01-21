#include <iostream>
#include <thread>
#include <functional>
#include <unistd.h>
#include <stdio.h>
#include <string>
#include <string.h>

void print(){
    std::cout << "hello thread~!" << std::endl;
}

void print_else(){
    std::cout << "hello thread x2" << std::endl;
}

class Foo{
public:
    void operator()()const{
        print();
        print_else();
    }
};

struct func{
    int& i;
    func(int&i_):i(i_){}
    void operator ()(){
        for(int j(0); j < 100000; ++j)
            printf("thread loops : %d, i = %d\n", j, i);
    }
};

void oops(){
    int some_local_state(0);
    func my_func(some_local_state);
    std::thread my_thread(my_func);
    my_thread.detach();
    sleep(1);
}


void f1(){
    int some_local_state = 0;
    func my_func(some_local_state);
    std::thread t(my_func);
    try{
        printf("my current thread\n");
    }
    catch(...){
        t.join();
        throw;
    }
    t.join();
}

class thread_guard{
    std::thread& t;
public:
    explicit thread_guard(std::thread& t_)
        :t(t_){}
    ~thread_guard(){
        if(t.joinable())
            t.join();
    }
    thread_guard(thread_guard const&) = delete;
    thread_guard& operator=(thread_guard const&) = delete;
};

void f2(){
    int some_local_state = 0;
    func my_func(some_local_state);
    std::thread t(my_func);
    thread_guard g(t);
    for(int i(0); i < 100; i++){
        printf("current thread\n");
    }
}

void f3(int i, const std::string& s){
    std::cout << "f3:" << i << "\tstring:" << s << std::endl;
}

void oops2(int some_param){
    char buffer[1024];
    memset(buffer, 0, 1024);
    sprintf(buffer, "hello");
    std::thread t(f3, 3,std::string(buffer));
    t.detach();
    printf("opps: %d\n", some_param);
}

class X{
public:
    void do_lengthy_word(int x){
        printf("x = %d\n",x);
    }
};

void testX(){
    int x(500);
    X my_x;
    std::thread t(&X::do_lengthy_word, &my_x, std::ref(x));
    t.join();
}

int main(){
    testX();
    return 0;
}

