import threading
import sys

ARRAY_SIZE = 1000000

a = 2.5
x = [1.0] * ARRAY_SIZE
y = [2.0] * ARRAY_SIZE

def daxpy_worker(start_idx, end_idx):
    for i in range(start_idx, end_idx):
        y[i] = a * x[i] + y[i]

def main():
    num_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    chunk_size = ARRAY_SIZE // num_threads
    threads = []
    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = ARRAY_SIZE if i == num_threads - 1 else (i + 1) * chunk_size
        t = threading.Thread(target=daxpy_worker, args=(start_idx, end_idx))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"Complete. y[0] = {y[0]}")

if __name__ == "__main__":
    main()
