🚀 Sorting Visualizer & Benchmark (PyQt6)

A modern, optimized, and user-friendly sorting algorithm visualizer + performance benchmark tool, built with PyQt6 and Matplotlib.

<img width="1263" height="797" alt="Screenshot 2025-12-04 124645" src="https://github.com/user-attachments/assets/39f6ef1a-6303-42b6-ac66-61b2b850802b" />

This application provides:

📊 Real-time sorting animations

⚡ Accurate performance benchmarking using time.perf_counter()

🖥️ Clean PyQt6 UI with interactive controls

📈 Line & Bar charts for comparing algorithms

🔧 Supports Quick Sort, Insertion Sort & Bubble Sort

🔁 Sorted / Reversed / Shuffled list generation

🔄 No file I/O — everything is in-memory and fast

🎨 Matplotlib embedded in a modern UI

📦 Features
✅ 1. Sorting Algorithm Animation

Watch how each algorithm sorts step-by-step:

Quick Sort (recursive generator)

Insertion Sort

Bubble Sort

Animation uses:

Efficient Python generators

Qt’s non-blocking QTimer

Smooth bar updates in Matplotlib

✅ 2. Benchmark Multiple Algorithms

Compare execution time of selected algorithms across input sizes.

You can configure:

Start size

End size

Step

Data order: Sorted / Reversed / Shuffled

Output:

Line graph of time vs. input size

Average execution time

Clean status summary

✅ 3. Single-Run Mode

Benchmark selected algorithms on a single list size and view results as a bar chart.

✅ 4. Modern PyQt6 Interface

The UI includes:

Parameter controls

Algorithm selectors

Animation settings

Matplotlib canvas

Live status updates

🛠️ Installation
Requirements
Python 3.8+
PyQt6
matplotlib
numpy

Install dependencies:
pip install pyqt6 matplotlib numpy

▶️ Running the Application

Save your main file as:

sorting_gui_pyqt6.py


Run using:

python sorting_gui_pyqt6.py

📁 Project Structure (single-file version)
sorting_gui_pyqt6.py  # main PyQt6 application


If needed, this can be modularized later into:

/src
   /ui
   /algorithms
   /visualizers
   /plots

🧠 Algorithms Included
Quick Sort

In-place

Lomuto partition scheme

Recursive generator for animation

Insertion Sort

Efficient for small or nearly-sorted lists

Smooth animation

Bubble Sort

Classic comparison sort

Early exit optimization

🖼️ Visualization

Uses Matplotlib bar charts for animations

Line & bar charts embedded in PyQt6

Responsive redrawing with tight_layout=True

Auto-adjusted Y-axis

⚙️ Performance Optimizations

✔ No file reads/writes (old project version used .txt logs)
✔ time.perf_counter() for high-precision timing
✔ Array copies handled per-algorithm to prevent contamination
✔ Minimised redraw overhead
✔ Simplified and optimized generator logic

🧩 Controls Overview
Array Generation

Start size

End size

Step

Order: sorted / reversed / shuffled

Algorithm Select

Quick Sort

Insertion Sort

Bubble Sort

Single Mode

N (list size)

Bar chart output

Shows execution time

Animation Mode

Speed (ms/frame)

Algorithm selection

Start/Stop toggle

📊 Example Outputs
🔹 Bar Chart (single run)

Shows time taken by each selected algorithm.

🔹 Line Graph (comparison)

Plots execution time across increasing input sizes.

🔹 Animation

Live bar-graph visualization of the sorting process.
