import time
import numpy as np

# Size of data array selected to exceed standard cache residency bounds
ARRAY_SIZE = 16777216

def execute_scalar_addition(list_a, list_b):
    # Simulates standard scalar behavior via an explicit processing loop
    c = []
    for i in range(ARRAY_SIZE):
        c.append(list_a[i] + list_b[i])
    return c

def execute_vector_addition(arr_a, arr_b):
    # Simulates dedicated array pipeline structures via optimized array math
    return arr_a + arr_b

def main():
    # Constructing data points
    print("Populating data configurations...")
    list_a = [1.5] * ARRAY_SIZE
    list_b = [2.5] * ARRAY_SIZE

    arr_a = np.array(list_a, dtype=np.float32)
    arr_b = np.array(list_b, dtype=np.float32)

    # Benchmark Scalar Pipeline Execution
    print("Running scalar loop simulation...")
    start_scalar = time.time()
    execute_scalar_addition(list_a, list_b)
    end_scalar = time.time()
    scalar_duration = (end_scalar - start_scalar) * 1000

    # Benchmark Vector Pipeline Execution
    print("Running vector array simulation...")
    start_vector = time.time()
    execute_vector_addition(arr_a, arr_b)
    end_vector = time.time()
    vector_duration = (end_vector - start_vector) * 1000

    print("\n=== SIMULATION RESULTS ===")
    print(f"Scalar Core Loop Duration: {scalar_duration:.3f} ms")
    print(f"Vector Processing Loop Duration: {vector_duration:.3f} ms")
    print(f"Measured Acceleration Factor: {(scalar_duration / vector_duration):.3f}x")

if __name__ == "__main__":
    main()
