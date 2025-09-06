# twitchChatLogsToPDF
Export CSV file downloaded from Twitch to readable PDF files

📖 Twitch Chat CSV to PDF
Easily convert your exported Twitch chat logs (CSV format) into a neatly formatted PDF — all with one click!
Perfect for archiving, sharing, or just reliving your favourite moments.

## Why do you need this program?

If you’ve ever tried reading Twitch chat logs directly from a CSV file, you know it’s a mess. Long lines, confusing columns, and no easy way to find specific dates or messages. This program solves that by turning those raw CSV chat logs into clean, easy-to-read PDFs:

- No more messy spreadsheets: Chat messages are neatly organized by date with clickable links for quick navigation.
- Readable timestamps: All times are converted to local time of your choice so you know exactly when things happened.
- ~Looks professional: Each PDF includes the streamer’s logo on the first page to make your archives look polished.~
- Easy to share and archive: PDFs are simple to open, search, and save, unlike bulky CSVs.
- This tool runs locally/offline, no data is sent or stored.
- No account or login required.

In short, this tool makes Twitch chat logs easy to read, understand, and keep, no spreadsheet skills required.

## Step 1 — Export Your Twitch Chat (CSV)

1. Go to Twitch and open **Settings**.

2. Click **Security and Privacy**.

4. Scroll to the bottom and click the **Download Your Data** button.

5. From the list of options, select **Viewing and Chat History**, then click Next.

6. Under **Select date range for your report**, choose how far back you want to retrieve your chat history. For example, you can go back to the date you created your Twitch account.

  - 💡 Tip: If you can’t click the Update button, it might be because the End Date is set to today. Change it to one day before, and it should work.

7. Click **Request Report** and wait for Twitch to process your chat logs into a CSV file.


## Step 2 — Download the EXE File 💾

1. From this [page](<https://mega.nz/file/EHgEmaBY#xOGKz7ga9oofWR7qxb0V8hrGchv6Rao7HrDGukDGCy8>), download the TwitchChatExportPDF.exe file.

2. Create a new folder, and place both the CSV file *(chat_messages.csv)* Twitch provided and the *TwitchChatExportPDF.exe* file you just downloaded into it.

<img width="500" height="500" alt="Screenshot 2025-08-13 201814" src="https://github.com/user-attachments/assets/453562f8-2919-4e1e-9887-1a2087facfc4" />





3. Run the TwitchChatExportPDF.exe file.


 - 💡 Tip: In case of emergency, you can press Ctrl + C to stop the program while its running.




   <img width="500" height="500" alt="Screenshot 2025-08-13 201841" src="https://github.com/user-attachments/assets/4e3af097-c312-4680-869f-9d3a445eb8c4" />




4. A new folder called **Twitch Chat History** will be created automatically.



<img width="500" height="500" alt="Screenshot 2025-08-13 202413" src="https://github.com/user-attachments/assets/6e9e67e1-6a20-44e0-9d3b-bafd072388f6" />


5. Inside the **Twitch Chat History** folder, you’ll find PDF files named after the various channels you’ve chatted in.

6. Enjoy looking back at your early days of Twitch messages.

## Step 2 (Alternative) — Run the Python Script Yourself
If you don’t want to run the EXE file, or if you want to see how the code works, you can run the Python script directly. This is great for users who want full control or are new to Python — we’ll walk you through the setup.

1. Install Python (which includes pip)
- Go to the official Python website: https://www.python.org/downloads/windows/
Click the Download Python 3.x.x button (choose the latest version 3.8 or above).
Run the installer. Important: During installation, check the box that says “Add Python to PATH” before clicking Install.
Wait for the installation to finish.

2. Open Command Prompt
- Press Windows Key + R
- Type cmd and press Enter
A black terminal window will open — this is where you will type commands.

3. In the Command Prompt, type:

```bash
python --version
```
You should see something like:
Python 3.x.x

Next, check pip (Python’s package installer) by typing:
```bash
pip --version
```
You should see something like:
pip x.x.x from ...

If you get an error, try typing:
```bash
python -m ensurepip --upgrade
```
Then try pip --version again.

4. Install required packages
- Now, run this command in Command Prompt to install all necessary Python libraries used by the script:
```bash
pip install pandas fpdf2 Pillow requests python-dotenv pytz
```
Wait for it to finish. It downloads and installs everything the script needs.

5. Prepare your files
- Put the Twitch CSV chat export file (chat_messages.csv) and the Python script (Download TwitchChatExportPDF.py from this page) into the same folder on your PC.

6. Run the Python script
- In Command Prompt, navigate to the folder where your files are saved. For example, if your files are in C:\Users\YourName\Downloads\TwitchChat, type:
```bash
cd C:\Users\YourName\Downloads\TwitchChat
```
- Then run the script by typing:
```bash
python TwitchChatExportPDF.py
```
7. View your PDFs
- After it finishes, a new folder named Twitch Chat History will appear in that folder, containing your readable PDF files! Enjoy looking back at your early days of Twitch messages.

## Example Output

- Folder containing PDFs with all your chat messages for each channel you’ve interacted with
<img width="500" height="402" alt="image" src="https://github.com/user-attachments/assets/2f3f5ebb-10b1-44e9-acc0-97a4fbf32944" />


- Each PDF has clickable date links for easy navigation through your chat history
<img width="500" height="500" alt="Screenshot 2025-08-13 at 11 37 44 PM" src="https://github.com/user-attachments/assets/2f520b65-55e8-4689-9f59-98b7e4931136" />



