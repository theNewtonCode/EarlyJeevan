from flask import Flask, request, render_template
from main import get_early_life_text as gelt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
        chars = int(request.form['chars'])

        output, length = gelt(name, chars)

        if output == "xyz":
            output = "This Person is not known yet!"
            return render_template('index.html', output=output, name=name, chars = chars)
        if chars>length:
            output = 'Too many sentences requested!'
            return render_template('index.html', output=output, name=name, chars = chars)
        return render_template('index.html', output=output, name=name, chars = chars)
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
