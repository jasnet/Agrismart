import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "app.db"
DATA_DIR = BASE_DIR / "data"
CSV_FILE = DATA_DIR / "Crop_recommendation.csv"

def seed_db():
    if not CSV_FILE.exists():
        print(f"CSV file not found at {CSV_FILE}")
        return

    df = pd.read_csv(CSV_FILE)
    
    # Normalize columns
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Calculate averages for each crop
    # Columns: n, p, k, temperature, humidity, ph, rainfall, label
    grouped = df.groupby('label').mean().reset_index()
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Clear existing data to avoid duplicates if re-run (optional, but good for seeding)
    # cur.execute("DELETE FROM crop_soil_profile")
    # cur.execute("DELETE FROM crop_types")
    
    print("Seeding crop_soil_profile...")
    for _, row in grouped.iterrows():
        crop_name = row['label']
        
        # Check if exists
        cur.execute("SELECT 1 FROM crop_soil_profile WHERE LOWER(crop_name)=?", (crop_name.lower(),))
        if cur.fetchone():
            continue

        # Format requirements as ranges or averages. Here using averages as string.
        # You might want to calculate min-max ranges, but average is a good start.
        # Or better, min-max. Let's do min-max for more realistic requirements.
        
        # Get min and max for this crop
        crop_df = df[df['label'] == crop_name]
        n_req = f"{crop_df['n'].min():.1f}-{crop_df['n'].max():.1f}"
        p_req = f"{crop_df['p'].min():.1f}-{crop_df['p'].max():.1f}"
        k_req = f"{crop_df['k'].min():.1f}-{crop_df['k'].max():.1f}"
        ph_req = f"{crop_df['ph'].min():.1f}-{crop_df['ph'].max():.1f}"
        # organic_carbon is not in CSV, leave empty or placeholder
        oc_req = "N/A" 
        rain_req = f"{crop_df['rainfall'].min():.1f}-{crop_df['rainfall'].max():.1f}"
        temp_req = f"{crop_df['temperature'].min():.1f}-{crop_df['temperature'].max():.1f}"
        
        cur.execute("""
            INSERT INTO crop_soil_profile (
                crop_name, nitrogen_req, phosphorus_req, potassium_req,
                pH_req, organic_carbon, rainfall_req, temperature_req
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (crop_name, n_req, p_req, k_req, ph_req, oc_req, rain_req, temp_req))
        
        # Also seed crop_types
        # We don't have type info in CSV (e.g. Kharif/Rabi), so we'll leave it or guess.
        # For now, insert into crop_types with generic type or skip.
        # Let's insert a placeholder type.
        cur.execute("INSERT INTO crop_types (crop_name, crop_type) VALUES (?, ?)", (crop_name, "Unknown"))

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
