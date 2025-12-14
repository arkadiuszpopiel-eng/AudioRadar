"""
GPU Performance Benchmarking (v4.3.1 ULEPSZENIE #2)

Benchmark GPU vs CPU FFT performance and provide metrics.
"""

import numpy as np
import time
from typing import Dict, Any
from core.logger import log


class GPUBenchmark:
    """
    GPU performance benchmarking and optimization.

    Measures FFT performance with different array sizes to determine
    optimal GPU vs CPU cutoff points.
    """

    def __init__(self, gpu_accelerator=None):
        """
        Initialize GPU benchmark.

        Args:
            gpu_accelerator: GPUAccelerator instance (optional)
        """
        self.gpu_accelerator = gpu_accelerator
        self.results = {}
        self.gpu_enabled = gpu_accelerator is not None and gpu_accelerator.enabled

    def run_fft_benchmark(self, iterations: int = 100) -> Dict[str, Any]:
        """
        Benchmark FFT performance for different array sizes.

        Args:
            iterations: Number of iterations per test

        Returns:
            Dictionary with benchmark results
        """
        log("Starting GPU FFT benchmark...", "INFO")

        sizes = [512, 1024, 2048, 4096, 8192, 16384]
        results = {}

        for size in sizes:
            # Generate test signal
            signal = np.random.randn(size).astype(np.float32)

            # Benchmark CPU
            start_cpu = time.perf_counter()
            for _ in range(iterations):
                np.fft.rfft(signal)
            cpu_time = (time.perf_counter() - start_cpu) / iterations

            # Benchmark GPU (if available)
            if self.gpu_enabled:
                start_gpu = time.perf_counter()
                for _ in range(iterations):
                    self.gpu_accelerator.fft_optimized(signal)
                gpu_time = (time.perf_counter() - start_gpu) / iterations
                speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            else:
                gpu_time = 0
                speedup = 0

            results[size] = {
                'cpu_time_ms': cpu_time * 1000,
                'gpu_time_ms': gpu_time * 1000 if self.gpu_enabled else None,
                'speedup': speedup,
                'faster': 'GPU' if speedup > 1 else 'CPU' if self.gpu_enabled else 'N/A'
            }

            log(f"FFT size={size}: CPU={cpu_time*1000:.3f}ms, GPU={gpu_time*1000:.3f}ms, Speedup={speedup:.2f}x", "INFO")

        self.results = results
        return results

    def get_recommendation(self) -> str:
        """
        Get recommendation for GPU usage based on benchmark results.

        Returns:
            Recommendation string
        """
        if not self.gpu_enabled:
            return "GPU not available - using CPU only"

        if not self.results:
            return "Run benchmark first with run_fft_benchmark()"

        # Find minimum size where GPU is faster
        gpu_faster_sizes = [
            size for size, data in self.results.items()
            if data['speedup'] > 1.0
        ]

        if not gpu_faster_sizes:
            return "GPU slower than CPU for all tested sizes - recommend CPU only"

        min_size = min(gpu_faster_sizes)
        max_speedup = max(data['speedup'] for data in self.results.values())

        return f"GPU recommended for FFT size >= {min_size} (max speedup: {max_speedup:.2f}x)"

    def generate_report(self) -> str:
        """
        Generate human-readable benchmark report.

        Returns:
            Formatted report string
        """
        if not self.results:
            return "No benchmark results available. Run run_fft_benchmark() first."

        report = []
        report.append("=" * 70)
        report.append("GPU FFT PERFORMANCE BENCHMARK (v4.3.1)")
        report.append("=" * 70)

        if self.gpu_enabled:
            gpu_info = self.gpu_accelerator.get_info()
            report.append(f"GPU Status: {gpu_info['backend']}")
            report.append(f"GPU Available: {gpu_info['gpu_available']}")
        else:
            report.append("GPU Status: Disabled")

        report.append("")
        report.append("FFT Performance Results:")
        report.append("-" * 70)
        report.append(f"{'Size':<10} {'CPU (ms)':<15} {'GPU (ms)':<15} {'Speedup':<10} {'Winner':<10}")
        report.append("-" * 70)

        for size, data in sorted(self.results.items()):
            cpu_time = f"{data['cpu_time_ms']:.3f}"
            gpu_time = f"{data['gpu_time_ms']:.3f}" if data['gpu_time_ms'] is not None else "N/A"
            speedup = f"{data['speedup']:.2f}x" if data['speedup'] > 0 else "N/A"
            faster = data['faster']

            report.append(f"{size:<10} {cpu_time:<15} {gpu_time:<15} {speedup:<10} {faster:<10}")

        report.append("-" * 70)
        report.append("")
        report.append("Recommendation:")
        report.append(self.get_recommendation())
        report.append("=" * 70)

        return "\n".join(report)


def run_gpu_benchmark_cli(gpu_accelerator=None):
    """
    Run GPU benchmark from command line.

    Args:
        gpu_accelerator: GPUAccelerator instance (optional)
    """
    benchmark = GPUBenchmark(gpu_accelerator)
    benchmark.run_fft_benchmark(iterations=100)
    print(benchmark.generate_report())


if __name__ == '__main__':
    # Run benchmark when executed directly
    print("GPU FFT Benchmark")
    print("Loading GPU accelerator...")

    try:
        from hardware.gpu import GPUAccelerator
        gpu = GPUAccelerator(enable_gpu=True)
        run_gpu_benchmark_cli(gpu)
    except ImportError:
        print("ERROR: Could not import GPUAccelerator")
        print("Run from app directory: python -m core.gpu_benchmark")
