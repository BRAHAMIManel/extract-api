import io
import pdfplumber
import pytesseract
from PIL import Image, UnidentifiedImageError
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/extract_text", methods=["POST"])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    filename = file.filename.lower()
    text = ""

    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                    else:
                        image = page.to_image(resolution=300).original
                        text += pytesseract.image_to_string(image) + "\n"

        elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image = Image.open(file.stream)
            text = pytesseract.image_to_string(image)

        else:
            return jsonify({"error": "Format non pris en charge"}), 400

        return jsonify({"extracted_text": text.strip()})

    except UnidentifiedImageError:
        return jsonify({"error": "Erreur de lecture de l'image"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'extraction : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
