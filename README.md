# Schriftzeichenblatt-Generator

Übungsblätter für chinesische Schriftzeichen erstellen und drucken, direkt im Browser.

**➜ App öffnen: https://smartuptake.github.io/schriftzeichenblatt-generator/**

Chinesische Zeichen eingeben, Aussehen anpassen, drucken oder als PDF sichern. Keine Installation, kein Konto nötig.

![Beispiel](Beispiel-Schriftzeichenblatt.pdf)

## Was auf dem Blatt steht

Für jedes Zeichen gibt es einen Block:

- **Kopfzeile:** Pinyin (blau) und daneben die Strichreihenfolge Strich für Strich. Der neue Strich ist rot, die fertigen schwarz, die kommenden hellgrau.
- **Erste Zeile:** Musterzeichen mit farbig hervorgehobenem Radikal (rot) und dunkelgrauem Rest. Danach folgen graue Zeichen zum Nachzeichnen und leere Kästchen.
- **Übungszeilen:** leere Kästchen mit 米- oder 田-Raster.
- **Darunter:** die Übersetzung auf Englisch, Deutsch und Französisch.

## Einstellungen

- Kästchen pro Zeile, Zahl der Nachzeichen-Kästchen, Zahl der leeren Übungszeilen
- Wiederholungen pro Zeichen, doppelte Zeichen zusammenfassen
- Rasterart (米 / 田 / leer) und alle Farben
- Pinyin in Wunschfarbe oder in Tonfarben
- Übersetzung Englisch, Deutsch und/oder Französisch, nebeneinander oder untereinander
- Papierformat (A4 / US Letter), Hoch- oder Querformat, Ränder
- Logo oben in der Mitte der ersten Seite (Höhe einstellbar, abschaltbar)
- Titel, Felder für Name und Datum, Seitenzahlen
- Pinyin und Übersetzungen lassen sich pro Zeichen bearbeiten; die Änderungen merkt sich der Browser
- Zeichenlisten lassen sich unter einem Namen speichern und wieder laden

## Ohne Internet benutzen

Die App ist eine einzige Datei ([`index.html`](index.html), ca. 13 MB), die alle Daten enthält: Pinyin, Übersetzungen und Strichdaten für 9.574 Zeichen. Wer sie herunterlädt und per Doppelklick im Browser öffnet, kann sie auch offline benutzen.

Tipp: Die Datei im Browser öffnen (Chrome, Safari, Edge, Firefox), nicht in einer Datei-Vorschau. Dort funktionieren Drucken und das Laden der Daten oft nicht.

## Datenquellen und Lizenzen

| Daten | Quelle | Lizenz |
|---|---|---|
| Strichdaten und Radikale | [hanzi-writer-data](https://github.com/chanind/hanzi-writer-data) / [Make Me a Hanzi](https://github.com/skishore/makemeahanzi), abgeleitet aus Schriften von Arphic Technology | [Arphic Public License](lizenzen/ARPHIC-PUBLIC-LICENSE.txt) |
| Pinyin, Zeichenzerlegung | [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) | siehe dortiges Projekt |
| Englische Übersetzungen | [CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Deutsche Übersetzungen | [HanDeDict](https://handedict.zydeo.net/) | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/de/) |
| Französische Übersetzungen | [CFDICT](http://www.chine-informations.com) (Chine-Informations.com) | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) |

Die daraus aufbereiteten Wörterbuchdaten (in `_Quellcode/zeichendaten.json.gz` und in `index.html`) stehen ebenfalls unter CC BY-SA. Mehr dazu in [`lizenzen/QUELLEN.md`](lizenzen/QUELLEN.md).

## Für Änderungen am Code

- `_Quellcode/vorlage.html`: der eigentliche Programmcode (HTML, CSS, JavaScript)
- `_Quellcode/zeichendaten.json.gz`: Wörterbuch und Strichdaten, komprimiert
- `_Quellcode/bauen.py`: setzt beides zur fertigen Datei zusammen:

  ```bash
  python3 _Quellcode/bauen.py index.html
  ```

- `_Quellcode/woerterbuch_bauen.py`: erzeugt die Wörterbuchdaten aus CC-CEDICT, HanDeDict und Make Me a Hanzi
