# Systems & Simulation

Moving from deterministic models to **Stochastic** models to account for real-world uncertainty.

## 1. Monte Carlo Simulation
Instead of using an "average" value, we sample from probability distributions.
- **Distributions**:
    - **Normal**: Bell curve (e.g., test scores, material strength).
    - **Uniform**: Equal probability within a range (e.g., simple estimation).
    - **Poisson**: Frequency of events over time (e.g., traffic arrivals).
- **Risk Analysis**: The simulation runs 2,000 trials to generate an outcome distribution. Look at the **95th Percentile** to understand the "worst-case" scenario.

## 2. Pareto Frontier
Used in **Multi-Objective Optimization**.
- **The Conflict**: Often, as we increase the **Reliability** of a system, the **Cost** also increases.
- **Efficiency**: The red line shows the "Pareto Frontier"—design points where you cannot improve one objective without sacrificing the other.
- **Decision Making**: Engineers choose a point on this frontier based on their specific budget or safety requirements.
