#include <cstdlib>
#include <time.h>
#include <iostream>
#include <string>
#include <sstream>

class Matrix {
     public:
     int x; int y;
     float* a;
     Matrix(int len, int wid){
        x = len;
        y = wid;
        std::cout << "Initializing " << x << "x" << y << std::endl;
        srand48(time(NULL));
        a = new float[x*y];
        for(int i = 0; i < x * y; i++){
        a[i] = drand48() * 10.0;
        }
     }
     Matrix(int len, int wid, float * ar):x(len), y(wid),  a(ar) {std::cout <<"Initializing from array" << std::endl;}
     ~Matrix(){}
     void print(){
         std::ostringstream pform;
         for(int i = 0; i < x * y; i++){
            pform << " " << a[i];
            if((i+1) % x == 0){
            std::cout <<pform.str()<<std::endl;
            pform.str("");
            pform.clear();
            }
         }
         for(int i = 0; i < x * y; i++){
             pform << " " << a[i];
             if((i+1) % x == 0 && i+1 <x*y){pform<<";";}
         }
         std::cout << std::endl << "numpy.matrix(\""<<pform.str() << "\")" <<std::endl;
     };
};
