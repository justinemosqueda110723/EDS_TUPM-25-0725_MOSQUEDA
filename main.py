import pandas as pd
import numpy as np
import plotly.express as px
import os
from scipy.stats import skew # Required for Table I

class TireDynamicsPipeline:
    def __init__(self, data_path):
        """Initializes the pipeline with student-specific data paths [cite: 85, 88]"""
        self.data_path = data_path
        self.df = None
        self.metrics = {}

    def ingest_data(self):
        """Module 1: Data Ingestion with Robust Error Handling [cite: 50]"""
        try:
            # Loading results.csv from the /data folder 
            file_path = os.path.join(self.data_path, "results.csv")
            self.df = pd.read_csv(file_path)
            print("Step 1: Successfully ingested telemetry data.")
        except FileNotFoundError:
            print("CRITICAL ERROR: results.csv not found in /data folder.")
        except Exception as e:
            print(f"An unexpected error occurred during ingestion: {e}")

    def clean_pipeline(self):
        """Module 2: Automated Cleaning & Unique Filtering"""
        if self.df is None: return

        # UNIQUE FILTER: Isolating 2026 Miami GP (Race ID 1110)
        self.df = self.df[self.df['raceId'] == 1110]
        
        # --- NEW FIX START ---
        # Convert 'grid' and 'milliseconds' to numeric, turning errors (like "\N") into NaN
        self.df['grid'] = pd.to_numeric(self.df['grid'], errors='coerce')
        self.df['milliseconds'] = pd.to_numeric(self.df['milliseconds'], errors='coerce')
        # --- NEW FIX END ---
        
        # Handle missing/null values and duplicates
        # We now drop rows where grid OR milliseconds are missing
        self.df = self.df.dropna(subset=['milliseconds', 'grid']) 
        self.df.drop_duplicates(inplace=True)
        
        # Numerical Transformation: Convert to seconds
        self.df['seconds'] = self.df['milliseconds'] / 1000.0
        print("Step 2: Data cleaning, unique filtering, and type conversion complete.")

    def perform_analytics(self):
        """Module 3: Engineering Analytics using NumPy & SciPy [cite: 51, 58-61]"""
        if self.df is None or self.df.empty:
            print("Error: No data available for analysis.")
            return

        # Comparative Analysis: Grouping by Grid Position [cite: 61]
        # Front Grid (Top 10) vs. Back Grid (11-20)
        front_grid = self.df[self.df['grid'] <= 10]['seconds'].values
        back_grid = self.df[self.df['grid'] > 10]['seconds'].values
        all_data = self.df['seconds'].values

        # Mandatory Statistical Calculations [cite: 51, 59]
        self.metrics = {
            'Overall': {
                'Mean': np.mean(all_data),
                'Variance': np.var(all_data),
                'Skewness': skew(all_data)
            },
            'Front_Grid': {
                'Mean': np.mean(front_grid),
                'Variance': np.var(front_grid),
                'Skewness': skew(front_grid)
            },
            'Back_Grid': {
                'Mean': np.mean(back_grid),
                'Variance': np.var(back_grid),
                'Skewness': skew(back_grid)
            }
        }
        
        # Print formatted table for Section V of the paper
        self.display_table()

    def display_table(self):
        """Generates the text-based table for IEEE reporting"""
        print("\n" + "="*65)
        print("TABLE I: DESCRIPTIVE ENGINEERING STATISTICS (2026 MIAMI GP)")
        print("="*65)
        print(f"{'Group':<15} | {'Mean (s)':<12} | {'Variance':<12} | {'Skewness':<10}")
        print("-"*65)
        for group, data in self.metrics.items():
            print(f"{group:<15} | {data['Mean']:<12.4f} | {data['Variance']:<12.6f} | {data['Skewness']:<10.4f}")
        print("="*65)

    def create_visualizations(self):
        """Module 4: Static & Animated Visuals [cite: 63-65]"""
        if self.df is None: return

        # Static Graph: Traction Distribution [cite: 65]
        fig_hist = px.histogram(self.df, x="seconds", 
                             title="Figure 1: Traction Performance Distribution (Miami GP)")
        fig_hist.write_image("outputs/static_histogram.png")

        # Animated Graph: Driver Performance Shifts [cite: 64]
        fig_anim = px.scatter(self.df, x="grid", y="position", 
                             animation_frame="driverId", 
                             title="Figure 2: Dynamic Driver Performance Shift")
        fig_anim.write_html("outputs/performance_animation.html")
        print("Step 4: Visualizations saved to /outputs folder.")

# --- Execution Block ---
if __name__ == "__main__":
    # Ensure the output directory exists 
    os.makedirs('outputs', exist_ok=True)
    
    # Initialize and Run the Engineering Pipeline
    pipeline = TireDynamicsPipeline("data")
    pipeline.ingest_data()
    pipeline.clean_pipeline()
    pipeline.perform_analytics()
    pipeline.create_visualizations()