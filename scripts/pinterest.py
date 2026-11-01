# Generates docs/pinterest.md: two pins per article, with length checks.
# Run: python3 scripts/pinterest.py
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://vasilismis.github.io/greece-honestly/articles/'
P = {
'retiring-to-greece-2026': [
 ('Retiring to Greece in 2026: visas, the 7% tax and healthcare, step by step', 'The order that saves months: choose your residence route (EU registration, Financially Independent Person permit or Golden Visa), decide between the normal tax scale and the 7% regime, then sort out healthcare with an S1 or full health insurance. Free, plain-English guide with sources.', '#retireingreece #greece #retirementplanning'),
 ('Retire to Greece from outside the EU: €3,500 a month and no work in Greece', 'The Financially Independent Person permit asks for at least €3,500 a month (€4,200 for a couple), full health insurance covering Greece, and no work in Greece. Foreign pensions, rents and dividends are fine. Step-by-step guide.', '#retirement #greece #expatlife')],
'greece-7-percent-flat-tax-foreign-pensions': [
 ('Greece\'s 7% flat tax for foreign pensions: who qualifies and the 31 October deadline', 'A flat 7% on all foreign income for up to 15 years. On a €40,000 pension that is €2,800 instead of about €8,900 on the normal scale. Who qualifies, the 2 July rule, the 31 October deadline and the one-payment catch.', '#retireingreece #greektax #expatlife'),
 ('The 7% pension tax in Greece: three dates you cannot miss', '2 July decides your first year. 31 October is the application deadline (it used to be 31 March). The last working day of December is the one-off payment, with no instalments. Free guide with official sources.', '#retirementplanning #greece #movingabroad')],
'greece-digital-nomad-visa-2026': [
 ('Greece digital nomad visa 2026: how much you need to earn and how to apply', 'At least €3,500 a month net, employers or clients outside Greece, and a type D visa from a consulate before you travel. The visa lasts up to 12 months; the permit after it, 2 years. Plain-English guide.', '#digitalnomad #greece #remotework'),
 ('Digital nomad in Greece: why you cannot arrive as a tourist and apply later', 'Since Law 5275/2026, Greek immigration lawyers report that you must get the type D national visa at a consulate first. Plus: the income rule, full health insurance, and why the 50% tax break usually does not fit nomads.', '#nomadlife #workfromanywhere #greece')],
'which-greek-island-is-right-for-you': [
 ('Which Greek island is right for you? A quick guide to the 7 island groups', 'Cyclades, Ionian, Crete, Dodecanese, North Aegean, Saronic and Sporades explained in plain English, plus a quick quiz: first time, famous views, nightlife, quiet, families, hiking or no ferries at all. Free guide.', '#greekislands #greece #travelplanning'),
 ('Greek islands you can fly straight into (no ferry needed)', 'Hate ferries? Corfu, Crete, Rhodes, Kos, Zakynthos, Kefalonia and Skiathos all have airports. Our island guide covers which group suits you and the best months to go, from the May–June sweet spot to quiet October.', '#greecetravel #islandhopping #visitgreece')],
'greek-island-hopping-three-routes': [
 ('Greek island hopping: three routes that actually work', 'Classic Cyclades (Paros, Naxos, Santorini), quiet Cyclades (Sifnos, Milos, Folegandros) and the Ionian by car (Corfu, Lefkada, Kefalonia). With the rules that stop a trip turning into a ferry marathon.', '#islandhopping #greekislands #greece'),
 ('Island hopping in Greece: why two or three islands beat five', 'At least three nights per island, stay on one ferry line, and keep the last night near your departure airport because wind can delay boats. Ferry times change every year, so always check. Free route guide.', '#travelplanning #cyclades #greecetravel')],
'what-to-order-in-a-greek-taverna': [
 ('What to order in a Greek taverna (and how the bill works)', 'Ten classics explained, from tzatziki and horiatiki to gemista, kleftiko and loukoumades. Plus why bread is on the bill, how fish by the kilo works and what kerasméno means. Free guide.', '#greekfood #taverna #greece'),
 ('Greek taverna menu decoder: 10 dishes to know before you sit down', 'Fava is not broad beans. Horiatiki has no lettuce. Saganaki is fried cheese. A plain-English guide to ten classic dishes, plus vegetarian and allergy words: chortofágos and alergikós.', '#greekcuisine #foodtravel #eatlikealocal')],
'greek-phrases-for-your-first-week': [
 ('20 Greek phrases for your first week in Greece', 'Kaliméra, efcharistó, parakaló and 17 more, with simple pronunciation. Greetings, shopping, the taverna, emergencies and a few phrases with real Greek character, like sigá-sigá and kaló mína.', '#learngreek #greek #greece'),
 ('Ne means yes: Greek words that confuse visitors', 'In Greek, ne means yes and óchi means no. Parakaló means both please and you are welcome. Learn 20 useful phrases for your first week, with stress marks and easy pronunciation.', '#greeklanguage #languagelearning #greecetravel')],
'how-to-read-greek-signs-alphabet': [
 ('How to read Greek signs: the alphabet in ten minutes', 'Ρ is r, Η is i and Β is v. Learn the look-alike letters, the ten new ones and the letter pairs, then practise on real signs: ΚΕΝΤΡΟ, ΛΙΜΑΝΙ, ΦΑΡΜΑΚΕΙΟ, ΕΞΟΔΟΣ and ΑΕΡΟΔΡΟΜΙΟ.', '#greekalphabet #learngreek #greece'),
 ('Greek alphabet cheat sheet: the 6 letters that look English but are not', 'Η, Ρ, Χ, Ν, Υ and Β look familiar but sound different. A ten-minute guide to reading Greek signs, plus a free alphabet cheat sheet to download.', '#languagelearning #greeklanguage #travelgreece')],
'lefkada-travel-guide': [
 ('Lefkada: a practical guide to the Greek island you can drive to', 'A floating bridge from the mainland, Aktion airport about 20 km away, cliff-lined west-coast beaches, the calm east coast, Vasiliki for windsurfing, Nydri boat trips and mountain villages. With sources for every fact.', '#lefkada #ionianislands #greece'),
 ('Lefkada beaches: how to reach Porto Katsiki, Milos and Egremni today', 'Porto Katsiki: a long flight of steps. Milos: a path from Agios Nikitas or a water taxi in season. Egremni: land access uncertain since the 2015 earthquake, so go by boat. Free Lefkada guide.', '#lefkas #greekislands #greecetravel')],
'ionian-islands-compared': [
 ('Ionian islands compared: Corfu, Paxos, Lefkada, Kefalonia, Ithaca and Zakynthos', 'Six islands side by side: how to get there, who each one suits, beaches, whether you need a car and the best months. Paxos and Ithaca have no airport; Lefkada you can drive to.', '#ionianislands #greece #greekislands'),
 ('Which Ionian island? Quiet, beaches, hiking or easy access', 'Peace and quiet: Paxos or Ithaca. Dramatic beaches and a road trip: Lefkada. Hiking: Kefalonia. Families and first visits: Corfu. Direct flights: Corfu, Kefalonia and Zakynthos.', '#corfu #kefalonia #travelplanning')],
'renting-a-flat-in-greece': [
 ('Renting a flat in Greece: how long-term leases work', 'The three-year minimum for a main residence, the deposit, what the contract should say, how the landlord declares the lease to AADE and you accept it online, and a checklist for before you sign.', '#rentingreece #greece #expatlife'),
 ('Renting in Greece: what to check before you sign', 'Heating, damp, building charges, the energy certificate, who owns the flat, and dated photos on moving day. Plus why you need an AFM before you rent. Free guide with official sources.', '#movingabroad #athens #firstapartment')],
'first-90-days-in-greece': [
 ('Your first 90 days in Greece: AFM, AMKA, bank, phone and residence, in order', 'Tax number first, then a Greek phone number, a registered lease, a bank account, AMKA and residence registration. The order that saves you second trips, with a week-by-week plan.', '#movingtogreece #greece #expatlife'),
 ('Moving to Greece? Do the paperwork in this order', 'The bank wants your AFM and proof of address. The proof of address is your lease. The lease needs your AFM. Here is the order that works, with official sources for every step.', '#movingabroad #greekbureaucracy #newbeginnings')],
'how-to-order-coffee-in-greece': [
 ('How to order coffee in Greece: freddo, frappé and Greek coffee', 'Freddo espresso, freddo cappuccino, frappé and Greek coffee explained, plus skétos, métrios and glykós: in Greece you choose the sugar when you order. Free guide with the exact words.', '#greekcoffee #freddoespresso #greece'),
 ('Skétos, métrios or glykós? Ordering coffee in Greek', 'One sentence gets you the perfect iced coffee: éna freddo cappuccino métrio, parakaló. Learn the four drinks, the three sweetness words and the café habits Greeks love.', '#coffeelover #learngreek #greecetravel')],
'greek-taverna-etiquette': [
 ('Greek taverna etiquette: bread, tipping, sharing plates and fish by the kilo', 'Order for the table, expect bread on the bill, ask the weight and price of fish before it is cooked, ask for the bill when ready, and tip about 5–10% in cash if you want to.', '#greekfood #taverna #traveltips'),
 ('Eating out in Greece: 8 unwritten rules', 'Why bread appears on the bill, what kerasméno means, how to order fish priced by the kilo, receipts and card payment, and how much to tip. A friendly guide to Greek taverna etiquette.', '#greece #eatlikealocal #greekcuisine')],
'getting-an-afm-greek-tax-number': [
 ('Getting your AFM (Greek tax number) as a foreigner', 'Apply online through myAADE, then confirm your identity by video call or at a tax office. Ask for your authentication key at the same time. Why the AFM comes before the flat and the bank.', '#movingtogreece #greece #expatlife'),
 ('Greek AFM explained: what it is, what it is not, and how to get it', 'The AFM is your Greek tax number. It is not a residence permit and does not make you a tax resident on its own. Non-residents can apply too, or use a representative. Official sources included.', '#movingabroad #greektax #expat')],
'amka-explained': [
 ('AMKA explained: who can get Greece\'s social security number, and how', 'Apply in person at a KEP or e-EFKA. EU citizens bring a passport or ID; non-EU citizens a passport and residence permit. What S1 pensioners do next, and the question to ask if your permit does not allow work.', '#movingtogreece #greece #expatlife'),
 ('AMKA vs AFM: the two Greek numbers you will need', 'The AFM is your tax number from AADE; the AMKA is your social security number, needed for the public health system. Where to get the AMKA, what to bring and how S1 registration works.', '#movingabroad #greekbureaucracy #retireingreece')],
'opening-a-greek-bank-account': [
 ('Opening a Greek bank account as a foreigner: what to bring', 'Passport or ID, your AFM, proof of address such as a registered lease, and your residence permit if you are not from the EU. Why the order matters, and your right to a basic account under EU rules.', '#movingtogreece #greece #expatlife'),
 ('Greek bank account checklist: avoid being sent home for one paper', 'AFM first, then a registered lease, then the bank, with everything in one folder. Plus the questions to ask at the desk and what to do if the bank says no.', '#movingabroad #personalfinance #expat')],
'where-to-live-in-athens': [
 ('Where to live in Athens: neighbourhoods for renters', 'Koukaki, Pangrati, Kypseli, Glyfada and Kifisia compared: what each is like, who it suits and what to think about. Plus the two-visit rule and the paperwork every renter needs.', '#athens #rentingreece #greece'),
 ('Athens neighbourhoods: central and walkable, by the sea, or leafy suburbs?', 'Walk everywhere from Koukaki, find a neighbourhood feel in Pangrati, save in Kypseli, live by the sea in Glyfada or find space in Kifisia. A renter\'s guide with sources.', '#athensgreece #expatlife #movingabroad')],
'greek-islands-in-october-and-november': [
 ('Greek islands in October and November: which ones stay open', 'Big islands keep living, small islands go to sleep. Crete, Rhodes, Corfu and Syros work out of season. Ferries still run with fewer sailings, and flights from Athens to Crete and Rhodes run all winter.', '#greekislands #offseason #autumntravel'),
 ('Autumn in the Greek islands: where to go after the summer', 'October is quieter and some places close on small islands. From November, choose a big island. What to check before you book, and why Mykonos is one to skip in late autumn.', '#greece #crete #slowtravel')],
'greek-ferries-how-to-book': [
 ('Greek ferries: how to book, which apps, what to know', 'Book on the operator\'s site, an app or at the port. Most companies accept e-tickets; bring your original ID and arrive about an hour before. Plus what to do when the wind blows.', '#greekferries #islandhopping #greece'),
 ('Greek ferry day checklist: tickets, ID and timing', 'E-ticket or paper? Which port? Is your name right? Arrive about an hour early, never put a ferry on flight day, and book early around 15 August. Free ferry guide.', '#greekislands #traveltips #greecetravel')],
'greek-public-holidays-2027': [
 ('Greek public holidays 2027: the dates, and what closes', 'Orthodox Easter is on 2 May 2027, Clean Monday on 15 March and Whit Monday on 21 June. Every 2027 holiday with its weekday, and how holidays affect offices, banks and travel.', '#greece #greekholidays #travelplanning'),
 ('Planning a move or a trip to Greece in 2027? Check these dates', 'Public offices, banks and many shops close on public holidays, and around 15 August ferries and islands hit their peak. The full 2027 list, with a planning guide for newcomers.', '#greekeaster #movingtogreece #visitgreece')],
'greek-phrases-for-the-pharmacy-and-doctor': [
 ('Greek phrases for the pharmacy and the doctor', 'Do you have something for a headache? It hurts here. I am allergic to… Simple Greek with easy pronunciation, plus how to find an on-duty pharmacy at night. 112 for emergencies.', '#learngreek #greece #traveltips'),
 ('At a Greek pharmacy: five sentences to know', 'Look for the green cross (farmakío). Échete káti giá ponokéfalo? Íme alergikós se… A free phrase guide for pharmacies and doctors, with the emergency numbers 112 and 166.', '#greecetravel #travelhealth #greekphrases')],
}
arts = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, 'src/articles')) if f.endswith('.md'))
errors = [f'missing pins for {a}' for a in arts if a not in P] + [f'pins for unknown article {a}' for a in P if a not in arts]
out = ['# Pinterest pins', '', 'Two pins per article. Titles ≤100 characters; descriptions ≤450 characters including 3 hashtags. Generated and checked by `scripts/pinterest.py`. Suggested image: the article\'s hero photo (its social-preview JPEG at `img/<hero>-og.jpg` on the site).', '']
for a in arts:
    src = open(os.path.join(ROOT, 'src/articles', a + '.md')).read()
    hero = re.search(r'^hero: (.+)$', src, re.M).group(1).strip()
    out += [f'## {a}', '', f'Link: {SITE}{a}/  ', f'Image: `{hero}`', '']
    for i, (t, d, h) in enumerate(P.get(a, []), 1):
        desc = f'{d} {h}'
        if len(t) > 100: errors.append(f'{a} pin {i} title {len(t)} chars')
        if len(desc) > 450: errors.append(f'{a} pin {i} description {len(desc)} chars')
        if len(h.split()) != 3 or not all(x.startswith('#') for x in h.split()): errors.append(f'{a} pin {i} hashtags')
        out += [f'**Pin {i} title** ({len(t)} chars): {t}', '', f'**Pin {i} description** ({len(desc)} chars): {desc}', '']
open(os.path.join(ROOT, 'docs/pinterest.md'), 'w').write('\n'.join(out))
if errors: print('\n'.join(errors)); sys.exit(1)
print(f'OK: {len(arts)} articles, {2*len(arts)} pins, all limits met')
