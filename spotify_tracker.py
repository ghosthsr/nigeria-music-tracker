import urllib.request
import csv
import io
import os
from datetime import datetime

def fetch_nigeria_spotify():
    # Official direct chart storage file link
    url = "https://githubusercontent.com"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        print("Connecting to storage cluster...")
        response = urllib.request.urlopen(req)
        csv_text = response.read().decode('utf-8')
        csv_file = io.StringIO(csv_text)
        
        reader = csv.reader(csv_file)
        header = next(reader)
        col_map = {col.lower().strip(): idx for idx, col in enumerate(header)}
        
        output_file = "nigeria_spotify_daily_database.csv"
        file_exists = os.path.exists(output_file)
        
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Rank", "Track_Name", "Artist_Name", "Daily_Streams", "Date_Extracted"])
                
            today_str = datetime.today().strftime('%Y-%m-%d')
            count = 0
            
            for row in reader:
                if not row:
                    continue
                rank = row[col_map['position']] if 'position' in col_map else 'N/A'
                track_name = row[col_map['track name']] if 'track name' in col_map else 'Unknown'
                artist_name = row[col_map['artist']] if 'artist' in col_map else 'Unknown'
                
                try:
                    streams_str = row[col_map['streams']] if 'streams' in col_map else '0'
                    streams_val = int(streams_str.replace(',', ''))
                except:
                    streams_val = 0
                    
                if streams_val >= 100:
                    writer.writerow([rank, track_name, artist_name, streams_val, today_str])
                    count += 1
                    
        print(f"[SUCCESS] Collected {count} tracks.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_nigeria_spotify()
