
import time
from multiprocessing import Pool

# Total element count selected to demonstrate loop scalability
ARRAY_SIZE = 4000000
CHUNK_SIZE = 1000000

def process_data_chunk(chunk_data):
    # Simulates an intensive mathematical transformation loop inside a worker path
    return [(item * 3.14159) ** 2 for item in chunk_data]

def main():
    print("Initializing array element spaces...")
    data_list = list(range(ARRAY_SIZE))

    # Benchmark Sequential Loop Execution Pattern
    print("Executing standard sequential loop process...")
    start_sequential = time.time()
    sequential_results = []
    for item in data_list:
        sequential_results.append((item * 3.14159) ** 2)
    end_sequential = time.time()
    sequential_time = (end_sequential - start_sequential) * 1000

    # Benchmark Parallel Loop Level Execution Pattern via Slicing Chunks
    print("Executing enhanced parallel chunk loop process...")
    start_parallel = time.time()
    
    # Restructuring the loop by dividing the array into independent memory slices
    chunks = [data_list[i:i + CHUNK_SIZE] for i in range(0, ARRAY_SIZE, CHUNK_SIZE)]
    
    # Activating four concurrent execution pathways to map the split loop blocks
    with Pool(processes=4) as pool:
        parallel_chunk_results = pool.map(process_data_chunk, chunks)
        
    # Reassembling the independent output buffers into a unified collection
    parallel_results = [item for sublist in parallel_chunk_results for item in sublist]
    end_parallel = time.time()
    parallel_time = (end_parallel - start_parallel) * 1000

    print("\n=== LOOP LEVEL ACCELERATION TELEMETRY ===")
    print(f"Sequential Loop Execution Runtime: {sequential_time:.3f} ms")
    print(f"Parallel Chunk Loop Execution Runtime: {parallel_time:.3f} ms")
    print(f"Measured Acceleration Multiplier: {(sequential_time / parallel_time):.3f}x")

if __name__ == "__main__":
    main()

