import argparse
from pathlib import Path

import numpy as np


RTOL = 1e-9
ATOL = 1e-9


def generate_matrices(size, seed=42):
    if size <= 0:
        raise ValueError("Matrix size must be positive")
    generator = np.random.default_rng(seed)
    return generator.uniform(-10, 10, (size, size)), generator.uniform(-10, 10, (size, size))


def write_matrix(path, matrix):
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be nonempty and square")
    if not np.isfinite(matrix).all():
        raise ValueError("Matrix must contain only finite values")

    with Path(path).open("w", encoding="utf-8") as output:
        output.write(f"{matrix.shape[0]}\n")
        np.savetxt(output, matrix, fmt="%.17g")


def read_matrix(path):
    with Path(path).open("r", encoding="utf-8") as source:
        header = source.readline().strip()
        if not header.isascii() or not header.isdigit() or int(header) <= 0:
            raise ValueError(f"{path}: first line must contain a positive integer")
        size = int(header)
        values = source.read().split()

    if len(values) != size * size:
        raise ValueError(f"{path}: expected {size * size} values, got {len(values)}")
    try:
        matrix = np.asarray(values, dtype=np.float64).reshape(size, size)
    except ValueError as error:
        raise ValueError(f"{path}: invalid matrix value") from error
    if not np.isfinite(matrix).all():
        raise ValueError(f"{path}: matrix contains a non-finite value")
    return matrix


def reference_product(a, b):
    if a.ndim != 2 or a.shape[0] == 0 or a.shape[0] != a.shape[1] or b.shape != a.shape:
        raise ValueError("A and B must be nonempty square matrices of equal size")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Input matrices contain a non-finite value")
    with np.errstate(over="raise", invalid="raise"):
        return a @ b


def compare_result(expected, actual, rtol=RTOL, atol=ATOL):
    if actual.shape != expected.shape:
        raise ValueError(f"Result shape {actual.shape} differs from {expected.shape}")
    if not np.isfinite(expected).all() or not np.isfinite(actual).all():
        raise ValueError("Result or reference contains a non-finite value")
    with np.errstate(over="ignore"):
        max_abs = float(np.max(np.abs(actual - expected)))
    return {
        "passed": bool(np.allclose(actual, expected, rtol=rtol, atol=atol)),
        "accuracy_max_abs": max_abs,
    }


def verify_files(a_path, b_path, c_path):
    a = read_matrix(a_path)
    b = read_matrix(b_path)
    return compare_result(reference_product(a, b), read_matrix(c_path))


def main():
    parser = argparse.ArgumentParser(description="Verify C against NumPy A @ B")
    parser.add_argument("a", type=Path)
    parser.add_argument("b", type=Path)
    parser.add_argument("c", type=Path)
    args = parser.parse_args()
    try:
        result = verify_files(args.a, args.b, args.c)
    except (OSError, ValueError, FloatingPointError) as error:
        parser.exit(1, f"Verification error: {error}\n")

    print(f"passed={result['passed']}")
    print(f"accuracy_max_abs={result['accuracy_max_abs']:.17g}")
    print(f"rtol={RTOL}")
    print(f"atol={ATOL}")
    if not result["passed"]:
        parser.exit(1, "Verification failed: result differs from NumPy A @ B\n")


if __name__ == "__main__":
    main()
