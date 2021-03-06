#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


__global__ 
void AsyncvecAddK(int *A, int *B, int *C, int len, int offset)
{
	int i = threadIdx.x+blockDim.x*blockIdx.x+offset;
        if(i<len) C[i] = A[i] - B[i];

}

__global__
void vecAddK(int *A, int *B, int *C, int len)
{
	int i = threadIdx.x+blockDim.x*blockIdx.x;
        if(i<len) C[i] = A[i] - B[i];

}


void populateArray(int a[], int l){
        time(NULL);
        int prev = rand() % 10;
        int nxt;
	for(int i = 1; i < l; i++){
        	do{
		    nxt = rand() % 10; 
                }while(nxt==prev);
            a[i] = nxt;
            prev = nxt;
	}
}

__host__
void svecAdd(){
    
    int const items = 1;
    int const len = 1024*1024;
    int const nStreams = 4;
    ///Device query boilerplate
    int deviceCount = 0;
    
    cudaError_t error_id = cudaGetDeviceCount(&deviceCount);
    
    if (error_id != cudaSuccess)
    {
        printf("cudaGetDeviceCount returned %d\n-> %s\n", (int)error_id, cudaGetErrorString(error_id));
        printf("Result = FAIL\n");
        exit(EXIT_FAILURE);
    }

    // This function call returns 0 if there are no CUDA capable devices.
    if (deviceCount == 0)
    {
        printf("There are no available device(s) that support CUDA\n");
	return;
    }
    else
    {
        printf("Detected %d CUDA Capable device(s)\n", deviceCount);
    }
    int fastestDevice = 0;
    int fastestSpeed = 0;
    int bx = 0;
    int gx = 0;
    for (int dev = 0; dev < deviceCount; ++dev)
    {
        cudaSetDevice(dev);
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, dev);
        int speed = deviceProp.multiProcessorCount;
        if(speed > fastestSpeed){
	    fastestDevice = dev;
            fastestSpeed = speed;
            bx = deviceProp.maxThreadsDim[0];
            gx = deviceProp.maxGridSize[0];
	}
    }
    cudaSetDevice(fastestDevice);
    
    int BLOCK = 256; 
    while(BLOCK * gx < len && BLOCK < bx){///While current block size is too small  
        BLOCK *= 2;
    }

    //int A[items][len];
    //int B[items][len];
    
    ///float A[SIZE];float B[SIZE];float C[SIZE];
    //for(int i=0; i < items; i++){
        //int a[len];
	//populateArray(a, len);
        //int b[len];
	//populateArray(b, len);
        //for(int j=0; j < len; j++){
        //    A[i][j] = a[j];
        //    B[i][j] = b[j];
        //}
    //}

    int size = len*sizeof(int);
    cudaStream_t stream[nStreams];
    
    int * dA;
    int * hA;
    int * dB;
    int * hB;
    int * dC;
    int * hC;
    

    ///Create streams and allocated memory to accomodate one vector
    for (int i = 0; i < nStreams; ++i){
	cudaStreamCreate(&stream[i]);
    }

    cudaMallocHost((void**)&hA, size); 
    cudaMalloc((void **) &dA, size);
    cudaMalloc((void **) &dB, size);
    cudaMallocHost((void**)&hB, size);
    cudaMalloc((void **) &dC, size);
    cudaMallocHost((void**)&hC, size);
    
    float gms = 0.0; //Time for all Asynch GPU
    float sgms = 0.0; //Time for all synch GPU
    float cms = 0.0; //Time for all CPU
    cudaEvent_t startEvent, stopEvent;
    cudaEventCreate(&startEvent);
    cudaEventCreate(&stopEvent);
    int segSize = len/nStreams;
    dim3 DimGrid = (segSize-1)/BLOCK + 1;
    dim3 DimBlock = BLOCK;
    
    for(int h = 0; h < items; h++){
        populateArray(hA, len);
        populateArray(hB, len);
        //int * hA = A[h];
        //int * hB = B[h];
        float ms;
        cudaEventRecord(startEvent,0);    
	for(int i = 0; i < nStreams; i++){ //transfer and compute with segment size
            int offset = i * segSize;
	    cudaMemcpyAsync(&dA[offset], &hA[offset], segSize*sizeof(int), cudaMemcpyHostToDevice, stream[i]);
	    cudaMemcpyAsync(&dB[offset], &hB[offset], segSize*sizeof(int), cudaMemcpyHostToDevice, stream[i]);	
	    AsyncvecAddK<<<DimGrid, DimBlock, 0 , stream[i%nStreams]>>>(dA,dB,dC,len, offset);
            cudaMemcpyAsync(&hC[offset], &dC[offset], segSize*sizeof(int), cudaMemcpyDeviceToHost, stream[i]);
            cudaStreamSynchronize(stream[i]);   
        }
        cudaEventRecord(stopEvent, 0);
        cudaEventSynchronize(stopEvent);
        cudaEventElapsedTime(&ms, startEvent, stopEvent);
        gms+=ms;
    	ms = 0.0;
        dim3 DimSGrid((len-1)/BLOCK + 1);
        dim3 DimSBlock(BLOCK);
        cudaEventRecord(startEvent,0);
	cudaMemcpy(dA, hA, size, cudaMemcpyHostToDevice);
        cudaMemcpy(dB, hB, size, cudaMemcpyHostToDevice);
        vecAddK<<<DimSGrid, DimSBlock>>>(dA, dB,dC, len);
	cudaMemcpy(hC, dC, size, cudaMemcpyDeviceToHost);
        cudaEventRecord(stopEvent, 0);
        cudaEventSynchronize(stopEvent);
        cudaEventElapsedTime(&ms, startEvent, stopEvent);
        sgms+=ms;

        time_t start, end;
        time(&start); 
        for(int j = 0; j < len; j++){//cpu
           hC[j]=hA[j]-hB[j];
	}
        time(&end);
        cms += (float) difftime(end, start)*1000;   
     }
    printf("Async GPU: %f\nGPU: %f\nCPU: %f\n", sgms/ (float) items, gms / (float) items, cms / (float) items);
    
    cudaFree(dA);cudaFree(dB);cudaFree(dC);
    for (int i = 0; i < nStreams; ++i)cudaStreamDestroy(stream[i]);
}


int main(){

    svecAdd();
    return 0;
}

