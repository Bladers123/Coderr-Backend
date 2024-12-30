import json
from django.contrib.auth import get_user_model
from freelancer_platform_app.models import Offer, OfferDetail

User = get_user_model()

# Datei einlesen
file_path = "test_data.json"

try:
    # 1. JSON-Daten laden
    with open(file_path, "r") as file:
        data = json.load(file)

    # 2. Benutzer erstellen
    for user_data in data.get("users", []):
        if not User.objects.filter(id=user_data["id"]).exists():
            User.objects.create_user(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                last_name=user_data["last_name"],
                first_name=user_data["first_name"]
            )
    print(f"Benutzer wurden erstellt.")

except FileNotFoundError:
    print(f"Die Datei '{file_path}' wurde nicht gefunden.")
except Exception as e:
    print(f"Fehler: {e}")



# python manage.py shell
# exec(open("testdata_script.py").read())






