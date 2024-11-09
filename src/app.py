from flask import Flask, render_template, jsonify, request
import pandas as pd
import utils
import MailSender
import EventTracker

app = Flask(__name__)

# Instantiate MailSender
mail_sender = MailSender.SendMails('' , '' , '')
eventcounts= ["IDOL" , 0 , 0 , 0]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Submit', methods=['POST'])
def submit():
    response = None
    if request.method == 'POST':
        try:
            sender_name = request.form['SenderName']
            sender_position = request.form['SenderPosition']
            sender_email = request.form['SenderEmail']
            ScheduleOrSend = request.form['ScheduleOrSend']
            Delay = request.form['Delay']
            Delay = int(Delay) if Delay != '' else 0
            sender_company = request.form['SenderCompany']
            user_prompt = request.form['prompt']
            datafile = request.files.get('DataFile')

            # Processing the file
            df = utils.readFile(datafile, datafile.filename)
            IntroText = f"My name is {sender_name}, I am {sender_position} at {sender_company} and my email is {sender_email} "
            mail_sender = MailSender.SendMails(df, IntroText + user_prompt, sender_email)
            # Execute sending or scheduling
            if ScheduleOrSend == 'sendIntantly':
                mail_sender.sender(eventcounts)
                response = "Emails sent instantly!"
            else:
                mail_sender.schedule_email(Delay , eventcounts )
                response = f"Emails scheduled with a delay of {Delay} minutes between each email."
        
        except Exception as e:
            response = f"An error occurred: {e}"

    return jsonify(response=response)

# Route to get the current count values
@app.route('/get_counts', methods=['GET'])
def get_counts():
    counts = {
        'status': eventcounts[0],
        'count1': eventcounts[1],
        'count2': eventcounts[2],
        'count3': eventcounts[3]
    }
    return jsonify(counts=counts)


@app.route('/dashboard')
def dashboard():
    # Fetch email events from Mailgun
    events = EventTracker.fetch_email_events()

    if not events:
        return render_template("dashboard.html", message="No email events found in the last 2 days.")

    # Convert events to CSV format
    csv_data = EventTracker.events_to_csv(events)

    # Return the rendered HTML page with the events and CSV data
    return render_template("dashboard.html", events=events, csv_data=csv_data)

if __name__ == "__main__":
    app.run(debug=True)
