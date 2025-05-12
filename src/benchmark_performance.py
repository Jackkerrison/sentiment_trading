# src/benchmark_performance.py

import time
from .load_dummy import load_articles
from .finbert_prototype import analyse_and_signal

def benchmark(sentences):
    # 1. Warm-up
    for s in sentences[:5]:
        analyse_and_signal(s)

    # 2. Timed runs
    times = []
    for text in sentences:
        start = time.perf_counter()
        analyse_and_signal(text)
        end = time.perf_counter()
        times.append(end - start)

    # 3. Report
    total = len(times)
    avg   = sum(times) / total
    mn    = min(times)
    mx    = max(times)
    print(f"Processed {total} samples")
    print(f"Average latency: {avg:.4f} s/sample")
    print(f"Min latency:     {mn:.4f} s")
    print(f"Max latency:     {mx:.4f} s")

if __name__ == "__main__":
    # Load your dummy feed
    data     = load_articles()
    texts    = [art["text"] for art in data]
    # Repeat to have a larger batch (e.g. 50)
    pool     = texts * (50 // len(texts) + 1)
    to_test  = pool[:50]

    benchmark(to_test)
