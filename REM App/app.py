from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

def get_wake_times(bedtime_str):
    bedtime = datetime.strptime(bedtime_str, "%H:%M")
    fall_asleep = bedtime + timedelta(minutes=14)
    times = []
    for cycles in range(1, 7):
        t = fall_asleep + timedelta(minutes=90 * cycles)
        times.append((cycles, t.strftime("%I:%M %p")))
    return times

def get_bed_times(wakeup_str):
    wake = datetime.strptime(wakeup_str, "%H:%M")
    times = []
    for cycles in range(6, 0, -1):
        t = wake - timedelta(minutes=(90 * cycles + 14))
        times.append((cycles, t.strftime("%I:%M %p")))
    return times

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        mode = request.form.get("mode")
        time_str = request.form.get("time")
        if mode == "wake":
            result = get_wake_times(time_str)
            title = f"If you go to bed at {datetime.strptime(time_str,'%H:%M').strftime('%I:%M %p')}, wake at:"
        else:
            result = get_bed_times(time_str)
            title = f"If you want to wake at {datetime.strptime(time_str,'%H:%M').strftime('%I:%M %p')}, go to bed at:"
        return render_template("index.html", result=result, title=title, mode=mode)
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
