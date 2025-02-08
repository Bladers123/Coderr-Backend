# Projekt-Setup-Anleitung für Python 3.12.9
## Diese Anleitung beschreibt die Schritte zur Installation und Konfiguration des Projekts mit Python 3.12.7.

## Installation und Einrichtung
  Lade dir VS-Code herunter und öffne über VS-Code das Projekt (Join-Backend). Öffne das Terminal.


### - Python-Version überprüfen
  Stelle sicher, dass Python 3.12.9 installiert ist:
  **python --version**

### - Virtuelle Umgebung erstellen
  Erstelle eine virtuelle Umgebung im Projektverzeichnis:
  **python -m venv env**

### - Virtuelle Umgebung aktivieren
   Aktiviere die virtuelle Umgebung:
  - **.\env\Scripts\activate**  # Für Windows PowerShell
  - **env\Scripts\activate.bat**  # Für Windows CMD
  - **source env/bin/activate**  # Für Unix/Linux

### - Hinweis: Wenn ein Fehler bezüglich der Ausführungsrichtlinien auftritt, führe folgenden Befehl in PowerShell als Administrator aus:
  **Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser**

### - Abhängigkeiten installieren
  Installiere alle benötigten Pakete aus der requirements.txt:
  **pip install -r requirements.txt**

### - Wenn du die Pakete manuell installieren möchtest, nutze folgende Befehle:
 - **python -m pip install Django**  # Installiert Django
 - **pip install djangorestframework**  # Installiert Django REST Framework
 - **python -m pip install django-cors-headers**  # Installiert django-cors-headers für externen Zugriff

### - Datenbankmigrationen durchführen
  - Erstelle Migrationsdateien basierend auf den Modellen in models.py:
  **python manage.py makemigrations** 
  - Führe die Migrationen aus, um die Tabellen in der Datenbank zu erstellen:
  **python manage.py migrate**

### - Superuser erstellen
  - Erstelle einen superuser:
  **python manage.py createsuperuser** 
  
### - Server starten
  Navigiere in das Projektverzeichnis und starte den Server:
  **python manage.py runserver**
  Der Server wird standardmäßig unter http://127.0.0.1:8000 laufen.
