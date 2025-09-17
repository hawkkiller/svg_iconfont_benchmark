import matplotlib.pyplot as plt
import numpy as np
import json
import os
import re
from pathlib import Path
import shutil

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

def generate_chart(iconfont_data, svg_data, svg_vec_data, folder_name, output_path):
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
    svg_vec_vals = [svg_vec_data[m] for m in metrics]
    
    # Bar chart setup
    x = np.arange(len(metrics))
    width = 0.25
    
    _, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - width, iconfont_vals, width, label="Iconfont")
    ax.bar(x, svg_vals, width, label="SVG")
    ax.bar(x + width, svg_vec_vals, width, label="SVG Vec")
    
    # Labels and formatting
    ax.set_ylabel("Time (ms)")
    ax.set_title(f"Rasterizer Time Comparison ({folder_name})")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=25, ha="right")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    print(f"Chart saved to {output_path}")

def copy_build_files_to_metrics():
    """
    Copies and organizes performance report files from the build directory
    to the metrics directory.
    """
    # The script is run from 'create_report', so 'build' is one level up.
    build_dir = Path(__file__).parent.parent / "build"
    metrics_dir = Path("metrics")

    if not build_dir.exists():
        print(f"Build directory {build_dir} does not exist. Skipping file copy.")
        return

    metrics_dir.mkdir(exist_ok=True)

    # Regex to find files like 'icons_20_svg.timeline_summary.json'
    pattern = re.compile(r"icons_(\d+)_(.*)")

    print(f"Scanning {build_dir} for report files...")
    for f in build_dir.iterdir():
        if f.is_file():
            match = pattern.match(f.name)
            if match:
                number = match.group(1)
                rest_of_filename = match.group(2)
                
                target_dir = metrics_dir / f"icons_{number}"
                target_dir.mkdir(exist_ok=True)
                
                target_file = target_dir / rest_of_filename
                print(f"Copying {f} to {target_file}")
                shutil.copy(f, target_file)
    print("File copying complete.")

def main():
    """Process all metrics folders and generate charts"""
    copy_build_files_to_metrics()

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
        svg_vec_file = folder / "svg_vec.timeline_summary.json"
        
        # Check if all required files exist
        required_files = [iconfont_file, svg_file, svg_vec_file]
        if not all(f.exists() for f in required_files):
            print(f"  Warning: Not all report files found, skipping {folder_name}")
            for f in required_files:
                if not f.exists():
                    print(f"    Missing: {f}")
            continue

        try:
            # Read the data
            iconfont_data = read_timeline_summary(iconfont_file)
            svg_data = read_timeline_summary(svg_file)
            svg_vec_data = read_timeline_summary(svg_vec_file)
            
            # Generate output path
            output_path = folder / f"rasterizer_comparison_{folder_name}.png"
            
            # Generate and save chart
            generate_chart(iconfont_data, svg_data, svg_vec_data, folder_name, output_path)
            
        except Exception as e:
            print(f"  Error processing {folder_name}: {e}")
            continue
    
    print("Done processing all folders!")
if __name__ == "__main__":
    main()
