# 🔍 Incremental Search Logger

Skrip Python buat nge-bracket akar fungsi `f(x)` pakai metode **Incremental Search** — tahap pra-proses sebelum lanjut ke Bisection Method. Tiap iterasi ditembak ke terminal *real-time* dan dicatat ke CSV buat audit trail.

## ⚙️ Fitur

- Auto-bracket akar dengan safety guard (`MAX_ITERATIONS`) — anti infinite loop
- Logging real-time ke terminal via modul `logging` bawaan Python
- Auto-generate `data_log/execute.csv` & `data_log/iteration_details.csv` lengkap dengan header
- Modular: algoritma murni, I/O, dan orkestrasi dipisah rapi — gampang di-unit-test atau di-import

## 📦 Requirements

- Python 3.8+
- Zero dependency eksternal (stdlib doang: `csv`, `logging`, `os`, `time`, `dataclasses`, `datetime`, `typing`)

## 🚀 Cara Pakai

```bash
python automation.py
```

Default run: `f(x) = 2x - 5`, `start = -75`, `interval = 7`.

**Ganti fungsi** — edit dua tempat ini bareng-bareng (sengaja didekatkan biar gak lupa sync):

```python
def f(x: float) -> float:
    return 2 * x - 5

FX_LABEL = "2x-5"  # WAJIB disamakan manual dengan f(x) di atas
```

**Ganti titik awal / interval pencarian** — di pemanggilan `main()`:

```python
if __name__ == "__main__":
    main(start=-75, interval=7)
```

## 📁 Struktur Output

```
data_log/
├── execute.csv             # 1 baris / run → ringkasan eksekusi
└── iteration_details.csv   # 1 baris / iterasi → histori pencarian
```

| execute.csv | run_id | fx | start | interval | end_time |
|---|---|---|---|---|---|

| iteration_details.csv | timestamp | left | right | f_left | f_right | status | run_id |
|---|---|---|---|---|---|---|---|

## ⚠️ Gotcha

- Newline CSV ditaruh **di depan** tiap baris baru (bukan di belakang) → file gak diakhiri newline di EOF. Ini desain sengaja, bukan bug — jangan panik kalau linter/`diff` protes "no newline at end of file".
- `FX_LABEL` gak auto-derive dari `f(x)`. Ganti fungsi = wajib ganti label manual.
- `SLEEP_SECONDS = 1` sengaja dikasih delay biar bisa diamatin live di terminal. Set `0` kalau lagi buru-buru testing.

---
Dibikin buat belajar logging sederhana sebelum lanjut ke Bisection Method. 🚧
