"""German text for the app (Deutsch). Keyed by the English source string (DE), by ui.T key (DE_T) and by
evidence.E key (DE_E). Drafted with an AI assistant; a German speaker should check it before submission.
Anything missing falls back to English."""

MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
          "Dezember"]

DE = {
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
    "Only zones an extra check backs": "Nur Zonen mit zusätzlicher Bestätigung",
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
    "**What is nearby.** Of the {t} zones, {r} have a mapped road within {rk} km, {w} a railway line within "
    "{rk} km and {p} a village, town or suburb within {pk} km; {x} have none of these that close. Distances are "
    "straight lines from the edge of the zone. Near does not mean at risk: it tells whoever looks after that "
    "road, line or village which leads concern them.":
        "**Was in der Nähe liegt.** Von den {t} Zonen haben {r} eine kartierte Straße im Umkreis von {rk} km, {w} eine "
        "Bahnstrecke im Umkreis von {rk} km und {p} ein Dorf, eine Stadt oder einen Vorort im Umkreis von {pk} km; "
        "{x} haben nichts davon so nah. Die Entfernungen sind Luftlinien vom Rand der Zone. Nähe bedeutet nicht "
        "Gefährdung: Sie zeigt denen, die für diese Straße, Strecke oder dieses Dorf zuständig sind, welche Hinweise "
        "sie betreffen.",
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
    "Everything NISAR found around Pune: take the 3D tour, or open the flat map for each zone's radar evidence.":
        "Alles, was NISAR rund um Pune fand: Machen Sie die 3D-Tour oder öffnen Sie die flache Karte für die Radarbelege "
        "jeder Zone.",
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
    "3D tour": "3D-Tour",
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
    "are doubled so the hills read.":
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
