from flask import Flask, render_template, request, redirect, url_for
import threading
from load_test import run_load_test

app = Flask(__name__)

# Global results dictionary to store load test results
results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-test', methods=['POST'])
def start_test():
    global results
    # Get form inputs
    url = request.form['url']
    num_requests = int(request.form['num_requests'])
    concurrent_requests = int(request.form['concurrent_requests'])

    # Clear previous results
    results.clear()

    # Start the load test in a separate thread
    thread = threading.Thread(target=run_load_test, args=(url, num_requests, concurrent_requests, results))
    thread.start()

    # Redirect to results page
    return redirect(url_for('results_page'))

@app.route('/results')
def results_page():
    global results
    print("Current Results:", results)  # Debugging output
    if not results:
        return render_template('results.html', results=None)
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
