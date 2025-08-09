import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
from datetime import datetime
import pytz

# Function to remove non-ASCII characters
def remove_non_ascii(text):
    if isinstance(text, str):
        return ''.join(char if ord(char) < 128 else '?' for char in text)
    return ''

# Function to convert the timestamp (string format) to Malaysian Time (MYT)
def convert_timestamp_to_local(timestamp, timezone='Asia/Kuala_Lumpur'):
    try:
        utc_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        utc_time = pytz.utc.localize(utc_time)
        local_time = utc_time.astimezone(pytz.timezone(timezone))
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return timestamp

# === MAIN SCRIPT ===

csv_file = 'chat_messages.csv'

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"CSV file '{csv_file}' not found in the current folder.")

df = pd.read_csv(csv_file)

try:
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df = df.sort_values(by='time', ascending=True)
except Exception as e:
    print(f"Error sorting timestamps: {e}")

output_folder = "Twitch Chat History"
os.makedirs(output_folder, exist_ok=True)

for channel in df['channel'].dropna().unique():
    channel_messages = df[df['channel'] == channel]

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, f"Messages from channel '{channel}'",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(10)

    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 10, "Date Index (click to jump)",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    date_links = {}
    unique_dates = sorted(channel_messages['time'].dropna().dt.date.unique())

    # Multi-row clickable date layout
    link_per_row = 5
    cell_width = pdf.w / link_per_row - 10
    cell_height = 8
    col_count = 0

    for date in unique_dates:
        date_str = str(date)
        link_id = pdf.add_link()
        date_links[date_str] = link_id

        pdf.set_text_color(0, 0, 255)  # blue link color
        pdf.cell(cell_width, cell_height, date_str, border=1,
                 new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', link=link_id)

        col_count += 1
        if col_count >= link_per_row:
            pdf.ln(cell_height)
            col_count = 0

    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # ===== PAGES FOR EACH DATE =====
    for date in unique_dates:
        date_str = str(date)
        pdf.add_page()
        pdf.set_link(date_links[date_str])
        pdf.set_font("helvetica", 'B', 14)
        pdf.cell(0, 10, f"Messages on {date_str}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        daily_msgs = channel_messages[channel_messages['time'].dt.date == date]

        pdf.set_font("helvetica", size=12)
        for index, row in daily_msgs.iterrows():
            timestamp = row['time']
            if pd.notnull(timestamp):
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                timestamp = convert_timestamp_to_local(timestamp)
            else:
                timestamp = "Unknown Time"

            message = remove_non_ascii(row.get('body', ''))
            pdf.multi_cell(0, 8, text=f"{timestamp}: {message}")
            pdf.ln(1)

            if index % 100 == 0:
                print(f"Exporting message {index + 1}/{len(daily_msgs)} for {date_str}...")

    # Save PDF
    pdf_output_file = os.path.join(output_folder, f'{channel}_messages.pdf')
    pdf.output(pdf_output_file)

    print(f"✅ Export completed for channel '{channel}'! Saved as '{pdf_output_file}'.")

print("🎉 All channel PDFs have been exported successfully!")
