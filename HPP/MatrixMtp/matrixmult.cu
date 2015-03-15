#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "matrix.h"

int SIZE = 16;

#define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true)
{
   if (code != cudaSuccess) 
   {
      fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
      if (abort) exit(code);
   }
}


   
__global__ 
void matrixMultK(float *A, float *B, float *C, int n, int m, int k)
{
    int Row = blockIdx.y*blockDim.y+threadIdx.y;
    int Col = blockIdx.x*blockDim.x+threadIdx.x;
    if ((Row < m) && (Col < k)){
        float Cvalue = 0.0;
        for(int i = 0; i < n; i++){
             Cvalue += A[Row*n+i]*B[Col+i*k];
        }
        C[Row*k+Col] = Cvalue;
        
    }
    
    
}
__host__
void matrixMult(float *h_A, float *h_B, float *h_C, int n, int m, int k){
    
    float *d_A, *d_B, *d_C; 
    cudaMalloc((void **) &d_A, sizeof(float)*n*m);
    cudaMalloc((void **) &d_B, sizeof(float)*n*k);
    cudaMalloc((void **) &d_C, sizeof(float)*k*m);    
    
    cudaMemcpy(d_A, h_A, sizeof(float)*n*m, cudaMemcpyHostToDevice); 
    cudaMemcpy(d_B, h_B, sizeof(float)*n*k, cudaMemcpyHostToDevice);
    
    dim3 dimGrid((k-1)/SIZE+1, (m-1)/SIZE+1, 1);
    dim3 dimBlock(SIZE, SIZE, 1);
    
    matrixMultK<<<dimGrid, dimBlock>>>(d_A,d_B,d_C,n,m,k);

    cudaMemcpy(h_C, d_C, sizeof(float)*k*m, cudaMemcpyDeviceToHost);
    cudaFree(d_A);cudaFree(d_B);cudaFree(d_C);
    
}


int main(){
    srand(time(NULL));
    int Ax, Ay, Bx, By;
    do {
    Ax = SIZE + rand() % SIZE;
    Ay = SIZE + rand() % SIZE;
    Bx = SIZE + rand() % SIZE;
    By = SIZE + rand() % SIZE;
    }while(Ax!=By);
    Matrix A (Ax,Ay);
    Matrix B (Bx,By);
    A.print();
    B.print();
    float c [A.y*B.x];
    matrixMult(A.a, B.a, c, A.x, A.y, B.x);
    Matrix C (B.x, A.y, c);
    C.print();
    return 0;
}

