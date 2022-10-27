from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/vote", methods=["POST"])
def vote():
    key = request.form.get("KEY")
    candidate = request.form.get("candidate")
    print(f"Voted for {candidate} with key '{key}'!")
    
    with open("all_keys.json") as f: all_keys = json.load(f)
    with open("done_keys.json") as f: done_keys = json.load(f)

    if key not in all_keys:
        return render_template("failure.html", message="Invalid key!")
    if key in done_keys:
        return render_template("failure.html", message="You have voted already!")
    
    done_keys.append(key)
    with open("done_keys.json", "w") as f: done_keys = json.dump(done_keys, f)
    
    with open("votes.json") as file: data = json.load(file)
    data[candidate] += 1
    with open("votes.json", "w") as file: json.dump(data, file)

    return render_template("success.html")

@app.route("/results")
def results():
    with open("votes.json") as file:
        data = json.load(file)
    agneev = data["agneev"]
    vanshaj = data["vanshaj"]
    return render_template("results.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, host="192.168.0.100", port=5050)