from flask import Flask, render_template, request
import re
from collections import Counter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        text = file.read().decode('utf-8')

        words = re.findall(r'\b[а-яА-Яa-zA-ZёЁ]+\b', text.lower())

        counter = Counter(words)

        if not words:
            return render_template(
                'result.html',
                word='Слова не найдены',
                count=0
            )

        most_common_word, count = counter.most_common(1)[0]

        return render_template(
            'result.html',
            word=most_common_word,
            count=count
        )

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)