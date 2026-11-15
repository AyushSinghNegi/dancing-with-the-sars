<!--
German story text (drafted with an AI assistant; a German speaker should check it before submission).
Same rules as story.md: one "## " heading per step, in the same order, numbers only as {placeholders}.
-->

## Der Regen
In der ersten Juliwoche 2026 fiel in den Westghats oberhalb von Pune tagelang extremer Regen. Flüsse stiegen,
tief gelegene Straßen liefen voll, und Hänge gaben nach. Zwischen dem 3. und 8. Juli 2026 wurden im ganzen Distrikt
Pune in Indien Überschwemmungen und Erdrutsche gemeldet. Das Diagramm zeigt den täglichen Niederschlag über unserem
Untersuchungsgebiet und die beiden Tage, an denen der Satellit NISAR darüber hinwegflog.

## Wolken verdecken den Boden. Radar nicht.
{cloud_sentence} NISAR trägt ein L-Band-Radar: Es sendet eigene Mikrowellenimpulse von etwa 24 cm Wellenlänge,
die Wolken und Regen durchdringen und vom Boden zurückkommen. Glattes Wasser spiegelt den Impuls weg und wirkt
deshalb dunkel. Rauer Boden, Bäume und Gebäude werfen ihn zurück und wirken hell. Genau diesen einfachen
Kontrast messen wir.

## Vorher und nachher
Ziehen Sie den Regler, um das Radarbild vom {before}, vor den Stürmen, mit dem vom {after} zu vergleichen, zwei
Tage nach dem Schlimmsten. Dunkle Flächen, die im zweiten Bild neu auftauchen, sind neues Wasser. Achten Sie
auf die Flüsse und das tiefe Land östlich der Ghats.

## Was sich änderte
Zwischen den beiden Überflügen stiegen die Stauseen und Flüsse, die Pune versorgen: {rise_km2} km² neues Wasser
an ihren Rändern. Wo zwischen 1984 und 2021 nie Wasser verzeichnet wurde, stand am {after} noch {flood_km2} km²
Hochwasser. An den steilen Hängen fanden wir {slide_zones} wahrscheinliche Rutschungszonen, {slide_high} davon
mit hoher Sicherheit: Stellen, an denen der Boden zwischen den Überflügen nicht mehr zu sich selbst passte und das
Radarsignal sprang. {crosstrack_sentence} Weiße Markierungen sind Ereignisse aus den Nachrichten; ein Klick
zeigt die Quelle.

## Die Wochen danach
NISAR überflog Pune weiter alle 12 Tage. Aus demselben Orbit und im selben Radarmodus gesehen, wuchs die
Wasserfläche der Flüsse und Stauseen von {res_first} km² am {res_first_date} auf {res_peak} km² am
{res_peak_date}{res_last_clause}. Der Juli-Sturm war der Beginn des Monsuns, nicht sein Ende: Die Stauseen
westlich von Pune füllten sich noch wochenlang.

## Was das Radar nicht sehen konnte
Radar ist keine Zauberei, und wir zeigen, wo es an Grenzen stößt. Der stärkste Regen fiel vom 5. bis 8. Juli 2026,
zwischen den NISAR-Überflügen am 3. und 10. Juli, und hatte am 9. Juli fast aufgehört: Das Hochwasser hatte zwei
Tage Zeit abzulaufen, bevor das Radar zurückkam. Von den gemeldeten Überschwemmungen, die das Radar sehen konnte,
hatten {flood_hits} von {flood_observable} einen Fund in der Nähe; bei Erdrutschen {slide_hits} von
{slide_observable}. Wasser zwischen hohen Gebäuden versteckt sich in hellen Radarechos, und Rutschungen schmaler
als unsere 40-m-Pixel können durchrutschen. Diese Grenzen zu kennen macht den Rest der Karte vertrauenswürdig.
