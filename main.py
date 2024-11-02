from flask import Flask, render_template, request
from generate import generate_encounter 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Collect form data
    level_range = f"{request.form.get('low')}-{request.form.get('high')}"
    difficulty = request.form.get("difficulty")
    biome = request.form.get("biome")
    context = request.form.get("context")

    # Call the generate_encounter function
    encounter = generate_encounter(level_range, difficulty, biome, context)

    print(encounter)
    
    # Render encounter on a result page
    return render_template("result.html", encounter=encounter)

if __name__ == "__main__":
    app.run(debug=True)