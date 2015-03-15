#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <time.h>

int SIZE = 2;
__global__ 
void vecAddK(float *A, float *B, float *C, int len)
{
	int i = threadIdx.x+blockDim.x*blockIdx.x;
        if(i<len) C[i] = A[i] + B[i];

}

__host__
void vecAdd(float *h_A, float *h_B, float *h_C, int len){
    int size = len*sizeof(float);
    float *d_A, *d_B, *d_C;

    cudaMalloc((void **) &d_A, size);
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    
    cudaMalloc((void **) &d_B, size);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);
    
    cudaMalloc((void **) &d_C, size);
    
    dim3 DimGrid((len-1)/256 +1, 1, 1);
    dim3 DimBlock(256, 1, 1);
    vecAddK<<<DimGrid, DimBlock>>>(d_A, d_B,d_C, len);
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);
    cudaFree(d_A);cudaFree(d_B);cudaFree(d_C);

}

void populateArray(float a[]){
	for(int i = 0; i < SIZE; i++){
        	srand48(time(NULL)); 
		a[i] = drand48() * 100;
	}
}


int main(){
    float A[SIZE];float B[SIZE];float C[SIZE];
    populateArray(A);
    populateArray(B);

    int block_size = 16;
    vecAdd(A,B,C,SIZE);
    std::cout << A[0] << " + " << B[0] << "=" << C[0] << std::endl; 


	return 0;
}

