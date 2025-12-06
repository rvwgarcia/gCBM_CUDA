import numpy as np
import time

# Define a wrapper that uses NumPy when CUDA GPU is unavailable
def use_cupy_or_numpy(use_gpu):
    if use_gpu:
        try:
            import cupy as cp
            
            # Check if CUDA is available
            if cp.cuda.is_available():
                device = cp.cuda.runtime.getDevice()
                props = cp.cuda.runtime.getDeviceProperties(device)

                cuda_version = cp.cuda.runtime.runtimeGetVersion()
                major = cuda_version // 1000
                minor = (cuda_version % 1000) // 10
                print(f"\n✅ CUDA available. Runtime Version: {major}.{minor}")
                print(f"Using GPU {device}: {props['name'].decode()}")
                print(f"  Total Memory: {props['totalGlobalMem'] / 1e9:.2f} GB")
                print(f"  Multiprocessors: {props['multiProcessorCount']}")
                return cp
            else:
                print("❌ CUDA GPU not available: Using CPU")
                return np
        except ImportError:
            print("CuPy not installed, using NumPy")
            return np
    else:
        print("Using CPU")
        return np
    
#Force CPU:
xp = use_cupy_or_numpy(use_gpu=False)  

tic = time.time()

N = 1024
A = xp.random.rand(N,N)
B = xp.random.rand(N,N)
C = A * B
D = xp.linalg.inv(C)

elapsed_time = time.time() - tic
print(f"Elapsed time on CPU: {elapsed_time:.4f} seconds")

#Force GPU:
xp = use_cupy_or_numpy(use_gpu=True)  
tic = time.time()

N = 1024
A = xp.random.rand(N,N)
B = xp.random.rand(N,N)
C = A @ B
D = xp.linalg.inv(C)

elapsed_time = time.time() - tic
print(f"Elapsed time with CUDA: {elapsed_time:.4f} seconds")