import matplotlib.pyplot as plt
import numpy as np
import json
import os
import re
from pathlib import Path
import shutil
from matplotlib.patches import Patch

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

def generate_chart(data_sources, metrics, title, y_label, output_path):
    """
    Generate and save a bar chart for the given metrics and data sources.

    :param data_sources: A dict where keys are labels (e.g., "Iconfont") and values are data dicts.
    :param metrics: A list of metric keys to plot.
    :param title: The chart title.
    :param y_label: The label for the Y-axis.
    :param output_path: The path to save the generated chart image.
    """
    # Bar chart setup
    x = np.arange(len(metrics))
    num_sources = len(data_sources)
    width = 0.8 / num_sources  # Adjust bar width based on number of sources
    
    _, ax = plt.subplots(figsize=(12, 7))

    for i, (label, data) in enumerate(data_sources.items()):
        # Calculate position for each bar group
        offset = width * (i - (num_sources - 1) / 2)
        
        # Extract values, using 0 if a metric is missing
        values = []
        for m in metrics:
            if m not in data:
                print(f"  Warning: Metric '{m}' not found in data for '{label}'. Using 0.")
                values.append(0)
            else:
                values.append(data[m])
        
        ax.bar(x + offset, values, width, label=label)
    
    # Labels and formatting
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=25, ha="right")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    print(f"Chart saved to {output_path}")

def generate_stacked_chart(data_sources, metric_pairs, title, y_label, output_path):
    """
    Generate and save a stacked bar chart.

    :param data_sources: Dict of data sources.
    :param metric_pairs: List of tuples, where each tuple is (bottom_metric, top_metric).
    :param title: The chart title.
    :param y_label: The label for the Y-axis.
    :param output_path: The path to save the chart.
    """
    x_labels = [pair[0].replace('_frame_build_time_millis', '').replace('_', ' ').title() for pair in metric_pairs]
    x = np.arange(len(x_labels))
    num_sources = len(data_sources)
    width = 0.8 / num_sources

    fig, ax = plt.subplots(figsize=(12, 8))

    # Get default color cycle for implementations
    prop_cycle = plt.rcParams['axes.prop_cycle']
    impl_colors = prop_cycle.by_key()['color']
    
    # Hatching for components
    hatches = {'bottom': '\\', 'top': '//'}

    for i, (label, data) in enumerate(data_sources.items()):
        offset = width * (i - (num_sources - 1) / 2)
        color = impl_colors[i % len(impl_colors)]

        bottom_values = []
        top_values = []
        for bottom_metric, top_metric in metric_pairs:
            bottom_values.append(data.get(bottom_metric, 0))
            top_values.append(data.get(top_metric, 0))

        # Plot bottom bars (Build Time)
        ax.bar(x + offset, bottom_values, width, facecolor=color, edgecolor='black', hatch=hatches['bottom'], linewidth=1.0)
        # Plot top bars (Rasterizer Time) on top of the bottom ones
        ax.bar(x + offset, top_values, width, bottom=bottom_values, facecolor=color, edgecolor='black', hatch=hatches['top'], linewidth=1.0)

    # --- Create Legends ---
    # Legend for components (hatching)
    component_legend_elements = [
        Patch(facecolor='white', edgecolor='black', hatch=hatches['bottom'], label='Build Time'),
        Patch(facecolor='white', edgecolor='black', hatch=hatches['top'], label='Rasterizer Time')
    ]
    legend1 = ax.legend(handles=component_legend_elements, loc='upper left', title="Frame Components")
    ax.add_artist(legend1)

    # Legend for implementations (colors) - create custom handles to avoid showing hatch
    impl_legend_elements = []
    for i, label in enumerate(data_sources.keys()):
        color = impl_colors[i % len(impl_colors)]
        impl_legend_elements.append(Patch(facecolor=color, edgecolor='black', label=label))
    ax.legend(handles=impl_legend_elements, loc='upper right', title="Implementations")

    # Labels and formatting
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=25, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
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
            
            data_sources = {
                "Iconfont": iconfont_data,
                "SVG": svg_data,
                "SVG Vec": svg_vec_data,
            }

            chart_definitions = [
                {
                    "type": "stacked",
                    "filename": "total_frame_time_comparison",
                    "title": f"Total Frame Time (Build + Raster) ({folder_name})",
                    "y_label": "Time (ms)",
                    "metric_pairs": [
                        ("average_frame_build_time_millis", "average_frame_rasterizer_time_millis"),
                        ("90th_percentile_frame_build_time_millis", "90th_percentile_frame_rasterizer_time_millis"),
                        ("99th_percentile_frame_build_time_millis", "99th_percentile_frame_rasterizer_time_millis"),
                    ],
                },
                {
                    "type": "bar",
                    "filename": "missed_frames_gc_comparison",
                    "title": f"Missed Frames & GC Count ({folder_name})",
                    "y_label": "Count",
                    "metrics": [
                        "missed_frame_build_budget_count",
                        "missed_frame_rasterizer_budget_count",
                        "new_gen_gc_count",
                        "old_gen_gc_count",
                    ],
                },
                {
                    "type": "bar",
                    "filename": "picture_cache_comparison",
                    "title": f"Picture Cache Memory ({folder_name})",
                    "y_label": "Memory (MB)",
                    "metrics": [
                        "average_picture_cache_memory",
                        "worst_picture_cache_memory",
                    ],
                },
            ]
            
            for chart_def in chart_definitions:
                output_path = folder / f"{chart_def['filename']}_{folder_name}.png"
                if chart_def.get("type") == "stacked":
                    generate_stacked_chart(data_sources, chart_def["metric_pairs"], chart_def["title"], chart_def["y_label"], output_path)
                else: # Default to simple bar chart
                    generate_chart(data_sources, chart_def["metrics"], chart_def["title"], chart_def["y_label"], output_path)

        except Exception as e:
            print(f"  Error processing {folder_name}: {e}")
            continue
    
    print("Done processing all folders!")
if __name__ == "__main__":
    main()
