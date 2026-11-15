"""Hindi text for the app (हिन्दी). Keyed like i18n_de: by the English source string (HI), by ui.T key (HI_T) and by
evidence.E key (HI_E). Drafted with an AI assistant; a Hindi speaker should check it. Anything missing falls back to
English."""

MONTHS = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]

HI = {
    # reasons from pipeline/validate.py, shown by evidence.reason_text
    "happened before the radar pair ({a} to {b})": "रडार जोड़ी से पहले हुआ ({a} से {b})",
    "happened after the radar pair ({a} to {b})": "रडार जोड़ी के बाद हुआ ({a} से {b})",
    "location in the report is too vague to score (about {k} km)": "रिपोर्ट में दी गई जगह आँकने के लिए बहुत अस्पष्ट है (लगभग {k} किमी)",
    "water may have drained before the {d} pass": "{d} के पास से पहले पानी शायद उतर गया था",
    "ground near the report is gentler than our {s}° slide search": "रिपोर्ट की जगह की ज़मीन हमारी {s}° से शुरू होने वाली भूस्खलन खोज से कम ढलान वाली है",
    "dense buildings: radar bounces off walls, which hides street flooding": "घनी इमारतें: रडार दीवारों से टकराकर लौटता है, जिससे सड़कों की बाढ़ छिप जाती है",
    "flooding smaller than our 40 m pixels or under thick canopy": "हमारे 40 मी पिक्सेल से छोटी बाढ़, या घने पेड़ों के नीचे का पानी",
    "slide smaller than a few 40 m pixels, or coherence lost everywhere nearby": "कुछ 40 मी पिक्सेल से छोटा भूस्खलन, या आसपास हर जगह कोहेरेंस खो गया",
    "outside the radar box": "रडार क्षेत्र से बाहर",
    "no radar data at this spot (edge of swath)": "इस जगह रडार डेटा नहीं (पट्टी का किनारा)",
    "event type has no radar layer (e.g. road closure)": "इस तरह की घटना के लिए रडार परत नहीं (जैसे सड़क बंद)",
    "in or near a town, where buildings can hide flooded streets (a likely reason, not a measured one)":
        "शहर में या उसके पास, जहाँ इमारतें बाढ़ वाली गलियों को छिपा सकती हैं (संभावित कारण, मापा नहीं गया)",
    "Why": "क्यों",
    "Check a place":
        "कोई जगह जाँचें",
    "likely slide zones on slopes of {a}° to {b}°, {h} of them high confidence":
        "{a}° से {b}° ढलान पर संभावित भूस्खलन क्षेत्र, इनमें से {h} उच्च भरोसे वाले",
    "Leads to check, not verdicts: {u} have no reported event within 2 km.":
        "जाँचने लायक संकेत, फ़ैसले नहीं: {u} के 2 किमी के भीतर कोई दर्ज घटना नहीं है।",
    "Shown as possible water, never added to the flood figure.":
        "संभावित पानी के रूप में दिखाया गया, बाढ़ के आँकड़े में कभी नहीं जोड़ा गया।",
    "People who live there":
        "वहाँ रहने वाले लोग",
    "Pick your village or town and see what NISAR found within 2, 5 or 10 km, with a link you can send on.":
        "अपना गाँव या शहर चुनें और देखें कि निसार को 2, 5 या 10 किमी के भीतर क्या मिला, एक लिंक के साथ जिसे आप आगे भेज सकते हैं।",
    "District disaster teams":
        "ज़िला आपदा दल",
    "A ranked check list of likely slide zones with radar images of each spot, a printable sheet and KML for phones.":
        "संभावित भूस्खलन क्षेत्रों की क्रमबद्ध जाँच सूची, हर जगह की रडार तस्वीरों के साथ, छापने लायक शीट और फ़ोन के लिए KML।",
    "Field check list":
        "फ़ील्ड जाँच सूची",
    "Researchers and journalists":
        "शोधकर्ता और पत्रकार",
    "Every number traced to its NISAR file, the checks behind it, and the maps as GeoTIFF and GeoJSON.":
        "हर आँकड़ा उसकी निसार फ़ाइल तक, उसके पीछे की जाँचें, और नक्शे GeoTIFF व GeoJSON में।",
    "Method and data":
        "पद्धति और डेटा",
    "See how each number was made, and the full validation table":
        "देखें कि हर आँकड़ा कैसे बना, और पूरी सत्यापन तालिका",
    "of open water in rivers and reservoirs on {d}, up from {v} km² on {f}":
        "{d} को नदियों और जलाशयों में खुला पानी, {f} के {v} वर्ग किमी से बढ़कर",
    "{n} NISAR passes, same orbit and radar mode. Watch it on the map's season slider.":
        "{n} निसार अवलोकन, एक ही कक्षा और रडार मोड। नक्शे के मौसम स्लाइडर पर देखें।",
    "How we checked it":
        "हमने कैसे जाँचा",
    "Reported floods":
        "दर्ज बाढ़ें",
    "Second NISAR orbit":
        "दूसरी निसार कक्षा",
    "slide zones in its view found again, {l}× more often than chance{p}. A small sample.":
        "उसकी दृष्टि में आए भूस्खलन क्षेत्र फिर मिले, संयोग से {l}× अधिक बार{p}। नमूना छोटा है।",
    "Second elevation map":
        "दूसरा ऊँचाई नक्शा",
    "slide zones kept when slope comes from NASA's NASADEM instead of Copernicus.":
        "भूस्खलन क्षेत्र जो तब भी बने रहे जब ढलान Copernicus की जगह नासा के NASADEM से ली गई।",
    "Water threshold moved":
        "पानी की सीमा बदली गई",
    "Reservoir rise stays between {a} and {b} km²; flooding swings from {c} to {d} km².":
        "जलाशयों की बढ़त {a} से {b} वर्ग किमी के बीच रहती है; बाढ़ {c} से {d} वर्ग किमी तक बदलती है।",
    "Who it is for":
        "यह किसके लिए है",
    "With the water threshold 1 dB lower or higher: {a} to {b} km².":
        "पानी की सीमा 1 dB कम या ज़्यादा करने पर: {a} से {b} वर्ग किमी।",
    "Depends strongly on the water threshold: {a} to {b} km² with it moved 1 dB either way.":
        "पानी की सीमा पर बहुत निर्भर: उसे किसी भी ओर 1 dB बदलने पर {a} से {b} वर्ग किमी।",
    "that radar could observe had a detection nearby. Landslides: {h} of {o}":
        "जिन्हें रडार देख सकता था, उनके पास कोई पहचान मिली। भूस्खलन: {o} में से {h}",
    "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>; if it keeps its 12-day repeat, the next is <b>{n}</b>. The same open code turns each new pass into these maps and lists.":
        "निसार हर 12 दिन में पुणे के ऊपर से गुज़रता है, बादल हों या न हों। हमारे डेटा में आख़िरी अवलोकन: <b>{l}</b>; अगर 12 दिन का चक्र बना रहा, तो अगला <b>{n}</b> को है। वही खुला कोड हर नए अवलोकन को इन नक्शों और सूचियों में बदल देता है।",
    ", both near one zone that a second elevation map does not keep.":
        ", दोनों एक ही क्षेत्र के पास, जिसे दूसरा ऊँचाई नक्शा नहीं रखता।",
    "Base map":
        "आधार नक्शा",
    "Layer opacity":
        "परत की पारदर्शिता",
    "Slide zones shown":
        "दिखाए गए भूस्खलन क्षेत्र",
    "What the map shows":
        "नक्शा क्या दिखाता है",
    "NISAR pass":
        "निसार अवलोकन",
    "Show the whole area":
        "पूरा क्षेत्र दिखाएँ",
    "Slide zones":
        "भूस्खलन क्षेत्र",
    "Flood water":
        "बाढ़ का पानी",
    "Rain and timeline":
        "बारिश और समयरेखा",
    "Reported events":
        "दर्ज घटनाएँ",
    "Downloads":
        "डाउनलोड",
    " ({s}{v:.0f} km² since {f})":
        " ({f} से {s}{v:.0f} वर्ग किमी)",
    "NISAR passes on {b} and {a}. Switch radar layers with the button at the top right of the map; click a zone or a marker for details, or pick a zone below to see its radar evidence.":
        "{b} और {a} को निसार अवलोकन। नक्शे के ऊपर दाईं ओर के बटन से रडार परतें बदलें; विवरण के लिए किसी क्षेत्र या निशान पर क्लिक करें, या उसका रडार प्रमाण देखने के लिए नीचे कोई क्षेत्र चुनें।",
    "{n} likely slide zones, sorted by score. Score adds three pieces of evidence: steepness, radar change, and coherence lost compared with the surrounding kilometre. Select a row to zoom the map to it and see its radar evidence.":
        "{n} संभावित भूस्खलन क्षेत्र, अंक के क्रम में। अंक तीन प्रमाण जोड़ता है: ढलान, रडार में बदलाव, और आसपास के एक किलोमीटर की तुलना में कोहेरेंस में गिरावट। नक्शे को वहाँ ले जाने और उसका रडार प्रमाण देखने के लिए एक पंक्ति चुनें।",
    "{n} flood patches: new water on {a} where no water was recorded between 1984 and 2021. Select one to zoom the map to it and see the radar before and after.":
        "{n} बाढ़ वाले हिस्से: {a} को नया पानी, जहाँ 1984 से 2021 तक कभी पानी दर्ज नहीं हुआ। नक्शे को वहाँ ले जाने और पहले व बाद का रडार देखने के लिए एक चुनें।",
    "Open water on every NISAR pass of the same orbit and radar mode. Press play, or drag the slider inside the map, to watch the reservoirs fill after the July storm. The map keeps its zoom while the date changes.":
        "एक ही कक्षा और रडार मोड के हर निसार अवलोकन पर खुला पानी। जुलाई के तूफ़ान के बाद जलाशयों को भरते देखने के लिए चलाएँ दबाएँ, या नक्शे के भीतर का स्लाइडर खींचें। तारीख़ बदलने पर भी नक्शे का ज़ूम बना रहता है।",
    "Open water on this pass":
        "इस अवलोकन पर खुला पानी",
    "Since the pass on {p}: {r:.0f} mm of rain, open water {s}{v:.0f} km².":
        "{p} के अवलोकन से अब तक: {r:.0f} मिमी बारिश, खुला पानी {s}{v:.0f} वर्ग किमी।",
    "Rain: NASA GPM IMERG Late Run daily totals, averaged over the whole study box, in UTC days from the day after the previous pass to the day of this pass. An average over the box is far lower than totals at single rain gauges, and Late Run values may change slightly in the Final Run.":
        "बारिश: नासा GPM IMERG Late Run के दैनिक कुल, पूरे अध्ययन क्षेत्र का औसत, पिछले अवलोकन के अगले दिन से इस अवलोकन के दिन तक (UTC दिन)। पूरे क्षेत्र का औसत किसी एक वर्षामापी के कुल से बहुत कम होता है, और Final Run में Late Run के मान थोड़े बदल सकते हैं।",
    "Field check list: print it, KML for phones, CSV":
        "फ़ील्ड जाँच सूची: छापें, फ़ोन के लिए KML, CSV",
    "All water numbers and thresholds":
        "पानी के सभी आँकड़े और सीमाएँ",
    "of open water inside the area where water has ever been recorded (JRC, 1984 to 2021) on {d}":
        "{d} को उस इलाक़े के भीतर खुला पानी जहाँ कभी पानी दर्ज हुआ है (JRC, 1984 से 2021)",
    "High confidence only":
        "केवल उच्च भरोसा",
    "Medium and high":
        "मध्यम और उच्च",
    "All, including low":
        "सभी, कम सहित",
    "Map zoomed to {i}":
        "नक्शा {i} पर ज़ूम किया गया",
    "Patch":
        "हिस्सा",
    "Nearest reported flood":
        "सबसे नज़दीकी दर्ज बाढ़",
    "What changed, {b} to {a}":
        "क्या बदला, {b} से {a}",
    "Water through the season, {f} to {l}":
        "पूरे मौसम में पानी, {f} से {l}",
    "Area (ha)":
        "क्षेत्रफल (हेक्टेयर)",
    "Darker by (dB)":
        "कितना गहरा (dB)",
    "Field check list for district teams":
        "ज़िला दलों के लिए फ़ील्ड जाँच सूची",
    "Method and limits":
        "पद्धति और सीमाएँ",
    "Where next":
        "आगे कहाँ",
    "Watch the water spread on the map":
        "नक्शे पर पानी फैलते देखें",
    "Printable list with radar images":
        "रडार तस्वीरों के साथ छापने लायक सूची",
    "KML for Google Earth and phone maps":
        "गूगल अर्थ और फ़ोन नक्शों के लिए KML",
    "Spreadsheet (CSV)":
        "स्प्रेडशीट (CSV)",
    "Confidence":
        "भरोसा",
    "Backed by an extra check":
        "किसी अतिरिक्त जाँच का समर्थन",
    "Near a place":
        "किसी जगह के पास",
    "{n} of {t} zones. Select a row to see its radar evidence.":
        "{t} में से {n} क्षेत्र। रडार प्रमाण देखने के लिए एक पंक्ति चुनें।",
    "No slide zones in this run.":
        "इस रन में कोई भूस्खलन क्षेत्र नहीं।",
    "The flood matches are no more than chance gives: places nobody reported match {e} of {n}.":
        "बाढ़ के मिलान संयोग से ज़्यादा नहीं हैं: जिन जगहों पर किसी ने कुछ दर्ज नहीं किया, वे {n} में से {e} बार मिलती हैं।",
    "Map shows":
        "नक्शा दिखाता है",
    "Pass by pass, {f} to {l}":
        "हर अवलोकन, {f} से {l}",
    "Drag the slider on the map, or press play, to step through NISAR's passes; the view stays where you put it. Same orbit and radar mode on every date. Red is HH, green HV, blue HH/HV: water is dark, forest green, buildings bright. Blue overlay: open water mapped on that date. NISAR used a different mode on this orbit from 27 August to 2 October, so those passes are not shown. Click the map to check any other point.":
        "निसार के अवलोकनों से गुज़रने के लिए नक्शे का स्लाइडर खींचें या चलाएँ दबाएँ; दृश्य वहीं रहता है जहाँ आपने रखा। हर तारीख़ पर एक ही कक्षा और रडार मोड। लाल HH है, हरा HV, नीला HH/HV: पानी गहरा, जंगल हरा, इमारतें चमकीली। नीली परत: उस तारीख़ को नक्शे पर आया खुला पानी। 27 अगस्त से 2 अक्टूबर तक इस कक्षा पर निसार ने अलग मोड इस्तेमाल किया, इसलिए वे अवलोकन नहीं दिखाए गए। कोई और जगह जाँचने के लिए नक्शे पर क्लिक करें।",
    "Play":
        "चलाएँ",
    "Open water":
        "खुला पानी",
    "What is nearby (CSV)":
        "पास में क्या है (CSV)",
    "Road nearby":
        "पास की सड़क",
    "Settlement nearby":
        "पास की बस्ती",
    "Nearest mapped road within {km} km of the zone's edge (OpenStreetMap)":
        "क्षेत्र के किनारे से {km} किमी के भीतर सबसे नज़दीकी नक्शे पर दर्ज सड़क (OpenStreetMap)",
    "Nearest village, town or suburb within {km} km of the zone's edge (OpenStreetMap)":
        "क्षेत्र के किनारे से {km} किमी के भीतर सबसे नज़दीकी गाँव, शहर या उपनगर (OpenStreetMap)",
    "**What is nearby.** {r} of {t} zones lie within {rk} km of a mapped road, {w} of a railway line, and {p} within {pk} km of a village, town or suburb. Near does not mean at risk: it shows who should look at which lead.":
        "**पास में क्या है।** {t} में से {r} क्षेत्र नक्शे पर दर्ज किसी सड़क से {rk} किमी के भीतर हैं, {w} किसी रेल लाइन से, और {p} किसी गाँव, शहर या उपनगर से {pk} किमी के भीतर। पास होने का मतलब ख़तरा नहीं: इससे पता चलता है कि कौन सा संकेत किसे देखना चाहिए।",
    "Roads, railway lines and settlements © OpenStreetMap contributors (expressways down to tertiary roads; smaller roads, tracks and hamlets are not counted).":
        "सड़कें, रेल लाइनें और बस्तियाँ © OpenStreetMap योगदानकर्ता (एक्सप्रेसवे से लेकर तृतीयक सड़कों तक; छोटी सड़कें, पगडंडियाँ और पुरवे नहीं गिने गए)।",
    "Found again by the second NISAR orbit, kept with NASADEM, or a reported event within 2 km.":
        "दूसरी निसार कक्षा ने फिर पाया, NASADEM के साथ बना रहा, या 2 किमी के भीतर कोई दर्ज घटना।",
    "e.g. Mulshi":
        "जैसे मुळशी",
    "Every likely slide zone NISAR found between {b} and {a}, ranked, with the radar images of the spot, why it was flagged and which independent checks it passed. For district teams: print it, open it in Google Earth or on a phone, and record what you find. These are leads to check, not confirmed landslides.":
        "{b} और {a} के बीच निसार को मिला हर संभावित भूस्खलन क्षेत्र, क्रम में, उस जगह की रडार तस्वीरों के साथ, उसे क्यों चिह्नित किया गया और उसने कौन सी स्वतंत्र जाँचें पास कीं। ज़िला दलों के लिए: इसे छापें, गूगल अर्थ या फ़ोन पर खोलें, और जो मिले उसे दर्ज करें। ये जाँचने लायक संकेत हैं, पुष्ट भूस्खलन नहीं।",
    "Zone":
        "क्षेत्र",
    "Nearest place":
        "सबसे नज़दीकी जगह",
    "Nearest place names © OpenStreetMap contributors (Nominatim). Score: steepness, radar change and coherence loss, each up to a third.":
        "नज़दीकी जगहों के नाम © OpenStreetMap योगदानकर्ता (Nominatim)। अंक: ढलान, रडार में बदलाव और कोहेरेंस में गिरावट, हर एक अधिकतम एक-तिहाई।",
    "kept":
        "बना रहा",
    "not kept":
        "नहीं बना रहा",
    "Score":
        "अंक",
    "2nd orbit":
        "दूसरी कक्षा",
    "Nearest report":
        "सबसे नज़दीकी रिपोर्ट",
    "Slope (°)":
        "ढलान (°)",
    "Map":
        "नक्शा",
    "Evidence for":
        "प्रमाण:",
    "This list comes from one pair of NISAR passes. NISAR returns every 12 days: the last pass in our data is <b>{l}</b>, and if it keeps its repeat the next is <b>{n}</b>. The same code rebuilds the list from each new pass.":
        "यह सूची निसार के अवलोकनों की एक जोड़ी से बनी है। निसार हर 12 दिन में लौटता है: हमारे डेटा में आख़िरी अवलोकन <b>{l}</b> है, और चक्र बना रहा तो अगला <b>{n}</b> को है। वही कोड हर नए अवलोकन से सूची फिर बनाता है।",
    "High":
        "उच्च",
    "Medium":
        "मध्यम",
    "Low":
        "कम",
    "NISAR track 106, 3 to 15 July":
        "निसार ट्रैक 106, 3 से 15 जुलाई",
    "Slide rule re-run with NASA's NASADEM elevation map":
        "नासा के NASADEM ऊँचाई नक्शे के साथ भूस्खलन नियम दोबारा चलाया गया",
    "Distance to the nearest reported flood or landslide":
        "सबसे नज़दीकी दर्ज बाढ़ या भूस्खलन की दूरी",
    "Open":
        "खोलें",
    "found again":
        "फिर मिला",
    "partly":
        "आंशिक",
    "not seen":
        "नहीं दिखा",
    "outside view":
        "दृष्टि से बाहर",
    "Village, town or suburb":
        "गाँव, शहर या उपनगर",
    "Type a name, for example Lonavala":
        "नाम लिखें, जैसे लोणावला",
    "Distance":
        "दूरी",
    "the point you picked":
        "आपका चुना हुआ बिंदु",
    "Click the map to check any other point.":
        "कोई और बिंदु जाँचने के लिए नक्शे पर क्लिक करें।",
    "Pick a village or town, or click anywhere on the map, to see what NISAR radar found around it between {b} and {a}: likely slide zones, flood water, rising reservoirs, and the events people reported.":
        "कोई गाँव या शहर चुनें, या नक्शे पर कहीं भी क्लिक करें, और देखें कि {b} और {a} के बीच निसार रडार को उसके आसपास क्या मिला: संभावित भूस्खलन क्षेत्र, बाढ़ का पानी, भरते जलाशय, और लोगों की दर्ज की गई घटनाएँ।",
    "Choose one of {n} villages, towns and suburbs in the study area (names from OpenStreetMap), or click the map. The result has its own link, so you can send it to someone.":
        "अध्ययन क्षेत्र के {n} गाँवों, शहरों और उपनगरों में से एक चुनें (नाम OpenStreetMap से), या नक्शे पर क्लिक करें। नतीजे का अपना लिंक होता है, जिसे आप किसी को भी भेज सकते हैं।",
    "city":
        "महानगर",
    "town":
        "शहर",
    "suburb":
        "उपनगर",
    "village":
        "गाँव",
    "This point is outside the area we processed NISAR data for. Pick a place inside the dashed box.":
        "यह बिंदु उस इलाक़े से बाहर है जिसके लिए हमने निसार डेटा जाँचा। बिंदीदार घेरे के भीतर की कोई जगह चुनें।",
    "Copy the address bar to share this result.":
        "यह नतीजा साझा करने के लिए पता बार कॉपी करें।",
    "NISAR passes over Pune every 12 days, cloud or not. Last pass in our data: <b>{l}</b>. If it keeps its 12-day repeat, the next is <b>{n}</b>, and this page can be rebuilt from it.":
        "निसार हर 12 दिन में पुणे के ऊपर से गुज़रता है, बादल हों या न हों। हमारे डेटा में आख़िरी अवलोकन: <b>{l}</b>। अगर 12 दिन का चक्र बना रहा, तो अगला <b>{n}</b> को है, और उससे यह पेज फिर बनाया जा सकता है।",
    "Start with a place":
        "किसी जगह से शुरू करें",
    "flood patches still standing on {a}":
        "{a} को अब भी खड़े बाढ़ वाले हिस्से",
    "of new water as reservoirs and rivers rose":
        "जलाशयों और नदियों के बढ़ने से आया नया पानी",
    "reported floods or landslides":
        "दर्ज बाढ़ या भूस्खलन",
    "NISAR found no slide zone or flood water here. That is not an all-clear: radar misses water between buildings, slides narrower than 40 m, and anything that came and went between passes.":
        "निसार को यहाँ कोई भूस्खलन क्षेत्र या बाढ़ का पानी नहीं मिला। इसे पूरी तरह सुरक्षित न मानें: रडार इमारतों के बीच का पानी, 40 मीटर से संकरे भूस्खलन, और दो अवलोकनों के बीच आकर चला गया पानी नहीं देख पाता।",
    "Likely slide zones":
        "संभावित भूस्खलन क्षेत्र",
    "{n} more zones":
        "{n} और क्षेत्र",
    "What people reported":
        "लोगों ने क्या दर्ज किया",
    "likely slide zones":
        "संभावित भूस्खलन क्षेत्र",
    "Nearest likely slide zone: {id}, {k} km away.":
        "सबसे नज़दीकी संभावित भूस्खलन क्षेत्र: {id}, {k} किमी दूर।",
    "radar found something within range":
        "रडार को दायरे में कुछ मिला",
    "radar missed it":
        "रडार से छूट गया",
    "radar could not observe it":
        "रडार इसे देख नहीं सकता था",
    "not scored":
        "गिना नहीं गया",
    "Within {k} km of":
        "{k} किमी के भीतर:",
    ", {h} high confidence":
        ", {h} उच्च भरोसे वाले",
    "{k} km away":
        "{k} किमी दूर",
    "Calm water looks dark":
        "शांत पानी गहरा दिखता है",
    "A smooth surface reflects the radar away, like a mirror.":
        "चिकनी सतह रडार को शीशे की तरह दूर परावर्तित कर देती है।",
    "Rough ground looks bright":
        "खुरदरी ज़मीन चमकीली दिखती है",
    "Trees, rock and debris scatter some radar back.":
        "पेड़, चट्टान और मलबा कुछ रडार वापस बिखेरते हैं।",
    "Water by walls: very bright":
        "दीवार के पास पानी: बहुत चमकीला",
    "Water and a wall or trunk bounce it straight back.":
        "पानी और दीवार या तना उसे सीधे वापस उछाल देते हैं।",
    "Coherence: did it stay put?":
        "कोहेरेंस: क्या ज़मीन वैसी ही रही?",
    "Two passes 12 days apart: a slide scrambles the pattern.":
        "12 दिन के अंतर पर दो अवलोकन: भूस्खलन पैटर्न को बिगाड़ देता है।",
    "How NISAR's L-band radar sees water, rough ground, double bounce and coherence":
        "निसार का L-बैंड रडार पानी, खुरदरी ज़मीन, दोहरा परावर्तन और कोहेरेंस कैसे देखता है",
    "Light or dark: ⋮ menu (top right) › Settings.":
        "हल्का या गहरा रंग: ⋮ मेन्यू (ऊपर दाईं ओर) › Settings।",
    "Built by team iGenfinity for NASA Space Apps 2026":
        "नासा स्पेस ऐप्स 2026 के लिए टीम iGenfinity ने बनाया",
    "What NASA-ISRO NISAR radar saw through the 2026 Pune monsoon":
        "2026 के पुणे मानसून में नासा-इसरो निसार रडार ने क्या देखा",
    "NASA-ISRO NISAR · L-band radar · Pune, India":
        "नासा-इसरो निसार · L-बैंड रडार · पुणे, भारत",
    "Optical satellites, 3 to 8 July: only cloud":
        "ऑप्टिकल उपग्रह, 3 से 8 जुलाई: केवल बादल",
    "NISAR radar, {d}: sees the ground, new water in blue":
        "निसार रडार, {d}: ज़मीन दिखती है, नया पानी नीले में",
    "Cloud drawn as an illustration. Radar: real NISAR L-band image.":
        "बादल चित्र के रूप में बनाए गए हैं। रडार: असली निसार L-बैंड तस्वीर।",
    "Pause animation":
        "एनिमेशन रोकें",
    "Play animation":
        "एनिमेशन चलाएँ",
    "Animation: the NISAR satellite passes over Pune and its radar sees through the monsoon cloud to the flood water and slide zones below.":
        "एनिमेशन: निसार उपग्रह पुणे के ऊपर से गुज़रता है और उसका रडार मानसून के बादलों के पार नीचे बाढ़ के पानी और भूस्खलन क्षेत्रों को देखता है।",
    "Next expected NISAR pass over Pune: {d}":
        "पुणे के ऊपर निसार का अगला अपेक्षित अवलोकन: {d}",
    "Explore the map":
        "नक्शा देखें",
    "GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84. File descriptions are in English.":
        "GeoTIFF विश्लेषण ग्रिड पर हैं (UTM ज़ोन 43N, 40 मीटर)। GeoJSON WGS84 में है। फ़ाइलों का विवरण अंग्रेज़ी में है।",
    "Place":
        "जगह",
    "Event":
        "घटना",
    "Date":
        "तारीख़",
    "Result":
        "नतीजा",
    "Why (in English)":
        "कारण (अंग्रेज़ी में)",
    "Everything NISAR found around Pune on one map: flood water, rising reservoirs, likely slide zones, and the events people reported. Pick a zone or a flood patch below to see its radar evidence.":
        "पुणे के आसपास निसार को जो कुछ मिला, सब एक नक्शे पर: बाढ़ का पानी, भरते जलाशय, संभावित भूस्खलन क्षेत्र, और लोगों की दर्ज की गई घटनाएँ। उसका रडार प्रमाण देखने के लिए नीचे कोई क्षेत्र या बाढ़ वाला हिस्सा चुनें।",
    "All findings on one map":
        "सारे नतीजे एक नक्शे पर",
    "Next expected NISAR pass over Pune":
        "पुणे के ऊपर निसार का अगला अपेक्षित अवलोकन",
    "tomorrow":
        "कल",
    "in {n} days":
        "{n} दिन में",
    "Every 12 days, cloud or not.":
        "हर 12 दिन, बादल हों या न हों।",
    "The Rain":
        "बारिश",
    "Cloud":
        "बादल",
    "Before and After":
        "पहले और बाद में",
    "What Changed":
        "क्या बदला",
    "The Weeks After":
        "उसके बाद के हफ़्ते",
    "Limits":
        "सीमाएँ",
    "Rain measured from space: NASA GPM IMERG, daily":
        "अंतरिक्ष से नापी गई बारिश: नासा GPM IMERG, दैनिक",
    "What optical satellites saw: NASA Worldview":
        "ऑप्टिकल उपग्रहों ने क्या देखा: नासा Worldview",
    "NISAR L-band radar, HH, track {t}":
        "निसार L-बैंड रडार, HH, ट्रैक {t}",
    "NISAR findings, {b} to {a}":
        "निसार के नतीजे, {b} से {a}",
    "NISAR, every pass of track {t} in the same radar mode":
        "निसार, एक ही रडार मोड में ट्रैक {t} का हर अवलोकन",
    "Reported events checked against the radar":
        "दर्ज घटनाओं का रडार से मिलान",
    "Tip: the ← and → keys move between chapters.":
        "सुझाव: ← और → कुंजियों से अध्याय बदलें।",
    "Everything on one map":
        "सब कुछ एक नक्शे पर",
    "Every layer, the season slider and the radar evidence for each zone and flood patch.":
        "हर परत, मौसम स्लाइडर, और हर क्षेत्र व बाढ़ वाले हिस्से का रडार प्रमाण।",
    "A satellite passes":
        "एक उपग्रह गुज़रता है",
    "NISAR flies over Pune every 12 days, day or night.":
        "निसार हर 12 दिन में पुणे के ऊपर से उड़ता है, दिन हो या रात।",
    "Radar sees through cloud":
        "रडार बादलों के पार देखता है",
    "Its radar passes through cloud and rain. Calm water looks dark.":
        "उसका रडार बादल और बारिश के पार जाता है। शांत पानी गहरा दिखता है।",
    "We map the change":
        "हम बदलाव का नक्शा बनाते हैं",
    "We compare passes before and after the storm and map what changed.":
        "हम तूफ़ान से पहले और बाद के अवलोकनों की तुलना करके बदलाव का नक्शा बनाते हैं।",
    "How it works":
        "यह कैसे काम करता है",
    "See it in 3D":
        "3D में देखें",
    "A one-minute tour of what NISAR found, on a model of the land.":
        "ज़मीन के एक मॉडल पर, निसार के नतीजों की एक मिनट की सैर।",
    "likely slide zones on steep slopes, {h} of them high confidence":
        "खड़ी ढलानों पर संभावित भूस्खलन क्षेत्र, इनमें से {h} उच्च भरोसे वाले",
    "Leads to check: {u} have no reported event within 2 km.":
        "जाँचने लायक संकेत: {u} के 2 किमी के भीतर कोई दर्ज घटना नहीं है।",
    "Could be {a} to {b} km², depending on the water threshold.":
        "पानी की सीमा के अनुसार {a} से {b} वर्ग किमी हो सकता है।",
    "Could be {a} to {b} km²: very sensitive to the water threshold.":
        "{a} से {b} वर्ग किमी हो सकता है: पानी की सीमा पर बहुत निर्भर।",
    "{n} NISAR passes, same orbit.":
        "{n} निसार अवलोकन, एक ही कक्षा।",
    "See what NISAR found near your village or town.":
        "देखें कि आपके गाँव या शहर के पास निसार को क्या मिला।",
    "A ranked list of slide zones to check, with radar images, for print and phones.":
        "जाँचने के लिए भूस्खलन क्षेत्रों की क्रमबद्ध सूची, रडार तस्वीरों के साथ, छापने और फ़ोन के लिए।",
    "Every number traced to its NISAR file, with the checks and the data.":
        "हर आँकड़ा उसकी निसार फ़ाइल तक, जाँचों और डेटा के साथ।",
    "Water between buildings":
        "इमारतों के बीच का पानी",
    "Radar bounces off walls, so city flooding is under-counted.":
        "रडार दीवारों से टकराकर लौटता है, इसलिए शहर की बाढ़ कम गिनी जाती है।",
    "Between passes":
        "दो अवलोकनों के बीच",
    "Water that came and went between {b} and {a} is not seen.":
        "{b} और {a} के बीच आकर चला गया पानी नहीं दिखता।",
    "Small slides":
        "छोटे भूस्खलन",
    "Slides narrower than about {r} m can slip through.":
        "लगभग {r} मीटर से संकरे भूस्खलन छूट सकते हैं।",
    "Hidden slopes":
        "छिपी ढलानें",
    "{p}% of steep ground faces away from the radar and is left out.":
        "{p}% खड़ी ज़मीन रडार से उलटी ओर है और छोड़ दी गई है।",
    "Early data":
        "शुरुआती डेटा",
    "These NISAR products are provisional; the numbers may shift.":
        "ये निसार उत्पाद अस्थायी हैं; आँकड़े बदल सकते हैं।",
    "For each zone's radar evidence and the tables, switch to the flat map above.":
        "हर क्षेत्र के रडार प्रमाण और तालिकाओं के लिए ऊपर सपाट नक्शे पर जाएँ।",
    "Layers: button at the top right of the map. Click a marker, or pick a row below, for details.":
        "परतें: नक्शे के ऊपर दाईं ओर का बटन। विवरण के लिए किसी निशान पर क्लिक करें, या नीचे कोई पंक्ति चुनें।",
    "{n} likely slide zones, highest score first. Select a row to zoom to it and see its radar evidence.":
        "{n} संभावित भूस्खलन क्षेत्र, सबसे ऊँचे अंक पहले। वहाँ ज़ूम करने और रडार प्रमाण देखने के लिए एक पंक्ति चुनें।",
    "{n} flood patches: water on {a} where none was recorded from 1984 to 2021. Select one to see its radar before and after.":
        "{n} बाढ़ वाले हिस्से: {a} को पानी, जहाँ 1984 से 2021 तक कभी पानी दर्ज नहीं हुआ। पहले और बाद का रडार देखने के लिए एक चुनें।",
    "Flat map: what changed, {b} to {a}":
        "सपाट नक्शा: क्या बदला, {b} से {a}",
    "Drag to turn the model; point at a pin for details.":
        "मॉडल घुमाने के लिए खींचें; विवरण के लिए किसी पिन पर पॉइंटर रखें।",
    "Every likely slide zone from {b} to {a}, ranked, with its radar images. Print it or open it on a phone, then go and check: these are leads, not confirmed landslides.":
        "{b} से {a} तक का हर संभावित भूस्खलन क्षेत्र, क्रम में, रडार तस्वीरों के साथ। छापें या फ़ोन पर खोलें, फिर जाकर जाँचें: ये संकेत हैं, पुष्ट भूस्खलन नहीं।",
    "Pick your village or town, or click the map, to see what NISAR found nearby between {b} and {a}.":
        "अपना गाँव या शहर चुनें, या नक्शे पर क्लिक करें, और देखें कि {b} और {a} के बीच निसार को पास में क्या मिला।",
    "Relief":
        "उभार",
    "Radar":
        "रडार",
    "Flooding":
        "बाढ़",
    "Reported":
        "दर्ज",
    "Names":
        "नाम",
    "Next":
        "आगे",
    "Back":
        "पीछे",
    "Take the tour":
        "टूर शुरू करें",
    "Pause":
        "रोकें",
    "Water before the storm":
        "तूफ़ान से पहले का पानी",
    "New water by {a}":
        "{a} तक नया पानी",
    "Flooding on dry land":
        "सूखी ज़मीन पर बाढ़",
    "Likely slide zone":
        "संभावित भूस्खलन क्षेत्र",
    "Reported flood or landslide":
        "दर्ज बाढ़ या भूस्खलन",
    "Heights ×2. Elevation: Copernicus GLO-30. Radar: NISAR.":
        "ऊँचाई ×2। ऊँचाई डेटा: Copernicus GLO-30। रडार: निसार।",
    "Pune district, India":
        "पुणे ज़िला, भारत",
    "slope":
        "ढलान",
    "score":
        "अंक",
    "high confidence":
        "उच्च भरोसा",
    "medium confidence":
        "मध्यम भरोसा",
    "low confidence":
        "कम भरोसा",
    "near":
        "पास में",
    "Flood patch":
        "बाढ़ वाला हिस्सा",
    "ha of water":
        "हेक्टेयर पानी",
    "landslide":
        "भूस्खलन",
    "flood":
        "बाढ़",
    "The 3D view needs WebGL, which this browser has turned off. The flat map below shows the same findings.":
        "3D दृश्य के लिए WebGL चाहिए, जो इस ब्राउज़र में बंद है। नीचे का सपाट नक्शा वही नतीजे दिखाता है।",
    "Point north":
        "उत्तर की ओर करें",
    "3D model of the study area with NISAR's findings":
        "निसार के नतीजों के साथ अध्ययन क्षेत्र का 3D मॉडल",
    "Where this is":
        "यह कहाँ है",
    "Pune district, Maharashtra, India: an 85 km box from the Western Ghats hills (left) to Pune city (right). Heights are doubled so the hills stand out.":
        "पुणे ज़िला, महाराष्ट्र, भारत: पश्चिमी घाट की पहाड़ियों (बाएँ) से पुणे शहर (दाएँ) तक 85 किमी का क्षेत्र। पहाड़ियाँ साफ़ दिखें, इसलिए ऊँचाई दोगुनी की गई है।",
    "The Western Ghats":
        "पश्चिमी घाट",
    "Steep, forested hills where the monsoon rain falls hardest. In early July the whole area averaged up to {r} mm of rain in a day, and slopes gave way.":
        "खड़ी, जंगल से ढकी पहाड़ियाँ जहाँ मानसून की बारिश सबसे ज़ोर से गिरती है। जुलाई की शुरुआत में पूरे क्षेत्र में एक दिन में औसतन {r} मिमी तक बारिश हुई, और ढलानें धँस गईं।",
    "Your turn":
        "अब आपकी बारी",
    "Drag to turn the model, scroll or pinch to zoom, and point at a pin for details.":
        "मॉडल घुमाने के लिए खींचें, ज़ूम के लिए स्क्रॉल या पिंच करें, और विवरण के लिए किसी पिन पर पॉइंटर रखें।",
    "Reservoirs filled up":
        "जलाशय भर गए",
    "Blue edges are new water: between {b} and {a}, Pune's reservoirs and rivers grew by {k} km².":
        "नीले किनारे नया पानी हैं: {b} और {a} के बीच पुणे के जलाशय और नदियाँ {k} वर्ग किमी बढ़ीं।",
    "Orange pins: {n} places on steep slopes where the ground changed between passes. Tall pins are the {h} high-confidence ones. Leads to check, not confirmed landslides.":
        "नारंगी पिन: खड़ी ढलानों पर {n} जगहें जहाँ दो अवलोकनों के बीच ज़मीन बदली। ऊँचे पिन {h} उच्च भरोसे वाले हैं। ये जाँचने लायक संकेत हैं, पुष्ट भूस्खलन नहीं।",
    "Flooded land":
        "बाढ़ग्रस्त ज़मीन",
    "Dark-blue pins: water still standing on {a} where no water was recorded from 1984 to 2021, {k} km² in all.":
        "गहरे नीले पिन: {a} को खड़ा पानी, जहाँ 1984 से 2021 तक कभी पानी दर्ज नहीं हुआ, कुल {k} वर्ग किमी।",
    "Pune city":
        "पुणे शहर",
    "White pins are floods and landslides people reported. Radar sees water between buildings poorly, so many city reports were missed. Overall, {h} of {o} reported floods it could observe had a detection nearby.":
        "सफ़ेद पिन लोगों की दर्ज की गई बाढ़ और भूस्खलन हैं। रडार इमारतों के बीच का पानी ठीक से नहीं देख पाता, इसलिए शहर की कई रिपोर्टें छूट गईं। कुल मिलाकर, जिन {o} दर्ज बाढ़ों को वह देख सकता था, उनमें से {h} के पास कोई पहचान मिली।",
    "that radar could see had a detection nearby. Landslides: {h} of {o}":
        "जिन्हें रडार देख सकता था, उनके पास कोई पहचान मिली। भूस्खलन: {o} में से {h}",
    ", weak support.":
        ", कमज़ोर समर्थन।",
    "slide zones found again, {l}× more than chance{p}.":
        "भूस्खलन क्षेत्र फिर मिले, संयोग से {l}× अधिक{p}।",
    "slide zones kept with NASA's NASADEM elevation map.":
        "नासा के NASADEM ऊँचाई नक्शे के साथ बने रहे भूस्खलन क्षेत्र।",
    "Reservoir rise: {a} to {b} km². Flooding: {c} to {d} km².":
        "जलाशयों की बढ़त: {a} से {b} वर्ग किमी। बाढ़: {c} से {d} वर्ग किमी।",
    "White pins are floods and landslides people reported. Radar sees water between buildings poorly, so the city reports were mostly missed: {h} of {o} reported floods had something nearby, no better than chance.":
        "सफ़ेद पिन लोगों की दर्ज की गई बाढ़ और भूस्खलन हैं। रडार इमारतों के बीच का पानी ठीक से नहीं देख पाता, इसलिए शहर की ज़्यादातर रिपोर्टें छूट गईं: {o} में से {h} दर्ज बाढ़ों के पास कुछ मिला, जो संयोग से बेहतर नहीं है।",
    "No better than chance: places nobody reported match {e} of {n}.":
        "संयोग से बेहतर नहीं: जिन जगहों पर किसी ने कुछ दर्ज नहीं किया, वे {n} में से {e} बार मिलती हैं।",
    "HV change (dB)":
        "HV बदलाव (dB)",
    "HH change (dB)":
        "HH बदलाव (dB)",
    "Coherence":
        "कोहेरेंस",
    "Coherence vs 1 km":
        "1 किमी की तुलना में कोहेरेंस",
    "Place names: © OpenStreetMap contributors (Nominatim). Zones are leads to check, not confirmed landslides.":
        "जगहों के नाम: © OpenStreetMap योगदानकर्ता (Nominatim)। क्षेत्र जाँचने लायक संकेत हैं, पुष्ट भूस्खलन नहीं।",
    "Dark water on each date, counted inside the area where the JRC record has seen water at least once (1984 to 2021), so rain-soaked fields are left out. Every point is the same orbit and radar mode; NISAR used a different mode on this orbit from 27 August to 2 October, so those passes are not shown.":
        "हर तारीख़ पर गहरा पानी, उस इलाक़े के भीतर गिना गया जहाँ JRC रिकॉर्ड ने कम से कम एक बार पानी देखा है (1984 से 2021), ताकि बारिश से भीगे खेत छूट जाएँ। हर बिंदु एक ही कक्षा और रडार मोड का है; 27 अगस्त से 2 अक्टूबर तक इस कक्षा पर निसार ने अलग मोड इस्तेमाल किया, इसलिए वे अवलोकन नहीं दिखाए गए।",
    "floods and landslides reported":
        "बाढ़ और भूस्खलन दर्ज हुए",
    "radar pass 1":
        "रडार अवलोकन 1",
    "radar pass 2":
        "रडार अवलोकन 2",
    "mm per day":
        "मिमी प्रति दिन",
    "water surface, km²":
        "पानी की सतह, वर्ग किमी",
    "Field check list for district teams, with radar images":
        "ज़िला दलों के लिए फ़ील्ड जाँच सूची, रडार तस्वीरों के साथ",
    "Technical page in English. The numbers and the story are in German on the other pages.":
        "तकनीकी पेज अंग्रेज़ी में है। आँकड़े और कहानी बाक़ी पेजों पर हिन्दी में हैं।",
    "Rainfall chart appears here once `data/reference/rainfall.csv` is added.":
        "`data/reference/rainfall.csv` जोड़ने पर बारिश का चार्ट यहाँ दिखेगा।",
    "NISAR's L-band radar (wavelength about 24 cm) works day and night, through cloud and rain.":
        "निसार का L-बैंड रडार (तरंगदैर्ध्य लगभग 24 सेमी) दिन-रात, बादल और बारिश के पार काम करता है।",
    "Surface area of Pune's rivers and reservoirs on each NISAR pass of this orbit":
        "इस कक्षा के हर निसार अवलोकन पर पुणे की नदियों और जलाशयों का सतही क्षेत्रफल",
    "Score adds three pieces of evidence":
        "अंक तीन प्रमाण जोड़ता है",
    "slide zones kept when the rule is re-run on NASA's NASADEM{h}.":
        "भूस्खलन क्षेत्र जो नासा के NASADEM पर नियम दोबारा चलाने पर भी बने रहे{h}।",
    ", including {a} of {b} high-confidence ones":
        ", इनमें {b} में से {a} उच्च भरोसे वाले",
    "better than chance: {c} of the {n} zones it covers were found again{e}{p}.":
        "संयोग से बेहतर: उसकी दृष्टि के {n} क्षेत्रों में से {c} फिर मिले{e}{p}।",
    ", chance gives {x}":
        ", संयोग से {x}",
    "Reported landslides":
        "दर्ज भूस्खलन",
    "radar could see had a slide zone nearby":
        "जिन्हें रडार देख सकता था, उनके पास भूस्खलन क्षेत्र मिला",
    "both near one zone, {z}":
        "दोनों एक ही क्षेत्र के पास, {z}",
    "none with NASADEM":
        "NASADEM के साथ एक भी नहीं",
    "{n} with NASADEM":
        "NASADEM के साथ {n}",
    "No better than chance ({e} of {n}): flooding between buildings hides from radar.":
        "संयोग से बेहतर नहीं ({n} में से {e}): इमारतों के बीच की बाढ़ रडार से छिप जाती है।",
    "that radar could see had a detection nearby.":
        "जिन्हें रडार देख सकता था, उनके पास कोई पहचान मिली।",
    "Try one of these":
        "इनमें से कोई आज़माएँ",
    "A one-minute flight over what NISAR found, on a model of the land.":
        "ज़मीन के एक मॉडल पर, निसार के नतीजों के ऊपर एक मिनट की उड़ान।",
    "Everything NISAR found around Pune: fly over it in 3D, or open the flat map for each zone's radar evidence.":
        "पुणे के आसपास निसार को जो कुछ मिला: 3D में उसके ऊपर उड़ें, या हर क्षेत्र के रडार प्रमाण के लिए सपाट नक्शा खोलें।",
    "3D view":
        "3D दृश्य",
    "Other formats":
        "अन्य फ़ॉर्मैट",
    "Fly over the findings":
        "नतीजों के ऊपर उड़ें",
    "A one-minute guide to every page":
        "हर पेज की एक मिनट की गाइड",
    "Finish":
        "समाप्त",
    "Close the tour":
        "टूर बंद करें",
    "{i} of {n}":
        "{n} में से {i}",
    "Welcome to MonsoonLens":
        "MonsoonLens में आपका स्वागत है",
    "In July 2026 cloud hid Pune from ordinary satellites. This app shows what NISAR's radar saw through it: new water, flooding and likely landslide zones.":
        "जुलाई 2026 में बादलों ने पुणे को साधारण उपग्रहों से छिपा दिया। यह ऐप दिखाता है कि निसार के रडार ने उनके पार क्या देखा: नया पानी, बाढ़ और संभावित भूस्खलन क्षेत्र।",
    "Six pages":
        "छह पेज",
    "Move between pages here. On a phone, open this menu with the arrow at the top left.":
        "यहाँ से पेज बदलें। फ़ोन पर यह मेन्यू ऊपर बाईं ओर के तीर से खोलें।",
    "Your language":
        "आपकी भाषा",
    "Read everything in English, Hindi, Marathi or German.":
        "सब कुछ अंग्रेज़ी, हिन्दी, मराठी या जर्मन में पढ़ें।",
    "Drag to turn the land. Press “Fly over the findings” for a one-minute flight to each one.":
        "ज़मीन घुमाने के लिए खींचें। हर नतीजे तक एक मिनट की उड़ान के लिए “नतीजों के ऊपर उड़ें” दबाएँ।",
    "The headline numbers":
        "मुख्य आँकड़े",
    "What the radar found. Each card says how sure we are.":
        "रडार को क्या मिला। हर कार्ड बताता है कि हम कितने आश्वस्त हैं।",
    "Every result is tested, and we show the tests that came out weak too.":
        "हर नतीजा परखा गया है, और जो जाँचें कमज़ोर निकलीं, वे भी हम दिखाते हैं।",
    "The story":
        "कहानी",
    "Six short chapters, from the rain to what radar could not see. Click a stop, or use the ← and → keys.":
        "बारिश से लेकर उस तक जो रडार नहीं देख सका, छह छोटे अध्याय। किसी पड़ाव पर क्लिक करें, या ← और → कुंजियाँ इस्तेमाल करें।",
    "Choose the 3D view, the flat map with radar evidence for each zone, or water through the season.":
        "3D दृश्य चुनें, हर क्षेत्र के रडार प्रमाण वाला सपाट नक्शा, या पूरे मौसम का पानी।",
    "Type your village or town to see what was found within 2, 5 or 10 km. Share the page link with others.":
        "अपना गाँव या शहर लिखें और देखें कि 2, 5 या 10 किमी के भीतर क्या मिला। पेज का लिंक दूसरों से साझा करें।",
    "For district teams":
        "ज़िला दलों के लिए",
    "Print the ranked list with radar images, or open it on a phone in Google Earth (KML), and go and check.":
        "रडार तस्वीरों वाली क्रमबद्ध सूची छापें, या फ़ोन पर गूगल अर्थ (KML) में खोलें, और जाकर जाँचें।",
    "How every number was made":
        "हर आँकड़ा कैसे बना",
    "The NISAR files, each step of the method, every check and the limits, for researchers and journalists.":
        "निसार फ़ाइलें, पद्धति का हर चरण, हर जाँच और सीमाएँ, शोधकर्ताओं और पत्रकारों के लिए।",
    "You are ready":
        "आप तैयार हैं",
    "Start with the story, or check your own village. You can take this tour again from the menu.":
        "कहानी से शुरू करें, या अपना गाँव जाँचें। यह टूर मेन्यू से फिर ले सकते हैं।",
    # method page, maps, downloads, credits
    "Radar could see it": "रडार इसे देख सकता था",
    "Every number in this app comes from the pipeline in our public repository, run on the NISAR files listed below. Nothing is estimated by hand, and every check is reported, including the ones that came out weak.":
        "इस ऐप का हर आँकड़ा हमारी सार्वजनिक रिपॉज़िटरी की पाइपलाइन से आता है, नीचे दी गई निसार फ़ाइलों पर चलाई गई। कुछ भी हाथ से अनुमानित नहीं है, और हर जाँच बताई गई है, कमज़ोर निकलीं वे भी।",
    "Mission facts: [ISRO, NISAR launch page](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) and [eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar). Tracks and times: the NISAR file names in the Data table.":
        "मिशन की जानकारी: [इसरो, निसार प्रक्षेपण पेज](https://www.isro.gov.in/Mission_GSLVF16_NISAR.html) और [eoPortal, NISAR](https://www.eoportal.org/satellite-missions/nisar)। ट्रैक और समय: डेटा तालिका में निसार फ़ाइलों के नाम।",
    "How radar sees through cloud":
        "रडार बादलों के पार कैसे देखता है",
    "NISAR's L-band radar has a wavelength of about 24 cm: it passes through cloud and rain, and partly through forest canopy. It sends two polarisations: HH (horizontal out, horizontal back) responds to surfaces and structures, HV (horizontal out, vertical back) mostly to vegetation.":
        "निसार के L-बैंड रडार की तरंगदैर्ध्य लगभग 24 सेमी है: यह बादल और बारिश के पार, और कुछ हद तक जंगल की छतरी के पार भी जाता है। यह दो ध्रुवीकरण भेजता है: HH (क्षैतिज जाकर, क्षैतिज लौटकर) सतहों और ढाँचों पर प्रतिक्रिया देता है, HV (क्षैतिज जाकर, ऊर्ध्वाधर लौटकर) मुख्यतः वनस्पति पर।",
    "yes":
        "हाँ",
    "no":
        "नहीं",
    "before, track 034":
        "पहले, ट्रैक 034",
    "after, track 034":
        "बाद में, ट्रैक 034",
    "coherence, track 034":
        "कोहेरेंस, ट्रैक 034",
    "second-track check, before, track 106":
        "दूसरे ट्रैक की जाँच, पहले, ट्रैक 106",
    "second-track check, after, track 106":
        "दूसरे ट्रैक की जाँच, बाद में, ट्रैक 106",
    "second-track check, coherence, track 106":
        "दूसरे ट्रैक की जाँच, कोहेरेंस, ट्रैक 106",
    "Data":
        "डेटा",
    "File":
        "फ़ाइल",
    "Valid share of box":
        "क्षेत्र का मान्य हिस्सा",
    "Link":
        "लिंक",
    "File names and data sources are kept as published, in English.":
        "फ़ाइलों के नाम और डेटा स्रोत प्रकाशित रूप में, अंग्रेज़ी में रखे गए हैं।",
    "The code is public, and the Pune crops of every NISAR file above are in the repository (a few MB each), so one command rebuilds every number, map and list in this app from them. Fetching the crops again from NASA's archive needs a free Earthdata login. The whole pipeline runs in about two minutes on a two-core computer.":
        "कोड सार्वजनिक है, और ऊपर की हर निसार फ़ाइल के पुणे वाले टुकड़े रिपॉज़िटरी में हैं (हर एक कुछ MB), इसलिए एक ही कमांड इस ऐप का हर आँकड़ा, नक्शा और सूची फिर से बना देती है। नासा के संग्रह से टुकड़े दोबारा लाने के लिए मुफ़्त Earthdata लॉगिन चाहिए। पूरी पाइपलाइन दो-कोर कंप्यूटर पर लगभग दो मिनट में चलती है।",
    "To point it at another place, change the study box and the NISAR files in `pipeline/config.py`.":
        "किसी और जगह के लिए `pipeline/config.py` में अध्ययन क्षेत्र और निसार फ़ाइलें बदलें।",
    "NISAR in brief":
        "निसार संक्षेप में",
    "How radar sees":
        "रडार कैसे देखता है",
    "Reproduce it":
        "दोबारा बनाएँ",
    "Team":
        "टीम",
    " and ":
        " और ",
    "Launched":
        "प्रक्षेपण",
    "30 July 2025 on ISRO's GSLV-F16, from Sriharikota, India":
        "30 जुलाई 2025, इसरो के GSLV-F16 से, श्रीहरिकोटा, भारत",
    "Orbit":
        "कक्षा",
    "Sun-synchronous, about 747 km up, inclined 98.4°":
        "सूर्य-समकालिक, लगभग 747 किमी ऊँचाई, 98.4° झुकी",
    "Repeat":
        "पुनरावृत्ति",
    "The same ground track every 12 days":
        "हर 12 दिन में वही ज़मीनी पथ",
    "Radars":
        "रडार",
    "L-band (NASA/JPL, 24 cm wavelength) and S-band (ISRO), sharing one 12 m mesh reflector":
        "L-बैंड (नासा/JPL, 24 सेमी तरंगदैर्ध्य) और S-बैंड (इसरो), एक ही 12 मीटर जालीदार परावर्तक साझा करते हुए",
    "Swath":
        "पट्टी की चौड़ाई",
    "242 km wide on the ground":
        "ज़मीन पर 242 किमी चौड़ी",
    "What this app uses":
        "यह ऐप क्या इस्तेमाल करता है",
    "L-band, tracks {t}, southbound evening passes ({u} UTC), level-2 GCOV and GUNW products":
        "L-बैंड, ट्रैक {t}, दक्षिण की ओर जाते शाम के अवलोकन ({u} UTC), लेवल-2 GCOV और GUNW उत्पाद",
    "Read the radar":
        "रडार पढ़ें",
    "Find the change":
        "बदलाव खोजें",
    "Check it":
        "जाँचें",
    "Hand it over":
        "सौंपें",
    "Water threshold":
        "पानी की सीमा",
    "Results table":
        "नतीजों की तालिका",
    "Sanity check: on {d} the radar saw **{p}** of the JRC permanent-water pixels as water. A low value would mean the threshold or the data is off.":
        "जाँच: {d} को रडार ने JRC के स्थायी-पानी वाले पिक्सलों में से **{p}** को पानी के रूप में देखा। कम मान का मतलब होता कि सीमा या डेटा में गड़बड़ है।",
    "Permanent water":
        "स्थायी पानी",
    "Elevation and slope":
        "ऊँचाई और ढलान",
    "Place names":
        "जगहों के नाम",
    "Provisional data":
        "अस्थायी डेटा",
    "These are NISAR provisional products (released from June 2026); calibration may still change.":
        "ये निसार के अस्थायी उत्पाद हैं (जून 2026 से जारी); कैलिब्रेशन अभी बदल सकता है।",
    "Two snapshots, twelve days apart":
        "बारह दिन के अंतर पर दो तस्वीरें",
    "Anything that flooded and drained between {b} and {a} is invisible.":
        "{b} और {a} के बीच जो पानी भरा और उतर गया, वह नहीं दिखता।",
    "Cities":
        "शहर",
    "Buildings make flooded streets bright, not dark. Our new-water map under-counts urban flooding.":
        "इमारतों के कारण बाढ़ वाली गलियाँ गहरी नहीं, चमकीली दिखती हैं। हमारा नए पानी का नक्शा शहरी बाढ़ कम गिनता है।",
    "Pixel size":
        "पिक्सल का आकार",
    "{r} m pixels. Slides narrower than about two pixels are easily missed.":
        "{r} मीटर के पिक्सल। लगभग दो पिक्सल से संकरे भूस्खलन आसानी से छूट जाते हैं।",
    "Same-mode rule":
        "एक ही मोड का नियम",
    "From 27 August to 2 October NISAR imaged this track in a different mode (2005, quad-pol); 14 October is back in the July mode. Brightness is only compared between passes with the same track, mode and polarisation.":
        "27 अगस्त से 2 अक्टूबर तक निसार ने इस ट्रैक को अलग मोड (2005, क्वाड-पोल) में देखा; 14 अक्टूबर को फिर जुलाई वाला मोड। चमक की तुलना केवल एक ही ट्रैक, मोड और ध्रुवीकरण वाले अवलोकनों के बीच होती है।",
    "Water areas may be underestimates":
        "पानी का क्षेत्रफल कम आँका गया हो सकता है",
    "On {d} only {p} of the area the JRC record marks as permanent water looked dark enough to pass our water test. Part of that is reservoirs drawn down before the monsoon; part is water roughened by wind or rain, which our test misses.":
        "{d} को JRC रिकॉर्ड में स्थायी पानी वाले क्षेत्र का केवल {p} हिस्सा हमारी पानी की जाँच पास करने लायक गहरा दिखा। इसका कुछ हिस्सा मानसून से पहले खाली हुए जलाशय हैं; कुछ हवा या बारिश से खुरदरा हुआ पानी, जिसे हमारी जाँच नहीं पकड़ती।",
    "Small samples":
        "छोटे नमूने",
    "Every check is counted, not turned into an accuracy: floods {fh} of {fo}, landslides {sh} of {so}, and the second-track check covers only part of the area.":
        "हर जाँच गिनी गई है, सटीकता में नहीं बदली गई: बाढ़ {fo} में से {fh}, भूस्खलन {so} में से {sh}, और दूसरे ट्रैक की जाँच क्षेत्र का केवल कुछ हिस्सा ही देखती है।",
    "Flood area is threshold-sensitive":
        "बाढ़ का क्षेत्रफल सीमा पर निर्भर",
    "The flood figure can move several-fold with a 1 dB change in the water threshold; the reservoir rise much less (see the water-threshold check).":
        "पानी की सीमा में 1 dB बदलाव से बाढ़ का आँकड़ा कई गुना बदल सकता है; जलाशयों की बढ़त बहुत कम (पानी की सीमा वाली जाँच देखें)।",
    "Slope near the limits":
        "सीमाओं के पास ढलान",
    "Many zones sit close to the {a}° or {b}° limits, so a different elevation map moves some of them in or out (see the elevation-map check).":
        "कई क्षेत्र {a}° या {b}° की सीमाओं के पास हैं, इसलिए अलग ऊँचाई नक्शा उनमें से कुछ को अंदर या बाहर कर देता है (ऊँचाई नक्शे वाली जाँच देखें)।",
    "Leads, not verdicts":
        "संकेत, फ़ैसले नहीं",
    "Slide zones are places to check, not confirmed landslides: {u} of {z} have no reported event within 2 km.":
        "भूस्खलन क्षेत्र जाँचने की जगहें हैं, पुष्ट भूस्खलन नहीं: {z} में से {u} के 2 किमी के भीतर कोई दर्ज घटना नहीं है।",
    "Rainfall":
        "बारिश",
    "GPM IMERG Late Run, averaged over the whole study area per UTC day. It is lower than the single-station totals quoted in the news, and may shift slightly when the Final Run is released.":
        "GPM IMERG Late Run, हर UTC दिन के लिए पूरे अध्ययन क्षेत्र का औसत। यह ख़बरों में बताए किसी एक केंद्र के आँकड़ों से कम है, और Final Run आने पर थोड़ा बदल सकता है।",
    ". Landslides: {h} of {o}.":
        "। भूस्खलन: {o} में से {h}।",
    "Floods: **{fh} of {fo}** reports that radar could observe had a detection nearby. Landslides: **{sh} of {so}**. Counts, not an accuracy: the samples are small.":
        "बाढ़: रडार जिन्हें देख सकता था, उन **{fo} में से {fh}** रिपोर्टों के पास कोई पहचान मिली। भूस्खलन: **{so} में से {sh}**। ये गिनतियाँ हैं, सटीकता नहीं: नमूने छोटे हैं।",
    "Runs once reported events are added.":
        "दर्ज घटनाएँ जुड़ने पर चलता है।",
    "an independent NISAR orbit re-found {c} of the {n} zones it could see, {l}× more often than chance. A small sample, so support, not proof.":
        "एक स्वतंत्र निसार कक्षा ने अपनी दृष्टि के {n} क्षेत्रों में से {c} फिर पाए, संयोग से {l}× अधिक बार। नमूना छोटा है, इसलिए यह समर्थन है, प्रमाण नहीं।",
    "Same slide rule, run on NISAR track {t} ({b} to {a}). A track-034 zone counts as **found again** when a track-{t} zone lies within {m} m (allowing for small position differences between orbits). **Partial** means only one piece of the evidence is there (coherence loss or the backscatter jump): that alone is common in the monsoon, so we do not count it.":
        "वही भूस्खलन नियम, निसार ट्रैक {t} पर चलाया गया ({b} से {a})। ट्रैक-034 का कोई क्षेत्र तब **फिर मिला** माना जाता है जब ट्रैक-{t} का कोई क्षेत्र {m} मीटर के भीतर हो (कक्षाओं के बीच छोटे स्थान-अंतर की छूट)। **आंशिक** का मतलब है कि प्रमाण का केवल एक हिस्सा है (कोहेरेंस में गिरावट या परावर्तन में उछाल): मानसून में यह अकेले आम है, इसलिए हम इसे नहीं गिनते।",
    "Runs once the track-106 files are cropped.":
        "ट्रैक-106 की फ़ाइलें काटने के बाद चलता है।",
    "{f} of {z} zones survive when slope comes from NASA's NASADEM, including {hf} of {hz} high-confidence ones.":
        "ढलान नासा के NASADEM से लेने पर {z} में से {f} क्षेत्र बने रहते हैं, इनमें {hz} में से {hf} उच्च भरोसे वाले।",
    "Slope and slope direction decide where the slide rule looks, so we ran it again on the same radar pair with NASA's NASADEM elevation map instead of Copernicus. Overall the two slope maps agree closely (median difference {d}°). Near the {a}° and {b}° limits they do not: of the ground that either map puts inside that band, the other map puts {p} outside it.":
        "ढलान और ढलान की दिशा तय करती हैं कि भूस्खलन नियम कहाँ देखे, इसलिए हमने इसे उसी रडार जोड़ी पर Copernicus की जगह नासा के NASADEM ऊँचाई नक्शे के साथ दोबारा चलाया। कुल मिलाकर दोनों ढलान नक्शे काफ़ी मेल खाते हैं (माध्यिका अंतर {d}°)। {a}° और {b}° की सीमाओं के पास नहीं: जो ज़मीन कोई एक नक्शा उस पट्टी में रखता है, उसका {p} हिस्सा दूसरा नक्शा बाहर रखता है।",
    "**{f} of {z}** zones are found again within {m} m, including **{hf} of {hz}** high-confidence zones. NASADEM also finds {nw} zones of its own.":
        "**{z} में से {f}** क्षेत्र {m} मीटर के भीतर फिर मिलते हैं, इनमें **{hz} में से {hf}** उच्च भरोसे वाले। NASADEM अपने {nw} क्षेत्र भी खोजता है।",
    "Steeper than 45°":
        "45° से ज़्यादा खड़ी",
    "Gentler than 15°":
        "15° से हल्की",
    "Radar layover or shadow":
        "रडार लेओवर या छाया",
    "Near the edge of the slope band":
        "ढलान सीमा के किनारे के पास",
    "the reservoir rise holds up ({a} to {b} km²); the flood area does not ({c} to {d} km²), so read it as an order of magnitude.":
        "जलाशयों की बढ़त टिकती है ({a} से {b} वर्ग किमी); बाढ़ का क्षेत्रफल नहीं ({c} से {d} वर्ग किमी), इसलिए इसे केवल परिमाण का अंदाज़ा मानें।",
    "The water threshold is set from the radar itself on each date. Moving both dates' thresholds 1 dB down or up, and changing nothing else, keeps reservoir and river rise between **{a} and {b} km²** (we report {r}). Flooding on ground that was never wet swings from **{c} to {d} km²** (we report {f}): that figure depends heavily on the threshold, so read it as the order of magnitude, not a precise area.":
        "पानी की सीमा हर तारीख़ पर रडार से ही तय होती है। दोनों तारीख़ों की सीमा 1 dB नीचे या ऊपर करने पर, और कुछ न बदलने पर, जलाशयों और नदियों की बढ़त **{a} से {b} वर्ग किमी** के बीच रहती है (हम {r} बताते हैं)। कभी न भीगी ज़मीन पर बाढ़ **{c} से {d} वर्ग किमी** तक बदलती है (हम {f} बताते हैं): यह आँकड़ा सीमा पर बहुत निर्भर है, इसलिए इसे सटीक क्षेत्रफल नहीं, परिमाण का अंदाज़ा मानें।",
    "Roads and railways near each zone":
        "हर क्षेत्र के पास सड़कें और रेल लाइनें",
    "Elevation, second-map check":
        "ऊँचाई, दूसरे नक्शे की जाँच",
    "Daily rainfall":
        "दैनिक बारिश",
    "Cut the radar to Pune":
        "रडार को पुणे तक काटें",
    "NISAR's level-2 GCOV files hold radar brightness (gamma-nought, already corrected for terrain) on a map grid. A full frame is about 5 GB per layer, so we stream only the study box (lon {w} to {e}, lat {s} to {n}) and average 2 × 2 or more native pixels into a {r} m grid. Averaging reduces radar speckle; a Lee filter removes more.":
        "निसार की लेवल-2 GCOV फ़ाइलों में नक्शा-ग्रिड पर रडार की चमक (गामा-नॉट, भू-भाग के लिए पहले से सुधारी गई) होती है। एक पूरा फ़्रेम हर परत के लिए लगभग 5 GB का होता है, इसलिए हम केवल अध्ययन क्षेत्र (देशांतर {w} से {e}, अक्षांश {s} से {n}) स्ट्रीम करते हैं और 2 × 2 या अधिक मूल पिक्सलों का औसत लेकर {r} मीटर का ग्रिड बनाते हैं। औसत से रडार का धब्बापन घटता है; ली फ़िल्टर और कम करता है।",
    "Find water on each date":
        "हर तारीख़ पर पानी खोजें",
    "Smooth water reflects the radar away and looks dark in HH. The cut-off between water and land is set separately for each date with the minimum-error method of Kittler and Illingworth, trained on reservoir and river cores that the JRC Global Surface Water record says are water at least {o}% of the time, plus an equal number of land pixels. In these NISAR products open water sits near −16 dB and dry land near −5 dB.":
        "चिकना पानी रडार को दूर परावर्तित करता है और HH में गहरा दिखता है। पानी और ज़मीन के बीच की सीमा हर तारीख़ के लिए अलग से किटलर और इलिंगवर्थ की न्यूनतम-त्रुटि पद्धति से तय होती है, जलाशयों और नदियों के उन मध्य हिस्सों पर प्रशिक्षित जो JRC ग्लोबल सरफ़ेस वॉटर के अनुसार कम से कम {o}% समय पानी रहते हैं, उतने ही ज़मीन के पिक्सलों के साथ। इन निसार उत्पादों में खुला पानी लगभग −16 dB और सूखी ज़मीन लगभग −5 dB पर होती है।",
    "Keep only new water":
        "केवल नया पानी रखें",
    "A pixel is new water if it is water on {a} but not on {b}, clearly darker, outside permanent water, on flat ground, and part of a patch big enough not to be speckle.":
        "कोई पिक्सल नया पानी है अगर वह {a} को पानी है पर {b} को नहीं, साफ़ तौर पर गहरा है, स्थायी पानी से बाहर है, समतल ज़मीन पर है, और इतने बड़े हिस्से का भाग है कि धब्बा न हो।",
    "Flag possible hidden water":
        "छिपे संभावित पानी को चिह्नित करें",
    "At L-band, water under trees or between buildings makes the radar bounce twice and come back brighter. Flat ground that got brighter is shown as possible water, and never added to flood totals.":
        "L-बैंड पर पेड़ों के नीचे या इमारतों के बीच का पानी रडार को दो बार उछालता है और वह ज़्यादा चमकीला लौटता है। जो समतल ज़मीन चमकीली हुई, उसे संभावित पानी के रूप में दिखाया जाता है, और बाढ़ के कुल आँकड़े में कभी नहीं जोड़ा जाता।",
    "Find likely slide zones":
        "संभावित भूस्खलन क्षेत्र खोजें",
    "Outside the radar's layover and shadow, a zone needs all three: the ground stopped matching itself between passes (coherence, from the NISAR GUNW product); it lost much more coherence than its own 1 km neighbourhood, because monsoon vegetation lowers coherence everywhere; and the radar brightness jumped, from rough debris (HH up) or stripped vegetation (HV down), measured against the scene's own median change on dry land. Each zone gets a 0 to 1 score from slope, radar change and coherence loss.":
        "रडार के लेओवर और छाया से बाहर, किसी क्षेत्र को तीनों चाहिए: दो अवलोकनों के बीच ज़मीन पहले जैसी नहीं रही (कोहेरेंस, निसार GUNW उत्पाद से); उसने अपने 1 किमी के आसपास से कहीं ज़्यादा कोहेरेंस खोया, क्योंकि मानसून की वनस्पति हर जगह कोहेरेंस घटाती है; और रडार की चमक उछली, खुरदरे मलबे से (HH ऊपर) या हटी वनस्पति से (HV नीचे), सूखी ज़मीन पर दृश्य के अपने माध्यिका बदलाव की तुलना में। हर क्षेत्र को ढलान, रडार बदलाव और कोहेरेंस में गिरावट से 0 से 1 तक अंक मिलता है।",
    "Check against reports":
        "रिपोर्टों से मिलान करें",
    "Reported floods and landslides, from the news and official sources, each linked, are matched to detections nearby, or within the report's own location precision if that is larger.":
        "ख़बरों और आधिकारिक स्रोतों से दर्ज बाढ़ और भूस्खलन, हर एक का लिंक दिया गया, पास की पहचानों से मिलाए जाते हैं, या रिपोर्ट की अपनी स्थान-सटीकता के भीतर, अगर वह बड़ी हो।",
    "Check with a second track":
        "दूसरे ट्रैक से जाँचें",
    "The same slide rule runs on an independent NISAR pair from another orbit, which also spans the rain peak. A real slope failure changes the ground for good, so it should show in both; speckle or a geometry artefact of one orbit usually does not. Chance level comes from moving every zone to random steep, dry places and repeating the test.":
        "वही भूस्खलन नियम दूसरी कक्षा की एक स्वतंत्र निसार जोड़ी पर चलता है, जो बारिश के चरम को भी घेरती है। असली ढलान खिसकना ज़मीन को हमेशा के लिए बदल देता है, इसलिए वह दोनों में दिखना चाहिए; किसी एक कक्षा का धब्बापन या ज्यामिति की गड़बड़ी आमतौर पर नहीं दिखती। संयोग का स्तर हर क्षेत्र को बेतरतीब खड़ी, सूखी जगहों पर खिसकाकर और जाँच दोहराकर मिलता है।",
    "Check with a second elevation map":
        "दूसरे ऊँचाई नक्शे से जाँचें",
    "Slope and slope direction come from the Copernicus GLO-30 elevation map. We run the same slide rule again with NASA's NASADEM elevation map and record which zones it keeps.":
        "ढलान और ढलान की दिशा Copernicus GLO-30 ऊँचाई नक्शे से आती हैं। हम वही भूस्खलन नियम नासा के NASADEM ऊँचाई नक्शे के साथ दोबारा चलाते हैं और दर्ज करते हैं कि कौन से क्षेत्र बने रहे।",
    "Test the water threshold":
        "पानी की सीमा परखें",
    "Both dates' water thresholds are moved 1 dB down and up and the water numbers are recomputed, to show how much they depend on that one choice.":
        "दोनों तारीख़ों की पानी की सीमाएँ 1 dB नीचे और ऊपर की जाती हैं और पानी के आँकड़े दोबारा निकाले जाते हैं, यह दिखाने के लिए कि वे उस एक चुनाव पर कितने निर्भर हैं।",
    "Package the evidence":
        "प्रमाण तैयार करें",
    "For every slide zone and flood patch the pipeline cuts small image chips of that spot from the NISAR data (radar colour before and after, and coherence), notes the nearest reported event, and writes the field check list as a printable page, KML, CSV and GeoJSON.":
        "हर भूस्खलन क्षेत्र और बाढ़ वाले हिस्से के लिए पाइपलाइन निसार डेटा से उस जगह की छोटी तस्वीरें काटती है (पहले और बाद का रडार रंग, और कोहेरेंस), सबसे नज़दीकी दर्ज घटना लिखती है, और फ़ील्ड जाँच सूची को छापने लायक पेज, KML, CSV और GeoJSON के रूप में लिखती है।",
    "radar found something near {h} of {o} reported floods it could see":
        "रडार जिन दर्ज बाढ़ों को देख सकता था, उनमें से {o} में से {h} के पास उसे कुछ मिला",
    "How the chance level is worked out: a report counts as matched when new water or a possible-water patch lies within its tolerance (the larger of the report's location precision and 500 m). For each report we take the share of a reference set that has a detection within that same tolerance, and add the shares up. Flat ground: every 40 m pixel with radar data on both dates, outside permanent water, slope ≤ 5° ({km} km²). Settlements: {p} OpenStreetMap villages, towns and suburbs with radar data. Getting {k} or more by chance has a probability of {pf} on flat ground and {ps} at settlements (exact, no random draws).":
        "संयोग का स्तर ऐसे निकाला गया: कोई रिपोर्ट तब मिलान वाली मानी जाती है जब नया पानी या संभावित-पानी का हिस्सा उसकी सहन-सीमा के भीतर हो (रिपोर्ट की स्थान-सटीकता और 500 मीटर में से बड़ा)। हर रिपोर्ट के लिए हम संदर्भ समूह का वह हिस्सा लेते हैं जिसके उसी सहन-सीमा के भीतर कोई पहचान है, और उन हिस्सों को जोड़ते हैं। समतल ज़मीन: दोनों तारीख़ों पर रडार डेटा वाला हर 40 मीटर पिक्सल, स्थायी पानी से बाहर, ढलान ≤ 5° ({km} वर्ग किमी)। बस्तियाँ: रडार डेटा वाले {p} OpenStreetMap गाँव, शहर और उपनगर। संयोग से {k} या अधिक मिलने की संभावना समतल ज़मीन पर {pf} और बस्तियों पर {ps} है (सटीक, कोई बेतरतीब चयन नहीं)।",
    "Track {t} sees only {c} of the study area, so only {n} of our zones could be checked. That is a small sample: treat it as support, not proof.":
        "ट्रैक {t} अध्ययन क्षेत्र का केवल {c} देखता है, इसलिए हमारे केवल {n} क्षेत्र जाँचे जा सके। यह छोटा नमूना है: इसे समर्थन मानें, प्रमाण नहीं।",
    "Between {b} and {a} the whole scene got about {h} dB darker in HH and {v} dB in HV, on flat and steep ground alike: ground and plants drying after the storm, or calibration of these provisional products. A landslide is a local change, so on both tracks we measure change against the scene's own median change on dry land.":
        "{b} और {a} के बीच पूरा दृश्य HH में लगभग {h} dB और HV में {v} dB गहरा हुआ, समतल और खड़ी ज़मीन पर एक जैसा: तूफ़ान के बाद ज़मीन और पौधों का सूखना, या इन अस्थायी उत्पादों का कैलिब्रेशन। भूस्खलन एक स्थानीय बदलाव है, इसलिए दोनों ट्रैकों पर हम बदलाव को सूखी ज़मीन पर दृश्य के अपने माध्यिका बदलाव से तुलना करके नापते हैं।",
    "Water areas from track {t} are not used: on {b}, in heavy rain, the radar saw less than half of the permanent reservoirs as dark water, because rain roughens the surface.":
        "ट्रैक {t} से पानी का क्षेत्रफल इस्तेमाल नहीं किया गया: {b} को, भारी बारिश में, रडार ने स्थायी जलाशयों के आधे से भी कम हिस्से को गहरे पानी के रूप में देखा, क्योंकि बारिश सतह को खुरदरा कर देती है।",
    "Passing both extra checks (found again by the second NISAR track and with NASADEM): **{z}**.":
        "दोनों अतिरिक्त जाँचें पास करने वाले (दूसरे निसार ट्रैक और NASADEM, दोनों से फिर मिले): **{z}**।",
    "{r} m grid":
        "{r} मीटर ग्रिड",
    "Lee filter":
        "ली फ़िल्टर",
    "threshold kept within {a} to {b} dB":
        "सीमा {a} से {b} dB के भीतर",
    "one threshold per date":
        "हर तारीख़ की एक सीमा",
    "≥ {d} dB darker":
        "≥ {d} dB गहरा",
    "JRC occurrence < {o}%":
        "JRC आवृत्ति < {o}%",
    "slope < {s}°":
        "ढलान < {s}°",
    "≥ {p} pixels":
        "≥ {p} पिक्सल",
    "≥ {d} dB brighter":
        "≥ {d} dB चमकीला",
    "shown hatched, never counted":
        "धारियों में दिखाया, कभी नहीं गिना",
    "slope {a}° to {b}°":
        "ढलान {a}° से {b}°",
    "coherence < {c}":
        "कोहेरेंस < {c}",
    "< 0.6 × its 1 km surroundings":
        "< अपने 1 किमी आसपास का 0.6 ×",
    "floods: 500 m":
        "बाढ़: 500 मीटर",
    "slides: 750 m":
        "भूस्खलन: 750 मीटर",
    "{n} reports":
        "{n} रिपोर्टें",
    "track 106":
        "ट्रैक 106",
    "3 to 15 July":
        "3 से 15 जुलाई",
    "random-placement baseline":
        "बेतरतीब स्थान वाला आधार",
    "1.9 km image chips":
        "1.9 किमी की तस्वीरें",
    "In short:":
        "संक्षेप में:",
    ", but places nobody reported score {e}: no better than chance":
        ", पर जिन जगहों पर किसी ने कुछ दर्ज नहीं किया, वे {e} पर आती हैं: संयोग से बेहतर नहीं",
    "Are the flood matches better than chance?":
        "क्या बाढ़ के मिलान संयोग से बेहतर हैं?",
    "the nearest mapped new open water is {lo} to {hi} km from every reported flood.":
        "हर दर्ज बाढ़ से सबसे नज़दीकी नक्शे पर आया नया खुला पानी {lo} से {hi} किमी दूर है।",
    "The count above differs from the {h} of {o} in the headline and the table below: a report's location was corrected after the last full pipeline run. The two will agree after the next run.":
        "ऊपर की गिनती शीर्ष और नीचे की तालिका के {o} में से {h} से अलग है: आख़िरी पूरे पाइपलाइन रन के बाद एक रिपोर्ट का स्थान सुधारा गया। अगले रन के बाद दोनों मेल खाएँगी।",
    "Every reported event":
        "हर दर्ज घटना",
    "The chance of doing this well by luck alone is about {p} (one-sided binomial test).":
        "केवल किस्मत से इतना अच्छा होने की संभावना लगभग {p} है (एकतरफ़ा द्विपद परीक्षण)।",
    "Our zones were found again about as often as chance ({l}×), so single-track zones need ground checks before anyone relies on them.":
        "हमारे क्षेत्र लगभग संयोग जितनी ही बार फिर मिले ({l}×), इसलिए एक ट्रैक वाले क्षेत्रों पर भरोसा करने से पहले ज़मीन पर जाँच ज़रूरी है।",
    "With NASADEM, {k} of {n} reports have a zone within range. So treat the landslide matches as weak support.":
        "NASADEM के साथ {n} में से {k} रिपोर्टों के दायरे में कोई क्षेत्र है। इसलिए भूस्खलन के मिलानों को कमज़ोर समर्थन मानें।",
    "On this page":
        "इस पेज पर",
    "source":
        "स्रोत",
    "Found again":
        "फिर मिले",
    "Partial":
        "आंशिक",
    "Not seen":
        "नहीं दिखे",
    "Not covered by track 106":
        "ट्रैक 106 से बाहर",
    "Found-again rate":
        "फिर मिलने की दर",
    "Our zones":
        "हमारे क्षेत्र",
    "Same zones moved to random steep places ({n} trials)":
        "वही क्षेत्र बेतरतीब खड़ी जगहों पर खिसकाए गए ({n} प्रयास)",
    "The chance of doing this well by luck alone is under 1%.":
        "केवल किस्मत से इतना अच्छा होने की संभावना 1% से कम है।",
    "Our zones were found again **{l}× more often than chance**.":
        "हमारे क्षेत्र **संयोग से {l}× अधिक बार** फिर मिले।",
    "By confidence:":
        "भरोसे के अनुसार:",
    "Not found with NASADEM because":
        "NASADEM के साथ न मिलने का कारण",
    "Zones":
        "क्षेत्र",
    "Threshold shift":
        "सीमा में बदलाव",
    "Threshold {d} (dB)":
        "सीमा {d} (dB)",
    "New water (km²)":
        "नया पानी (वर्ग किमी)",
    "Reservoir and river rise (km²)":
        "जलाशयों और नदियों की बढ़त (वर्ग किमी)",
    "Flooding (km²)":
        "बाढ़ (वर्ग किमी)",
    "Flood patches":
        "बाढ़ वाले हिस्से",
    "Permanent water seen dark":
        "गहरा दिखा स्थायी पानी",
    "Report":
        "रिपोर्ट",
    "Tolerance (m)":
        "सहन-सीमा (मीटर)",
    "Nearest detection (m)":
        "सबसे नज़दीकी पहचान (मीटर)",
    "Matched":
        "मिलान",
    "Nearest new open water (km)":
        "सबसे नज़दीकी नया खुला पानी (किमी)",
    "Flat ground within tolerance of a detection":
        "पहचान की सहन-सीमा में समतल ज़मीन",
    "Settlements within tolerance of a detection":
        "पहचान की सहन-सीमा में बस्तियाँ",
    "{c}: {f} of {n} found again":
        "{c}: {n} में से {f} फिर मिले",
    "The {n} reported landslides we matched ({ids}) are all matched to the same zone, {z}, {d} away.":
        "हमने जिन {n} दर्ज भूस्खलनों का मिलान किया ({ids}), वे सब एक ही क्षेत्र {z} से जुड़े हैं, {d} दूर।",
    "The {n} reported landslides we matched are {d} from their nearest zone.":
        "हमने जिन {n} दर्ज भूस्खलनों का मिलान किया, वे अपने सबसे नज़दीकी क्षेत्र से {d} दूर हैं।",
    "as chosen":
        "जैसा चुना",
    "With the reports as they stand now, **{k} of {n}** reported floods have a detection within their tolerance. The same rule applied to places nobody reported gives **{a} of {n}** on random flat ground and **{b} of {n}** at a random village, town or suburb.":
        "मौजूदा रिपोर्टों के अनुसार **{n} में से {k}** दर्ज बाढ़ों की सहन-सीमा में कोई पहचान है। वही नियम उन जगहों पर लगाने से, जहाँ किसी ने कुछ दर्ज नहीं किया, बेतरतीब समतल ज़मीन पर **{n} में से {a}** और किसी बेतरतीब गाँव, शहर या उपनगर में **{n} में से {b}** मिलता है।",
    "All {k} matches are to \"possible water under cover\" patches, which we show but never count as flood;":
        "सभी {k} मिलान \"ढके हुए संभावित पानी\" वाले हिस्सों से हैं, जिन्हें हम दिखाते हैं पर बाढ़ में कभी नहीं गिनते;",
    "So the flood count is what chance alone would give: it is not evidence that the map finds reported floods.":
        "इसलिए बाढ़ की गिनती उतनी ही है जितनी केवल संयोग से मिलती: यह इस बात का प्रमाण नहीं कि नक्शा दर्ज बाढ़ें खोजता है।",
    "**Yes.**":
        "**हाँ।**",
    "**No.**":
        "**नहीं।**",
    "GeoTIFFs are on the analysis grid (UTM zone 43N, 40 m). GeoJSON is in WGS84.":
        "GeoTIFF विश्लेषण ग्रिड पर हैं (UTM ज़ोन 43N, 40 मीटर)। GeoJSON WGS84 में है।",
    "all new water (GeoTIFF)":
        "सारा नया पानी (GeoTIFF)",
    "flooding only, never water before (GeoTIFF)":
        "केवल बाढ़, पहले कभी पानी नहीं (GeoTIFF)",
    "possible water under trees or buildings (GeoTIFF)":
        "पेड़ों या इमारतों के नीचे संभावित पानी (GeoTIFF)",
    "likely slide zones (GeoTIFF)":
        "संभावित भूस्खलन क्षेत्र (GeoTIFF)",
    "HH radar change in dB (GeoTIFF)":
        "HH रडार बदलाव, dB में (GeoTIFF)",
    "slide zones with scores and nearest place (GeoJSON)":
        "अंकों और सबसे नज़दीकी जगह के साथ भूस्खलन क्षेत्र (GeoJSON)",
    "new-water patches, flood and reservoir rise (GeoJSON)":
        "नए पानी के हिस्से, बाढ़ और जलाशयों की बढ़त (GeoJSON)",
    "reported events, matched or missed, with reasons (CSV)":
        "दर्ज घटनाएँ, मिलीं या छूटीं, कारणों सहित (CSV)",
    "water areas and thresholds (CSV)":
        "पानी के क्षेत्रफल और सीमाएँ (CSV)",
    "second-track check results (JSON)":
        "दूसरे ट्रैक की जाँच के नतीजे (JSON)",
    "elevation-map check results (JSON)":
        "ऊँचाई नक्शे की जाँच के नतीजे (JSON)",
    "every number in this app (JSON)":
        "इस ऐप का हर आँकड़ा (JSON)",
    "not checked":
        "जाँचा नहीं गया",
    "NISAR radar image of {f}":
        "{f} की निसार रडार तस्वीर",
    "Radar image":
        "रडार तस्वीर",
    "Compare {a} and {b}":
        "{a} और {b} की तुलना करें",
    "{id}: likely slide zone ({c}), {n}":
        "{id}: संभावित भूस्खलन क्षेत्र ({c}), {n}",
    "Radar colour, 28 Jun":
        "रडार रंग, 28 जून",
    "Radar colour, 10 Jul":
        "रडार रंग, 10 जुलाई",
    "Radar HH, 28 Jun":
        "रडार HH, 28 जून",
    "Radar HH, 10 Jul":
        "रडार HH, 10 जुलाई",
    "Change in HH (blue darker, red brighter)":
        "HH में बदलाव (नीला गहरा, लाल चमकीला)",
    "Coherence 28 Jun to 10 Jul (dark = changed)":
        "कोहेरेंस 28 जून से 10 जुलाई (गहरा = बदला)",
    "Rivers and reservoirs (JRC)":
        "नदियाँ और जलाशय (JRC)",
    "Possible water under cover":
        "ढका हुआ संभावित पानी",
    "Reservoirs and rivers rising":
        "बढ़ते जलाशय और नदियाँ",
    "Flooding (no water recorded here 1984 to 2021)":
        "बाढ़ (यहाँ 1984 से 2021 तक पानी दर्ज नहीं)",
    "Likely slide zones ({n})":
        "संभावित भूस्खलन क्षेत्र ({n})",
    "; also found by a second NISAR track":
        "; दूसरे निसार ट्रैक ने भी पाया",
    "Flood patches ({n})":
        "बाढ़ वाले हिस्से ({n})",
    "Reported events ({n})":
        "दर्ज घटनाएँ ({n})",
    "Score (0-1)":
        "अंक (0-1)",
    "Mean slope (°)":
        "औसत ढलान (°)",
    "Coherence vs 1 km area":
        "1 किमी आसपास की तुलना में कोहेरेंस",
    "With NASA's NASADEM elevation map":
        "नासा के NASADEM ऊँचाई नक्शे के साथ",
    "Second NISAR track (3-15 Jul)":
        "दूसरा निसार ट्रैक (3-15 जुलाई)",
    "Radar detection nearby":
        "पास में रडार पहचान",
    "No radar detection nearby":
        "पास में कोई रडार पहचान नहीं",
    "Radar could not observe this":
        "रडार इसे देख नहीं सकता था",
    "Study box":
        "अध्ययन क्षेत्र",
    "Study box (NISAR crop)":
        "अध्ययन क्षेत्र (निसार का टुकड़ा)",
    "Flood water on 10 July: {a} ha, {d} dB darker":
        "10 जुलाई को बाढ़ का पानी: {a} हेक्टेयर, {d} dB गहरा",
    ", near {n}":
        ", {n} के पास",
    "{a} to {b}":
        "{a} से {b}",
    "Team iGenfinity, NASA Space Apps Challenge 2026, GDG Ahlen.":
        "टीम iGenfinity, नासा स्पेस ऐप्स चैलेंज 2026, GDG आलेन।",
    "App and integration":
        "ऐप और एकीकरण",
    "Data and science":
        "डेटा और विज्ञान",
    "Validation, story and pitch":
        "सत्यापन, कहानी और पिच",
    "Radar: {n} NISAR L2 provisional files, tracks {t}, {w} (NASA/JPL-Caltech and ISRO, via ASF DAAC); every file is linked on the Method page. Results built {g}, pipeline v{v}.":
        "रडार: {n} अस्थायी निसार L2 फ़ाइलें, ट्रैक {t}, {w} (नासा/JPL-Caltech और इसरो, ASF DAAC के ज़रिए); हर फ़ाइल का लिंक पद्धति पेज पर है। नतीजे बने {g}, पाइपलाइन v{v}।",
    "iGenfinity team logo":
        "टीम iGenfinity का लोगो",
    "matched to a detection":
        "पहचान से मिलान हुआ",
    "Random flat ground":
        "बेतरतीब समतल ज़मीन",
    "expected by chance":
        "संयोग से अपेक्षित",
    "Random settlements":
        "बेतरतीब बस्तियाँ",
    "matches out of {n} reported floods":
        "{n} दर्ज बाढ़ों में से मिलान",
}

HI_T = {
    "title":
        "2026 के पुणे मानसून में निसार रडार ने क्या देखा",
    "lede":
        "जब लोगों को ज़मीन देखने की सबसे ज़्यादा ज़रूरत होती है, तभी मानसून के बादल उसे उपग्रहों से छिपा लेते हैं। {cloud} नासा और इसरो का निसार उपग्रह रडार से बादलों के पार देखता है। हमने 3 से 8 जुलाई 2026 की बाढ़ और भूस्खलन से पहले और बाद के उसके अवलोकनों की तुलना की।",
    "dates_line":
        "पुणे ज़िले, भारत के ऊपर निसार L-बैंड रडार के दो अवलोकन: {b} और {a} {y}",
    "found":
        "रडार को क्या मिला",
    "new_water":
        "नदियों और जलाशयों से बाहर, समतल ज़मीन पर नया खुला पानी",
    "rise":
        "पुणे के जलाशयों और नदियों के बढ़ने और भरने से आया नया पानी",
    "flood":
        "10 जुलाई को अब भी खड़ा बाढ़ का पानी, जहाँ 1984 से 2021 तक कभी पानी दर्ज नहीं हुआ",
    "legend_flood":
        "बाढ़ (1984 से 2021 तक पानी नहीं)",
    "legend_rise":
        "बढ़ते जलाशय और नदियाँ",
    "slides":
        "{smin}° से {smax}° ढलान पर संभावित भूस्खलन क्षेत्र, इनमें से {high} उच्च भरोसे वाले। ये जाँचने लायक संकेत हैं: {unrep} के 2 किमी के भीतर कोई दर्ज घटना नहीं है",
    "xt_good":
        "उन भूस्खलन क्षेत्रों में से जिन्हें दूसरा निसार ट्रैक देख सकता था, उसने भी इन्हें पाया, संयोग से {lift}× अधिक बार",
    "xt_good_small":
        "उन भूस्खलन क्षेत्रों में से जिन्हें दूसरा निसार ट्रैक देख सकता था, उसने भी इन्हें पाया: संयोग से {lift}× अधिक बार, छोटे नमूने से, क्योंकि वह ट्रैक क्षेत्र का {cov} ही देखता है",
    "xt_story_good_small":
        "दूसरी निसार कक्षा ने अपनी दृष्टि के {n} क्षेत्रों में से {c} को फिर पाया: संयोग से {lift}× अधिक बार, हालाँकि नमूना छोटा है।",
    "xt_weak":
        "दूसरी निसार कक्षा ने अपनी दृष्टि के क्षेत्रों में से कुछ ही फिर पाए, लगभग उतने जितने संयोग से मिलते।",
    "xt_story_good":
        "दूसरी निसार कक्षा ने अपनी दृष्टि के {n} क्षेत्रों में से {c} को फिर पाया: संयोग से {lift}× अधिक बार।",
    "xt_story_weak":
        "दूसरी निसार कक्षा ने अपनी दृष्टि के {n} क्षेत्रों में से केवल {c} फिर पाए, लगभग उतने जितने संयोग से मिलते, इसलिए हर क्षेत्र को जाँचने लायक संकेत मानें।",
    "xt_col":
        "दूसरा ट्रैक",
    "brighter":
        "जहाँ पानी पेड़ों के नीचे या इमारतों के बीच छिपा हो सकता है (बाढ़ में नहीं गिना गया)",
    "matched":
        "रडार जिन दर्ज घटनाओं को देख सकता था, उनमें से जिनसे किसी पहचान का मिलान हुआ",
    "start_story":
        "कहानी शुरू करें",
    "explore":
        "नक्शा देखें",
    "method":
        "हमने यह कैसे किया",
    "before":
        "पहले",
    "after":
        "बाद में",
    "couldnt":
        "रडार क्या नहीं देख सका",
    "lim_streets":
        "**इमारतों के बीच बाढ़ वाली गलियाँ।** रडार दीवारों से टकराकर उपग्रह की ओर लौटता है, इसलिए बाढ़ वाली गली गहरी नहीं, चमकीली दिख सकती है। {built_sentence}",
    "lim_built_all":
        "जो {n} दर्ज बाढ़ें छूटीं, वे सभी बसे हुए इलाक़ों में थीं।",
    "lim_built_some":
        "जो {n} दर्ज बाढ़ें छूटीं, उनमें से {k} बसे हुए इलाक़ों में थीं।",
    "lim_timing":
        "**दो अवलोकनों के बीच आकर चला गया पानी।** सबसे भारी बारिश {p1} से {p2} तक हुई; निसार ने {b} को देखा और फिर {a} को। नक्शा वह दिखाता है जो {a} को भी खड़ा था, चरम नहीं।",
    "lim_small":
        "**छोटे भूस्खलन, और हल्की ढलान पर भूस्खलन।** हमारे नक्शे के पिक्सल {res} मीटर के हैं और यह {smin}° से {smax}° की ढलान खोजता है। एक घर जितना चौड़ा भूस्खलन छूट सकता है{gentle_part}।",
    "lim_gentle":
        ", और {n} दर्ज भूस्खलन इससे हल्की ढलान पर थे",
    "lim_hidden":
        "**उपग्रह से छिपी ढलानें।** लगभग {pct}% खड़ी ज़मीन रडार से उलटी ओर है या तस्वीर में अपने ऊपर मुड़ जाती है। हम उन ढलानों को छोड़ देते हैं और अनुमान नहीं लगाते।",
    "lim_early":
        "**शुरुआती डेटा।** नासा ने इन निसार उत्पादों को कैलिब्रेट किया है, पर अब तक सीमित जगहों पर ही सत्यापित किया है। डेटा परिपक्व होने पर हमारे आँकड़े बदलेंगे।",
    "lim_lead":
        "हर संभावित भूस्खलन क्षेत्र ज़मीन पर जाँचने लायक संकेत है, फ़ैसला नहीं: {z} क्षेत्रों में से {u} के 2 किमी के भीतर कोई दर्ज घटना नहीं है।",
    "res_last_clause":
        ", और {d} को {v} वर्ग किमी रहे",
    "timeline_caption":
        "एक ही कक्षा और रडार मोड के हर निसार अवलोकन पर गहरा पानी, उस इलाक़े के भीतर गिना गया जहाँ JRC रिकॉर्ड ने कम से कम एक बार पानी देखा है (1984 से 2021)।",
    "cloud_sentence":
        "{f} से {t} तक, इलाक़े की नासा की सभी {n} दैनिक उपग्रह तस्वीरों में केवल बादल दिखे।",
    "cloud_caption":
        "हमारे अध्ययन क्षेत्र की नासा की दैनिक उपग्रह तस्वीरें। पंक्तियाँ: {sensors}; स्तंभ: तारीख़ें (महीना-दिन)। {f} से {t} तक, उपलब्ध सभी {n} तस्वीरों में केवल बादल हैं; रडार वाले दिनों, {p1} और {p2}, बादल टूटे हुए थे। काला: उस दिन इलाक़े की कोई तस्वीर नहीं। स्रोत: [NASA Worldview]({url}) (GIBS)।",
    "demo":
        "<b>डेमो डेटा।</b> इस पेज पर रडार के मान कृत्रिम हैं, निसार के फ़ाइल फ़ॉर्मैट में बनाए गए ताकि असली पुणे फ़ाइलें प्रोसेस होने से पहले ऐप बन सके। भू-भाग, नदियाँ और जलाशय असली हैं; बाढ़ और भूस्खलन क्षेत्र नहीं।",
    "no_data":
        "नतीजे अभी नहीं बने हैं। `python -m pipeline.run_all` चलाएँ।",
    "layers":
        "परतें",
    "legend_new_water":
        "नया खुला पानी",
    "legend_slides":
        "संभावित भूस्खलन क्षेत्र",
    "legend_brighter":
        "ढके हुए संभावित पानी",
    "legend_permanent":
        "नदियाँ और जलाशय",
    "legend_events":
        "दर्ज घटना",
    "lang":
        "भाषा",
    "step":
        "{n} में से चरण {i}",
    "back":
        "पीछे",
    "next":
        "आगे",
    "story_title":
        "कहानी",
    "matched_floods":
        "रडार जिन दर्ज बाढ़ों को देख सकता था, उनके पास कोई पहचान मिली",
    "matched_slides":
        "रडार जिन दर्ज भूस्खलनों को देख सकता था, उनके पास कोई पहचान मिली",
    "x_of_y":
        "{y} में से {x}",
    "and_join":
        "{a} और {b}",
    "slide_fragile_one":
        "भूस्खलन के दोनों मिलान एक ही क्षेत्र से हैं, रिपोर्टों से {d} किमी दूर, और जब भूस्खलन नियम नासा के NASADEM ऊँचाई नक्शे का इस्तेमाल करता है तो दोनों में से कोई नहीं टिकता (पद्धति देखें)।",
    "slide_fragile":
        "नासा के NASADEM ऊँचाई नक्शे के साथ, {n} भूस्खलन मिलानों में से {k} टिकते हैं (पद्धति देखें)।",
    "fell_short":
        "रडार कहाँ चूका, और क्यों",
    "rain_caption":
        "अध्ययन क्षेत्र का औसत दैनिक वर्षा। स्रोत: {src}।",
    "swipe_caption":
        "तुलना के लिए खींचें। गहरा मतलब चिकना: पानी। चमकीला मतलब खुरदरा: इमारतें, पेड़, चट्टान। दिखाया गया हिस्सा: अध्ययन क्षेत्र का वह भाग जहाँ सबसे ज़्यादा बदलाव हुआ।",
}

HI_E = {
    "why_h":
        "रडार ने इसे क्यों चिह्नित किया",
    "slope":
        "खड़ी ज़मीन: औसतन {s}°।",
    "coh":
        "दो अवलोकनों के बीच ज़मीन पहले जैसी नहीं रही: कोहेरेंस {c}, आसपास के किलोमीटर का {r}×।",
    "hv":
        "HV {v} dB गिरा (वनस्पति हटी)",
    "hh":
        "HH {v} dB बढ़ा (खुरदरा मलबा)",
    "bs":
        "रडार की चमक बदली: {x}।",
    "bs_rel":
        "रडार की चमक बाक़ी दृश्य से ज़्यादा बदली।",
    "and":
        " और ",
    "checks_h":
        "अतिरिक्त जाँचें",
    "orbit":
        "दूसरी निसार कक्षा, 3 से 15 जुलाई",
    "orbit_confirmed":
        "इसे फिर पाया",
    "orbit_partial":
        "प्रमाण का कुछ हिस्सा देखा",
    "orbit_not seen":
        "इसे नहीं देखा",
    "orbit_not covered":
        "उसकी दृष्टि से बाहर",
    "dem":
        "नासा का NASADEM ऊँचाई नक्शा",
    "dem_found":
        "बना रहा",
    "dem_not":
        "नहीं बना रहा: {r}",
    "rep":
        "2 किमी के भीतर दर्ज घटना",
    "rep_yes":
        "{place}, {km} किमी",
    "rep_no":
        "कोई नहीं (सबसे नज़दीकी {km} किमी)",
    "conf_high":
        "उच्च भरोसा",
    "conf_medium":
        "मध्यम भरोसा",
    "conf_low":
        "कम भरोसा",
    "maps":
        "गूगल मैप्स में खोलें",
    "chip_before":
        "28 जून",
    "chip_after":
        "10 जुलाई",
    "chip_coh":
        "कोहेरेंस",
    "chip_note":
        "1.9 किमी चौड़ा, 40 मीटर पिक्सल। रडार रंग: लाल HH, हरा HV, नीला HH/HV। कोहेरेंस: गहरा = ज़मीन बदली।",
    "flood_title":
        "बाढ़ का पानी",
    "flood_area":
        "10 जुलाई को {a} हेक्टेयर पानी, 28 जून से {d} dB गहरा, जहाँ 1984 से 2021 तक कभी पानी दर्ज नहीं हुआ।",
    "flood_rep":
        "सबसे नज़दीकी दर्ज बाढ़: {place}, {km} किमी।",
    "lead":
        "ज़मीन पर जाँचने लायक संकेत, पुष्ट भूस्खलन नहीं।",
    "near_h":
        "पास में क्या है",
    "near_road":
        "{km} किमी के भीतर सड़क",
    "near_rail":
        "{km} किमी के भीतर रेलवे",
    "near_place":
        "{km} किमी के भीतर बस्ती",
    "near_none":
        "कोई नहीं (सबसे नज़दीकी: {x}, {d})",
    "near_nothing":
        "कोई नहीं",
    "near_rail_line":
        "रेल लाइन",
    "near_unnamed":
        "बेनाम सड़क",
    "near_note":
        "क्षेत्र के किनारे से सीधी दूरी, OpenStreetMap से। पास होने का मतलब ख़तरा नहीं।",
}

REASON = {"steeper than 45°": "45° से ज़्यादा खड़ी", "gentler than 15°": "15° से हल्की", "radar layover or shadow": "रडार लेओवर या छाया", "near the edge of the slope band": "ढलान सीमा के किनारे के पास"}

TYPE = {"landslide": "भूस्खलन", "flood": "बाढ़", "river_overflow": "नदी का उफान", "waterlogging": "जलभराव"}
