# sorting_gui_pyqt6.py
# PyQt6-based sorting visualizer & benchmark
# Requires: PyQt6, matplotlib, numpy
# Run: python sorting_gui_pyqt6.py

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton,
    QSpinBox, QHBoxLayout, QVBoxLayout, QGroupBox, QFormLayout, QCheckBox
)
import sys
import random
import time
import numpy as np

# Matplotlib (Qt6 backend)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ------------------------------
# Sorting algorithms (optimized/timed)
# Reworked from your Sorting_Methods.py logic but using perf_counter
# ------------------------------
def time_quick_sort(arr):
    arr_copy = arr.copy()
    start = time.perf_counter()
    if len(arr_copy) > 1:
        _quick_sort_inplace(arr_copy, 0, len(arr_copy) - 1)
    end = time.perf_counter()
    return end - start

def _quick_sort_inplace(arr, low, high):
    if low < high:
        p = _partition(arr, low, high)
        _quick_sort_inplace(arr, low, p-1)
        _quick_sort_inplace(arr, p+1, high)

def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def time_insertion_sort(arr):
    arr_copy = arr.copy()
    start = time.perf_counter()
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i-1
        while j >= 0 and arr_copy[j] > key:
            arr_copy[j+1] = arr_copy[j]
            j -= 1
        arr_copy[j+1] = key
    end = time.perf_counter()
    return end - start

def time_bubble_sort(arr):
    arr_copy = arr.copy()
    start = time.perf_counter()
    n = len(arr_copy)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                swapped = True
        if not swapped:
            break
    end = time.perf_counter()
    return end - start

# ------------------------------
# Generator versions for animation (based on Sorting_Visualization.py)
# ------------------------------
def gen_bubble(arr):
    A = arr.copy()
    n = len(A)
    if n <= 1:
        yield A
        return
    for i in range(n-1):
        for j in range(n-1-i):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]
                yield A

def gen_insertion(arr):
    A = arr.copy()
    n = len(A)
    if n <= 1:
        yield A
        return
    for i in range(1, n):
        j = i
        while j > 0 and A[j-1] > A[j]:
            A[j], A[j-1] = A[j-1], A[j]
            j -= 1
            yield A

def gen_quick(arr):
    A = arr.copy()
    if len(A) <= 1:
        yield A
        return
    # We'll implement recursive generator
    yield from _gen_quick_helper(A, 0, len(A)-1)

def _gen_quick_helper(A, low, high):
    if low >= high:
        return
    pivot = A[high]
    pi = low
    for j in range(low, high):
        if A[j] < pivot:
            A[j], A[pi] = A[pi], A[j]
            pi += 1
            yield A
    A[pi], A[high] = A[high], A[pi]
    yield A
    yield from _gen_quick_helper(A, low, pi-1)
    yield from _gen_quick_helper(A, pi+1, high)

# ------------------------------
# Utility: generate lists
# (Inspired by ListMaker_Saver.py but in-memory and interactive)
# ------------------------------
def generate_lists(start, end, step):
    lists = []
    sizes = list(range(start, end+1, step))
    for s in sizes:
        lists.append(list(range(s)))
    return lists, sizes

def make_array(size, order):
    arr = list(range(1, size + 1))
    if order == "shuffled":
        random.shuffle(arr)
    elif order == "reversed":
        arr.reverse()
    # 'sorted' leaves it ascending
    return arr

# ------------------------------
# PyQt6 UI
# ------------------------------
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)

    def plot_bar(self, labels, values, title=""):
        self.ax.clear()
        self.ax.bar(labels, values)
        self.ax.set_title(title)
        self.ax.set_ylabel("Time (s)")
        self.draw()

    def plot_line(self, x_values, series, labels, title=""):
        self.ax.clear()
        for y, lab in zip(series, labels):
            self.ax.plot(x_values, y, marker='o', label=lab)
        self.ax.set_xlabel("Number of elements")
        self.ax.set_ylabel("Time (s)")
        self.ax.set_title(title)
        self.ax.legend()
        self.draw()

    def draw_bars_for_array(self, array, title=""):
        self.ax.clear()
        self.ax.bar(range(len(array)), array, align='edge')
        self.ax.set_title(title)
        self.ax.set_xlim(0, len(array))
        self.ax.set_ylim(0, max(array) * 1.1 if array else 1)
        self.draw()

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Visualizer & Benchmark — PyQt6")
        self.setMinimumSize(1000, 650)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # Left: Controls
        controls = QVBoxLayout()
        main_layout.addLayout(controls, 1)

        # Parameters group
        param_box = QGroupBox("Array generation")
        param_layout = QFormLayout()
        param_box.setLayout(param_layout)
        controls.addWidget(param_box)

        self.spin_start = QSpinBox()
        self.spin_start.setRange(1, 10000)
        self.spin_start.setValue(10)
        self.spin_end = QSpinBox()
        self.spin_end.setRange(1, 10000)
        self.spin_end.setValue(100)
        self.spin_step = QSpinBox()
        self.spin_step.setRange(1, 10000)
        self.spin_step.setValue(10)
        self.order_combo = QComboBox()
        self.order_combo.addItems(["sorted", "reversed", "shuffled"])

        param_layout.addRow("Start size:", self.spin_start)
        param_layout.addRow("End size:", self.spin_end)
        param_layout.addRow("Step:", self.spin_step)
        param_layout.addRow("Order:", self.order_combo)

        # Algorithm selection
        algo_box = QGroupBox("Algorithms")
        algo_layout = QVBoxLayout()
        algo_box.setLayout(algo_layout)
        controls.addWidget(algo_box)

        self.check_quick = QCheckBox("Quick Sort")
        self.check_insertion = QCheckBox("Insertion Sort")
        self.check_bubble = QCheckBox("Bubble Sort")
        # default both selected
        self.check_quick.setChecked(True)
        self.check_insertion.setChecked(True)
        self.check_bubble.setChecked(True)
        algo_layout.addWidget(self.check_quick)
        algo_layout.addWidget(self.check_insertion)
        algo_layout.addWidget(self.check_bubble)

        # Buttons
        btn_box = QHBoxLayout()
        controls.addLayout(btn_box)
        self.btn_run_single = QPushButton("Run single (one size)")
        self.btn_compare = QPushButton("Compare")
        self.btn_animate = QPushButton("Animate")
        btn_box.addWidget(self.btn_run_single)
        btn_box.addWidget(self.btn_compare)
        btn_box.addWidget(self.btn_animate)

        # Lower controls: pick a single N for run/animate
        single_box = QGroupBox("Single run / animate settings")
        single_layout = QFormLayout()
        single_box.setLayout(single_layout)
        controls.addWidget(single_box)
        self.spin_single_n = QSpinBox()
        self.spin_single_n.setRange(1, 2000)
        self.spin_single_n.setValue(50)
        self.anim_interval = QSpinBox()
        self.anim_interval.setRange(10, 2000)
        self.anim_interval.setValue(50)  # milliseconds
        self.algo_choice = QComboBox()
        self.algo_choice.addItems(["Quick Sort", "Insertion Sort", "Bubble Sort"])
        single_layout.addRow("N (for single):", self.spin_single_n)
        single_layout.addRow("Animation speed (ms):", self.anim_interval)
        single_layout.addRow("Algorithm (for animate):", self.algo_choice)

        controls.addStretch()

        # Right: Plot area
        plot_layout = QVBoxLayout()
        main_layout.addLayout(plot_layout, 3)
        self.canvas = PlotCanvas(self, width=8, height=6, dpi=100)
        plot_layout.addWidget(self.canvas)

        # Status bar
        self.status = QLabel("")
        plot_layout.addWidget(self.status)

        # Connect signals
        self.btn_run_single.clicked.connect(self.handle_run_single)
        self.btn_compare.clicked.connect(self.handle_compare)
        self.btn_animate.clicked.connect(self.handle_animate)

        # animation state
        self._anim_timer = None
        self._anim_gen = None

    # -------------------------
    # Handlers
    # -------------------------
    def handle_run_single(self):
        n = self.spin_single_n.value()
        order = self.order_combo.currentText()
        arr = make_array(n, order if order else "shuffled")
        algos = []
        if self.check_quick.isChecked():
            algos.append(("Quick Sort", time_quick_sort))
        if self.check_insertion.isChecked():
            algos.append(("Insertion Sort", time_insertion_sort))
        if self.check_bubble.isChecked():
            algos.append(("Bubble Sort", time_bubble_sort))

        if not algos:
            self.status.setText("Select at least one algorithm.")
            return

        labels = []
        times = []
        for name, fn in algos:
            t = fn(arr)
            labels.append(name)
            times.append(t)

        # show bar chart, also show raw array bars to visualize initial state
        self.canvas.plot_bar(labels, times, title=f"Time for N={n} ({order})")
        self.status.setText(" | ".join(f"{lab}: {t:.6f}s" for lab, t in zip(labels, times)))

    def handle_compare(self):
        start = self.spin_start.value()
        end = self.spin_end.value()
        step = self.spin_step.value()
        if start > end:
            self.status.setText("Start must be <= End.")
            return
        order = self.order_combo.currentText()
        sizes = list(range(start, end+1, step))
        if not sizes:
            self.status.setText("Invalid range (no sizes).")
            return

        selected = []
        labels = []
        if self.check_quick.isChecked():
            selected.append(time_quick_sort); labels.append("Quick Sort")
        if self.check_insertion.isChecked():
            selected.append(time_insertion_sort); labels.append("Insertion Sort")
        if self.check_bubble.isChecked():
            selected.append(time_bubble_sort); labels.append("Bubble Sort")
        if not selected:
            self.status.setText("Select at least one algorithm.")
            return

        series = []
        # For performance, for each size generate one array (with the chosen order),
        # and time selected algorithms on copies of that array.
        for fn in selected:
            times = []
            for s in sizes:
                arr = make_array(s, order)
                t = fn(arr)
                times.append(t)
            series.append(times)

        self.canvas.plot_line(sizes, series, labels, title=f"Compare ({order})")
        # show a compact summary in the status
        summary = []
        for lab, times in zip(labels, series):
            avg = sum(times) / len(times)
            summary.append(f"{lab} avg: {avg:.6f}s")
        self.status.setText(" | ".join(summary))

    def handle_animate(self):
        if self._anim_timer and self._anim_timer.isActive():
            # stop current animation
            self._anim_timer.stop()
            self._anim_timer = None
            self._anim_gen = None
            self.btn_animate.setText("Animate")
            self.status.setText("Animation stopped.")
            return

        n = self.spin_single_n.value()
        alg = self.algo_choice.currentText()
        order = self.order_combo.currentText()
        arr = make_array(n, order)

        if alg == "Quick Sort":
            gen = gen_quick(arr)
        elif alg == "Insertion Sort":
            gen = gen_insertion(arr)
        else:
            gen = gen_bubble(arr)

        # prepare display
        self.canvas.draw_bars_for_array(arr, title=f"{alg} (animating)...")
        self._anim_gen = iter(gen)
        self._anim_timer = QtCore.QTimer(self)
        self._anim_timer.setInterval(self.anim_interval.value())
        self._anim_timer.timeout.connect(self._on_anim_frame)
        self._anim_timer.start()
        self.btn_animate.setText("Stop")
        self.status.setText("Animation running...")

    def _on_anim_frame(self):
        try:
            frame = next(self._anim_gen)
            self.canvas.draw_bars_for_array(frame, title="Animating...")
        except StopIteration:
            self._anim_timer.stop()
            self._anim_timer = None
            self._anim_gen = None
            self.btn_animate.setText("Animate")
            self.status.setText("Animation completed.")

# ------------------------------
# Run the app
# ------------------------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
