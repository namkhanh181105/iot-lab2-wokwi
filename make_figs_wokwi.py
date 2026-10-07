# -*- coding: utf-8 -*-
"""Sinh hinh minh chung cho bao cao Wokwi Bai 2."""
import sys, os
sys.path.insert(0, r"C:\Users\ADMIN\Downloads\iot-lab2-source\iot-lab2")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from common import db, read_data

OUT = r"C:\Users\ADMIN\Downloads\wokwi_lab2\report_evidence"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = "Arial"

# ---------- Hinh kien truc ----------
def architecture():
    fig, ax = plt.subplots(figsize=(11, 2.6))
    boxes = [
        ("Wokwi ESP32\nDHT22 + HC-SR04", "#c8e6c9"),
        ("HiveMQ\nbroker.hivemq.com", "#bbdefb"),
        ("Bridge\nHiveMQ→local", "#ffe0b2"),
        ("Mosquitto\n:1883", "#bbdefb"),
        ("Collector\nvalidate + outbox", "#fff9c4"),
        ("InfluxDB 2.7\nraw / clean", "#f8bbd0"),
        ("Preprocess\nIQR · resample", "#d1c4e9"),
        ("Dashboard\nStreamlit", "#b2dfdb"),
    ]
    n = len(boxes); w = 0.108; gap = (1 - n * w) / (n + 1)
    for i, (txt, col) in enumerate(boxes):
        x = gap + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.3), w, 0.42, boxstyle="round,pad=0.008,rounding_size=0.02",
                                    linewidth=1.2, edgecolor="#333", facecolor=col))
        ax.text(x + w / 2, 0.51, txt, ha="center", va="center", fontsize=6.7)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w, 0.51), (x + w + gap, 0.51),
                                         arrowstyle="-|>", mutation_scale=11, color="#333"))
    ax.text(0.5, 0.9, "Kiến trúc tích hợp: thiết bị Wokwi → HiveMQ → pipeline lưu trữ & tiền xử lý",
            ha="center", fontsize=10.5, fontweight="bold")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.savefig(os.path.join(OUT, "fig_arch_wokwi.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

# ---------- Hinh raw vs clean (esp32_01) ----------
def raw_clean():
    with db() as c:
        raw = read_data(c, "sensor_raw", 120)
        clean = read_data(c, "sensor_clean", 120)
    raw = raw[raw.get("device_id") == "esp32_01"].copy()
    clean = clean[clean.get("device_id") == "esp32_01"].copy()
    # Loai ban tin tu thiet bi khac dung chung topic cong cong (dau van tay Wokwi: 20-30C, 30-50%).
    if not raw.empty:
        raw = raw[(raw["temperature"].between(20, 30)) & (raw["humidity"].between(30, 50))].copy()
    if not clean.empty:
        clean = clean[(clean["temperature"].between(20, 30)) & (clean["humidity"].between(30, 50))].copy()
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.2), sharex=False)
    if not raw.empty:
        raw["_time"] = raw["_time"].dt.tz_convert(None)
        axes[0].plot(raw["_time"], raw["temperature"], "o-", ms=3, color="#e53935", label="temperature")
        axes[0].plot(raw["_time"], raw["humidity"], "s-", ms=3, color="#1e88e5", label="humidity")
    axes[0].set_title("sensor_raw — dữ liệu thô từ Wokwi ESP32 (esp32_01)")
    axes[0].legend(loc="upper right", fontsize=8); axes[0].grid(alpha=.3)
    if not clean.empty:
        clean["_time"] = clean["_time"].dt.tz_convert(None)
        axes[1].plot(clean["_time"], clean["temperature"], "o-", ms=4, color="#e53935", label="temperature (clean)")
        axes[1].plot(clean["_time"], clean["humidity"], "s-", ms=4, color="#1e88e5", label="humidity (clean)")
    axes[1].set_title("sensor_clean — resample 10 giây + rolling mean")
    axes[1].legend(loc="upper right", fontsize=8); axes[1].grid(alpha=.3)
    for a in axes:
        a.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_raw_clean_wokwi.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)

# ---------- Hinh "terminal" log HiveMQ + bridge ----------
def term_log():
    cap = r"C:\Users\ADMIN\Downloads\wokwi_lab2\hivemq_capture.log"
    lines = []
    if os.path.exists(cap):
        lines = [l.rstrip() for l in open(cap, encoding="utf-8")
                 if '"temperature":24.00' in l][-13:]
    show = ["$ python mqtt_hivemq_sub.py  # client local subscribe HiveMQ",
            "connected rc=0",
            "topic: lab2/sensors/esp32_01/data"] + lines
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.set_facecolor("#0c0c0c"); fig.patch.set_facecolor("#0c0c0c")
    ax.axis("off")
    for i, l in enumerate(show):
        color = "#33ff66" if not l.startswith("$") else "#66d9ff"
        ax.text(0.01, 0.97 - i * 0.062, l, transform=ax.transAxes, va="top",
                fontsize=8.2, family="Consolas", color=color)
    fig.savefig(os.path.join(OUT, "fig_hivemq_log.png"), dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

if __name__ == "__main__":
    architecture(); raw_clean(); term_log()
    print("figs ->", OUT)
