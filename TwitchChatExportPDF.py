import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
from datetime import datetime
import pytz

# === Hardcoded country -> timezone mapping (primary tz) ===
COUNTRY_TIMEZONES = {
    "afghanistan": "Asia/Kabul",
    "albania": "Europe/Tirane",
    "algeria": "Africa/Algiers",
    "andorra": "Europe/Andorra",
    "angola": "Africa/Luanda",
    "antigua and barbuda": "America/Antigua",
    "argentina": "America/Argentina/Buenos_Aires",
    "armenia": "Asia/Yerevan",
    "australia": "Australia/Sydney",
    "austria": "Europe/Vienna",
    "azerbaijan": "Asia/Baku",
    "bahamas": "America/Nassau",
    "bahrain": "Asia/Bahrain",
    "bangladesh": "Asia/Dhaka",
    "barbados": "America/Barbados",
    "belarus": "Europe/Minsk",
    "belgium": "Europe/Brussels",
    "belize": "America/Belize",
    "benin": "Africa/Porto-Novo",
    "bhutan": "Asia/Thimphu",
    "bolivia": "America/La_Paz",
    "bosnia and herzegovina": "Europe/Sarajevo",
    "botswana": "Africa/Gaborone",
    "brazil": "America/Sao_Paulo",
    "brunei": "Asia/Brunei",
    "bulgaria": "Europe/Sofia",
    "burkina faso": "Africa/Ouagadougou",
    "burundi": "Africa/Bujumbura",
    "cambodia": "Asia/Phnom_Penh",
    "cameroon": "Africa/Douala",
    "canada": "America/Toronto",
    "cape verde": "Atlantic/Cape_Verde",
    "central african republic": "Africa/Bangui",
    "chad": "Africa/Ndjamena",
    "chile": "America/Santiago",
    "china": "Asia/Shanghai",
    "colombia": "America/Bogota",
    "comoros": "Indian/Comoro",
    "congo": "Africa/Brazzaville",
    "costa rica": "America/Costa_Rica",
    "croatia": "Europe/Zagreb",
    "cuba": "America/Havana",
    "cyprus": "Asia/Nicosia",
    "czech republic": "Europe/Prague",
    "denmark": "Europe/Copenhagen",
    "djibouti": "Africa/Djibouti",
    "dominica": "America/Dominica",
    "dominican republic": "America/Santo_Domingo",
    "ecuador": "America/Guayaquil",
    "egypt": "Africa/Cairo",
    "el salvador": "America/El_Salvador",
    "equatorial guinea": "Africa/Malabo",
    "eritrea": "Africa/Asmara",
    "estonia": "Europe/Tallinn",
    "eswatini": "Africa/Mbabane",
    "ethiopia": "Africa/Addis_Ababa",
    "fiji": "Pacific/Fiji",
    "finland": "Europe/Helsinki",
    "france": "Europe/Paris",
    "gabon": "Africa/Libreville",
    "gambia": "Africa/Banjul",
    "georgia": "Asia/Tbilisi",
    "germany": "Europe/Berlin",
    "ghana": "Africa/Accra",
    "greece": "Europe/Athens",
    "grenada": "America/Grenada",
    "guatemala": "America/Guatemala",
    "guinea": "Africa/Conakry",
    "guinea-bissau": "Africa/Bissau",
    "guyana": "America/Guyana",
    "haiti": "America/Port-au-Prince",
    "honduras": "America/Tegucigalpa",
    "hungary": "Europe/Budapest",
    "iceland": "Atlantic/Reykjavik",
    "india": "Asia/Kolkata",
    "indonesia": "Asia/Jakarta",
    "iran": "Asia/Tehran",
    "iraq": "Asia/Baghdad",
    "ireland": "Europe/Dublin",
    "israel": "Asia/Jerusalem",
    "italy": "Europe/Rome",
    "ivory coast": "Africa/Abidjan",
    "jamaica": "America/Jamaica",
    "japan": "Asia/Tokyo",
    "jordan": "Asia/Amman",
    "kazakhstan": "Asia/Almaty",
    "kenya": "Africa/Nairobi",
    "kiribati": "Pacific/Tarawa",
    "kuwait": "Asia/Kuwait",
    "kyrgyzstan": "Asia/Bishkek",
    "laos": "Asia/Vientiane",
    "latvia": "Europe/Riga",
    "lebanon": "Asia/Beirut",
    "lesotho": "Africa/Maseru",
    "liberia": "Africa/Monrovia",
    "libya": "Africa/Tripoli",
    "liechtenstein": "Europe/Vaduz",
    "lithuania": "Europe/Vilnius",
    "luxembourg": "Europe/Luxembourg",
    "madagascar": "Indian/Antananarivo",
    "malawi": "Africa/Blantyre",
    "malaysia": "Asia/Kuala_Lumpur",
    "maldives": "Indian/Maldives",
    "mali": "Africa/Bamako",
    "malta": "Europe/Malta",
    "marshall islands": "Pacific/Majuro",
    "mauritania": "Africa/Nouakchott",
    "mauritius": "Indian/Mauritius",
    "mexico": "America/Mexico_City",
    "micronesia": "Pacific/Chuuk",
    "moldova": "Europe/Chisinau",
    "monaco": "Europe/Monaco",
    "mongolia": "Asia/Ulaanbaatar",
    "montenegro": "Europe/Podgorica",
    "morocco": "Africa/Casablanca",
    "mozambique": "Africa/Maputo",
    "myanmar": "Asia/Yangon",
    "namibia": "Africa/Windhoek",
    "nauru": "Pacific/Nauru",
    "nepal": "Asia/Kathmandu",
    "netherlands": "Europe/Amsterdam",
    "new zealand": "Pacific/Auckland",
    "nicaragua": "America/Managua",
    "niger": "Africa/Niamey",
    "nigeria": "Africa/Lagos",
    "north korea": "Asia/Pyongyang",
    "north macedonia": "Europe/Skopje",
    "norway": "Europe/Oslo",
    "oman": "Asia/Muscat",
    "pakistan": "Asia/Karachi",
    "palau": "Pacific/Palau",
    "panama": "America/Panama",
    "papua new guinea": "Pacific/Port_Moresby",
    "paraguay": "America/Asuncion",
    "peru": "America/Lima",
    "philippines": "Asia/Manila",
    "poland": "Europe/Warsaw",
    "portugal": "Europe/Lisbon",
    "qatar": "Asia/Qatar",
    "romania": "Europe/Bucharest",
    "russia": "Europe/Moscow",
    "rwanda": "Africa/Kigali",
    "saint kitts and nevis": "America/St_Kitts",
    "saint lucia": "America/St_Lucia",
    "saint vincent and the grenadines": "America/St_Vincent",
    "samoa": "Pacific/Apia",
    "san marino": "Europe/San_Marino",
    "saudi arabia": "Asia/Riyadh",
    "senegal": "Africa/Dakar",
    "serbia": "Europe/Belgrade",
    "seychelles": "Indian/Mahe",
    "sierra leone": "Africa/Freetown",
    "singapore": "Asia/Singapore",
    "slovakia": "Europe/Bratislava",
    "slovenia": "Europe/Ljubljana",
    "solomon islands": "Pacific/Guadalcanal",
    "somalia": "Africa/Mogadishu",
    "south africa": "Africa/Johannesburg",
    "south korea": "Asia/Seoul",
    "south sudan": "Africa/Juba",
    "spain": "Europe/Madrid",
    "sri lanka": "Asia/Colombo",
    "sudan": "Africa/Khartoum",
    "suriname": "America/Paramaribo",
    "sweden": "Europe/Stockholm",
    "switzerland": "Europe/Zurich",
    "syria": "Asia/Damascus",
    "taiwan": "Asia/Taipei",
    "tajikistan": "Asia/Dushanbe",
    "tanzania": "Africa/Dar_es_Salaam",
    "thailand": "Asia/Bangkok",
    "togo": "Africa/Lome",
    "tonga": "Pacific/Tongatapu",
    "trinidad and tobago": "America/Port_of_Spain",
    "tunisia": "Africa/Tunis",
    "turkey": "Europe/Istanbul",
    "turkmenistan": "Asia/Ashgabat",
    "tuvalu": "Pacific/Funafuti",
    "uganda": "Africa/Kampala",
    "ukraine": "Europe/Kiev",
    "united arab emirates": "Asia/Dubai",
    "united kingdom": "Europe/London",
    "united states": "America/New_York",
    "uruguay": "America/Montevideo",
    "uzbekistan": "Asia/Tashkent",
    "vanuatu": "Pacific/Efate",
    "vatican": "Europe/Vatican",
    "venezuela": "America/Caracas",
    "vietnam": "Asia/Ho_Chi_Minh",
    "yemen": "Asia/Aden",
    "zambia": "Africa/Lusaka",
    "zimbabwe": "Africa/Harare",
}

# === Common aliases ===
ALIASES = {
    "usa": "united states",
    "us": "united states",
    "uk": "united kingdom",
    "pst": "America/Los_Angeles",
    "est": "America/New_York",
    "cst": "America/Chicago",
    "mst": "America/Denver",
}

# Function to remove non-ASCII characters
def remove_non_ascii(text):
    if isinstance(text, str):
        return ''.join(char if ord(char) < 128 else '?' for char in text)
    return ''

# Resolve input to timezone
def resolve_timezone(user_input):
    user_input = user_input.strip().lower()
    if user_input in ALIASES:
        tz = ALIASES[user_input]
        return pytz.timezone(tz)
    if user_input in COUNTRY_TIMEZONES:
        return pytz.timezone(COUNTRY_TIMEZONES[user_input])
    return None

# === MAIN SCRIPT ===
try:
    csv_file = 'chat_messages.csv'

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file '{csv_file}' not found in the current folder.")

    df = pd.read_csv(csv_file)

    # Ask for target
    country_input = input("Enter country or timezone alias (e.g. Malaysia, Japan, US, PST, UK): ")
    target_tz = resolve_timezone(country_input)

    if target_tz is None:
        print(f"⚠️ Could not resolve '{country_input}', defaulting to UTC")
        target_tz = pytz.UTC
    else:
        print(f"✅ Using timezone: {target_tz}")

    # === Key fix: Twitch CSV is in PST originally ===
    source_tz = pytz.timezone("America/Los_Angeles")

    try:
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df = df.dropna(subset=['time'])

        # localize as PST
        df['time'] = df['time'].dt.tz_localize(source_tz, ambiguous='NaT', nonexistent='shift_forward')
        # convert to target
        df['time'] = df['time'].dt.tz_convert(target_tz)

        df = df.sort_values(by='time', ascending=True)
    except Exception as e:
        print(f"Error parsing timestamps: {e}")

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

        link_per_row = 5
        cell_width = pdf.w / link_per_row - 10
        cell_height = 8
        col_count = 0

        for date in unique_dates:
            date_str = str(date)
            link_id = pdf.add_link()
            date_links[date_str] = link_id

            pdf.set_text_color(0, 0, 255)
            pdf.cell(cell_width, cell_height, date_str, border=1,
                     new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', link=link_id)

            col_count += 1
            if col_count >= link_per_row:
                pdf.ln(cell_height)
                col_count = 0

        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)

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
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
                else:
                    timestamp = "Unknown Time"

                message = remove_non_ascii(row.get('body', ''))
                pdf.multi_cell(0, 8, text=f"{timestamp}: {message}")
                pdf.ln(1)

        pdf_output_file = os.path.join(output_folder, f'{channel}_messages.pdf')
        pdf.output(pdf_output_file)
        print(f"✅ Export completed for channel '{channel}'! Saved as '{pdf_output_file}'.")

    print("🎉 All channel PDFs have been exported successfully!")

except KeyboardInterrupt:
    print("\n⛔ Process interrupted by user (Ctrl+C). Exiting safely...")