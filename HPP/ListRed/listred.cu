#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


const int BLOCK = 256;


__global__ 
void AddListK(float *I, float *O, int l)
{
    int b = blockIdx.x; 
    int t = threadIdx.x;
    __shared__ float pSum[BLOCK*2];
    unsigned int start = 2*blockDim.x*b;
    (start+t < l) ? pSum[t] = I[start+t]: pSum[t] = 0.0;//First half
    (start+blockDim.x+t < l) ? pSum[t+blockDim.x] = I[start+blockDim.x+t] : pSum[t+blockDim.x] = 0.0;//Second half
    __syncthreads();
    for(unsigned int s = blockDim.x; s > 0; s/=2){
        __syncthreads();
        (t < s) ? pSum[t] += pSum[t+s] : pSum[t]+= 0;
    }
    //printf("Sum =%f ", pSum[0]);
     
        O[b] = pSum[0];
    
}
__host__
double addList(float *h_I, int h_l){
    
    float *d_I, *d_O;
    int olen;    
    olen = h_l / (BLOCK<<1); //The output length equals twice the total of the length divided by width
    if (olen % (BLOCK<<1)) { 
        olen++;
    }
    
    float h_O[olen];
 
    cudaMalloc((void **) &d_I, sizeof(float)*h_l);
    cudaMalloc((void **) &d_O, sizeof(float)*olen);
    
      
    cudaMemcpy(d_I, h_I, sizeof(float)*h_l, cudaMemcpyHostToDevice); 
    
    
    dim3 dimGrid(olen, 1, 1);
    dim3 dimBlock(BLOCK, 1, 1);
    
    AddListK<<<dimGrid, dimBlock>>>(d_I, d_O, h_l);

    cudaMemcpy(h_O, d_O, sizeof(float)*olen, cudaMemcpyDeviceToHost);
    cudaFree(d_I);cudaFree(d_O);
    
    double total = 0.0;
    for(int i = 0; i < olen; i ++){
	total+=h_O[i];
    }
    return total;
}

void populateArray(float a[], int l){
        srand48(time(NULL));
        float prev = drand48()*100;
        float nxt;
	for(int i = 1; i < l; i++){
        	do{
		    nxt = drand48()*100; 
                }while(nxt==prev);
            a[i] = nxt;
            prev = nxt;
	}
}


int main(){
    srand(time(NULL));

    //int ilen = (rand() % 6553) * BLOCK;
    int ilen = 2000000;
    float I[ilen];
    populateArray(I, ilen);
    printf("Input length %d", ilen);
    time_t gstart = time(NULL);
    double gtotal = 0.0;
    for(int i = 0; i < 1000; i ++){
        gtotal = addList(I,ilen);
    }
    time_t gstop = time(NULL);
    time_t start = time(NULL);
    double total = 0.0;
    for(int i = 0; i < 1000; i ++){
        total = 0.0;
        for(int i = 0; i < ilen; i ++){
	    total+=I[i];
        }
    }
    time_t stop = time(NULL);
    printf("Average times\n GPU: %f    CPU: %f", difftime(gstop, gstart), difftime(stop, start));
    printf("TOTAL: %f == %f \n DIF: %f", total, gtotal, total-gtotal);

    return 0;
}

