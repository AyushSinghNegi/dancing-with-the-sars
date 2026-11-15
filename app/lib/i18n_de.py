"""German text for the app (Deutsch). Keyed by the English source string (DE), by ui.T key (DE_T) and by
evidence.E key (DE_E). Drafted with an AI assistant; a German speaker should check it before submission.
Anything missing falls back to English."""

MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
          "Dezember"]

DE = {
    # reasons from pipeline/validate.py, shown by evidence.reason_text
    "happened before the radar pair ({a} to {b})": "geschah vor den beiden verglichenen Radarüberflügen ({a} bis {b})",
    "happened after the radar pair ({a} to {b})": "geschah nach den beiden verglichenen Radarüberflügen ({a} bis {b})",
    "location in the report is too vague to score (about {k} km)": "Ortsangabe im Bericht zu ungenau für eine Bewertung (etwa {k} km)",
    "water may have drained before the {d} pass": "das Wasser ist vor dem Überflug am {d} vielleicht abgeflossen",
    "ground near the report is gentler than our {s}° slide search": "das Gelände am gemeldeten Ort ist flacher als unsere Rutschungssuche ab {s}°",
    "dense buildings: radar bounces off walls, which hides street flooding": "dichte Bebauung: Das Radar prallt an Wänden ab, was überflutete Straßen verbirgt",
    "flooding smaller than our 40 m pixels or under thick canopy": "Überflutung kleiner als unsere 40-m-Pixel oder unter dichtem Blätterdach",
    "slide smaller than a few 40 m pixels, or coherence lost everywhere nearby": "Rutschung kleiner als einige 40-m-Pixel, oder die Kohärenz ging ringsum überall verloren",
    "outside the radar box": "außerhalb des Radarausschnitts",
    "no radar data at this spot (edge of swath)": "an dieser Stelle keine Radardaten (Rand des Aufnahmestreifens)",
    "event type has no radar layer (e.g. road closure)": "für diese Ereignisart gibt es keine Radarebene (z. B. Straßensperrung)",
    "in or near a town, where buildings can hide flooded streets (a likely reason, not a measured one)":
        "in oder nahe einer Stadt, wo Gebäude überflutete Straßen verbergen können (ein wahrscheinlicher Grund, kein gemessener)",
    "Why": "Warum",
    # overview
    "Check a place": "Ort prüfen",
    "likely slide zones on slopes of {a}° to {b}°, {h} of them high confidence":
        "wahrscheinliche Rutschungszonen an Hängen von {a}° bis {b}°, davon {h} mit hoher Sicherheit",
    "Leads to check, not verdicts: {u} have no reported event within 2 km.":
        "Hinweise zum Prüfen, keine Urteile: Bei {u} gibt es im Umkreis von 2 km kein gemeldetes Ereignis.",
    "Shown as possible water, never added to the flood figure.":
        "Als mögliches Wasser gezeigt, nie zur Überschwemmungsfläche gezählt.",
    "People who live there": "Menschen vor Ort",
    "Pick your village or town and see what NISAR found within 2, 5 or 10 km, with a link you can send on.":
        "Wählen Sie Ihr Dorf oder Ihre Stadt und sehen Sie, was NISAR im Umkreis von 2, 5 oder 10 km gefunden hat, "
        "mit einem Link zum Weitergeben.",
    "District disaster teams": "Katastrophenschutz im Distrikt",
    "A ranked check list of likely slide zones with radar images of each spot, a printable sheet and KML for phones.":
        "Eine gereihte Checkliste wahrscheinlicher Rutschungszonen mit Radarbildern jeder Stelle, als Druckblatt und "
        "als KML fürs Handy.",
    "Field check list": "Feld-Checkliste",
    "Researchers and journalists": "Forschung und Presse",
    "Every number traced to its NISAR file, the checks behind it, and the maps as GeoTIFF and GeoJSON.":
        "Jede Zahl bis zu ihrer NISAR-Datei zurückverfolgt, die Prüfungen dahinter und die Karten als GeoTIFF und GeoJSON.",
    "Method and data": "Methode und Daten",
    "See how each number was made, and the full validation table":
        "Wie jede Zahl entstand, mit Validierungstabelle",
    "of open water in rivers and reservoirs on {d}, up from {v} km² on {f}":
        "offene Wasserfläche in Flüssen und Stauseen am {d}, nach {v} km² am {f}",
    "{n} NISAR passes, same orbit and radar mode. Watch it on the map's season slider.":
        "{n} NISAR-Überflüge, gleicher Orbit und Radarmodus. Auf der Karte mit dem Jahreszeit-Regler ansehen.",
    "How we checked it": "So haben wir es geprüft",
    "Reported floods": "Gemeldete Überschwemmungen",
    "Second NISAR orbit": "Zweiter NISAR-Orbit",
    "slide zones in its view found again, {l}× more often than chance{p}. A small sample.":
        "Rutschungszonen in seinem Blickfeld erneut gefunden, {l}× häufiger als per Zufall{p}. Eine kleine Stichprobe.",
    "Second elevation map": "Zweites Höhenmodell",
    "slide zones kept when slope comes from NASA's NASADEM instead of Copernicus.":
        "Rutschungszonen bleiben erhalten, wenn die Hangneigung aus NASAs NASADEM statt aus Copernicus stammt.",
    "Water threshold moved": "Wasserschwelle verschoben",
    "Reservoir rise stays between {a} and {b} km²; flooding swings from {c} to {d} km².":
        "Der Anstieg der Stauseen bleibt zwischen {a} und {b} km²; die Überschwemmung schwankt von {c} bis {d} km².",
    "Who it is for": "Für wen es gedacht ist",
    "With the water threshold 1 dB lower or higher: {a} to {b} km².":
        "Mit der Wasserschwelle 1 dB niedriger oder höher: {a} bis {b} km².",
    "Depends strongly on the water threshold: {a} to {b} km² with it moved 1 dB either way.":
        "Hängt stark von der Wasserschwelle ab: {a} bis {b} km², wenn sie um 1 dB verschoben wird.",
    "that radar could observe had a detection nearby. Landslides: {h} of {o}":
        "die das Radar sehen konnte, hatten einen Fund in der Nähe. Erdrutsche: {h} von {o}",
    "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>; if it keeps its 12-day "
    "repeat, the next is <b>{n}</b>. The same open code turns each new pass into these maps and lists.":
        "NISAR überfliegt Pune alle 12 Tage, mit oder ohne Wolken. Letzter Überflug in unseren Daten: <b>{l}</b>; "
        "bleibt es beim 12-Tage-Zyklus, folgt der nächste am <b>{n}</b>. Derselbe offene Code macht aus jedem neuen "
        "Überflug diese Karten und Listen.",
    ", both near one zone that a second elevation map does not keep.":
        ", beide nahe einer Zone, die ein zweites Höhenmodell nicht bestätigt.",
    # explore
    "Base map": "Grundkarte",
    "Layer opacity": "Deckkraft der Ebenen",
    "Slide zones shown": "Angezeigte Rutschungszonen",
    "What the map shows": "Was die Karte zeigt",
    "NISAR pass": "NISAR-Überflug",
    "Show the whole area": "Ganzes Gebiet zeigen",
    "Slide zones": "Rutschungszonen",
    "Flood water": "Hochwasser",
    "Rain and timeline": "Regen und Zeitverlauf",
    "Reported events": "Gemeldete Ereignisse",
    "Downloads": "Downloads",
    " ({s}{v:.0f} km² since {f})": " ({s}{v:.0f} km² seit {f})",
    "NISAR passes on {b} and {a}. Switch radar layers with the button at the top right of the map; click a zone or a "
    "marker for details, or pick a zone below to see its radar evidence.":
        "NISAR-Überflüge am {b} und {a}. Radarebenen schalten Sie oben rechts auf der Karte um; klicken Sie eine Zone "
        "oder Markierung für Details an, oder wählen Sie unten eine Zone, um ihre Radarbelege zu sehen.",
    "{n} likely slide zones, sorted by score. Score adds three pieces of evidence: steepness, radar change, and "
    "coherence lost compared with the surrounding kilometre. Select a row to zoom the map to it and see its radar "
    "evidence.":
        "{n} wahrscheinliche Rutschungszonen, nach Punktzahl sortiert. Die Punktzahl vereint drei Belege: Steilheit, "
        "Radaränderung und Kohärenzverlust gegenüber dem umgebenden Kilometer. Wählen Sie eine Zeile, um die Karte "
        "dorthin zu zoomen und die Radarbelege zu sehen.",
    "{n} flood patches: new water on {a} where no water was recorded between 1984 and 2021. Select one to zoom the map "
    "to it and see the radar before and after.":
        "{n} Überschwemmungsflächen: neues Wasser am {a}, wo zwischen 1984 und 2021 nie Wasser verzeichnet wurde. "
        "Wählen Sie eine, um die Karte dorthin zu zoomen und das Radar vorher und nachher zu sehen.",
    "Open water on every NISAR pass of the same orbit and radar mode. Press play, or drag the slider inside the "
    "map, to watch the reservoirs fill after the July storm. The map keeps its zoom while the date changes.":
        "Offenes Wasser bei jedem NISAR-Überflug mit gleichem Orbit und Radarmodus. Drücken Sie auf Abspielen oder "
        "ziehen Sie den Regler in der Karte und sehen Sie, wie sich die Stauseen nach dem Juli-Sturm füllen. Die Karte "
        "behält ihren Zoom, während das Datum wechselt.",
    "Open water on this pass": "Offenes Wasser bei diesem Überflug",
    "Since the pass on {p}: {r:.0f} mm of rain, open water {s}{v:.0f} km².":
        "Seit dem Überflug am {p}: {r:.0f} mm Regen, offenes Wasser {s}{v:.0f} km².",
    "Rain: NASA GPM IMERG Late Run daily totals, averaged over the whole study box, in UTC days from the day after "
    "the previous pass to the day of this pass. An average over the box is far lower than totals at single rain "
    "gauges, and Late Run values may change slightly in the Final Run.":
        "Regen: Tagessummen aus NASA GPM IMERG Late Run, gemittelt über das ganze Untersuchungsgebiet, in UTC-Tagen vom "
        "Tag nach dem vorigen Überflug bis zum Tag dieses Überflugs. Ein Gebietsmittel liegt weit unter den Summen "
        "einzelner Regenmesser, und Late-Run-Werte können sich im Final Run leicht ändern.",
    "Field check list: print it, KML for phones, CSV": "Feld-Checkliste: drucken, KML fürs Handy, CSV",
    "All water numbers and thresholds": "Alle Wasserzahlen und Schwellenwerte",
    "of open water inside the area where water has ever been recorded (JRC, 1984 to 2021) on {d}":
        "offenes Wasser am {d} innerhalb der Fläche, auf der je Wasser verzeichnet wurde (JRC, 1984 bis 2021)",
    "High confidence only": "Nur hohe Sicherheit",
    "Medium and high": "Mittel und hoch",
    "All, including low": "Alle, auch niedrig",
    "Map zoomed to {i}": "Karte auf {i} gezoomt",
    "Patch": "Fläche",
    "Nearest reported flood": "Nächste gemeldete Überschwemmung",
    "What changed, {b} to {a}": "Was sich änderte, {b} bis {a}",
    "Water through the season, {f} to {l}": "Wasser im Jahresverlauf, {f} bis {l}",
    "Area (ha)": "Fläche (ha)",
    "Darker by (dB)": "Dunkler um (dB)",
    # story
    "Field check list for district teams": "Feld-Checkliste für Einsatzteams",
    "Method and limits": "Methode und Grenzen",
    "Where next": "Wie weiter",
    "Watch the water spread on the map": "Das Wasser auf der Karte wachsen sehen",
    # field
    "Printable list with radar images": "Druckbare Liste mit Radarbildern",
    "KML for Google Earth and phone maps": "KML für Google Earth und Handy-Karten",
    "Spreadsheet (CSV)": "Tabelle (CSV)",
    "Confidence": "Sicherheit",
    "Backed by an extra check": "Von einer Zusatzprüfung gestützt",
    "Near a place": "In der Nähe von",
    "{n} of {t} zones. Select a row to see its radar evidence.":
        "{n} von {t} Zonen. Wählen Sie eine Zeile, um die Radarbelege zu sehen.",
    "No slide zones in this run.": "In diesem Lauf gibt es keine Rutschungszonen.",
    "The flood matches are no more than chance gives: places nobody reported match {e} of {n}.":
        "Die Hochwasser-Treffer sind nicht mehr, als der Zufall liefert: Orte, die niemand gemeldet hat, treffen "
        "{e} von {n}.",
    "Map shows": "Die Karte zeigt",
    "What changed, {b} to {a}": "Was sich änderte, {b} bis {a}",
    "Pass by pass, {f} to {l}": "Überflug für Überflug, {f} bis {l}",
    "Drag the slider on the map, or press play, to step through NISAR's passes; the view stays where you "
    "put it. Same orbit and radar mode on every date. Red is HH, green HV, blue HH/HV: water is dark, "
    "forest green, buildings bright. Blue overlay: open water mapped on that date. NISAR used a different "
    "mode on this orbit from 27 August to 2 October, so those passes are not shown. Click the map to check "
    "any other point.":
        "Ziehen Sie den Regler auf der Karte oder drücken Sie Abspielen, um die NISAR-Überflüge durchzugehen; der "
        "Kartenausschnitt bleibt, wo Sie ihn hingelegt haben. An jedem Datum dieselbe Umlaufbahn und derselbe "
        "Radarmodus. Rot ist HH, Grün HV, Blau HH/HV: Wasser ist dunkel, Wald grün, Gebäude hell. Blaue Ebene: an "
        "diesem Datum kartiertes offenes Wasser. Vom 27. August bis 2. Oktober nutzte NISAR auf dieser Umlaufbahn "
        "einen anderen Modus, daher fehlen diese Überflüge. Klicken Sie auf die Karte, um einen anderen Punkt zu "
        "prüfen.",
    "Play": "Abspielen",
    "Open water": "Offenes Wasser",
    "What is nearby (CSV)": "Was in der Nähe liegt (CSV)",
    "Road nearby": "Straße in der Nähe",
    "Settlement nearby": "Siedlung in der Nähe",
    "Nearest mapped road within {km} km of the zone's edge (OpenStreetMap)":
        "Nächste kartierte Straße im Umkreis von {km} km um den Rand der Zone (OpenStreetMap)",
    "Nearest village, town or suburb within {km} km of the zone's edge (OpenStreetMap)":
        "Nächstes Dorf, nächste Stadt oder nächster Vorort im Umkreis von {km} km um den Rand der Zone (OpenStreetMap)",
    "**What is nearby.** {r} of {t} zones lie within {rk} km of a mapped road, {w} of a railway line, and {p} "
    "within {pk} km of a village, town or suburb. Near does not mean at risk: it shows who should look at which lead.":
        "**Was in der Nähe liegt.** {r} von {t} Zonen liegen höchstens {rk} km von einer kartierten Straße entfernt, "
        "{w} von einer Bahnstrecke und {p} höchstens {pk} km von einem Dorf, einer Stadt oder einem Vorort. Nähe "
        "bedeutet nicht Gefährdung: Sie zeigt, wer welchen Hinweis prüfen sollte.",
    "Roads, railway lines and settlements © OpenStreetMap contributors (expressways down to tertiary roads; "
    "smaller roads, tracks and hamlets are not counted).":
        "Straßen, Bahnstrecken und Siedlungen © OpenStreetMap-Mitwirkende (Autobahnen bis Straßen dritter Ordnung; "
        "kleinere Straßen, Wege und Weiler werden nicht gezählt).",
    "Found again by the second NISAR orbit, kept with NASADEM, or a reported event within 2 km.":
        "Vom zweiten NISAR-Orbit erneut gefunden, mit NASADEM bestätigt oder ein gemeldetes Ereignis im Umkreis von 2 km.",
    "e.g. Mulshi": "z. B. Mulshi",
    "Every likely slide zone NISAR found between {b} and {a}, ranked, with the radar images of the spot, why it was "
    "flagged and which independent checks it passed. For district teams: print it, open it in Google Earth or on a "
    "phone, and record what you find. These are leads to check, not confirmed landslides.":
        "Jede wahrscheinliche Rutschungszone, die NISAR zwischen {b} und {a} fand, gereiht, mit Radarbildern der Stelle, "
        "dem Grund der Markierung und den bestandenen unabhängigen Prüfungen. Für Einsatzteams: ausdrucken, in Google "
        "Earth oder auf dem Handy öffnen und vor Ort festhalten, was Sie finden. Es sind Hinweise zum Prüfen, keine "
        "bestätigten Erdrutsche.",
    "Zone": "Zone",
    "Nearest place": "Nächster Ort",
    "Nearest place names © OpenStreetMap contributors (Nominatim). Score: steepness, radar change and coherence loss, "
    "each up to a third.":
        "Ortsnamen © OpenStreetMap-Mitwirkende (Nominatim). Punktzahl: Steilheit, Radaränderung und Kohärenzverlust, "
        "je bis zu einem Drittel.",
    "kept": "bestätigt",
    "not kept": "nicht bestätigt",
    "Score": "Punktzahl",
    "2nd orbit": "2. Orbit",
    "Nearest report": "Nächste Meldung",
    "Slope (°)": "Neigung (°)",
    "Map": "Karte",
    "Evidence for": "Belege für",
    "This list comes from one pair of NISAR passes. NISAR returns every 12 days: the last pass in our data is "
    "<b>{l}</b>, and if it keeps its repeat the next is <b>{n}</b>. The same code rebuilds the list from each new pass.":
        "Diese Liste stammt aus einem Paar von NISAR-Überflügen. NISAR kommt alle 12 Tage wieder: Der letzte Überflug "
        "in unseren Daten ist der <b>{l}</b>, und bleibt es beim Zyklus, folgt der nächste am <b>{n}</b>. Derselbe "
        "Code erstellt die Liste aus jedem neuen Überflug neu.",
    "High": "Hoch", "Medium": "Mittel", "Low": "Niedrig",
    "NISAR track 106, 3 to 15 July": "NISAR-Spur 106, 3. bis 15. Juli",
    "Slide rule re-run with NASA's NASADEM elevation map": "Rutschungsregel erneut mit NASAs Höhenmodell NASADEM",
    "Distance to the nearest reported flood or landslide":
        "Entfernung zur nächsten gemeldeten Überschwemmung oder zum nächsten gemeldeten Erdrutsch",
    "Open": "Öffnen",
    "found again": "erneut gefunden", "partly": "teilweise", "not seen": "nicht gesehen", "outside view": "außer Sicht",
    # place
    "Village, town or suburb": "Dorf, Stadt oder Stadtteil",
    "Type a name, for example Lonavala": "Namen eingeben, zum Beispiel Lonavala",
    "Distance": "Entfernung",
    "the point you picked": "der gewählte Punkt",
    "Click the map to check any other point.": "Klicken Sie in die Karte, um einen anderen Punkt zu prüfen.",
    "Pick a village or town, or click anywhere on the map, to see what NISAR radar found around it between {b} and "
    "{a}: likely slide zones, flood water, rising reservoirs, and the events people reported.":
        "Wählen Sie ein Dorf oder eine Stadt oder klicken Sie irgendwo in die Karte, um zu sehen, was das NISAR-Radar "
        "zwischen {b} und {a} in der Umgebung gefunden hat: wahrscheinliche Rutschungszonen, Hochwasser, steigende "
        "Stauseen und die Ereignisse, die Menschen gemeldet haben.",
    "Choose one of {n} villages, towns and suburbs in the study area (names from OpenStreetMap), or click the map. The "
    "result has its own link, so you can send it to someone.":
        "Wählen Sie einen von {n} Orten im Untersuchungsgebiet (Namen aus OpenStreetMap) oder klicken Sie in die "
        "Karte. Das Ergebnis hat einen eigenen Link, den Sie weitergeben können.",
    "city": "Großstadt", "town": "Stadt", "suburb": "Stadtteil", "village": "Dorf",
    "This point is outside the area we processed NISAR data for. Pick a place inside the dashed box.":
        "Dieser Punkt liegt außerhalb des Gebiets, für das wir NISAR-Daten ausgewertet haben. Wählen Sie einen Ort "
        "innerhalb des gestrichelten Rahmens.",
    "Copy the address bar to share this result.": "Kopieren Sie die Adresszeile, um dieses Ergebnis zu teilen.",
    "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>. If it keeps its 12-day "
    "repeat, the next is <b>{n}</b>, and this page can be rebuilt from it.":
        "NISAR überfliegt Pune alle 12 Tage, mit oder ohne Wolken. Letzter Überflug in unseren Daten: <b>{l}</b>. "
        "Bleibt es beim 12-Tage-Zyklus, folgt der nächste am <b>{n}</b>, und diese Seite lässt sich daraus neu erstellen.",
    "Start with a place": "Mit einem Ort beginnen",
    "flood patches still standing on {a}": "Überschwemmungsflächen, die am {a} noch standen",
    "of new water as reservoirs and rivers rose": "neues Wasser durch steigende Stauseen und Flüsse",
    "reported floods or landslides": "gemeldete Überschwemmungen oder Erdrutsche",
    "NISAR found no slide zone or flood water here. That is not an all-clear: radar misses water between buildings, "
    "slides narrower than 40 m, and anything that came and went between passes.":
        "NISAR hat hier keine Rutschungszone und kein Hochwasser gefunden. Das ist keine Entwarnung: Das Radar übersieht "
        "Wasser zwischen Gebäuden, Rutschungen schmaler als 40 m und alles, was zwischen zwei Überflügen kam und ging.",
    "Likely slide zones": "Wahrscheinliche Rutschungszonen",
    "{n} more zones": "{n} weitere Zonen",
    "What people reported": "Was Menschen gemeldet haben",
    "likely slide zones": "wahrscheinliche Rutschungszonen",
    "Nearest likely slide zone: {id}, {k} km away.": "Nächste wahrscheinliche Rutschungszone: {id}, {k} km entfernt.",
    "radar found something within range": "Radar fand etwas in Reichweite",
    "radar missed it": "Radar hat es nicht erfasst",
    "radar could not observe it": "Radar konnte es nicht beobachten",
    "not scored": "nicht gewertet",
    "Within {k} km of": "Im Umkreis von {k} km um",
    ", {h} high confidence": ", davon {h} mit hoher Sicherheit",
    "{k} km away": "{k} km entfernt",
    # radar explainer
    "Calm water looks dark": "Ruhiges Wasser wirkt dunkel",
    "A smooth surface reflects the radar away, like a mirror.":
        "Eine glatte Fläche spiegelt das Radar weg, wie ein Spiegel.",
    "Rough ground looks bright": "Rauer Boden wirkt hell",
    "Trees, rock and debris scatter some radar back.": "Bäume, Fels und Geröll streuen Radar zurück.",
    "Water by walls: very bright": "Wasser an Wänden: sehr hell",
    "Water and a wall or trunk bounce it straight back.": "Wasser und Wand oder Stamm werfen es direkt zurück.",
    "Coherence: did it stay put?": "Kohärenz: alles beim Alten?",
    "Two passes 12 days apart: a slide scrambles the pattern.":
        "Zwei Überflüge im Abstand von 12 Tagen: Eine Rutschung verwirbelt das Muster.",
    "How NISAR's L-band radar sees water, rough ground, double bounce and coherence":
        "Wie NISARs L-Band-Radar Wasser, rauen Boden, Doppelreflexion und Kohärenz sieht",
    # sidebar, hero
    "Light or dark: ⋮ menu (top right) › Settings.": "Hell oder dunkel: Menü ⋮ (oben rechts) › Settings.",
    "Built by team iGenfinity for NASA Space Apps 2026": "Gebaut von Team iGenfinity für NASA Space Apps 2026",
    "What NASA-ISRO NISAR radar saw through the 2026 Pune monsoon":
        "Was das Radar von NASA und ISRO (NISAR) im Monsun 2026 über Pune sah",
    "NASA-ISRO NISAR · L-band radar · Pune, India": "NASA-ISRO NISAR · L-Band-Radar · Pune, Indien",
    "Optical satellites, 3 to 8 July: only cloud": "Optische Satelliten, 3. bis 8. Juli: nur Wolken",
    "NISAR radar, {d}: sees the ground, new water in blue": "NISAR-Radar, {d}: sieht den Boden, neues Wasser in Blau",
    "Cloud drawn as an illustration. Radar: real NISAR L-band image.":
        "Wolken als Illustration gezeichnet. Radar: echtes NISAR-L-Band-Bild.",
    "Pause animation": "Animation anhalten", "Play animation": "Animation abspielen",
    "Animation: the NISAR satellite passes over Pune and its radar sees through the monsoon cloud to the flood water "
    "and slide zones below.":
        "Animation: Der Satellit NISAR überfliegt Pune, und sein Radar blickt durch die Monsunwolken auf Hochwasser und "
        "Rutschungszonen darunter.",
    "Next expected NISAR pass over Pune: {d}": "Nächster NISAR-Überflug über Pune, erwartet: {d}",
    "Explore the map": "Karte erkunden",
    "GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84. File descriptions are in English.":
        "GeoTIFFs liegen im Analyseraster (UTM-Zone 43N, 40 m), GeoJSON in WGS84. Die Dateibeschreibungen sind auf "
        "Englisch.",
    "Place": "Ort", "Event": "Ereignis", "Date": "Datum", "Result": "Ergebnis", "Why (in English)": "Grund (Englisch)",
    "Everything NISAR found around Pune on one map: flood water, rising reservoirs, likely slide zones, and the events "
    "people reported. Pick a zone or a flood patch below to see its radar evidence.":
        "Alles, was NISAR rund um Pune gefunden hat, auf einer Karte: Hochwasser, steigende Stauseen, wahrscheinliche "
        "Rutschungszonen und die gemeldeten Ereignisse. Wählen Sie unten eine Zone oder Überschwemmungsfläche, um ihre "
        "Radarbelege zu sehen.",
    "All findings on one map": "Alle Ergebnisse auf einer Karte",
    "Next expected NISAR pass over Pune": "Nächster erwarteter NISAR-Überflug über Pune",
    "tomorrow": "morgen", "in {n} days": "in {n} Tagen",
    "Every 12 days, cloud or not.": "Alle 12 Tage, mit oder ohne Wolken.",
    "The Rain": "Der Regen", "Cloud": "Wolken", "Before and After": "Vorher, nachher", "What Changed": "Was sich änderte",
    "The Weeks After": "Die Wochen danach", "Limits": "Grenzen",
    "Rain measured from space: NASA GPM IMERG, daily": "Regen, aus dem All gemessen: NASA GPM IMERG, täglich",
    "What optical satellites saw: NASA Worldview": "Was optische Satelliten sahen: NASA Worldview",
    "NISAR L-band radar, HH, track {t}": "NISAR-L-Band-Radar, HH, Spur {t}",
    "NISAR findings, {b} to {a}": "NISAR-Ergebnisse, {b} bis {a}",
    "NISAR, every pass of track {t} in the same radar mode": "NISAR, jeder Überflug auf Spur {t} im selben Radarmodus",
    "Reported events checked against the radar": "Gemeldete Ereignisse, mit dem Radar abgeglichen",
    "Tip: the ← and → keys move between chapters.": "Tipp: Mit den Tasten ← und → wechseln Sie die Kapitel.",
    "Everything on one map": "Alles auf einer Karte",
    "Every layer, the season slider and the radar evidence for each zone and flood patch.":
        "Alle Ebenen, der Jahreszeit-Regler und die Radarbelege für jede Zone und Überschwemmungsfläche.",
    # overview, 3 steps, limits
    "A satellite passes": "Ein Satellit fliegt vorbei",
    "NISAR flies over Pune every 12 days, day or night.": "NISAR überfliegt Pune alle 12 Tage, bei Tag und Nacht.",
    "Radar sees through cloud": "Radar sieht durch Wolken",
    "Its radar passes through cloud and rain. Calm water looks dark.":
        "Sein Radar dringt durch Wolken und Regen. Ruhiges Wasser wirkt dunkel.",
    "We map the change": "Wir kartieren die Änderung",
    "We compare passes before and after the storm and map what changed.":
        "Wir vergleichen Überflüge vor und nach dem Sturm und kartieren, was sich änderte.",
    "How it works": "So funktioniert es",
    "See it in 3D": "In 3D ansehen",
    "A one-minute tour of what NISAR found, on a model of the land.":
        "Eine einminütige Tour durch NISARs Ergebnisse, auf einem Modell der Landschaft.",
    "likely slide zones on steep slopes, {h} of them high confidence":
        "wahrscheinliche Rutschungszonen an steilen Hängen, {h} davon mit hoher Sicherheit",
    "Leads to check: {u} have no reported event within 2 km.":
        "Hinweise zum Prüfen: Bei {u} gibt es im Umkreis von 2 km keine Meldung.",
    "Could be {a} to {b} km², depending on the water threshold.": "Je nach Wasserschwelle {a} bis {b} km².",
    "Could be {a} to {b} km²: very sensitive to the water threshold.":
        "Könnten {a} bis {b} km² sein: stark abhängig von der Wasserschwelle.",
    "{n} NISAR passes, same orbit.": "{n} NISAR-Überflüge, gleicher Orbit.",
    "See what NISAR found near your village or town.": "Sehen Sie, was NISAR nahe Ihrem Dorf oder Ihrer Stadt fand.",
    "A ranked list of slide zones to check, with radar images, for print and phones.":
        "Eine gereihte Liste zu prüfender Rutschungszonen mit Radarbildern, zum Drucken und fürs Handy.",
    "Every number traced to its NISAR file, with the checks and the data.":
        "Jede Zahl bis zu ihrer NISAR-Datei zurückverfolgt, mit Prüfungen und Daten.",
    "Water between buildings": "Wasser zwischen Gebäuden",
    "Radar bounces off walls, so city flooding is under-counted.":
        "Radar prallt von Wänden ab, daher wird Hochwasser in der Stadt unterschätzt.",
    "Between passes": "Zwischen den Überflügen",
    "Water that came and went between {b} and {a} is not seen.":
        "Wasser, das zwischen {b} und {a} kam und ging, bleibt unsichtbar.",
    "Small slides": "Kleine Rutschungen",
    "Slides narrower than about {r} m can slip through.": "Rutschungen schmaler als etwa {r} m können fehlen.",
    "Hidden slopes": "Verdeckte Hänge",
    "{p}% of steep ground faces away from the radar and is left out.":
        "{p} % des steilen Geländes sind vom Radar abgewandt und fehlen.",
    "Early data": "Frühe Daten",
    "These NISAR products are provisional; the numbers may shift.":
        "Diese NISAR-Produkte sind vorläufig; die Zahlen können sich ändern.",
    # explore, place, field
    "For each zone's radar evidence and the tables, switch to the flat map above.":
        "Für die Radarbelege jeder Zone und die Tabellen oben zur flachen Karte wechseln.",
    "Layers: button at the top right of the map. Click a marker, or pick a row below, for details.":
        "Ebenen: Schaltfläche oben rechts auf der Karte. Für Details eine Markierung anklicken oder unten eine Zeile wählen.",
    "{n} likely slide zones, highest score first. Select a row to zoom to it and see its radar evidence.":
        "{n} wahrscheinliche Rutschungszonen, höchste Punktzahl zuerst. Eine Zeile wählen, um dorthin zu zoomen und die "
        "Radarbelege zu sehen.",
    "{n} flood patches: water on {a} where none was recorded from 1984 to 2021. Select one to see its radar before and "
    "after.":
        "{n} Überschwemmungsflächen: Wasser am {a}, wo von 1984 bis 2021 nie Wasser verzeichnet wurde. Eine wählen, um "
        "das Radar vorher und nachher zu sehen.",
    "Flat map: what changed, {b} to {a}": "Flache Karte: was sich änderte, {b} bis {a}",
    "Drag to turn the model; point at a pin for details.":
        "Ziehen, um das Modell zu drehen; für Details auf eine Nadel zeigen.",
    "Every likely slide zone from {b} to {a}, ranked, with its radar images. Print it or open it on a phone, then go and "
    "check: these are leads, not confirmed landslides.":
        "Jede wahrscheinliche Rutschungszone vom {b} bis {a}, gereiht, mit Radarbildern. Drucken oder aufs Handy laden und "
        "vor Ort prüfen: Es sind Hinweise, keine bestätigten Erdrutsche.",
    "Pick your village or town, or click the map, to see what NISAR found nearby between {b} and {a}.":
        "Wählen Sie Ihr Dorf oder Ihre Stadt oder klicken Sie in die Karte, um zu sehen, was NISAR zwischen {b} und {a} "
        "in der Nähe fand.",
    # 3D view
    "Relief": "Relief", "Radar": "Radar", "Flooding": "Hochwasser", "Reported": "Gemeldet", "Names": "Namen",
    "Next": "Weiter", "Back": "Zurück", "Take the tour": "Tour starten", "Play": "Abspielen", "Pause": "Pause",
    "Water before the storm": "Wasser vor dem Sturm", "New water by {a}": "Neues Wasser bis {a}",
    "Flooding on dry land": "Hochwasser auf trockenem Land", "Likely slide zone": "Wahrscheinliche Rutschungszone",
    "Reported flood or landslide": "Gemeldete Überschwemmung oder Erdrutsch",
    "Heights ×2. Elevation: Copernicus GLO-30. Radar: NISAR.": "Höhen ×2. Höhenmodell: Copernicus GLO-30. Radar: NISAR.",
    "Pune district, India": "Distrikt Pune, Indien",
    "slope": "Neigung", "score": "Punktzahl", "high confidence": "hohe Sicherheit",
    "medium confidence": "mittlere Sicherheit", "low confidence": "niedrige Sicherheit", "near": "nahe",
    "Flood patch": "Überschwemmungsfläche", "ha of water": "ha Wasser", "landslide": "Erdrutsch", "flood": "Überschwemmung",
    "The 3D view needs WebGL, which this browser has turned off. The flat map below shows the same findings.":
        "Die 3D-Ansicht braucht WebGL, das in diesem Browser ausgeschaltet ist. Die flache Karte zeigt dieselben Ergebnisse.",
    "Point north": "Nach Norden ausrichten",
    "3D model of the study area with NISAR's findings": "3D-Modell des Untersuchungsgebiets mit NISARs Ergebnissen",
    "Where this is": "Wo das ist",
    "Pune district, Maharashtra, India: an 85 km box from the Western Ghats hills (left) to Pune city (right). Heights "
    "are doubled so the hills stand out.":
        "Distrikt Pune, Maharashtra, Indien: ein 85 km großes Gebiet von den Hügeln der Westghats (links) bis zur Stadt "
        "Pune (rechts). Die Höhen sind verdoppelt, damit die Hügel gut zu sehen sind.",
    "The Western Ghats": "Die Westghats",
    "Steep, forested hills where the monsoon rain falls hardest. In early July the whole area averaged up to {r} mm of "
    "rain in a day, and slopes gave way.":
        "Steile, bewaldete Hügel, wo der Monsunregen am stärksten fällt. Anfang Juli fielen im Mittel über das ganze "
        "Gebiet bis zu {r} mm Regen an einem Tag, und Hänge gaben nach.",
    "Your turn": "Jetzt Sie",
    "Drag to turn the model, scroll or pinch to zoom, and point at a pin for details.":
        "Ziehen, um das Modell zu drehen, scrollen oder mit zwei Fingern zoomen, und für Details auf eine Nadel zeigen.",
    "Reservoirs filled up": "Die Stauseen füllten sich",
    "Blue edges are new water: between {b} and {a}, Pune's reservoirs and rivers grew by {k} km².":
        "Blaue Ränder sind neues Wasser: Zwischen {b} und {a} wuchsen Punes Stauseen und Flüsse um {k} km².",
    "Orange pins: {n} places on steep slopes where the ground changed between passes. Tall pins are the {h} "
    "high-confidence ones. Leads to check, not confirmed landslides.":
        "Orange Nadeln: {n} Stellen an steilen Hängen, an denen sich der Boden zwischen den Überflügen veränderte. Die "
        "hohen Nadeln sind die {h} mit hoher Sicherheit. Hinweise zum Prüfen, keine bestätigten Erdrutsche.",
    "Flooded land": "Überflutetes Land",
    "Dark-blue pins: water still standing on {a} where no water was recorded from 1984 to 2021, {k} km² in all.":
        "Dunkelblaue Nadeln: Wasser, das am {a} noch stand, wo von 1984 bis 2021 nie Wasser verzeichnet wurde, insgesamt "
        "{k} km².",
    "Pune city": "Stadt Pune",
    "White pins are floods and landslides people reported. Radar sees water between buildings poorly, so many city "
    "reports were missed. Overall, {h} of {o} reported floods it could observe had a detection nearby.":
        "Weiße Nadeln sind gemeldete Überschwemmungen und Erdrutsche. Wasser zwischen Gebäuden sieht das Radar schlecht, "
        "daher wurden viele Meldungen aus der Stadt nicht erfasst. Insgesamt hatten {h} von {o} sichtbaren gemeldeten "
        "Überschwemmungen einen Fund in der Nähe.",
    "that radar could see had a detection nearby. Landslides: {h} of {o}":
        "die das Radar sehen konnte, hatten einen Fund in der Nähe. Erdrutsche: {h} von {o}",
    ", weak support.": ", schwache Stütze.",
    "slide zones found again, {l}× more than chance{p}.": "Rutschungszonen erneut gefunden, {l}× häufiger als per Zufall{p}.",
    "slide zones kept with NASA's NASADEM elevation map.": "Rutschungszonen bestätigt mit NASAs Höhenmodell NASADEM.",
    "Reservoir rise: {a} to {b} km². Flooding: {c} to {d} km².": "Anstieg der Stauseen: {a} bis {b} km². Hochwasser: {c} bis {d} km².",
    "White pins are floods and landslides people reported. Radar sees water between buildings poorly, so the city "
    "reports were mostly missed: {h} of {o} reported floods had something nearby, no better than chance.":
        "Weiße Nadeln sind gemeldete Überschwemmungen und Erdrutsche. Wasser zwischen Gebäuden sieht das Radar schlecht, "
        "daher wurden die Meldungen aus der Stadt meist nicht erfasst: Bei {h} von {o} gemeldeten Überschwemmungen gab es "
        "etwas in der Nähe, nicht mehr als per Zufall.",
    "No better than chance: places nobody reported match {e} of {n}.":
        "Nicht besser als Zufall: Orte ohne Meldung kommen auf {e} von {n}.",
    "HV change (dB)": "HV-Änderung (dB)", "HH change (dB)": "HH-Änderung (dB)",
    "Coherence": "Kohärenz", "Coherence vs 1 km": "Kohärenz ggü. 1 km",
    "Place names: © OpenStreetMap contributors (Nominatim). Zones are leads to check, not confirmed landslides.":
        "Ortsnamen: © OpenStreetMap-Mitwirkende (Nominatim). Die Zonen sind Hinweise zum Prüfen, keine bestätigten "
        "Erdrutsche.",
    "Dark water on each date, counted inside the area where the JRC record has seen water at least once (1984 to "
    "2021), so rain-soaked fields are left out. Every point is the same orbit and radar mode; NISAR used a different "
    "mode on this orbit from 27 August to 2 October, so those passes are not shown.":
        "Dunkles Wasser an jedem Datum, gezählt innerhalb der Fläche, auf der der JRC-Datensatz mindestens einmal Wasser "
        "sah (1984 bis 2021); regengetränkte Felder fallen so heraus. Jeder Punkt stammt aus demselben Orbit und "
        "Radarmodus; vom 27. August bis 2. Oktober nutzte NISAR auf diesem Orbit einen anderen Modus, diese Überflüge "
        "fehlen daher.",
    "floods and landslides reported": "gemeldete Überschwemmungen und Erdrutsche",
    "radar pass 1": "Radar-Überflug 1", "radar pass 2": "Radar-Überflug 2", "mm per day": "mm pro Tag",
    "water surface, km²": "Wasserfläche, km²",
    "Field check list for district teams, with radar images": "Feld-Checkliste mit Radarbildern für Einsatzteams",
    "Technical page in English. The numbers and the story are in German on the other pages.":
        "Technische Seite auf Englisch. Zahlen und Geschichte gibt es auf den anderen Seiten auf Deutsch.",
    "Rainfall chart appears here once `data/reference/rainfall.csv` is added.":
        "Das Regendiagramm erscheint, sobald `data/reference/rainfall.csv` vorhanden ist.",
    "NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain.":
        "NISARs L-Band-Radar (Wellenlänge etwa 24 cm) arbeitet Tag und Nacht, durch Wolken und Regen.",
    "Surface area of Pune's rivers and reservoirs on each NISAR pass of this orbit":
        "Wasserfläche von Punes Flüssen und Stauseen bei jedem NISAR-Überflug dieses Orbits",
    "Score adds three pieces of evidence": "Die Punktzahl vereint drei Belege",
    # check band
    "slide zones kept when the rule is re-run on NASA's NASADEM{h}.":
        "Rutschungszonen, die bleiben, wenn die Regel mit NASAs NASADEM wiederholt wird{h}.",
    ", including {a} of {b} high-confidence ones": ", darunter {a} von {b} mit hoher Sicherheit",
    "better than chance: {c} of the {n} zones it covers were found again{e}{p}.":
        "besser als Zufall: {c} der {n} Zonen in seinem Blickfeld wurden wiedergefunden{e}{p}.",
    ", chance gives {x}": ", der Zufall ergibt {x}",
    "Reported landslides": "Gemeldete Erdrutsche",
    "radar could see had a slide zone nearby": "die das Radar sehen konnte, hatten eine Rutschungszone in der Nähe",
    "both near one zone, {z}": "beide nahe einer Zone, {z}", "none with NASADEM": "mit NASADEM keine",
    "{n} with NASADEM": "mit NASADEM {n}",
    "No better than chance ({e} of {n}): flooding between buildings hides from radar.":
        "Nicht besser als Zufall ({e} von {n}): Hochwasser zwischen Gebäuden bleibt dem Radar verborgen.",
    "that radar could see had a detection nearby.": "die das Radar sehen konnte, hatten einen Fund in der Nähe.",
    "Try one of these": "Probieren Sie eines davon",
    # app tour
    "A one-minute flight over what NISAR found, on a model of the land.":
        "Ein einminütiger Flug über das, was NISAR fand, auf einem Modell der Landschaft.",
    "Everything NISAR found around Pune: fly over it in 3D, or open the flat map for each zone's radar evidence.":
        "Alles, was NISAR rund um Pune fand: in 3D darüberfliegen oder die flache Karte mit den Radarbelegen jeder "
        "Zone öffnen.",
    "3D view": "3D-Ansicht", "Other formats": "Weitere Formate", "Fly over the findings": "Über die Ergebnisse fliegen",
    "A one-minute guide to every page": "Eine einminütige Anleitung zu jeder Seite",
    "Finish": "Fertig", "Close the tour": "Tour schließen", "{i} of {n}": "{i} von {n}",
    "Welcome to MonsoonLens": "Willkommen bei MonsoonLens",
    "In July 2026 cloud hid Pune from ordinary satellites. This app shows what NISAR's radar saw through it: new water, "
    "flooding and likely landslide zones.":
        "Im Juli 2026 verbargen Wolken Pune vor gewöhnlichen Satelliten. Diese App zeigt, was NISARs Radar durch sie "
        "hindurch sah: neues Wasser, Überschwemmungen und wahrscheinliche Erdrutschzonen.",
    "Six pages": "Sechs Seiten",
    "Move between pages here. On a phone, open this menu with the arrow at the top left.":
        "Hier wechseln Sie die Seiten. Auf dem Handy öffnen Sie dieses Menü mit dem Pfeil oben links.",
    "Your language": "Ihre Sprache",
    "Read everything in English, Hindi, Marathi or German.": "Alles auf Englisch, Hindi, Marathi oder Deutsch lesen.",
    "Drag to turn the land. Press “Fly over the findings” for a one-minute flight to each one.":
        "Ziehen, um die Landschaft zu drehen. „Über die Ergebnisse fliegen“ startet einen einminütigen Flug zu jedem Fund.",
    "The headline numbers": "Die wichtigsten Zahlen",
    "What the radar found. Each card says how sure we are.": "Was das Radar fand. Jede Karte sagt, wie sicher wir sind.",
    "Every result is tested, and we show the tests that came out weak too.":
        "Jedes Ergebnis wird geprüft, und wir zeigen auch die Prüfungen, die schwach ausfielen.",
    "The story": "Die Geschichte",
    "Six short chapters, from the rain to what radar could not see. Click a stop, or use the ← and → keys.":
        "Sechs kurze Kapitel, vom Regen bis zu dem, was das Radar nicht sehen konnte. Klicken Sie auf eine Station oder "
        "nutzen Sie die Tasten ← und →.",
    "Choose the 3D view, the flat map with radar evidence for each zone, or water through the season.":
        "Wählen Sie die 3D-Ansicht, die flache Karte mit Radarbelegen für jede Zone oder das Wasser im Lauf der Saison.",
    "Type your village or town to see what was found within 2, 5 or 10 km. Share the page link with others.":
        "Geben Sie Ihr Dorf oder Ihre Stadt ein, um zu sehen, was im Umkreis von 2, 5 oder 10 km gefunden wurde. Den "
        "Link der Seite können Sie teilen.",
    "For district teams": "Für Distriktteams",
    "Print the ranked list with radar images, or open it on a phone in Google Earth (KML), and go and check.":
        "Drucken Sie die gereihte Liste mit Radarbildern oder öffnen Sie sie auf dem Handy in Google Earth (KML), und "
        "prüfen Sie vor Ort.",
    "How every number was made": "Wie jede Zahl entstand",
    "The NISAR files, each step of the method, every check and the limits, for researchers and journalists.":
        "Die NISAR-Dateien, jeder Schritt der Methode, jede Prüfung und die Grenzen, für Forschende und Journalisten.",
    "You are ready": "Los geht’s",
    "Start with the story, or check your own village. You can take this tour again from the menu.":
        "Beginnen Sie mit der Geschichte oder prüfen Sie Ihr eigenes Dorf. Diese Tour können Sie im Menü jederzeit "
        "wiederholen.",
    # method page, maps, downloads, credits
    "Radar could see it": "Das Radar konnte es sehen",
    "Every number in this app comes from the pipeline in our public repository, run on the NISAR files listed below. Nothing is estimated by hand, and every check is reported, including the ones that came out weak.":
        "Jede Zahl in dieser App stammt aus der Pipeline in unserem öffentlichen Repository, angewandt auf die unten aufgeführten NISAR-Dateien. Nichts ist von Hand geschätzt, und jede Prüfung wird berichtet, auch die schwach ausgefallenen.",
    "Mission facts: [ISRO, NISAR launch page](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) and [eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). Tracks and times: the NISAR file names in the Data table.":
        "Missionsdaten: [ISRO, NISAR-Startseite](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) und [eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). Bahnen und Zeiten: die NISAR-Dateinamen in der Datentabelle.",
    "How radar sees through cloud":
        "Wie Radar durch Wolken sieht",
    "NISAR's L-band radar has a wavelength of about 24 cm: it passes through cloud and rain, and partly through forest canopy. It sends two polarisations: HH (horizontal out, horizontal back) responds to surfaces and structures, HV (horizontal out, vertical back) mostly to vegetation.":
        "NISARs L-Band-Radar hat eine Wellenlänge von etwa 24 cm: Es durchdringt Wolken und Regen und teilweise auch das Kronendach. Es sendet zwei Polarisationen: HH (horizontal hin, horizontal zurück) reagiert auf Oberflächen und Bauten, HV (horizontal hin, vertikal zurück) vor allem auf Vegetation.",
    "yes":
        "ja",
    "no":
        "nein",
    "before, track 034":
        "vorher, Bahn 034",
    "after, track 034":
        "nachher, Bahn 034",
    "coherence, track 034":
        "Kohärenz, Bahn 034",
    "second-track check, before, track 106":
        "Prüfung mit zweiter Bahn, vorher, Bahn 106",
    "second-track check, after, track 106":
        "Prüfung mit zweiter Bahn, nachher, Bahn 106",
    "second-track check, coherence, track 106":
        "Prüfung mit zweiter Bahn, Kohärenz, Bahn 106",
    "Data":
        "Daten",
    "File":
        "Datei",
    "Valid share of box":
        "Gültiger Anteil des Gebiets",
    "Link":
        "Link",
    "File names and data sources are kept as published, in English.":
        "Dateinamen und Datenquellen bleiben wie veröffentlicht auf Englisch.",
    "The code is public, and the Pune crops of every NISAR file above are in the repository (a few MB each), so one command rebuilds every number, map and list in this app from them. Fetching the crops again from NASA's archive needs a free Earthdata login. The whole pipeline runs in about two minutes on a two-core computer.":
        "Der Code ist öffentlich, und die Pune-Ausschnitte jeder oben genannten NISAR-Datei liegen im Repository (je einige MB). Ein Befehl erzeugt daraus jede Zahl, Karte und Liste dieser App neu. Um die Ausschnitte erneut aus NASAs Archiv zu laden, braucht man ein kostenloses Earthdata-Konto. Die ganze Pipeline läuft auf einem Rechner mit zwei Kernen in etwa zwei Minuten.",
    "To point it at another place, change the study box and the NISAR files in `pipeline/config.py`.":
        "Für einen anderen Ort ändern Sie das Untersuchungsgebiet und die NISAR-Dateien in `pipeline/config.py`.",
    "NISAR in brief":
        "NISAR in Kürze",
    "How radar sees":
        "Wie Radar sieht",
    "Reproduce it":
        "Nachvollziehen",
    "Team":
        "Team",
    " and ":
        " und ",
    "Launched":
        "Start",
    "30 July 2025 on ISRO's GSLV-F16, from Sriharikota, India":
        "30. Juli 2025 mit ISROs GSLV-F16 von Sriharikota, Indien",
    "Orbit":
        "Umlaufbahn",
    "Sun-synchronous, about 747 km up, inclined 98.4°":
        "Sonnensynchron, etwa 747 km hoch, 98,4° geneigt",
    "Repeat":
        "Wiederholung",
    "The same ground track every 12 days":
        "Dieselbe Bodenspur alle 12 Tage",
    "Radars":
        "Radare",
    "L-band (NASA/JPL, 24 cm wavelength) and S-band (ISRO), sharing one 12 m mesh reflector":
        "L-Band (NASA/JPL, 24 cm Wellenlänge) und S-Band (ISRO), mit einem gemeinsamen 12-m-Gitterreflektor",
    "Swath":
        "Streifenbreite",
    "242 km wide on the ground":
        "242 km breit am Boden",
    "What this app uses":
        "Was diese App nutzt",
    "L-band, tracks {t}, southbound evening passes ({u} UTC), level-2 GCOV and GUNW products":
        "L-Band, Bahnen {t}, südwärts gerichtete Abendüberflüge ({u} UTC), Level-2-Produkte GCOV und GUNW",
    "Read the radar":
        "Radar lesen",
    "Find the change":
        "Die Änderung finden",
    "Check it":
        "Prüfen",
    "Hand it over":
        "Übergeben",
    "Water threshold":
        "Wasserschwelle",
    "Results table":
        "Ergebnistabelle",
    "Sanity check: on {d} the radar saw **{p}** of the JRC permanent-water pixels as water. A low value would mean the threshold or the data is off.":
        "Plausibilitätsprüfung: Am {d} sah das Radar **{p}** der JRC-Pixel mit Dauerwasser als Wasser. Ein niedriger Wert würde bedeuten, dass Schwelle oder Daten nicht stimmen.",
    "Permanent water":
        "Dauerhaftes Wasser",
    "Elevation and slope":
        "Höhe und Neigung",
    "Place names":
        "Ortsnamen",
    "Provisional data":
        "Vorläufige Daten",
    "These are NISAR provisional products (released from June 2026); calibration may still change.":
        "Dies sind vorläufige NISAR-Produkte (veröffentlicht ab Juni 2026); die Kalibrierung kann sich noch ändern.",
    "Two snapshots, twelve days apart":
        "Zwei Momentaufnahmen, zwölf Tage auseinander",
    "Anything that flooded and drained between {b} and {a} is invisible.":
        "Was zwischen {b} und {a} überflutet war und wieder ablief, ist unsichtbar.",
    "Cities":
        "Städte",
    "Buildings make flooded streets bright, not dark. Our new-water map under-counts urban flooding.":
        "Gebäude lassen überflutete Straßen hell statt dunkel erscheinen. Unsere Karte des neuen Wassers unterschätzt städtisches Hochwasser.",
    "Pixel size":
        "Pixelgröße",
    "{r} m pixels. Slides narrower than about two pixels are easily missed.":
        "{r}-m-Pixel. Rutschungen schmaler als etwa zwei Pixel werden leicht übersehen.",
    "Same-mode rule":
        "Gleicher-Modus-Regel",
    "From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol); 14 October is back in the July mode. Brightness is only compared between passes with the same track, mode and polarisation.":
        "Vom 27. August bis 2. Oktober nahm NISAR diese Bahn in einem anderen Modus auf (2005, Quad-Pol); am 14. Oktober wieder im Juli-Modus. Helligkeit wird nur zwischen Überflügen mit gleicher Bahn, gleichem Modus und gleicher Polarisation verglichen.",
    "Water areas may be underestimates":
        "Wasserflächen können unterschätzt sein",
    "On {d} only {p} of the area the JRC record marks as permanent water looked dark enough to pass our water test. Part of that is reservoirs drawn down before the monsoon; part is water roughened by wind or rain, which our test misses.":
        "Am {d} sahen nur {p} der Fläche, die die JRC-Aufzeichnung als Dauerwasser führt, dunkel genug aus, um unseren Wassertest zu bestehen. Teils sind Stauseen vor dem Monsun abgesenkt, teils ist das Wasser durch Wind oder Regen aufgeraut, was unser Test übersieht.",
    "Small samples":
        "Kleine Stichproben",
    "Every check is counted, not turned into an accuracy: floods {fh} of {fo}, landslides {sh} of {so}, and the second-track check covers only part of the area.":
        "Jede Prüfung wird gezählt, nicht in eine Genauigkeit umgerechnet: Überschwemmungen {fh} von {fo}, Erdrutsche {sh} von {so}, und die Prüfung mit zweiter Bahn deckt nur einen Teil des Gebiets ab.",
    "Flood area is threshold-sensitive":
        "Hochwasserfläche hängt von der Schwelle ab",
    "The flood figure can move several-fold with a 1 dB change in the water threshold; the reservoir rise much less (see the water-threshold check).":
        "Die Hochwasserzahl kann sich bei 1 dB Änderung der Wasserschwelle vervielfachen; der Anstieg der Stauseen viel weniger (siehe Prüfung der Wasserschwelle).",
    "Slope near the limits":
        "Neigung nahe den Grenzen",
    "Many zones sit close to the {a}° or {b}° limits, so a different elevation map moves some of them in or out (see the elevation-map check).":
        "Viele Zonen liegen nahe den Grenzen von {a}° oder {b}°, daher schiebt ein anderes Höhenmodell einige hinein oder hinaus (siehe Prüfung mit dem Höhenmodell).",
    "Leads, not verdicts":
        "Hinweise, keine Urteile",
    "Slide zones are places to check, not confirmed landslides: {u} of {z} have no reported event within 2 km.":
        "Rutschungszonen sind Orte zum Prüfen, keine bestätigten Erdrutsche: {u} von {z} haben kein gemeldetes Ereignis im Umkreis von 2 km.",
    "Rainfall":
        "Niederschlag",
    "GPM IMERG Late Run, averaged over the whole study area per UTC day. It is lower than the single-station totals quoted in the news, and may shift slightly when the Final Run is released.":
        "GPM IMERG Late Run, gemittelt über das ganze Untersuchungsgebiet je UTC-Tag. Das liegt unter den Einzelstationswerten aus den Nachrichten und kann sich mit dem Final Run leicht ändern.",
    ". Landslides: {h} of {o}.":
        ". Erdrutsche: {h} von {o}.",
    "Floods: **{fh} of {fo}** reports that radar could observe had a detection nearby. Landslides: **{sh} of {so}**. Counts, not an accuracy: the samples are small.":
        "Überschwemmungen: Bei **{fh} von {fo}** Meldungen, die das Radar sehen konnte, gab es einen Fund in der Nähe. Erdrutsche: **{sh} von {so}**. Zählungen, keine Genauigkeit: Die Stichproben sind klein.",
    "Runs once reported events are added.":
        "Läuft, sobald gemeldete Ereignisse vorliegen.",
    "an independent NISAR orbit re-found {c} of the {n} zones it could see, {l}× more often than chance. A small sample, so support, not proof.":
        "ein unabhängiger NISAR-Orbit fand {c} der {n} Zonen in seinem Blickfeld wieder, {l}× häufiger als Zufall. Eine kleine Stichprobe: Unterstützung, kein Beweis.",
    "Same slide rule, run on NISAR track {t} ({b} to {a}). A track-034 zone counts as **found again** when a track-{t} zone lies within {m} m (allowing for small position differences between orbits). **Partial** means only one piece of the evidence is there (coherence loss or the backscatter jump): that alone is common in the monsoon, so we do not count it.":
        "Dieselbe Rutschungsregel, angewandt auf NISAR-Bahn {t} ({b} bis {a}). Eine Zone von Bahn 034 gilt als **wiedergefunden**, wenn eine Zone von Bahn {t} innerhalb von {m} m liegt (für kleine Lageunterschiede zwischen Orbits). **Teilweise** heißt, nur ein Beleg ist da (Kohärenzverlust oder Rückstreusprung): Das allein ist im Monsun häufig, daher zählen wir es nicht.",
    "Runs once the track-106 files are cropped.":
        "Läuft, sobald die Dateien von Bahn 106 zugeschnitten sind.",
    "{f} of {z} zones survive when slope comes from NASA's NASADEM, including {hf} of {hz} high-confidence ones.":
        "{f} von {z} Zonen bleiben, wenn die Neigung aus NASAs NASADEM stammt, darunter {hf} von {hz} mit hoher Sicherheit.",
    "Slope and slope direction decide where the slide rule looks, so we ran it again on the same radar pair with NASA's NASADEM elevation map instead of Copernicus. Overall the two slope maps agree closely (median difference {d}°). Near the {a}° and {b}° limits they do not: of the ground that either map puts inside that band, the other map puts {p} outside it.":
        "Neigung und Hangrichtung bestimmen, wo die Rutschungsregel sucht. Daher haben wir sie für dasselbe Radarpaar mit NASAs NASADEM statt Copernicus wiederholt. Insgesamt stimmen beide Neigungskarten gut überein (Median-Unterschied {d}°). Nahe den Grenzen von {a}° und {b}° nicht: Von dem Gelände, das eine Karte in diesem Bereich sieht, legt die andere {p} außerhalb.",
    "**{f} of {z}** zones are found again within {m} m, including **{hf} of {hz}** high-confidence zones. NASADEM also finds {nw} zones of its own.":
        "**{f} von {z}** Zonen werden innerhalb von {m} m wiedergefunden, darunter **{hf} von {hz}** mit hoher Sicherheit. NASADEM findet außerdem {nw} eigene Zonen.",
    "Steeper than 45°":
        "Steiler als 45°",
    "Gentler than 15°":
        "Flacher als 15°",
    "Radar layover or shadow":
        "Radar-Überlagerung oder -Schatten",
    "Near the edge of the slope band":
        "Nahe am Rand des Neigungsbereichs",
    "the reservoir rise holds up ({a} to {b} km²); the flood area does not ({c} to {d} km²), so read it as an order of magnitude.":
        "der Anstieg der Stauseen hält ({a} bis {b} km²); die Hochwasserfläche nicht ({c} bis {d} km²), daher als Größenordnung lesen.",
    "The water threshold is set from the radar itself on each date. Moving both dates' thresholds 1 dB down or up, and changing nothing else, keeps reservoir and river rise between **{a} and {b} km²** (we report {r}). Flooding on ground that was never wet swings from **{c} to {d} km²** (we report {f}): that figure depends heavily on the threshold, so read it as the order of magnitude, not a precise area.":
        "Die Wasserschwelle wird an jedem Datum aus dem Radar selbst bestimmt. Verschiebt man beide Schwellen um 1 dB nach unten oder oben und ändert sonst nichts, bleibt der Anstieg von Stauseen und Flüssen zwischen **{a} und {b} km²** (wir berichten {r}). Hochwasser auf nie nassem Boden schwankt zwischen **{c} und {d} km²** (wir berichten {f}): Dieser Wert hängt stark von der Schwelle ab, also als Größenordnung lesen, nicht als genaue Fläche.",
    "Roads and railways near each zone":
        "Straßen und Bahnlinien nahe jeder Zone",
    "Elevation, second-map check":
        "Höhe, Prüfung mit zweiter Karte",
    "Daily rainfall":
        "Täglicher Niederschlag",
    "Cut the radar to Pune":
        "Radar auf Pune zuschneiden",
    "NISAR's level-2 GCOV files hold radar brightness (gamma-nought, already corrected for terrain) on a map grid. A full frame is about 5 GB per layer, so we stream only the study box (lon {w} to {e}, lat {s} to {n}) and average 2 × 2 or more native pixels into a {r} m grid. Averaging reduces radar speckle; a Lee filter removes more.":
        "NISARs Level-2-GCOV-Dateien enthalten die Radarhelligkeit (Gamma-Null, bereits geländekorrigiert) auf einem Kartenraster. Ein ganzer Rahmen hat etwa 5 GB pro Ebene, daher streamen wir nur das Untersuchungsgebiet (Länge {w} bis {e}, Breite {s} bis {n}) und mitteln 2 × 2 oder mehr Originalpixel zu einem {r}-m-Raster. Das Mitteln mindert das Radar-Speckle; ein Lee-Filter entfernt weiteres.",
    "Find water on each date":
        "Wasser an jedem Datum finden",
    "Smooth water reflects the radar away and looks dark in HH. The cut-off between water and land is set separately for each date with the minimum-error method of Kittler and Illingworth, trained on reservoir and river cores that the JRC Global Surface Water record says are water at least {o}% of the time, plus an equal number of land pixels. In these NISAR products open water sits near −16 dB and dry land near −5 dB.":
        "Glattes Wasser lenkt das Radar weg und wirkt in HH dunkel. Die Grenze zwischen Wasser und Land wird für jedes Datum getrennt mit der Minimum-Error-Methode von Kittler und Illingworth bestimmt, trainiert an Kernen von Stauseen und Flüssen, die laut JRC Global Surface Water mindestens {o}% der Zeit Wasser sind, plus gleich vielen Landpixeln. In diesen NISAR-Produkten liegt offenes Wasser bei etwa −16 dB und trockenes Land bei etwa −5 dB.",
    "Keep only new water":
        "Nur neues Wasser behalten",
    "A pixel is new water if it is water on {a} but not on {b}, clearly darker, outside permanent water, on flat ground, and part of a patch big enough not to be speckle.":
        "Ein Pixel ist neues Wasser, wenn es am {a} Wasser ist, am {b} aber nicht, deutlich dunkler, außerhalb von Dauerwasser, auf flachem Boden und Teil einer Fläche, die groß genug ist, um kein Speckle zu sein.",
    "Flag possible hidden water":
        "Mögliches verborgenes Wasser markieren",
    "At L-band, water under trees or between buildings makes the radar bounce twice and come back brighter. Flat ground that got brighter is shown as possible water, and never added to flood totals.":
        "Im L-Band lässt Wasser unter Bäumen oder zwischen Gebäuden das Radar zweimal abprallen und heller zurückkommen. Flacher Boden, der heller wurde, wird als mögliches Wasser gezeigt und nie zur Hochwasserfläche addiert.",
    "Find likely slide zones":
        "Wahrscheinliche Rutschungszonen finden",
    "Outside the radar's layover and shadow, a zone needs all three: the ground stopped matching itself between passes (coherence, from the NISAR GUNW product); it lost much more coherence than its own 1 km neighbourhood, because monsoon vegetation lowers coherence everywhere; and the radar brightness jumped, from rough debris (HH up) or stripped vegetation (HV down), measured against the scene's own median change on dry land. Each zone gets a 0 to 1 score from slope, radar change and coherence loss.":
        "Außerhalb von Radar-Überlagerung und -Schatten braucht eine Zone alle drei: Der Boden stimmte zwischen den Überflügen nicht mehr mit sich überein (Kohärenz, aus dem NISAR-GUNW-Produkt); sie verlor deutlich mehr Kohärenz als ihre eigene 1-km-Umgebung, weil Monsunvegetation die Kohärenz überall senkt; und die Radarhelligkeit sprang, durch rauen Schutt (HH hoch) oder entfernte Vegetation (HV runter), gemessen an der Median-Änderung der Szene auf trockenem Land. Jede Zone erhält eine Punktzahl von 0 bis 1 aus Neigung, Radaränderung und Kohärenzverlust.",
    "Check against reports":
        "Mit Meldungen abgleichen",
    "Reported floods and landslides, from the news and official sources, each linked, are matched to detections nearby, or within the report's own location precision if that is larger.":
        "Gemeldete Überschwemmungen und Erdrutsche aus Nachrichten und amtlichen Quellen, jeweils verlinkt, werden mit Funden in der Nähe abgeglichen, oder innerhalb der eigenen Ortsgenauigkeit der Meldung, falls diese größer ist.",
    "Check with a second track":
        "Mit einer zweiten Bahn prüfen",
    "The same slide rule runs on an independent NISAR pair from another orbit, which also spans the rain peak. A real slope failure changes the ground for good, so it should show in both; speckle or a geometry artefact of one orbit usually does not. Chance level comes from moving every zone to random steep, dry places and repeating the test.":
        "Dieselbe Rutschungsregel läuft auf einem unabhängigen NISAR-Paar aus einem anderen Orbit, das ebenfalls den Regenhöhepunkt umfasst. Ein echter Hangrutsch verändert den Boden dauerhaft und sollte in beiden erscheinen; Speckle oder ein Geometriefehler eines Orbits meist nicht. Das Zufallsniveau ergibt sich, indem jede Zone an zufällige steile, trockene Orte verschoben und der Test wiederholt wird.",
    "Check with a second elevation map":
        "Mit einem zweiten Höhenmodell prüfen",
    "Slope and slope direction come from the Copernicus GLO-30 elevation map. We run the same slide rule again with NASA's NASADEM elevation map and record which zones it keeps.":
        "Neigung und Hangrichtung stammen aus dem Copernicus-GLO-30-Höhenmodell. Wir wiederholen dieselbe Rutschungsregel mit NASAs NASADEM und halten fest, welche Zonen bleiben.",
    "Test the water threshold":
        "Die Wasserschwelle testen",
    "Both dates' water thresholds are moved 1 dB down and up and the water numbers are recomputed, to show how much they depend on that one choice.":
        "Die Wasserschwellen beider Daten werden um 1 dB nach unten und oben verschoben und die Wasserzahlen neu berechnet, um zu zeigen, wie stark sie von dieser einen Wahl abhängen.",
    "Package the evidence":
        "Die Belege packen",
    "For every slide zone and flood patch the pipeline cuts small image chips of that spot from the NISAR data (radar colour before and after, and coherence), notes the nearest reported event, and writes the field check list as a printable page, KML, CSV and GeoJSON.":
        "Für jede Rutschungszone und Überschwemmungsfläche schneidet die Pipeline kleine Bildausschnitte dieser Stelle aus den NISAR-Daten (Radarfarbe vorher und nachher sowie Kohärenz), vermerkt das nächste gemeldete Ereignis und schreibt die Feld-Checkliste als druckbare Seite, KML, CSV und GeoJSON.",
    "radar found something near {h} of {o} reported floods it could see":
        "das Radar fand etwas nahe {h} von {o} gemeldeten Überschwemmungen, die es sehen konnte",
    "How the chance level is worked out: a report counts as matched when new water or a possible-water patch lies within its tolerance (the larger of the report's location precision and 500 m). For each report we take the share of a reference set that has a detection within that same tolerance, and add the shares up. Flat ground: every 40 m pixel with radar data on both dates, outside permanent water, slope ≤ 5° ({km} km²). Settlements: {p} OpenStreetMap villages, towns and suburbs with radar data. Getting {k} or more by chance has a probability of {pf} on flat ground and {ps} at settlements (exact, no random draws).":
        "So wird das Zufallsniveau berechnet: Eine Meldung gilt als getroffen, wenn neues Wasser oder eine Fläche möglichen Wassers innerhalb ihrer Toleranz liegt (dem Größeren aus Ortsgenauigkeit der Meldung und 500 m). Für jede Meldung nehmen wir den Anteil einer Referenzmenge mit einem Fund innerhalb derselben Toleranz und addieren die Anteile. Flaches Land: jedes 40-m-Pixel mit Radardaten an beiden Daten, außerhalb von Dauerwasser, Neigung ≤ 5° ({km} km²). Siedlungen: {p} OpenStreetMap-Dörfer, -Städte und -Vororte mit Radardaten. {k} oder mehr Treffer durch Zufall haben eine Wahrscheinlichkeit von {pf} auf flachem Land und {ps} bei Siedlungen (exakt, ohne Zufallsziehungen).",
    "Track {t} sees only {c} of the study area, so only {n} of our zones could be checked. That is a small sample: treat it as support, not proof.":
        "Bahn {t} sieht nur {c} des Untersuchungsgebiets, daher konnten nur {n} unserer Zonen geprüft werden. Das ist eine kleine Stichprobe: Unterstützung, kein Beweis.",
    "Between {b} and {a} the whole scene got about {h} dB darker in HH and {v} dB in HV, on flat and steep ground alike: ground and plants drying after the storm, or calibration of these provisional products. A landslide is a local change, so on both tracks we measure change against the scene's own median change on dry land.":
        "Zwischen {b} und {a} wurde die ganze Szene in HH um etwa {h} dB und in HV um {v} dB dunkler, auf flachem wie steilem Gelände: trocknender Boden und Pflanzen nach dem Sturm oder die Kalibrierung dieser vorläufigen Produkte. Ein Erdrutsch ist eine lokale Änderung, daher messen wir auf beiden Bahnen die Änderung relativ zur Median-Änderung der Szene auf trockenem Land.",
    "Water areas from track {t} are not used: on {b}, in heavy rain, the radar saw less than half of the permanent reservoirs as dark water, because rain roughens the surface.":
        "Wasserflächen von Bahn {t} werden nicht verwendet: Am {b}, bei starkem Regen, sah das Radar weniger als die Hälfte der dauerhaften Stauseen als dunkles Wasser, weil Regen die Oberfläche aufraut.",
    "Passing both extra checks (found again by the second NISAR track and with NASADEM): **{z}**.":
        "Bestehen beide Zusatzprüfungen (von der zweiten NISAR-Bahn und mit NASADEM wiedergefunden): **{z}**.",
    "{r} m grid":
        "{r}-m-Raster",
    "Lee filter":
        "Lee-Filter",
    "threshold kept within {a} to {b} dB":
        "Schwelle zwischen {a} und {b} dB",
    "one threshold per date":
        "eine Schwelle pro Datum",
    "≥ {d} dB darker":
        "≥ {d} dB dunkler",
    "JRC occurrence < {o}%":
        "JRC-Häufigkeit < {o}%",
    "slope < {s}°":
        "Neigung < {s}°",
    "≥ {p} pixels":
        "≥ {p} Pixel",
    "≥ {d} dB brighter":
        "≥ {d} dB heller",
    "shown hatched, never counted":
        "schraffiert gezeigt, nie gezählt",
    "slope {a}° to {b}°":
        "Neigung {a}° bis {b}°",
    "coherence < {c}":
        "Kohärenz < {c}",
    "< 0.6 × its 1 km surroundings":
        "< 0,6 × ihre 1-km-Umgebung",
    "floods: 500 m":
        "Überschwemmungen: 500 m",
    "slides: 750 m":
        "Rutschungen: 750 m",
    "{n} reports":
        "{n} Meldungen",
    "track 106":
        "Bahn 106",
    "3 to 15 July":
        "3. bis 15. Juli",
    "random-placement baseline":
        "Basis mit zufälliger Platzierung",
    "1.9 km image chips":
        "1,9-km-Bildausschnitte",
    "In short:":
        "Kurz gesagt:",
    ", but places nobody reported score {e}: no better than chance":
        ", doch Orte ohne Meldung erreichen {e}: nicht besser als Zufall",
    "Are the flood matches better than chance?":
        "Sind die Hochwasser-Treffer besser als Zufall?",
    "the nearest mapped new open water is {lo} to {hi} km from every reported flood.":
        "das nächste kartierte neue offene Wasser liegt {lo} bis {hi} km von jeder gemeldeten Überschwemmung entfernt.",
    "The count above differs from the {h} of {o} in the headline and the table below: a report's location was corrected after the last full pipeline run. The two will agree after the next run.":
        "Die Zahl oben weicht von {h} von {o} in der Übersicht und der Tabelle unten ab: Der Ort einer Meldung wurde nach dem letzten vollständigen Pipeline-Lauf korrigiert. Nach dem nächsten Lauf stimmen beide überein.",
    "Every reported event":
        "Jedes gemeldete Ereignis",
    "The chance of doing this well by luck alone is about {p} (one-sided binomial test).":
        "Die Wahrscheinlichkeit, allein durch Glück so gut abzuschneiden, liegt bei etwa {p} (einseitiger Binomialtest).",
    "Our zones were found again about as often as chance ({l}×), so single-track zones need ground checks before anyone relies on them.":
        "Unsere Zonen wurden etwa so oft wiedergefunden wie durch Zufall ({l}×), daher brauchen Zonen aus nur einer Bahn eine Prüfung vor Ort, bevor man sich darauf verlässt.",
    "With NASADEM, {k} of {n} reports have a zone within range. So treat the landslide matches as weak support.":
        "Mit NASADEM haben {k} von {n} Meldungen eine Zone in Reichweite. Die Erdrutsch-Treffer sind daher nur schwache Unterstützung.",
    "On this page":
        "Auf dieser Seite",
    "source":
        "Quelle",
    "Found again":
        "Wiedergefunden",
    "Partial":
        "Teilweise",
    "Not seen":
        "Nicht gesehen",
    "Not covered by track 106":
        "Nicht von Bahn 106 erfasst",
    "Found-again rate":
        "Wiederfundrate",
    "Our zones":
        "Unsere Zonen",
    "Same zones moved to random steep places ({n} trials)":
        "Dieselben Zonen an zufällige steile Orte verschoben ({n} Versuche)",
    "The chance of doing this well by luck alone is under 1%.":
        "Die Wahrscheinlichkeit, allein durch Glück so gut abzuschneiden, liegt unter 1 %.",
    "Our zones were found again **{l}× more often than chance**.":
        "Unsere Zonen wurden **{l}× häufiger als durch Zufall** wiedergefunden.",
    "By confidence:":
        "Nach Sicherheit:",
    "Not found with NASADEM because":
        "Mit NASADEM nicht gefunden, weil",
    "Zones":
        "Zonen",
    "Threshold shift":
        "Schwellenverschiebung",
    "Threshold {d} (dB)":
        "Schwelle {d} (dB)",
    "New water (km²)":
        "Neues Wasser (km²)",
    "Reservoir and river rise (km²)":
        "Anstieg Stauseen und Flüsse (km²)",
    "Flooding (km²)":
        "Hochwasser (km²)",
    "Flood patches":
        "Überschwemmungsflächen",
    "Permanent water seen dark":
        "Dauerwasser dunkel gesehen",
    "Report":
        "Meldung",
    "Tolerance (m)":
        "Toleranz (m)",
    "Nearest detection (m)":
        "Nächster Fund (m)",
    "Matched":
        "Getroffen",
    "Nearest new open water (km)":
        "Nächstes neues offenes Wasser (km)",
    "Flat ground within tolerance of a detection":
        "Flaches Land in Toleranz zu einem Fund",
    "Settlements within tolerance of a detection":
        "Siedlungen in Toleranz zu einem Fund",
    "{c}: {f} of {n} found again":
        "{c}: {f} von {n} wiedergefunden",
    "The {n} reported landslides we matched ({ids}) are all matched to the same zone, {z}, {d} away.":
        "Die {n} gemeldeten Erdrutsche, die wir trafen ({ids}), passen alle zur selben Zone, {z}, {d} entfernt.",
    "The {n} reported landslides we matched are {d} from their nearest zone.":
        "Die {n} gemeldeten Erdrutsche, die wir trafen, liegen {d} von ihrer nächsten Zone entfernt.",
    "as chosen":
        "wie gewählt",
    "With the reports as they stand now, **{k} of {n}** reported floods have a detection within their tolerance. The same rule applied to places nobody reported gives **{a} of {n}** on random flat ground and **{b} of {n}** at a random village, town or suburb.":
        "Nach den Meldungen in ihrem jetzigen Stand haben **{k} von {n}** gemeldeten Überschwemmungen einen Fund innerhalb ihrer Toleranz. Dieselbe Regel an Orten ohne Meldung ergibt **{a} von {n}** auf zufälligem flachem Land und **{b} von {n}** in einem zufälligen Dorf, einer Stadt oder einem Vorort.",
    "All {k} matches are to \"possible water under cover\" patches, which we show but never count as flood;":
        "Alle {k} Treffer betreffen Flächen „mögliches verdecktes Wasser“, die wir zeigen, aber nie als Hochwasser zählen;",
    "So the flood count is what chance alone would give: it is not evidence that the map finds reported floods.":
        "Die Hochwasser-Zahl entspricht also dem, was Zufall allein ergäbe: Sie belegt nicht, dass die Karte gemeldete Überschwemmungen findet.",
    "**Yes.**":
        "**Ja.**",
    "**No.**":
        "**Nein.**",
    "GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84.":
        "GeoTIFFs liegen auf dem Analyseraster (UTM-Zone 43N, 40 m). GeoJSON ist in WGS84.",
    "all new water (GeoTIFF)":
        "gesamtes neues Wasser (GeoTIFF)",
    "flooding only, never water before (GeoTIFF)":
        "nur Hochwasser, nie zuvor Wasser (GeoTIFF)",
    "possible water under trees or buildings (GeoTIFF)":
        "mögliches Wasser unter Bäumen oder Gebäuden (GeoTIFF)",
    "likely slide zones (GeoTIFF)":
        "wahrscheinliche Rutschungszonen (GeoTIFF)",
    "HH radar change in dB (GeoTIFF)":
        "HH-Radaränderung in dB (GeoTIFF)",
    "slide zones with scores and nearest place (GeoJSON)":
        "Rutschungszonen mit Punktzahl und nächstem Ort (GeoJSON)",
    "new-water patches, flood and reservoir rise (GeoJSON)":
        "Flächen neuen Wassers, Hochwasser und Anstieg der Stauseen (GeoJSON)",
    "reported events, matched or missed, with reasons (CSV)":
        "gemeldete Ereignisse, getroffen oder verfehlt, mit Gründen (CSV)",
    "water areas and thresholds (CSV)":
        "Wasserflächen und Schwellen (CSV)",
    "second-track check results (JSON)":
        "Ergebnisse der Prüfung mit zweiter Bahn (JSON)",
    "elevation-map check results (JSON)":
        "Ergebnisse der Höhenmodell-Prüfung (JSON)",
    "every number in this app (JSON)":
        "jede Zahl dieser App (JSON)",
    "not checked":
        "nicht geprüft",
    "NISAR radar image of {f}":
        "NISAR-Radarbild von {f}",
    "Radar image":
        "Radarbild",
    "Compare {a} and {b}":
        "{a} und {b} vergleichen",
    "{id}: likely slide zone ({c}), {n}":
        "{id}: wahrscheinliche Rutschungszone ({c}), {n}",
    "Radar colour, 28 Jun":
        "Radarfarbe, 28. Juni",
    "Radar colour, 10 Jul":
        "Radarfarbe, 10. Juli",
    "Radar HH, 28 Jun":
        "Radar HH, 28. Juni",
    "Radar HH, 10 Jul":
        "Radar HH, 10. Juli",
    "Change in HH (blue darker, red brighter)":
        "Änderung in HH (blau dunkler, rot heller)",
    "Coherence 28 Jun to 10 Jul (dark = changed)":
        "Kohärenz 28. Juni bis 10. Juli (dunkel = verändert)",
    "Rivers and reservoirs (JRC)":
        "Flüsse und Stauseen (JRC)",
    "Possible water under cover":
        "Mögliches verdecktes Wasser",
    "Reservoirs and rivers rising":
        "Steigende Stauseen und Flüsse",
    "Flooding (no water recorded here 1984 to 2021)":
        "Hochwasser (hier 1984 bis 2021 nie Wasser verzeichnet)",
    "Likely slide zones ({n})":
        "Wahrscheinliche Rutschungszonen ({n})",
    "; also found by a second NISAR track":
        "; auch von einer zweiten NISAR-Bahn gefunden",
    "Flood patches ({n})":
        "Überschwemmungsflächen ({n})",
    "Reported events ({n})":
        "Gemeldete Ereignisse ({n})",
    "Score (0-1)":
        "Punktzahl (0–1)",
    "Mean slope (°)":
        "Mittlere Neigung (°)",
    "Coherence vs 1 km area":
        "Kohärenz relativ zur 1-km-Umgebung",
    "With NASA's NASADEM elevation map":
        "Mit NASAs NASADEM-Höhenmodell",
    "Second NISAR track (3-15 Jul)":
        "Zweite NISAR-Bahn (3.–15. Juli)",
    "Radar detection nearby":
        "Radarfund in der Nähe",
    "No radar detection nearby":
        "Kein Radarfund in der Nähe",
    "Radar could not observe this":
        "Für das Radar nicht beobachtbar",
    "Study box":
        "Untersuchungsgebiet",
    "Study box (NISAR crop)":
        "Untersuchungsgebiet (NISAR-Ausschnitt)",
    "Flood water on 10 July: {a} ha, {d} dB darker":
        "Hochwasser am 10. Juli: {a} ha, {d} dB dunkler",
    ", near {n}":
        ", nahe {n}",
    "{a} to {b}":
        "{a} bis {b}",
    "Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen.":
        "Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen.",
    "App and integration":
        "App und Integration",
    "Data and science":
        "Daten und Wissenschaft",
    "Validation, story and pitch":
        "Validierung, Geschichte und Pitch",
    "Radar: {n} NISAR L2 provisional files, tracks {t}, {w} (NASA/JPL-Caltech and ISRO, via ASF DAAC); every file is linked on the Method page. Results built {g}, pipeline v{v}.":
        "Radar: {n} vorläufige NISAR-L2-Dateien, Bahnen {t}, {w} (NASA/JPL-Caltech und ISRO, über ASF DAAC); jede Datei ist auf der Methoden-Seite verlinkt. Ergebnisse erzeugt am {g}, Pipeline v{v}.",
    "iGenfinity team logo":
        "Logo des Teams iGenfinity",
    "matched to a detection":
        "einem Fund zugeordnet",
    "Random flat ground":
        "Zufälliges flaches Land",
    "expected by chance":
        "durch Zufall erwartet",
    "Random settlements":
        "Zufällige Siedlungen",
    "matches out of {n} reported floods":
        "Treffer von {n} gemeldeten Überschwemmungen",
}

DE_T = {
    "title": "Was das NISAR-Radar im Monsun 2026 über Pune sah",
    "lede": "Monsunwolken verdecken den Boden vor Satelliten genau dann, wenn Menschen ihn am dringendsten sehen "
            "müssen. {cloud} Der Satellit NISAR von NASA und ISRO blickt mit Radar durch die Wolken. Wir haben seine "
            "Überflüge vor und nach den Überschwemmungen und Erdrutschen vom 3. bis 8. Juli 2026 verglichen.",
    "dates_line": "Zwei NISAR-L-Band-Radarüberflüge über dem Distrikt Pune, Indien: {b} und {a} {y}",
    "found": "Was das Radar fand",
    "new_water": "neue offene Wasserfläche auf flachem Gelände, außerhalb von Flüssen und Stauseen",
    "rise": "neues Wasser, weil Punes Stauseen und Flüsse stiegen und sich füllten",
    "flood": "Hochwasser, das am 10. Juli noch stand, wo zwischen 1984 und 2021 nie Wasser verzeichnet wurde",
    "legend_flood": "Überschwemmung (kein Wasser 1984 bis 2021)",
    "legend_rise": "Stauseen und Flüsse steigen",
    "slides": "wahrscheinliche Rutschungszonen an Hängen von {smin}° bis {smax}°, davon {high} mit hoher Sicherheit. "
              "Es sind Hinweise zum Prüfen: Bei {unrep} gibt es im Umkreis von 2 km kein gemeldetes Ereignis",
    "xt_good": "der Rutschungszonen, die eine zweite NISAR-Spur sehen konnte, fand auch sie, {lift}× häufiger als per "
               "Zufall",
    "xt_good_small": "der Rutschungszonen, die eine zweite NISAR-Spur sehen konnte, fand auch sie: {lift}× häufiger als "
                     "per Zufall, bei kleiner Stichprobe, denn diese Spur deckt {cov} des Gebiets ab",
    "xt_story_good_small": "Ein zweiter NISAR-Orbit fand {c} der {n} Zonen in seinem Blickfeld wieder: {lift}× häufiger "
                           "als per Zufall, bei kleiner Stichprobe.",
    "xt_weak": "der Rutschungszonen, die eine zweite NISAR-Spur sehen konnte, fand auch sie, etwa so oft wie per "
               "Zufall: Zonen aus nur einer Spur besonders vorsichtig behandeln",
    "xt_story_good": "Ein zweiter NISAR-Orbit fand {c} der {n} Zonen in seinem Blickfeld wieder: {lift}× häufiger als per "
                     "Zufall.",
    "xt_story_weak": "Ein zweiter NISAR-Orbit fand nur {c} der {n} Zonen in seinem Blickfeld wieder, etwa so oft wie per "
                     "Zufall; jede Zone ist daher ein Hinweis zum Prüfen.",
    "xt_col": "Zweite Spur",
    "brighter": "wo Wasser unter Bäumen oder zwischen Gebäuden verborgen sein könnte (nicht als Überschwemmung gezählt)",
    "matched": "der gemeldeten Ereignisse, die das Radar sehen konnte, hatten einen Fund",
    "start_story": "Geschichte starten",
    "explore": "Karte erkunden",
    "method": "So haben wir es gemacht",
    "before": "Vorher",
    "after": "Nachher",
    "couldnt": "Was das Radar nicht sehen konnte",
    "lim_streets": "**Überflutete Straßen zwischen Gebäuden.** Radar prallt von Wänden zurück zum Satelliten, deshalb "
                   "kann eine überflutete Straße hell statt dunkel aussehen. {built_sentence}",
    "lim_built_all": "Alle {n} gemeldeten Überschwemmungen, die wir nicht erfasst haben, lagen in bebauten Gebieten.",
    "lim_built_some": "{k} der {n} gemeldeten Überschwemmungen, die wir nicht erfasst haben, lagen in bebauten Gebieten.",
    "lim_timing": "**Wasser, das zwischen zwei Überflügen kam und ging.** Der stärkste Regen fiel vom {p1} bis {p2}; "
                  "NISAR schaute am {b} und erneut am {a}. Die Karte zeigt, was am {a} noch stand, nicht den Höchststand.",
    "lim_small": "**Kleine Rutschungen und Rutschungen auf flachem Gelände.** Unsere Karte hat {res}-m-Pixel und sucht "
                 "an Hängen von {smin}° bis {smax}°. Eine Rutschung von der Breite eines Hauses kann durchrutschen"
                 "{gentle_part}.",
    "lim_gentle": ", und {n} gemeldete Erdrutsche lagen auf flacherem Gelände",
    "lim_hidden": "**Für den Satelliten verborgene Hänge.** Etwa {pct} % des steilen Geländes ist vom Radar abgewandt "
                  "oder faltet sich im Bild über sich selbst. Diese Hänge lassen wir weg und raten nicht.",
    "lim_early": "**Frühe Daten.** NASA hat diese NISAR-Produkte kalibriert, aber bisher nur an wenigen Orten validiert. "
                 "Unsere Zahlen werden sich mit reiferen Daten bewegen.",
    "lim_lead": "Jede wahrscheinliche Rutschungszone ist ein Hinweis zum Prüfen vor Ort, kein Urteil: Bei {u} der {z} "
                "Zonen gibt es im Umkreis von 2 km kein gemeldetes Ereignis.",
    "res_last_clause": " und lag am {d} bei {v} km²",
    "timeline_caption": "Dunkles Wasser bei jedem NISAR-Überflug mit gleichem Orbit und Radarmodus, gezählt innerhalb der "
                        "Fläche, auf der der JRC-Datensatz mindestens einmal Wasser sah (1984 bis 2021).",
    "cloud_sentence": "Vom {f} bis {t} zeigten alle {n} täglichen NASA-Satellitenbilder des Gebiets nur Wolken.",
    "cloud_caption": "Tägliche NASA-Satellitenbilder unseres Untersuchungsgebiets. Zeilen: {sensors}; Spalten: Daten "
                     "(Monat-Tag). Vom {f} bis {t} zeigen alle {n} verfügbaren Bilder nur Wolken; an den Radartagen, "
                     "{p1} und {p2}, war die Wolkendecke aufgelockert. Schwarz: an diesem Tag kein Bild des Gebiets. "
                     "Quelle: [NASA Worldview]({url}) (GIBS).",
    "demo": "<b>Demodaten.</b> Die Radarwerte auf dieser Seite sind synthetisch. Gelände, Flüsse und Stauseen sind echt; "
            "Überschwemmungen und Rutschungszonen nicht.",
    "no_data": "Die Ergebnisse sind noch nicht erstellt.",
    "layers": "Ebenen",
    "legend_new_water": "Neues offenes Wasser",
    "legend_slides": "Wahrscheinliche Rutschungszone",
    "legend_brighter": "Mögliches verdecktes Wasser",
    "legend_permanent": "Flüsse und Stauseen",
    "legend_events": "Gemeldetes Ereignis",
    "lang": "Sprache",
    "step": "Schritt {i} von {n}",
    "back": "Zurück",
    "next": "Weiter",
    "story_title": "Geschichte",
    "matched_floods": "gemeldete Überschwemmungen, die das Radar sehen konnte, hatten einen Fund in der Nähe",
    "matched_slides": "gemeldete Erdrutsche, die das Radar sehen konnte, hatten einen Fund in der Nähe",
    "x_of_y": "{x} von {y}",
    "and_join": "{a} und {b}",
    "slide_fragile_one": "Beide Erdrutsch-Treffer gehören zur selben Zone, {d} km von den Meldungen entfernt, und keiner "
                         "hält, wenn die Rutschungsregel stattdessen NASAs Höhenmodell NASADEM nutzt (siehe Methode).",
    "slide_fragile": "Mit NASAs Höhenmodell NASADEM halten {k} von {n} Erdrutsch-Treffern (siehe Methode).",
    "fell_short": "Wo das Radar nicht reichte, und warum",
    "rain_caption": "Täglicher Niederschlag, gemittelt über das Untersuchungsgebiet. Quelle: {src}.",
    "swipe_caption": "Zum Vergleichen ziehen. Dunkel ist glatt: Wasser. Hell ist rau: Gebäude, Bäume, Fels. Gezeigter "
                     "Ausschnitt: der Teil des Gebiets mit der stärksten Veränderung.",
}

DE_E = {
    "why_h": "Warum das Radar sie markierte",
    "slope": "Steiles Gelände: im Mittel {s}°.",
    "coh": "Der Boden passte zwischen den Überflügen nicht mehr zu sich selbst: Kohärenz {c}, {r}× der des "
           "umgebenden Kilometers.",
    "hv": "HV sank um {v} dB (Vegetation abgetragen)",
    "hh": "HH stieg um {v} dB (raues Geröll)",
    "bs": "Die Radarhelligkeit änderte sich: {x}.",
    "bs_rel": "Die Radarhelligkeit änderte sich stärker als im Rest der Szene.",
    "and": " und ",
    "checks_h": "Zusätzliche Prüfungen",
    "orbit": "Zweiter NISAR-Orbit, 3. bis 15. Juli",
    "orbit_confirmed": "erneut gefunden",
    "orbit_partial": "einen Teil der Belege gesehen",
    "orbit_not seen": "nicht gesehen",
    "orbit_not covered": "außerhalb seines Blickfelds",
    "dem": "NASAs Höhenmodell NASADEM",
    "dem_found": "bestätigt",
    "dem_not": "nicht bestätigt: {r}",
    "rep": "Gemeldetes Ereignis im Umkreis von 2 km",
    "rep_yes": "{place}, {km} km",
    "rep_no": "keins (nächstes {km} km)",
    "conf_high": "Hohe Sicherheit",
    "conf_medium": "Mittlere Sicherheit",
    "conf_low": "Niedrige Sicherheit",
    "maps": "In Google Maps öffnen",
    "chip_before": "28. Juni",
    "chip_after": "10. Juli",
    "chip_coh": "Kohärenz",
    "chip_note": "1,9 km breit, 40-m-Pixel. Radarfarbe: Rot HH, Grün HV, Blau HH/HV. Kohärenz: dunkel = der Boden "
                 "hat sich verändert.",
    "flood_title": "Hochwasser",
    "flood_area": "{a} ha Wasser am 10. Juli, {d} dB dunkler als am 28. Juni, wo zwischen 1984 und 2021 nie Wasser "
                  "verzeichnet wurde.",
    "flood_rep": "Nächste gemeldete Überschwemmung: {place}, {km} km.",
    "lead": "Ein Hinweis zum Prüfen vor Ort, kein bestätigter Erdrutsch.",
    "near_h": "Was in der Nähe liegt",
    "near_road": "Straße im Umkreis von {km} km",
    "near_rail": "Bahnstrecke im Umkreis von {km} km",
    "near_place": "Siedlung im Umkreis von {km} km",
    "near_none": "keine (nächste: {x}, {d})",
    "near_nothing": "keine",
    "near_rail_line": "Bahnstrecke",
    "near_unnamed": "unbenannte Straße",
    "near_note": "Luftlinie vom Rand der Zone, aus OpenStreetMap. Nähe bedeutet nicht Gefährdung.",
}

REASON = {"steeper than 45°": "steiler als 45°", "gentler than 15°": "flacher als 15°",
          "radar layover or shadow": "Radar-Überlagerung oder -Schatten",
          "near the edge of the slope band": "nahe am Rand des Neigungsbereichs"}

TYPE = {"landslide": "Erdrutsch", "flood": "Überschwemmung", "river_overflow": "Flussüberflutung",
        "waterlogging": "Staunässe"}
