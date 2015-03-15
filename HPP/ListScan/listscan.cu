#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


const int BLOCK = 256;


__global__ 
void ScanListK(float *I, float *O, int l)
{
    int b = blockIdx.x; 
    int t = threadIdx.x;
    
    __shared__ float tSum[BLOCK*2];
    int start = 2*blockDim.x*b;
        
    if(start+t < l){
          tSum[t] = I[start+t];
          //if(tSum[t]!=I[start+t])printf("Mismatch at %d\n", start+t);
     }
     else{
      tSum[t] = 0.0;//First half
     }
     if(start+blockDim.x+t < l){
          tSum[t+blockDim.x] = I[start+blockDim.x+t];
          //if(tSum[t+blockDim.x]!=I[start+blockDim.x+t])printf("Mismatch at %d\n", start+t+blockDim.x);
     } 
     else{ 
          tSum[t+blockDim.x] = 0.0;//Second half
     }
    __syncthreads();

    //Reduction
    for(int s = 1; s <= BLOCK; s*=2){
        int i = (t+1)*s*2-1;
        if (i < BLOCK*2) tSum[i] += tSum[i-s];         
        __syncthreads();
        
    }
    //Post-reduction
    
    for(int s = BLOCK/2; s > 0; s /= 2){
        __syncthreads();
        int j = (t+1)*s*2-1; // Same as other index
        if(j+s < 2*BLOCK)tSum[j+s] += tSum[j];
    } 
       
    
    if(start+t < l){
        O[start+t] = tSum[t];       
    } 
    if(t+start+blockDim.x < l) 
    O[t+start+blockDim.x] = tSum[t+blockDim.x];
    
}
__host__
void scanList(float *h_I, float * h_O, int h_l){
    
    float *d_I, *d_O;
    int olen;    
    olen = h_l / (BLOCK*2); //The output length equals twice the total of the length divided by width
    if ((h_l - olen*BLOCK*2) > 0) { 
        olen++;
    }
    printf("%d blocks\n", olen);
    cudaMalloc((void **) &d_I, sizeof(float)*h_l);
    cudaMalloc((void **) &d_O, sizeof(float)*h_l);
    
    
    cudaMemcpy(d_I, h_I, sizeof(float)*h_l, cudaMemcpyHostToDevice);
    cudaError_t error =  cudaGetLastError();   
    if(error!=cudaSuccess){
        fprintf(stderr,"ERROR1: %s\n", cudaGetErrorString(error) );
        
    }
    
    dim3 dimGrid(olen, 1, 1);
    dim3 dimBlock(BLOCK, 1, 1);
    
    ScanListK<<<dimGrid, dimBlock>>>(d_I, d_O, h_l);
 
    cudaDeviceSynchronize();
    error = cudaGetLastError();
    if(error!=cudaSuccess){
        fprintf(stderr,"ERROR: %s\n", cudaGetErrorString(error) );
        
    }
    cudaMemcpy(h_O, d_O, sizeof(float)*h_l, cudaMemcpyDeviceToHost);
    cudaFree(d_I);cudaFree(d_O);
    if(olen>1){
        for(int i = 1; i < olen; i++){
            float preSum = h_O[(BLOCK*i*2)-1];
	    for(int j = 0; j < 2*BLOCK; j++){
                int idx = (BLOCK*i*2)+j;
                if(idx < h_l){
                    h_O[idx]+=preSum;
                } 
            }
        }
    }
    
}

void populateArray(float a[], int l){
        srand48(time(NULL));
        float prev = drand48()*100;
        float nxt;
	for(int i = 1; i < l; i++){
        	do{
		    nxt = drand48()*10; 
                }while(nxt==prev);
            a[i] = nxt;
            prev = nxt;
	}
}

float absDif(float a, float b){
      float c = a-b;
      if(c < 0)c*=-1;
      return c;
}


int main(){
    int lengths[5] = {128, 256, 200, 1500, 1100};
    //for(int x=0; x < 5; x++){
    //int ilen = lengths[x];
    int ilen = 1500;
    float * I;
    I = new float [ilen];
    populateArray(I, ilen);
    printf("%d items\n", ilen);
    float gtotal[ilen];
    scanList(I,gtotal,ilen);
    float rtotal = 0.0;
    for(int i = 0; i < ilen; i ++){
            rtotal += I[i];
	    I[i]=rtotal;
     }
     for(int i =0; i < ilen; i++){
         float dif = absDif(I[i], gtotal[i]);
         if(dif > 1.0)printf("Mistatake @%d %f\n", i, dif); 
    }
    delete [] I;
    //}
    return 0;
}

