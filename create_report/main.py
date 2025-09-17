import matplotlib.pyplot as plt
import numpy as np
import json
import os
from pathlib import Path

def read_timeline_summary(file_path):
    """Read and parse timeline summary JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def get_metrics_folders():
    """Get all folders in the metrics directory"""
    metrics_dir = Path("metrics")
    if not metrics_dir.exists():
        print(f"Metrics directory {metrics_dir} does not exist")
        return []
    
    folders = [f for f in metrics_dir.iterdir() if f.is_dir()]
    return sorted(folders)

def generate_chart(iconfont_data, svg_data, folder_name, output_path):
    """Generate and save chart for given data"""
    # Metrics to keep
    metrics = [
        "average_frame_rasterizer_time_millis",
        "90th_percentile_frame_rasterizer_time_millis",
        "99th_percentile_frame_rasterizer_time_millis"
    ]
    
    # Extract values
    iconfont_vals = [iconfont_data[m] for m in metrics]
    svg_vals = [svg_data[m] for m in metrics]
    
    # Bar chart setup
    x = np.arange(len(metrics))
    width = 0.35
    
    _, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, iconfont_vals, width, label="Iconfont")
    ax.bar(x + width/2, svg_vals, width, label="SVG")
    
    # Labels and formatting
    ax.set_ylabel("Time (ms)")
    ax.set_title(f"Rasterizer Time Comparison: Iconfont vs SVG ({folder_name})")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=25, ha="right")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    print(f"Chart saved to {output_path}")

def main():
    """Process all metrics folders and generate charts"""
    folders = get_metrics_folders()
    
    if not folders:
        print("No metrics folders found!")
        return
    
    for folder in folders:
        folder_name = folder.name
        print(f"Processing {folder_name}...")
        
        # Paths to the timeline summary files
        iconfont_file = folder / "iconfont.timeline_summary.json"
        svg_file = folder / "svg.timeline_summary.json"
        
        # Check if both files exist
        if not iconfont_file.exists():
            print(f"  Warning: {iconfont_file} not found, skipping {folder_name}")
            continue
            
        if not svg_file.exists():
            print(f"  Warning: {svg_file} not found, skipping {folder_name}")
            continue
        
        try:
            # Read the data
            iconfont_data = read_timeline_summary(iconfont_file)
            svg_data = read_timeline_summary(svg_file)
            
            # Generate output path
            output_path = folder / f"rasterizer_comparison_{folder_name}.png"
            
            # Generate and save chart
            generate_chart(iconfont_data, svg_data, folder_name, output_path)
            
        except Exception as e:
            print(f"  Error processing {folder_name}: {e}")
            continue
    
    print("Done processing all folders!")
if __name__ == "__main__":
    main()
