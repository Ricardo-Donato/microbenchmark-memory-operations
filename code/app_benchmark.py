import argparse
import csv
import gc
import hashlib
import os
import platform
import time


# mede o tempo de execução de uma função, em milissegundos
def timed_ms(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


# executa um teste completo: alocar, escrever, ler e liberar um bloco
def run_single_test(block_size_mb, pattern):
    size_bytes = block_size_mb * 1024 * 1024

    buffer, t_alloc = timed_ms(bytearray, size_bytes)
    holder = {"buffer": buffer}
    del buffer

    def write_block():
        holder["buffer"][:] = pattern

    _, t_write = timed_ms(write_block)

    _, t_read = timed_ms(lambda: hashlib.md5(holder["buffer"]).digest())

    def free_block():
        del holder["buffer"]
        gc.collect()

    _, t_free = timed_ms(free_block)

    return t_alloc, t_write, t_read, t_free


# roda todos os blocos e repetições definidos, gravando o csv linha a linha
def run_all_tests(out_path, block_min, block_max, block_step, repetitions):
    block_sizes = list(range(block_min, block_max + 1, block_step))
    fieldnames = ["bloco_MB", "teste", "alloc_ms", "write_ms", "read_ms", "free_ms"]

    start_total = time.perf_counter()

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for block_mb in block_sizes:
            pattern = os.urandom(block_mb * 1024 * 1024)
            block_start = time.perf_counter()

            for teste in range(1, repetitions + 1):
                t_alloc, t_write, t_read, t_free = run_single_test(block_mb, pattern)
                writer.writerow({
                    "bloco_MB": block_mb,
                    "teste": teste,
                    "alloc_ms": round(t_alloc, 4),
                    "write_ms": round(t_write, 4),
                    "read_ms": round(t_read, 4),
                    "free_ms": round(t_free, 4),
                })

            f.flush()
            block_elapsed = time.perf_counter() - block_start
            print(f"bloco {block_mb} mb concluído ({repetitions} testes em {block_elapsed:.1f}s)")

    total_elapsed = time.perf_counter() - start_total
    return len(block_sizes) * repetitions, total_elapsed


# lê os parâmetros da linha de comando e conduz a execução do experimento
def main():
    parser = argparse.ArgumentParser(
        description="microbenchmark oficial de operações de memória (alocação, escrita, leitura, liberação)."
    )
    parser.add_argument("--out", type=str, default="resultados.csv",
                         help="arquivo csv de saída (padrão: resultados.csv)")
    parser.add_argument("--block-min", type=int, default=100,
                         help="menor tamanho de bloco, em mb (padrão: 100)")
    parser.add_argument("--block-max", type=int, default=1000,
                         help="maior tamanho de bloco, em mb (padrão: 1000)")
    parser.add_argument("--block-step", type=int, default=100,
                         help="incremento entre tamanhos de bloco, em mb (padrão: 100)")
    parser.add_argument("--repetitions", type=int, default=100,
                         help="número de repetições por tamanho de bloco (padrão: 100)")
    args = parser.parse_args()

    print("=== microbenchmark oficial de operações de memória ===")
    print(f"sistema operacional : {platform.system()} {platform.release()}")
    print(f"máquina             : {platform.machine()}")
    print(f"python              : {platform.python_version()}")
    print(f"blocos              : {args.block_min} a {args.block_max} mb, passo {args.block_step} mb")
    print(f"repetições por bloco: {args.repetitions}")
    print()

    total_testes, total_elapsed = run_all_tests(
        args.out, args.block_min, args.block_max, args.block_step, args.repetitions
    )

    print()
    print(f"total de testes gravados : {total_testes}")
    print(f"tempo total de execução  : {total_elapsed / 60:.1f} minutos")
    print(f"resultados salvos em     : {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()import argparse
import gc
import platform
import statistics
import threading
import time
from datetime import datetime

import psutil


# tenta obter modelo de processador prsa multiplataforma
def get_cpu_model():
    name = platform.processor()
    if name:
        return name

    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass

    return "não identificado"


# lista as particoes de disco e o espaco total/usado/livre de cada
def get_disk_info():
    disks = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        disks.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "total_gb": usage.total / (1024 ** 3),
            "used_gb": usage.used / (1024 ** 3),
            "free_gb": usage.free / (1024 ** 3),
        })
    return disks


# monta resumo do hardware do dispositivo (cpu, memoria, discos)
def gather_hardware_info():
    freq = None
    try:
        freq = psutil.cpu_freq()
    except (AttributeError, NotImplementedError, FileNotFoundError):
        freq = None

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "sistema": f"{platform.system()} {platform.release()}",
        "versao_detalhada": platform.version(),
        "arquitetura": platform.machine(),
        "processador": get_cpu_model(),
        "nucleos_fisicos": psutil.cpu_count(logical=False),
        "nucleos_logicos": psutil.cpu_count(logical=True),
        "frequencia_atual_mhz": freq.current if freq else None,
        "frequencia_max_mhz": freq.max if freq and freq.max else None,
        "ram_total_gb": vm.total / (1024 ** 3),
        "swap_total_gb": swap.total / (1024 ** 3),
        "discos": get_disk_info(),
    }


# simula requisicao: aloca, escreve, le e libera um bloco de memoria
def simulate_request(block_size_mb: int, seed: int):
    size_bytes = block_size_mb * 1024 * 1024
    buffer = bytearray(size_bytes)

    payload = (seed * 2654435761) % 256
    step = max(1, size_bytes // 4096)
    for i in range(0, size_bytes, step):
        buffer[i] = (payload + i) % 256

    checksum = 0
    for i in range(0, size_bytes, step):
        checksum = (checksum + buffer[i]) % 256

    del buffer
    gc.collect()
    return checksum


# executa simulacao de carga com o numero de requisicoes definido
def run_load(num_requests: int, block_size_mb: int, stop_flag: dict):
    for i in range(num_requests):
        simulate_request(block_size_mb, seed=i)
    stop_flag["done"] = True


# tenta ler temperatura dos sensor d hardware, se o so permitir
def read_temperatures():
    try:
        temps = psutil.sensors_temperatures()
    except (AttributeError, NotImplementedError):
        return None

    if not temps:
        return None

    result = {}
    for name, entries in temps.items():
        for entry in entries:
            label = entry.label or name
            result[f"{name}_{label}"] = entry.current
    return result


# coleta amostras de cpu, memoria e temperatura em intervalos regulares
def monitor_resources(process: psutil.Process, samples: dict, stop_flag: dict, interval: float):
    while not stop_flag.get("done"):
        samples["cpu_percent"].append(psutil.cpu_percent(interval=None))

        vm = psutil.virtual_memory()
        samples["system_mem_percent"].append(vm.percent)
        samples["system_mem_used_mb"].append(vm.used / (1024 * 1024))

        try:
            rss_mb = process.memory_info().rss / (1024 * 1024)
            samples["process_mem_mb"].append(rss_mb)
        except psutil.Error:
            pass

        temps = read_temperatures()
        if temps:
            for key, value in temps.items():
                samples["temperatures"].setdefault(key, []).append(value)
        else:
            samples["temperatures_available"] = False

        time.sleep(interval)

# calcula minimo, medio e maximo de cada valor
def stats_line(values):
    if not values:
        return "sem amostras coletadas"
    return (f"mínimo={min(values):.2f}  "
            f"médio={statistics.mean(values):.2f}  "
            f"máximo={max(values):.2f}")


# monta e grava o relatorio txt com hardware, execucao e metrica
def write_report(path, hw_info, num_requests, block_size_mb, duration_s, samples):
    lines = []
    lines.append("relatório de benchmark de carga - app público municipal")
    lines.append("=" * 60)
    lines.append("")

    lines.append("informações de hardware do dispositivo")
    lines.append("-" * 60)
    lines.append(f"sistema operacional     : {hw_info['sistema']}")
    lines.append(f"versão detalhada        : {hw_info['versao_detalhada']}")
    lines.append(f"arquitetura             : {hw_info['arquitetura']}")
    lines.append(f"processador             : {hw_info['processador']}")
    lines.append(f"núcleos físicos         : {hw_info['nucleos_fisicos']}")
    lines.append(f"núcleos lógicos         : {hw_info['nucleos_logicos']}")
    if hw_info["frequencia_atual_mhz"]:
        lines.append(f"frequência atual da cpu : {hw_info['frequencia_atual_mhz']:.0f} mhz")
    if hw_info["frequencia_max_mhz"]:
        lines.append(f"frequência máxima da cpu: {hw_info['frequencia_max_mhz']:.0f} mhz")
    lines.append(f"memória ram total       : {hw_info['ram_total_gb']:.2f} gb")
    lines.append(f"memória swap total      : {hw_info['swap_total_gb']:.2f} gb")
    if hw_info["discos"]:
        lines.append("discos:")
        for disk in hw_info["discos"]:
            lines.append(f"  {disk['device']} ({disk['mountpoint']}): "
                         f"total={disk['total_gb']:.2f} gb  "
                         f"usado={disk['used_gb']:.2f} gb  "
                         f"livre={disk['free_gb']:.2f} gb")
    else:
        lines.append("discos: não identificados")
    lines.append("")

    lines.append("dados da execução")
    lines.append("-" * 60)
    lines.append(f"data/hora da execução : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"requisições simuladas : {num_requests}")
    lines.append(f"tamanho do bloco      : {block_size_mb} mb por requisição")
    lines.append(f"duração total         : {duration_s:.2f} segundos")
    lines.append("")

    lines.append("uso de cpu (%)")
    lines.append("-" * 60)
    lines.append(stats_line(samples["cpu_percent"]))
    lines.append("")

    lines.append("uso de memória do sistema (%)")
    lines.append("-" * 60)
    lines.append(stats_line(samples["system_mem_percent"]))
    lines.append("")

    lines.append("uso de memória do sistema (mb)")
    lines.append("-" * 60)
    lines.append(stats_line(samples["system_mem_used_mb"]))
    lines.append("")

    lines.append("uso de memória do processo (rss, mb)")
    lines.append("-" * 60)
    lines.append(stats_line(samples["process_mem_mb"]))
    lines.append("")

    lines.append("temperaturas dos sensores (°c)")
    lines.append("-" * 60)
    if samples["temperatures"]:
        for sensor, values in samples["temperatures"].items():
            lines.append(f"{sensor}: {stats_line(values)}")
    else:
        lines.append("não disponível neste sistema operacional "
                      "(comum em windows sem software adicional de sensores)")
    lines.append("")

    lines.append(f"total de amostras coletadas: {len(samples['cpu_percent'])}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# le parametros, roda a carga com monitoramento e gera relatorio
def main():
    parser = argparse.ArgumentParser(
        description="benchmark de carga simulando um app público (ex.: chatbot municipal)."
    )
    parser.add_argument("--requests", type=int, choices=[100, 1000, 10000, 100000], default=100,
                         help="número de requisições simuladas (100, 1000 ou 10000)")
    parser.add_argument("--block-size", type=int, default=4,
                         help="tamanho do bloco de memória em mb por requisição (padrão: 4)")
    parser.add_argument("--interval", type=float, default=0.2,
                         help="intervalo entre amostras de monitoramento, em segundos (padrão: 0.2)")
    parser.add_argument("--out", type=str, default="relatorio.txt",
                         help="arquivo de relatório de saída (padrão: relatorio.txt)")
    args = parser.parse_args()

    print("=== benchmark de carga - app público municipal ===")
    print(f"sistema operacional : {platform.system()} {platform.release()}")
    print(f"requisições         : {args.requests}")
    print(f"tamanho do bloco    : {args.block_size} mb")
    print("iniciando monitoramento e carga...")

    process = psutil.Process()
    psutil.cpu_percent(interval=None)

    samples = {
        "cpu_percent": [],
        "system_mem_percent": [],
        "system_mem_used_mb": [],
        "process_mem_mb": [],
        "temperatures": {},
    }
    stop_flag = {"done": False}

    monitor_thread = threading.Thread(
        target=monitor_resources, args=(process, samples, stop_flag, args.interval)
    )
    monitor_thread.start()

    start = time.perf_counter()
    run_load(args.requests, args.block_size, stop_flag)
    duration = time.perf_counter() - start

    monitor_thread.join()

    write_report(args.out, gather_hardware_info(), args.requests, args.block_size, duration, samples)

    print(f"carga finalizada em {duration:.2f} segundos.")
    print(f"relatório salvo em: {args.out}")


if __name__ == "__main__":
    main()
