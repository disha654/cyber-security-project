import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_top_ips(df, title, filename):
    """Plots top 10 Source IPs."""
    if df.empty:
        print(f"No data to plot for {title}")
        return
    
    # Ensure reports directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    plt.figure(figsize=(10, 6))
    df['ip'].value_counts().head(10).plot(kind='bar', color='skyblue')
    plt.title(title)
    plt.xlabel('IP Address')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join('reports', filename))
    plt.close()

def plot_methods(df, title, filename):
    """Plots distribution of HTTP methods (for Apache)."""
    if df.empty or 'method' not in df.columns:
        return

    # Ensure reports directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    plt.figure(figsize=(8, 8))
    df['method'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title(title)
    plt.savefig(os.path.join('reports', filename))
    plt.close()
