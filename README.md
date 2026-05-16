# AUT-03: Tire Traction vs. Slip Angle
### Mechanical Engineering - Computer Programming and Fundamentals Final Project

## Project Overview

This project applies Object-Oriented Programming (OOP) and Engineering Data Analytics to evaluate the non-linear relationship governing lateral tire traction, grid positioning, and lap performance metrics using real-world tracking telemetry from the **2026 Miami Grand Prix (Race ID 1110)**. 

By analyzing telemetry vectors, this computational pipeline isolates how starting positions affect track constraints, calculates statistical performance symmetries, and identifies the physical saturation limits of mechanical grip under racing load.

## Features

* **Automated Telemetry Data Pipeline**: Built-in `try-except` data integrity wrappers to handle type conversions, unique tracking filters, and gracefully drop corrupted or null engineering strings via `pd.to_numeric(errors='coerce')`.
* **Engineering Analytics Engine**: Leverages high-speed vectorized **NumPy** matrix calculations and **SciPy** to calculate descriptive statistics including Mean Lap Times, Variance splits, and performance Skewness across the Front Grid, Back Grid, and Overall field.
* **Tire Adhesion Mapping**: Benchmarks track positioning behaviors to evaluate mechanical consistency and aerodynamic advantages in clean air versus midfield congestion traffic.
* **Interactive Visualization Engine**: Generates static engineering charts (`static_histogram.png`) tracking traction distribution and dynamic, frame-by-frame animated simulations (`performance_animation.html`) showcasing performance trajectory shifts sorted by individual driver profiles.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/justinemosqueda110723/EDS_TUPM-2025-0725_Mosqueda.git](https://github.com/justine110723/EDS_TUPM-2025-0725_Mosqueda.git)
   cd EDS_TUPM-2025-0725_Mosqueda