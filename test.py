import requests

url = "http://127.0.0.1:5000/extract_text"

file_path = "C:/Users/dell/Downloads/AttestationDroits (2).pdf"

try:
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files, timeout=10)
        print("Status:", response.status_code)
        print("Texte extrait :")
        print(response.text)
except Exception as e:
    print("Erreur :", e)

