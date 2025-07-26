"""
Simple Flask app to calculate recommended bed or wake times using REM cycle estimates.
Assumes ~14 minutes to fall asleep and 90-minute sleep cycles.
"""
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

def get_wake_times(bedtime_str):
    """Return wake-up times for up to six REM cycles after a given bed time."""
    bedtime = datetime.strptime(bedtime_str, "%H:%M")
    fall_asleep = bedtime + timedelta(minutes=14)
    times = []
    # calculate wake times for 1-6 cycles
    for cycles in range(1, 7):
        t = fall_asleep + timedelta(minutes=90 * cycles)
        times.append((cycles, t.strftime("%I:%M %p")))
    return times

def get_bed_times(wakeup_str):
    """Return bed times needed to wake up at a specified time after completing up to six cycles."""
    wake = datetime.strptime(wakeup_str, "%H:%M")
    times = []
    # iterate backwards to suggest earliest bed time first
    for cycles in range(6, 0, -1):
        t = wake - timedelta(minutes=(90 * cycles + 14))
        times.append((cycles, t.strftime("%I:%M %p")))
    return times

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle form submission and display calculated times."""
    result = None
    if request.method == "POST":
        mode = request.form.get("mode")  # "wake" or "bed"
        time_str = request.form.get("time")  # HH:MM formatted time
        if mode == "wake":
            result = get_wake_times(time_str)
            # Build a helpful title for the result list
            title = f"If you go to bed at {datetime.strptime(time_str,'%H:%M').strftime('%I:%M %p')}, wake at:"
        else:
            result = get_bed_times(time_str)
            # Build a helpful title for the result list
            title = f"If you want to wake at {datetime.strptime(time_str,'%H:%M').strftime('%I:%M %p')}, go to bed at:"
        # Render the results using the HTML template
        return render_template("index.html", result=result, title=title, mode=mode)
    # Initial GET request displays empty form
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)  # disable debug in production
