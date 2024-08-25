from flask import Flask, render_template, request
import json

from example_settings import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", candidates=candidates, allow_empty_submissions=allow_empty_submissions)

@app.route("/vote", methods=["POST"])
def vote():
    key = request.form.get("KEY")
    
    # Load the key data
    with open("all_keys.json") as f: 
        all_keys = json.load(f)
    try:
        with open("done_keys.json") as f: 
            done_keys = json.load(f)
    except FileNotFoundError:
        done_keys = []

    # Check if the key is valid and not already used
    if key not in all_keys:
        return render_template("failure.html", message="Invalid key!")
    if key in done_keys:
        return render_template("failure.html", message="You have voted already!")

    # Append the key to the list of used keys
    done_keys.append(key)
    with open("done_keys.json", "w") as f: 
        json.dump(done_keys, f)

    # Load the existing votes data
    try:
        with open("votes.json") as file: 
            data = json.load(file)
    except FileNotFoundError:
            data = {
                pos:{
                    cand: 0 for cand in candidates[pos]
                }  for pos in candidates
            }

    # Process the votes for each position
    for position in request.form:
        if position == "KEY":
            continue
        candidate = request.form.get(position)
        if candidate:
            # replace _ with " " in positions
            # position = 
            if position not in data:
                data[position] = {}
            if candidate not in data[position]:
                data[position][candidate] = 0
            data[position][candidate] += 1

    # Save the updated votes data
    with open("votes.json", "w") as file: 
        json.dump(data, file, indent=4)

    # Render the success page
    return render_template("success.html")

@app.route("/res")
def results():
    try:
        with open("votes.json") as file: 
            data = json.load(file)
    except FileNotFoundError:
        return render_template("results.html", message="No votes yet!", results={})

    return render_template("results.html", message=None, results=data)

if __name__ == "__main__":
    app.run(debug=debug, host=IP, port=PORT)
