import time
import numpy as np

SIMD_SIZE = 20000000

def scalar_multiply(list_a, list_b):
    # Emulates a scalar processor loop executing independent operations
    c = [0.0] * SIMD_SIZE
    for i in range(SIMD_SIZE):
        c[i] = list_a[i] * list_b[i]
    return c

def simd_multiply(arr_a, arr_b):
    # Leverages underlying SIMD architecture calls embedded within numpy
    return np.multiply(arr_a, arr_b)

def main():
    print("Initializing source data collections...")
    src_a_list = [2.0] * SIMD_SIZE
    src_b_list = [4.5] * SIMD_SIZE

    src_a_arr = np.array(src_a_list, dtype=np.float32)
    src_b_arr = np.array(src_b_list, dtype=np.float32)

    # Measure scalar multiplication runtime
    print("Measuring scalar multiplication pipeline...")
    start_scalar = time.time()
    scalar_multiply(src_a_list, src_b_list)
    end_scalar = time.time()
    scalar_time = (end_scalar - start_scalar) * 1000

    # Measure SIMD accelerated multiplication runtime
    print("Measuring SIMD multiplication pipeline...")
    start_simd = time.time()
    simd_multiply(src_a_arr, src_b_arr)
    end_simd = time.time()
    simd_time = (end_simd - start_simd) * 1000

    print("\n=== SIMD ACCELERATION METRIC COMPARISON ===")
    print(f"Scalar Vector Multiplication Runtime: {scalar_time:.3f} ms")
    print(f"SIMD Accelerated Multiplication Runtime: {simd_time:.3f} ms")
    print(f"Resulting Acceleration Multiplier: {(scalar_time / simd_time):.3f}x")

if __name__ == "__main__":
    main()
