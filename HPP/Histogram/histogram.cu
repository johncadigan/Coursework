#include <iostream>
#include <cuda.h>
#include <cstdlib>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <algorithm>


#define HISTOGRAM_LENGTH 256
#define CBLOCK 512


//@@ insert code here
__global__
	void FtoCKernel(float *IIData, unsigned char *ICData, int Ipixels){
	int pos = blockIdx.x*CBLOCK+threadIdx.x;
	if(pos < Ipixels) ICData[pos] = (unsigned char) 255.0 * IIData[pos];
}

__global__
	void RtoGKernel(unsigned char *IIData, unsigned char *ICGData, int Ipixels){
	int i = blockIdx.x*CBLOCK+threadIdx.x*3;
	if(i < Ipixels*3){
		ICGData[i] = (unsigned char) (0.21*IIData[i] + 0.71*IIData[i+1] + 0.07*IIData[i+2] );  
	}
	
}

__global__
	void HKernel(unsigned char * IIData, unsigned int * IHistogram, int Ipixels){
	int b = blockIdx.x *blockDim.x; 
        int t = threadIdx.x;
	__shared__ int pHistogram[HISTOGRAM_LENGTH];
	if(t < HISTOGRAM_LENGTH)pHistogram[t] = 0;
	__syncthreads();
	int i = b+t;
	int s = blockDim.x* gridDim.x;
	while(i < Ipixels){
		atomicAdd( &(pHistogram[IIData[i]]), 1);
		i+=s;
	}
	__syncthreads();
	if(t < HISTOGRAM_LENGTH)atomicAdd( &(IHistogram[t]), pHistogram[t]);	
}

__global__
	void CDFKernel(unsigned int * IHistogram, float * ICDF, float fIarea){ 
    int t = threadIdx.x;
	if(t < HISTOGRAM_LENGTH) ICDF[t] = 0.0;
	//reductio
	for(int s = 1; s <= HISTOGRAM_LENGTH/2; s*=2){
        int i = (t+1)*s*2-1;
        if (i < HISTOGRAM_LENGTH) ICDF[i] += (float) ICDF[i-s] / fIarea;         
        __syncthreads();
        
    }
	//post-reduction
    for(int s =  HISTOGRAM_LENGTH/4; s > 0; s /= 2){
        __syncthreads();
        int j = (t+1)*s*2-1; // Same as other index
        if(j+s < HISTOGRAM_LENGTH)ICDF[j+s] += (float) ICDF[j] / fIarea;
    } 
}

__global__
void CDFminKernel(float * I, float minv) {
    
    int t = threadIdx.x;
    __shared__ int pMin[HISTOGRAM_LENGTH];
    if(t < HISTOGRAM_LENGTH)pMin[t] = I[t];//First half
    __syncthreads();
    for(int s = blockDim.x/2; s > 0; s/=2){
        __syncthreads();
        if(t < s) pMin[t] = (pMin[t] < pMin[t+s]) ? pMin[t+s] : pMin[t];
    }
    minv = pMin[0];
}

void populateArray(float a[], int l){
        srand48(time(NULL));
        float prev = drand48();
        float nxt;
	for(int i = 1; i < l; i++){
        	do{
		    nxt = drand48(); 
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
    //int lengths[5] = {5, 10, 20, 40, 50};
    //for(int x=0; x < 5; x++){
    //int ilen = lengths[x];
    int ilen = 5;
    int imageWidth = ilen;
    int imageHeight = ilen;
    int imageChannels = 3;
    float * hostInputImageData;
    float * hostOutputImageData;
    const char * inputImageFile;
    float * dInputImageData;
    unsigned char * dcharImageData;
    unsigned char * charImageData; // host
    unsigned char * dcharGImageData;
    unsigned char * charGImageData; // host
    unsigned int * dImageHistogram;
    float * dImageCDF;
    float dminCDF;
    float * dOutputImageData;
    printf("Size %dx%d\n", ilen, ilen);
    int imageArea = imageWidth*imageHeight;
    float I[imageArea*imageChannels];
    populateArray(I, imageArea*imageChannels);
    //Cuda malloc
    cudaMalloc((void **) &dInputImageData, imageArea * imageChannels * sizeof(float));
    cudaMalloc((void **) &dcharImageData, imageArea * imageChannels * sizeof(unsigned char));
//    cudaMalloc((void **) &dImageHistogram, HISTOGRAM_LENGTH * sizeof(unsigned int));
//    cudaMalloc((void **) &dImageCDF, HISTOGRAM_LENGTH * sizeof(float));
//    cudaMalloc((void **) &dminCDF, sizeof(float));
//    cudaMalloc((void **) &dOutputImageData, imageArea * sizeof(float));
    //Cuda memcpy
    cudaMemcpy(dInputImageData,
               hostInputImageData,
               imageArea * imageChannels *sizeof(float),
               cudaMemcpyHostToDevice);
    //Cuda conv 1
    dim3 dimCGrid = (imageArea*imageChannels-1)/CBLOCK + 1; 
    dim3 dimCBlock = CBLOCK;
    FtoCKernel<<<dimCGrid, dimCBlock>>>(dInputImageData,dcharImageData,imageArea*imageChannels);
    cudaDeviceSynchronize();    
    //Cuda conv 2
    //dim3 dimGGrid = (imageArea-1)/CBLOCK + 1;
    //dim3 dimGBlock = CBLOCK;
    //RtoGKernel<<<dimGGrid, dimGBlock>>>(dcharImageData, dcharGImageData, imageArea);
    //cudaDeviceSynchronize(); 
    //Cuda mcpy to compare
    printf("Copying back\n");
    cudaError_t err = cudaMemcpy(charImageData,dcharImageData, imageArea * imageChannels *sizeof(unsigned char), cudaMemcpyDeviceToHost);
    printf("Copied\n");
    printf("Error %s\n", cudaGetErrorString(err));

//    for(int i = 0; i < imageArea*imageChannels; i ++){
//        unsigned char dres = charImageData[i];
//        unsigned char cres = (unsigned char) 255 * I[i];
//        if(dres != cres)printf("%c != %c at %d\n",dres, cres, i);
//        else printf("OK at %d\n", i);
//    }
    //cudaMemcpy(charGImageData,
    //           dcharGImageData,
    //           imageArea *sizeof(unsigned char),
    //           cudaMemcpyDeviceToHost);
    //for(int i = 0; i < imageArea; i++){
    //		if(charGImageData[i] != (unsigned char) (0.21*charImageData[i] + 0.71*charImageData[i+1] + 0.07*charImageData[i+2] ))printf("Error at %d", i);
    //}

    
    cudaFree(dInputImageData);cudaFree(dcharImageData);cudaFree(dcharImageData);
    cudaFree(dImageCDF); cudaFree(dOutputImageData);
    //}
    return 0;
}

