#!/usr/bin/env python3
"""
Customer Segmentation Analysis Pipeline
Main script to run the complete analysis workflow
"""

import os
import sys
import subprocess
import time

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd='scripts')
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print(f"❌ Error in {description}")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run {script_name}: {str(e)}")
        return False
    
    return True

def main():
    """Main analysis pipeline"""
    print("🎯 Customer Segmentation and Market Intelligence Platform")
    print("Starting complete analysis pipeline...")
    
    # Check if data directory exists
    if not os.path.exists('/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/data'):
        print("❌ Data directory not found. Please ensure data files are in the 'data' folder.")
        return
    
    # Analysis pipeline steps
    steps = [
        ("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/scripts/data_preprocessing.py", "Data Preprocessing and Feature Engineering"),
        ("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/scripts/eda.py", "Exploratory Data Analysis"),
        ("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/scripts/model_development.py", "Machine Learning Model Development"),
        ("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/scripts/insights_generation.py", "Business Insights Generation")
    ]
    
    # Run each step
    for script, description in steps:
        success = run_script(script, description)
        if not success:
            print(f"\n❌ Pipeline failed at: {description}")
            print("Please check the error messages above and fix any issues.")
            return
        
        time.sleep(1)  # Brief pause between steps
    
    print(f"\n{'='*60}")
    print("🎉 Analysis Pipeline Completed Successfully!")
    print(f"{'='*60}")
    print("\nGenerated Files:")
    print("📊 Visualizations: Check the 'visualizations' folder")
    print("📈 Data: Check the 'data' folder for processed datasets")
    print("📋 Results: Check the console output above for insights")
    
    print(f"\n{'='*60}")
    print("🚀 Next Steps:")
    print("1. Review the generated visualizations")
    print("2. Launch the interactive dashboard:")
    print("   streamlit run dashboard.py")
    print("3. Explore customer segments and insights")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

