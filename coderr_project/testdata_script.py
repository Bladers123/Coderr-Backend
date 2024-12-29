import json
from django.contrib.auth import get_user_model
from freelancer_platform_app.models import Offer, OfferDetail

User = get_user_model()

# Datei einlesen
file_path = "testdata.json"

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

    # 3. Angebote erstellen
    for offer_data in data.get("offers", []):
        try:
            user = User.objects.get(id=offer_data["user_id"])

            # Angebot prüfen und erstellen
            if not Offer.objects.filter(id=offer_data["id"]).exists():
                offer = Offer.objects.create(
                    user=user,
                    title=offer_data["title"],
                    description=offer_data["description"],
                    min_price=offer_data["min_price"],
                    min_delivery_time=offer_data["min_delivery_time"]
                )

                # Angebotsdetails hinzufügen
                for detail in offer_data.get("details", []):
                    if not OfferDetail.objects.filter(offer=offer, url=detail["url"]).exists():
                        OfferDetail.objects.create(offer=offer, url=detail["url"])
            else:
                print(f"Angebot mit ID {offer_data['id']} existiert bereits.")

        except User.DoesNotExist:
            print(f"Benutzer mit ID {offer_data['user_id']} existiert nicht.")

    print(f"Angebote wurden erstellt.")

except FileNotFoundError:
    print(f"Die Datei '{file_path}' wurde nicht gefunden.")
except Exception as e:
    print(f"Fehler: {e}")



# python manage.py shell
# exec(open("testdata_script.py").read())

