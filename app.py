from flask import Flask, request, render_template, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('data-419313-295934c65ef4.json', scopes)
client = gspread.authorize(credentials)

# Open the desired sheet
sheet = client.open('FirstSheet').sheet1

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if 'name' in request.form and 'email' in request.form and 'q1' in request.form:
        name = request.form['name']
        email = request.form['email'].strip()  # Remove leading and trailing whitespace
        q1 = request.form['q1']
        current_date = datetime.now().date()

        try:
            sheet.append_row([current_date.strftime('%Y-%m-%d'), name, email, q1])

            # Redirect to home page or some other page after successful login
            return redirect(url_for('/home'))

        except gspread.exceptions.APIError as error:
            # Handle Google Sheets API errors
            return render_template('index.html', error=str(error))

    else:
        # Handle missing form fields
        return render_template('index.html', error='Missing username, email, or security question')

@app.route('/home')
def home():
    # You can handle authenticated users here
    return render_template('a.html')

if __name__ == '__main__':
    app.run(debug=False)
