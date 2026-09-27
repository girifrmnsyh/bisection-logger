"""
Incremental Search (pra-pemrosesan sebelum Bisection).
Menyimpan log operasi (data_log/execute.csv) dan log detail iterasi
(data_log/iteration_details.csv), serta mencetak status setiap iterasi ke terminal.
"""

import csv
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List

# Konfigurasi
DATA_LOG_DIR = "data_log"
EXECUTE_LOG_PATH = os.path.join(DATA_LOG_DIR, "execute.csv")
ITERATION_LOG_PATH = os.path.join(DATA_LOG_DIR, "iteration_details.csv")

EXECUTE_HEADER = ["run_id", "fx", "start", "interval", "end_time"]
ITERATION_HEADER = ["timestamp", "left", "right", "f_left", "f_right", "status", "run_id"]

MAX_ITERATIONS = 1000  # safety guard: cegah infinite loop bila akar tak pernah ter-bracket
SLEEP_SECONDS = 1       # delay antar iterasi (set 0 untuk mode cepat/testing)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("incremental_search")


# Fungsi matematis
def f(x: float) -> float:
    """f(x) = x - 7"""
    return x - 7


# Label string untuk kebutuhan logging saja. Diletakkan tepat di bawah f(x)
# agar risiko desync (fx vs f(x)) mudah terlihat saat f(x) diubah.
FX_LABEL = "x-7"


@dataclass
class IterationLog:
    timestamp: str
    left: float
    right: float
    f_left: float
    f_right: float
    status: str


def incremental_search(
    func: Callable[[float], float],
    start: float,
    interval: float,
    max_iterations: int = MAX_ITERATIONS,
    sleep_seconds: float = SLEEP_SECONDS,
) -> List[IterationLog]:
    """
    Mencari interval [left, right] yang membracket akar
    (berhenti saat f(left) * f(right) <= 0).
    """
    logs: List[IterationLog] = []
    left, right = start, start + interval

    for iteration in range(1, max_iterations + 1):
        time.sleep(sleep_seconds)
        f_left, f_right = func(left), func(right)
        status = "invalid" if f_left * f_right > 0 else "valid"

        logs.append(
            IterationLog(
                timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
                left=left,
                right=right,
                f_left=f_left,
                f_right=f_right,
                status=status,
            )
        )

        logger.info(
            "Iterasi %-3d | [%9.3f, %9.3f] | f(left)=%9.3f  f(right)=%9.3f | status=%s",
            iteration, left, right, f_left, f_right, status,
        )

        if status == "valid":
            return logs

        left, right = right, right + interval

    raise RuntimeError(
        f"Akar tidak ditemukan dalam {max_iterations} iterasi. "
        "Periksa arah/tanda interval, atau naikkan max_iterations."
    )

# Logging ke CSV
def ensure_log_files() -> None:
    os.makedirs(DATA_LOG_DIR, exist_ok=True)
    _ensure_header(EXECUTE_LOG_PATH, EXECUTE_HEADER)
    _ensure_header(ITERATION_LOG_PATH, ITERATION_HEADER)


def _ensure_header(path: str, header: List[str]) -> None:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="") as fh:
            csv.writer(fh).writerow(header)


def write_execute_log(run_id: str, fx_label: str, start: float, interval: float, end_time: str) -> None:
    with open(EXECUTE_LOG_PATH, "a", newline="") as fh:
        csv.writer(fh).writerow([run_id, fx_label, start, interval, end_time])


def write_iteration_log(run_id: str, logs: List[IterationLog]) -> None:
    with open(ITERATION_LOG_PATH, "a", newline="") as fh:
        writer = csv.writer(fh)
        for log in logs:
            writer.writerow([log.timestamp, log.left, log.right, log.f_left, log.f_right, log.status, run_id])



# Orkestrasi
def main(start: float = -75, interval: float = 7) -> None:
    logger.info("Mulai incremental search | f(x)=%s | start=%s interval=%s", FX_LABEL, start, interval)

    try:
        ensure_log_files()
        logs = incremental_search(f, start, interval)
    except OSError as e:
        logger.error("Gagal menyiapkan/menulis file log: %s", e)
        raise
    except RuntimeError as e:
        logger.error(str(e))
        raise

    run_id = logs[0].timestamp
    write_execute_log(run_id, FX_LABEL, start, interval, logs[-1].timestamp)
    write_iteration_log(run_id, logs)

    logger.info(
        "Selesai: akar ter-bracket pada [%.3f, %.3f] setelah %d iterasi",
        logs[-1].left, logs[-1].right, len(logs),
    )
    logger.info("Log tersimpan -> %s, %s", EXECUTE_LOG_PATH, ITERATION_LOG_PATH)


if __name__ == "__main__":
    main()