import argparse
import csv
import gc
import os
import platform
import statistics
import time


# mede o tempo de execução de uma função em microssegundos
def timed(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_us = (time.perf_counter() - start) * 1_000_000
    return result, elapsed_us


# simula uma requisição do chatbot: aloca, escreve, lê e libera memória
def simulate_chatbot_request(block_size: int, payload_seed: int):
    buffer, t_alloc = timed(bytearray, block_size)

    payload = ((payload_seed * 2654435761) % 256)

    def write_payload():
        for i in range(block_size):
            buffer[i] = (payload + i) % 256

    _, t_write = timed(write_payload)

    def read_payload():
        checksum = 0
        for i in range(block_size):
            checksum = (checksum + buffer[i]) % 256
        return checksum

    _, t_read = timed(read_payload)

    holder = {"buffer": buffer}
    del buffer

    def free_block():
        del holder["buffer"]
        gc.collect()

    _, t_free = timed(free_block)

    return {
        "alloc_us": t_alloc,
        "write_us": t_write,
        "read_us": t_read,
        "free_us": t_free,
        "total_us": t_alloc + t_write + t_read + t_free,
    }


# repete a simulação de requisição várias vezes e junta os resultados
def run_benchmark(num_requests: int, block_size: int):
    results = []
    for i in range(num_requests):
        results.append(simulate_chatbot_request(block_size, payload_seed=i))
    return results


# calcula média, mediana, desvio padrão, mínimo e máximo de um campo
def summarize(results, field):
    values = [r[field] for r in results]
    return {
        "media": statistics.mean(values),
        "mediana": statistics.median(values),
        "desvio_padrao": statistics.pstdev(values) if len(values) > 1 else 0.0,
        "minimo": min(values),
        "maximo": max(values),
    }


# grava os resultados de cada requisição em um arquivo csv
def save_csv(results, path):
    fieldnames = ["request_id", "alloc_us", "write_us", "read_us", "free_us", "total_us"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, r in enumerate(results):
            row = {"request_id": i}
            row.update(r)
            writer.writerow(row)


# lê os parâmetros da linha de comando, roda o benchmark e mostra o resumo
def main():
    parser = argparse.ArgumentParser(
        description="microbenchmark de operações de memória (cenário: chatbot municipal)."
    )
    parser.add_argument("--requests", type=int, default=10000,
                         help="número de requisições simuladas (padrão: 10000)")
    parser.add_argument("--block-size", type=int, default=4096,
                         help="tamanho do bloco de memória em bytes por requisição (padrão: 4096)")
    parser.add_argument("--out", type=str, default="resultados.csv",
                         help="arquivo csv de saída (padrão: resultados.csv)")
    args = parser.parse_args()

    print("=== microbenchmark de operações de memória ===")
    print(f"sistema operacional : {platform.system()} {platform.release()}")
    print(f"máquina             : {platform.machine()}")
    print(f"python              : {platform.python_version()}")
    print(f"requisições         : {args.requests}")
    print(f"tamanho do bloco    : {args.block_size} bytes")
    print()

    results = run_benchmark(args.requests, args.block_size)

    print("--- resumo estatístico (microssegundos) ---")
    for field in ["alloc_us", "write_us", "read_us", "free_us", "total_us"]:
        stats = summarize(results, field)
        print(f"{field:10s} | media={stats['media']:.2f} "
              f"mediana={stats['mediana']:.2f} "
              f"desvio={stats['desvio_padrao']:.2f} "
              f"min={stats['minimo']:.2f} max={stats['maximo']:.2f}")

    save_csv(results, args.out)
    print()
    print(f"resultados detalhados salvos em: {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
