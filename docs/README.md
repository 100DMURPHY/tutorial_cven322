# CVEN322: Civil Engineering Systems

Welcome to the interactive platform for **CVEN322**. This platform is designed to provide high-transparency access to engineering concepts through live, interactive visualizations.

## Quick Start: How to Run

The application is distributed as a Python package. You can run it directly from GitHub using `uvx` without installing anything locally.

### Method 1: One-Line Run (Recommended)
If you have `uv` installed, run:
```bash
uvx --from git+https://github.com/100DMURPHY/tutorial_cven322.git cven-app
```

### Method 2: Local Development
1. Clone the repository.
2. Install dependencies: `pip install -e .`
3. Run the app: `python -m cven_app.main`

---

## Technical Overview
The platform is built using:
- **[NiceGUI](https://nicegui.io/)**: For the modern, responsive web interface.
- **[Apache ECharts](https://echarts.apache.org/)**: For high-performance interactive visualizations.
- **[NumPy](https://numpy.org/)**: For stochastic simulation and numerical analysis.

## Core Modules
- **[Engineering Economics](economics)**: TVM, IRR, and Depreciation.
- **[Optimization Modeling](optimization)**: Feasible regions, Shadow Prices, and Dijkstra's algorithm.
- **[Systems & Simulation](simulation)**: Monte Carlo risks and Pareto frontiers.

## Academic Integrity
This platform is for **educational purposes only**. All grading-related logic, private datasets, and PII have been removed to ensure a clean, public-facing teaching environment.
