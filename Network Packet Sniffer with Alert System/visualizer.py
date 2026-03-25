import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sqlite3
import pandas as pd
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def animate(i):
    try:
        conn = sqlite3.connect(config['db_path'])
        # Get count of packets in the last 1 second
        df = pd.read_sql_query("SELECT timestamp, length FROM packet_logs ORDER BY timestamp DESC LIMIT 500", conn)
        conn.close()
        
        if df.empty:
            return

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Group by 1 second intervals and count packets
        ts_counts = df.set_index('timestamp').resample('1S').count()
        
        plt.cla()
        plt.plot(ts_counts.index, ts_counts['length'], label='Packets/sec')
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.title('Real-time Traffic Monitor')
        plt.legend(loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
    except Exception as e:
        print(f"Visualization error: {e}")

def start_visualization():
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

if __name__ == '__main__':
    start_visualization()
