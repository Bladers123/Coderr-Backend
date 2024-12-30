import os
import sys
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr_project.settings')

    # Django-Umgebung initialisieren
    django.setup()

    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    User = get_user_model()  # Zugriff auf das User-Modell funktioniert jetzt

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Prüfen, ob der Server gestartet wird
    if len(sys.argv) > 1 and sys.argv[1] == "runserver" and os.environ.get("RUN_MAIN") != "true":
        load_testdata = input("\nMöchten Sie Testdaten laden? (y/n): ").strip().lower()
        if load_testdata == 'y':
            print("\nEs werden jetzt die erforderlichen Schritte ausgeführt, um die Testdaten zu laden...\n")
            try:
                # 1. Migrationen erstellen und anwenden
                print("1. Migrationen werden erstellt...")
                call_command("makemigrations")
                print("2. Migrationen werden angewendet...")
                call_command("migrate")

                # 2. Superuser erstellen (nur wenn keiner existiert)
                if not User.objects.filter(is_superuser=True).exists():
                    print("3. Superuser wird erstellt...")
                    call_command("createsuperuser")

                # 3. Testdaten laden
                print("4. Testdaten werden geladen...")
                exec(open("test_data_script.py").read())
                print("Testdaten wurden erfolgreich geladen.")
            except Exception as e:
                print(f"Fehler beim Ausführen der Schritte: {e}")
                return

        elif load_testdata == 'n':
            print("Testdaten werden nicht geladen. Der Server startet jetzt...")

        else:
            print("Ungültige Eingabe. Der Server startet jetzt ohne Testdaten...")

    # Django-Management-Befehle ausführen
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
