## Beschreibung

Dieses Skript löst das Problem, dass Programme mit Administratorrechten (z. B. OBS, AMD Adrenalin) Tastaturbefehle von nicht privilegierten Anwendungen oder Geräten (wie Streamdeck, AutoHotkey-Skripten) ignorieren.

Der `HotkeyService` fungiert als Vermittler:

- Empfängt Hotkey-Befehle über einen lokalen Socket (nur von `localhost`).
    
- Sendet die Tastenkombinationen mit Admin-Rechten über die `keyboard`\-Bibliothek (Win32-API).
    
- Blockiert gefährliche System-Hotkeys (z. B. `Win+L`, `Ctrl+Alt+Del`).
    

* * *

## Anwendungsfälle

- Steuerung von **OBS** (als Admin) über ein Streamdeck.
    
- Senden von Media-Tasten (Play/Pause) an privilegierte Apps.
    
- Auslösen von Screenshot-Hotkeys (z. B. `Strg+Umschalt+S` in AMD Adrenalin).
    

* * *

## Funktionen

✅ **Sichere Kommunikation**

- Nur lokale Verbindungen (`127.0.0.1`) werden akzeptiert.
    
- HMAC-Token zur Authentifizierung (basierend auf Zeitstempel + Secret).
    

✅ **Blocklist für gefährliche Hotkeys**

- Verhindert unerwünschte Systemaktionen (z. B. `Alt+F4`, `Win+R`).

✅ **Einfache Integration**

- Client-Skripte können Befehle über TCP senden.

* * *

## Installation

### Voraussetzungen

```bash
pip install keyboard
```

### Ausführen

```bash
python hotkeyservice.py
```

Wenn es im Hintergrund ausgeführt werden soll kann man die Datei einfach in `hotkeyservice.pyw` umbenannt werden.

### Installation in der Aufgabenplanung

Kompiliere das Script zum Beispiel mit `auto-py-to-exe` zu einer `Windows Based (hide the console)` Anwendung.

**In der Aufgabenplanung `taskschd.msc` dann eine neue Einfache Aufgabe erstellen**

1.  Klicke Rechts auf *„Aufgabenplanungsbibliothek“* → *„Aufgabe erstellen...“*
2.  Im Tab Allgemein: Name `HotkeyService` und Beschreibung *„Sendet Hotkeys mit Admin-Rechten an privilegierte Apps“*
3.  Im Tab Allgemein: Wähle *„Nur ausführen, wenn der Benutzer angemeldet ist“* & *„Mit höchsten Privilegien ausführen“*
4.  Im Tab Trigger: *„Neu...“* → Wähle im Menü *„Aufgabe starten: Bei Anmeldung“* → Wähle aus *„Bestimmte Benutzer: DeinPC/DeinName“* → Wähle unten *„Aktiviert“* → Klicke auf ***„OK“***
5.  Im Tab Aktionen: *„Neu...“* → Wähle im Menü Aktion: *„Programm starten“* → Trage deine kompilierte Anwendung ein → Klicke auf ***„OK“***
6.  Klicke unten auf ***„OK“***
7.  **Fertig** (Du kannst gerne in den anderen Reitern die Optionen anpassen)

Klicke Rechts auf die von dir erstellte Aufgabe und wähle *„Ausführen“* nun sollte die Anwendung auch im Task-Manager zu finden sein.

* * *

&nbsp;
