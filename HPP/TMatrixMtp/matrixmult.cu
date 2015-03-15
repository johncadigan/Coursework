#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "matrix.h"

const int SIZE = 4;


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
    int bx = blockIdx.x; int by = blockIdx.y;
    int tx = threadIdx.x; int ty = threadIdx.y;

    int Row = by*blockDim.y+ty;
    int Col = bx*blockDim.x+tx;
    __shared__ float s_A[SIZE][SIZE]; 
    __shared__ float s_B[SIZE][SIZE];
    
    float Cvalue = 0.0; 
    for(int t = 0; t < (n-1)/SIZE+1; t ++){
        if(t*SIZE+tx < n && Row < m){
            s_A[ty][tx] = A[Row*n+t*SIZE+tx];
        }
        else{
            s_A[ty][tx] = 0.0;
        }
        if(Col < k && t*SIZE+ty< n){
            s_B[ty][tx] = B[Col+(t*SIZE+ty)*k];
        }
        else{
            s_B[ty][tx] = 0.0;
        }
        
        __syncthreads();
        for(int i = 0; i < SIZE; i++){
             Cvalue += s_A[ty][i]*s_B[i][tx];
        };
        __syncthreads();
    }
    if(Row < k && Col < m){
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
    //Ax = SIZE + (rand() % SIZE)*2;
    //Ay = SIZE + (rand() % SIZE)*2;
    //Bx = SIZE + (rand() % SIZE)*2;
    //By = SIZE + (rand() % SIZE)*2;
    Ax = 128;
    Ay = 100;
    Bx = 56;
    By = 128;
    }while(Ax!=By);
    Matrix A (Ax,Ay);
    Matrix B (Bx,By);
    //float x[] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0};
    //float y[] = {1,0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0};
    //Matrix A (3,3,x);
    //Matrix B (3,3,y);
    
    A.print();
    B.print();
    float c [A.y*B.x];
    matrixMult(A.a, B.a, c, A.x, A.y, B.x);
    Matrix C (B.x, A.y, c);
    C.print();
    return 0;
}

