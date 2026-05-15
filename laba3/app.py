from flask import Flask, render_template, request
import re
from collections import Counter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        if not file.filename.endswith('.txt'):
            return render_template(
                'result.html',
                words='Можно загружать только файлы .txt',
                count=0
            )

        text = file.read().decode('utf-8')

        words = re.findall(r'\b[а-яА-Яa-zA-ZёЁ]+\b', text.lower())

        counter = Counter(words)

        if not words:
            return render_template(
                'result.html',
                words='Слова не найдены',
                count=0
            )

        max_count = max(counter.values())

        most_common_words = []
        for word, count in counter.items():
            if count == max_count:
                most_common_words.append(word)

        result_words = ', '.join(most_common_words)

        return render_template(
            'result.html',
            words=result_words,
            count=max_count
        )

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)