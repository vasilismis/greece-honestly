# Generates docs/social/*.md carousel scripts from the data below and checks every length rule.
# Run: python3 scripts/social.py
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGS = {f[:-4] for f in os.listdir(os.path.join(ROOT, 'src/static/img')) if f.endswith('.jpg')}
SITE = 'https://vasilismis.github.io/greece-honestly/articles/'
FS = 'Greece, Honestly fact sheet, checked in Greece'
END = 'AI characters, written in Greece.'

C = []
def car(slug, title, fmt, slides, caption, tags, sources, article):
    C.append(dict(slug=slug, title=title, fmt=fmt, slides=slides, caption=caption, tags=tags, sources=sources, article=article))

car('01-taverna-bill-myths', 'Taverna bill: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Your Greek taverna bill, decoded', 'Four things visitors get wrong about eating out in Greece.', 'taverna-tables'),
 ('Myth', '"The bread is free"', 'Bread often arrives without asking, and it is usually charged. Say if you do not want it.', 'taverna-chairs'),
 ('Fact', 'Fish is priced by the kilo', 'The menu price is per kilo, not per plate. Ask the weight and price before cooking.', 'corfu-boats'),
 ('Myth', '"You must tip 15%"', 'Tipping is optional. About 5–10% in cash if you were happy.', 'taverna-tables'),
 ('Fact', 'Kerasméno means on the house', 'That dessert you did not order? A gift from the taverna. Say efcharistó.', 'coffee'),
 ('Fact', 'You should get a receipt', 'And card payment should be possible. It is fine to ask.', 'athens-street'),
 ('Locals do this', 'Order several dishes and share', 'Plates go in the middle and everyone helps themselves. Order more later.', 'taverna-chairs'),
 ('Free guide', 'Read the full etiquette guide', 'Link in bio: Greek taverna etiquette, free on our website.', 'taverna-tables'),
], 'Bread on the bill? Fish by the kilo? Here is how a Greek taverna bill really works, so nothing surprises you. Free guide on our site.',
 ['#greece', '#greekfood', '#taverna', '#greecetravel', '#traveltips', '#eatlikealocal'],
 [f'All facts: {FS}'], 'greek-taverna-etiquette/')

car('02-island-quiz', 'Which Greek island are you?', 'Quiz', [
 ('Quick quiz', 'Which Greek island suits you?', 'Pick the answer that sounds like you. Each slide gives you islands to try.', 'santorini-wide'),
 ('First time?', 'Start with Naxos, Crete or Paros', 'Easy to reach, plenty to do, and good for a first island trip.', 'crete-rocks'),
 ('Famous views', 'Santorini, in May or October', 'The views are real. Go outside peak summer for a calmer visit.', 'santorini-dome'),
 ('Peace and quiet', 'Folegandros, Sifnos or Paxos', 'Smaller islands with a slower pace and fewer crowds.', 'cyclades-chairs'),
 ('Hiking', 'Crete, Ikaria, Amorgos, Kefalonia', 'Mountains, gorges and paths: bring proper shoes.', 'mountain-village'),
 ('Hate ferries?', 'Fly straight into these islands', 'Corfu, Crete, Rhodes, Kos, Zakynthos, Kefalonia and Skiathos all have airports.', 'corfu-boats'),
 ('Short on time', 'Aegina, Hydra or Poros', 'Saronic islands, one to two hours by boat from Piraeus.', 'ferry'),
 ('Free guide', 'The seven island groups explained', 'Link in bio: which Greek island is right for you?', 'santorini-wide'),
], 'First trip, quiet escape, hiking or no ferries? Seven answers, seven sets of islands. Which one are you? Full guide on our site.',
 ['#greekislands', '#greece', '#islandhopping', '#greecetravel', '#travelquiz', '#visitgreece'],
 [f'All facts: {FS}'], 'which-greek-island-is-right-for-you/')

car('03-coffee-say-this', 'Ordering coffee: say this, not that', 'Say this, not that', [
 ('Say this, not that', 'Order coffee like a Greek', 'The drink, the sweetness, then parakaló. Here is how it works.', 'coffee'),
 ('Not this', '"Iced coffee, sugar on the side"', 'In Greece the sugar usually goes in while the coffee is made.', 'laptop-sea'),
 ('Say this', '"Éna freddo cappuccino métrio, parakaló"', 'One iced cappuccino, medium sweet, please. A safe first order.', 'coffee'),
 ('Sweetness', 'Skétos, métrios or glykós', 'No sugar, medium or sweet. Say it when you order.', 'coffee'),
 ('Freddo espresso', 'Espresso shaken with ice', 'Served cold and lightly foamy. First made in Athens in 1991.', 'athens-street'),
 ('Frappé', 'The 1957 classic', 'Instant coffee shaken with water and ice into a thick foam.', 'cyclades-chairs'),
 ('Greek coffee', 'Small, hot, grounds at the bottom', 'Boiled in a small pot. Sip slowly and stop before the grounds.', 'coffee'),
 ('Free guide', 'How to order coffee in Greece', 'Link in bio: the full guide, free on our website.', 'coffee'),
], 'Skétos, métrios or glykós? In Greece you choose the sugar when you order, not after. Learn the one sentence that gets you the perfect freddo.',
 ['#greekcoffee', '#freddoespresso', '#greece', '#learngreek', '#coffeelover', '#greecetravel'],
 ['Freddo espresso, Athens 1991: https://www.tovima.com/culture/the-freddo-espresso-a-modern-greek-cultural-phenomenon/amp/',
  'Frappé, 1957 Thessaloniki fair: https://en.wikipedia.org/wiki/Frapp%C3%A9_coffee',
  'Sweetness terms: https://greektriplanner.me/blog/greek-coffee'], 'how-to-order-coffee-in-greece/')

car('04-seven-percent-numbers', 'The 7% tax in numbers', 'Money numbers', [
 ('Money numbers', 'Greece\'s 7% pension tax', 'A flat rate on foreign income for retirees who move. Here are the numbers.', 'coffee'),
 ('The rate', '7% on all foreign income', 'Not just the pension: all foreign-source income, at one flat rate.', 'athens-street'),
 ('How long', 'Up to 15 tax years', 'It cannot be extended beyond that.', 'mountain-village'),
 ('The example', '€40,000 pension: €8,900 vs €2,800', 'Normal 2026 scale, about €8,900 before credits. Under the 7% regime, €2,800.', 'coffee'),
 ('Deadline', 'Apply by 31 October', 'Of the year you want the regime to start. It used to be 31 March.', 'athens-street'),
 ('Payment', 'One instalment, in December', 'By the last working day of December. No instalment plans.', 'coffee'),
 ('Careful', 'Miss the payment, lose the regime', 'Not paying in full ends the regime from that year.', 'mountain-village'),
 ('Free guide', 'Who qualifies, step by step', 'Link in bio: the 7% flat tax explained. General information, not tax advice.', 'athens-street'),
], 'A €40,000 foreign pension: about €8,900 on the normal Greek scale, or €2,800 under the 7% regime. Who qualifies, and the dates you cannot miss.',
 ['#retireingreece', '#greece', '#expatlife', '#retirementplanning', '#movingabroad', '#greektax'],
 ['AADE, tax incentives for new residents: https://www.aade.gr/en/greeks-abroad-non-residents/income-taxation/tax-incentives-order-attract-new-tax-residents',
  f'2026 changes, 31 October deadline, earlier 31 March deadline, example figures: {FS}'], 'greece-7-percent-flat-tax-foreign-pensions/')

car('05-cafe-locals', 'Things locals do at a Greek café', 'Things locals do', [
 ('Things locals do', 'Café life in Greece', 'Six habits you will notice in your first week.', 'cyclades-chairs'),
 ('1', 'One coffee, a long time', 'A coffee is a reason to sit and talk. Nobody will hurry you.', 'coffee'),
 ('2', 'Sugar is chosen upfront', 'Skétos, métrios or glykós, said when ordering.', 'coffee'),
 ('3', 'Iced coffee is the favourite', 'Freddo espresso and freddo cappuccino, especially in the warm months.', 'laptop-sea'),
 ('4', 'Ask for the bill', 'Say to logariasmó, parakaló when you are ready to go.', 'athens-street'),
 ('5', 'Kaló mína on the 1st', 'People wish each other a happy new month on the first day.', 'athens-alley'),
 ('6', 'Sigá-sigá', 'Slowly, slowly. Take it easy. You will hear it a lot.', 'cyclades-chairs'),
 ('Free guide', '20 phrases for your first week', 'Link in bio: everyday Greek with simple pronunciation.', 'cyclades-chairs'),
], 'One coffee, a long chat, the sugar chosen upfront and kaló mína on the 1st. Six café habits you will spot in your first week in Greece.',
 ['#greece', '#greeklife', '#cafeculture', '#learngreek', '#slowtravel', '#greecetravel'],
 [f'Phrases and customs: {FS}', 'Coffee drinks: https://greektriplanner.me/blog/greek-coffee'], 'greek-phrases-for-your-first-week/')

car('06-nomad-myths', 'Digital nomad visa: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Greece\'s digital nomad visa', 'Four things people get wrong in 2026.', 'laptop-sea'),
 ('Myth', '"Arrive as a tourist, apply later"', 'Since Law 5275/2026, get the type D visa at a consulate first, lawyers report.', 'ferry'),
 ('Fact', '€3,500 a month, net', 'Plus 20% for a spouse and 15% per child.', 'laptop-sea'),
 ('Fact', 'Clients must be outside Greece', 'The permit is for remote work for employers or clients abroad.', 'athens-street'),
 ('Fact', 'Visa up to 12 months', 'The residence permit after it lasts 2 years and is renewable.', 'cyclades-harbour'),
 ('Myth', '"Travel insurance is enough"', 'You need full health insurance covering Greece.', 'laptop-sea'),
 ('Myth', '"The 50% tax break fits"', 'It usually does not: it needs a Greek employer or Greek establishment.', 'athens-street'),
 ('Free guide', 'How to apply, step by step', 'Link in bio: the digital nomad visa 2026. Not legal advice.', 'laptop-sea'),
], 'Arrive as a tourist and apply later? Not any more. The 2026 rules for Greece\'s digital nomad visa, minus the myths.',
 ['#digitalnomad', '#greece', '#remotework', '#workfromanywhere', '#nomadlife', '#movingabroad'],
 ['Ministry of Foreign Affairs, digital nomad visa: https://www.mfa.gr/en/services/working-in-greece-as-a-digital-nomad/',
  f'Income, consulate-first rule, insurance, visa/permit duration, article 5C: {FS} and founder confirmation'], 'greece-digital-nomad-visa-2026/')

car('07-fip-numbers', 'Financially Independent Person permit in numbers', 'Money numbers', [
 ('Money numbers', 'Retiring to Greece from outside the EU', 'The Financially Independent Person permit, in numbers.', 'mountain-village'),
 ('Income', '€3,500 a month', 'Minimum for the main applicant.', 'coffee'),
 ('Couple', '€4,200 a month', 'Add 20% for a spouse.', 'taverna-tables'),
 ('Family', '€4,725 with one child', 'Add 15% per child. €5,250 with two.', 'athens-alley'),
 ('Fees', '€1,000 main applicant', 'Plus €150 per adult family member and €16 per card.', 'athens-street'),
 ('Validity', '3 years, renewable for 3', 'Apply in the 2 months before expiry.', 'mountain-village'),
 ('The catch', 'No work in Greece', 'Foreign pensions, rents and dividends are fine. Jobs and self-employment are not.', 'coffee'),
 ('Free guide', 'Retiring to Greece, step by step', 'Link in bio: visas, the 7% tax and healthcare. Not legal advice.', 'mountain-village'),
], 'Retiring to Greece from outside the EU? The Financially Independent Person permit: €3,500 a month, €4,200 for a couple, no work in Greece.',
 ['#retireingreece', '#greece', '#retirement', '#expatlife', '#movingabroad', '#residencepermit'],
 [f'All figures (Law 5038/2023; JMD 225679/2024): {FS}'], 'retiring-to-greece-2026/')

car('08-yes-means-no', 'Ne means yes: say this, not that', 'Say this, not that', [
 ('Say this, not that', 'Greek words that trip you up', 'Six quick ones to get right in your first week.', 'cyclades-chairs'),
 ('Careful', 'Ne means yes', 'It sounds like no, but ne is yes.', 'athens-alley'),
 ('And', 'Óchi means no', 'With the throaty ch, like the Scottish loch.', 'cyclades-chairs'),
 ('Say this', 'Parakaló', 'Please, and also you are welcome. The most useful word.', 'coffee'),
 ('Say this', 'Yiá sas', 'Polite hello, and goodbye too.', 'athens-street'),
 ('Say this', 'Signómi', 'Sorry. Useful in a crowded bus or market.', 'athens-alley'),
 ('Say this', 'Efcharistó', 'Thank you. Stress the last syllable: ef-ha-ree-STO.', 'taverna-tables'),
 ('Free guide', '20 phrases for week one', 'Link in bio: simple pronunciation, free on our website.', 'cyclades-chairs'),
], 'In Greek, ne means yes and óchi means no. Six small words that make a big difference in your first week. Save this one.',
 ['#learngreek', '#greeklanguage', '#greece', '#greekwords', '#languagelearning', '#greecetravel'],
 [f'All phrases and pronunciation: {FS}'], 'greek-phrases-for-your-first-week/')

car('09-alphabet-quiz', 'Greek alphabet quiz', 'Quiz', [
 ('Quick quiz', 'Can you read these Greek letters?', 'Six letters look English but are not. Guess, then swipe.', 'greek-inscription'),
 ('Letter 1', 'Ρ looks like P…', 'But it is r. Ρ is never p.', 'greek-inscription'),
 ('Letter 2', 'Η looks like H…', 'But it sounds like i, as in machine.', 'athens-street'),
 ('Letter 3', 'Β looks like B…', 'But it is v.', 'greek-inscription'),
 ('Letter 4', 'Χ looks like X…', 'But it is ch, as in the Scottish loch.', 'cyclades-chairs'),
 ('Letter 5', 'Υ looks like Y…', 'But it also sounds like i.', 'greek-inscription'),
 ('Now read', 'ΦΑΡΜΑΚΕΙΟ', 'Farmakío: pharmacy. Ρ is r, and ΕΙ sounds like i.', 'athens-alley'),
 ('Free guide', 'The alphabet in ten minutes', 'Link in bio, plus a free alphabet cheat sheet.', 'greek-inscription'),
], 'Ρ is r, Η is i and Β is v. Can you read ΦΑΡΜΑΚΕΙΟ by the end? Six letters that look English but are not.',
 ['#greekalphabet', '#learngreek', '#greece', '#languagelearning', '#greeklanguage', '#travelgreece'],
 [f'Letters and sign words: {FS}', 'Greek alphabet: https://en.wikipedia.org/wiki/Greek_alphabet'], 'how-to-read-greek-signs-alphabet/')

car('10-greek-habits', 'Things locals say', 'Things locals do', [
 ('Things locals say', 'Five Greek phrases with character', 'You will hear these everywhere. Now you will know what they mean.', 'cyclades-chairs'),
 ('Kaló mína', 'Happy new month', 'Said on the 1st of every month.', 'athens-alley'),
 ('Sigá-sigá', 'Slowly, slowly', 'Take it easy, no rush. Almost a philosophy.', 'lefkada-bay'),
 ('Kalí órexi', 'Enjoy your meal', 'You will hear it when the food arrives.', 'taverna-tables'),
 ('Yiá mas', 'Cheers', 'Raise your glass before the first sip.', 'taverna-chairs'),
 ('Kaló taxídi', 'Have a good trip', 'What people say as you set off.', 'ferry'),
 ('Try it', 'Say kaló mína on the 1st', 'Wish it to the person at the bakery and watch them smile.', 'athens-street'),
 ('Free guide', '20 phrases for your first week', 'Link in bio, with simple pronunciation.', 'cyclades-chairs'),
], 'Kaló mína, sigá-sigá, yiá mas: the little Greek phrases you will hear every day, and when to use them yourself.',
 ['#learngreek', '#greece', '#greekculture', '#greekphrases', '#languagelearning', '#slowtravel'],
 [f'All phrases: {FS}'], 'greek-phrases-for-your-first-week/')

car('11-winter-islands-myths', 'Greek islands in winter: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Greek islands after the summer', 'What really happens in October and November.', 'crete-rocks'),
 ('Myth', '"All islands close in winter"', 'Big islands keep living. Small islands go to sleep.', 'crete-rocks'),
 ('Fact', 'October is quieter', 'On small islands, some places start to close.', 'cyclades-harbour'),
 ('Fact', 'Crete stays awake', 'Its northern towns stay active all year.', 'crete-rocks'),
 ('Fact', 'Rhodes Town stays lively', 'Resort areas go quiet, so stay in or near town.', 'santorini-wide'),
 ('Myth', '"Ferries stop in winter"', 'They run all year, but with fewer sailings.', 'ferry'),
 ('Best bets', 'Crete, Rhodes, Corfu, Syros', 'Islands that keep living outside summer. Pack a rain jacket for Corfu.', 'corfu-boats'),
 ('Free guide', 'Islands in October and November', 'Link in bio: which ones stay open, free on our site.', 'crete-rocks'),
], 'Do the Greek islands close in winter? The small ones mostly do. The big ones keep living. Where to go in October and November.',
 ['#greekislands', '#greece', '#offseason', '#autumntravel', '#crete', '#slowtravel'],
 [f'Months and islands for outside summer: {FS}', 'Crete, Rhodes, Corfu in winter: https://www.tovima.com/travel/do-the-greek-islands-shut-down-in-winter/',
  'Ferries in winter: https://blog.ferriesingreece.com/greek-ferries/in-winter'], 'greek-islands-in-october-and-november/')

car('12-tax-scale-numbers', 'Greek tax scale 2026', 'Money numbers', [
 ('Money numbers', 'Greece\'s 2026 income tax scale', 'For salaries and pensions, under Law 5246/2025.', 'athens-street'),
 ('First €10,000', '9%', 'The first band.', 'coffee'),
 ('To €20,000', '20%', 'On income between €10,000 and €20,000.', 'athens-alley'),
 ('To €30,000', '26%', 'On income between €20,000 and €30,000.', 'athens-street'),
 ('To €40,000', '34%', 'On income between €30,000 and €40,000.', 'athens-alley'),
 ('To €60,000', '39%', 'On income between €40,000 and €60,000.', 'athens-street'),
 ('Above €60,000', '44%', 'The top rate. Tax residents are taxed on worldwide income.', 'athens-alley'),
 ('Free guide', 'Retiring to Greece, step by step', 'Link in bio, including the 7% alternative. Not tax advice.', 'coffee'),
], 'Greece\'s 2026 tax scale for salaries and pensions: from 9% on the first €10,000 to 44% above €60,000. Save it for later.',
 ['#greektax', '#greece', '#expatlife', '#movingabroad', '#personalfinance', '#retireingreece'],
 ['KPMG Greece, tax updates: https://kpmg.com/gr/en/insights/2025/11/tax-updates-20112025.html',
  'Legal 500, Law 5246/2025: https://www.legal500.com/intelligence/greece/tax/tax-alert-new-law-5246-2025', f'Also: {FS}'], 'retiring-to-greece-2026/')

car('13-pharmacy-say-this', 'At the pharmacy: say this', 'Say this, not that', [
 ('Say this, not that', 'At a Greek pharmacy', 'Five sentences for when English is not enough.', 'cyclades-harbour'),
 ('Look for', 'The green cross', 'Farmakío: the Greek word for pharmacy.', 'athens-street'),
 ('Say this', 'Échete káti giá ponokéfalo?', 'Do you have something for a headache?', 'cyclades-harbour'),
 ('Say this', 'Ponái edó', 'It hurts here. Point, and you have said most of it.', 'athens-alley'),
 ('Say this first', 'Íme alergikós / alergikí se…', 'I am allergic to… (man / woman).', 'cyclades-harbour'),
 ('At night', 'Find an on-duty pharmacy', 'Pharmacies take turns staying open. Check the notice in the window.', 'athens-street'),
 ('Emergency', '112, or 166 for an ambulance', 'And shout voíthia! if you need help.', 'cyclades-harbour'),
 ('Free guide', 'Pharmacy and doctor phrases', 'Link in bio: free on our website.', 'cyclades-harbour'),
], 'A headache, sunburn, a sore throat. Five Greek sentences for the pharmacy, and how to find one open at night.',
 ['#learngreek', '#greece', '#traveltips', '#greecetravel', '#greekphrases', '#travelhealth'],
 ['Green cross and farmakío: https://www.greeceindex.com/health/greece_health_system_pharmacies/',
  'On-duty pharmacies in Attica: https://fsa-efimeries.gr/', 'Emergency numbers: https://www.gov.gr/en/sdg/healthcare/national-emergency-numbers',
  f'Alergikós/alergikí, voíthia: {FS}', 'Other phrases: general Greek vocabulary (unchecked against a source)'], 'greek-phrases-for-the-pharmacy-and-doctor/')

car('14-ferry-locals', 'Ferry habits of people who know', 'Things locals do', [
 ('Things locals do', 'How to ferry like you live here', 'Six habits that keep ferry day calm.', 'ferry'),
 ('1', 'Check the schedule every year', 'Ferry times change every year. Always check your dates.', 'ferry'),
 ('2', 'Carry the original ID', 'Tickets are in your name. Copies may not do.', 'cyclades-harbour'),
 ('3', 'Be there an hour early', 'Standard advice is about an hour before departure.', 'ferry'),
 ('4', 'One ferry line at a time', 'Islands in the same group connect easily.', 'cyclades-harbour'),
 ('5', 'No ferry on flight day', 'Wind can delay boats. Sleep near your departure airport.', 'lefkada-boats'),
 ('6', 'Book early around 15 August', 'It is peak season for ferries and islands.', 'ferry'),
 ('Free guide', 'Greek ferries: how to book', 'Link in bio: apps, e-tickets and what to know.', 'ferry'),
], 'Original ID, an hour early, one ferry line and never a ferry on flight day. Six habits that keep Greek ferry days calm.',
 ['#greekferries', '#greekislands', '#islandhopping', '#greece', '#traveltips', '#greecetravel'],
 [f'Schedules, rules of thumb, 15 August: {FS}', 'ID and arrival time: https://www.ferryhopper.com/en/blog/featured/ferries-greece-survival-guide'], 'greek-ferries-how-to-book/')

car('15-lefkada-quiz', 'Lefkada quiz', 'Quiz', [
 ('Quick quiz', 'How well do you know Lefkada?', 'Five questions about the Ionian island you can drive to.', 'lefkada-green'),
 ('Question 1', 'How do you reach Lefkada?', 'By road, over a floating bridge from the mainland. No ferry needed.', 'lefkada-bay'),
 ('Question 2', 'Where is the nearest airport?', 'Aktion (Preveza) on the mainland, about 20 km away.', 'lefkada-beach'),
 ('Question 3', 'Why do windsurfers love Vasiliki?', 'A thermal wind builds in the bay in the afternoon.', 'lefkada-boats'),
 ('Question 4', 'Which writer was born here?', 'Lafcadio Hearn, in 1850. His middle name comes from the island.', 'lefkada-cliff'),
 ('Question 5', 'Calm water: west or east?', 'East. The west coast faces the open sea.', 'lefkada-boats'),
 ('Bonus', 'Egremni beach access?', 'Uncertain since the 2015 earthquake. Go by boat, and ask locally.', 'lefkada-cliff'),
 ('Free guide', 'Lefkada: a practical guide', 'Link in bio: beaches, villages and when to go.', 'lefkada-green'),
], 'A floating bridge, a famous afternoon wind and a writer named after the island. How many of these Lefkada questions can you answer?',
 ['#lefkada', '#lefkas', '#ionianislands', '#greece', '#greekislands', '#travelquiz'],
 ['All facts with links in the Lefkada guide sources: ' + SITE + 'lefkada-travel-guide/'], 'lefkada-travel-guide/')

car('16-renting-myths', 'Renting in Greece: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Renting a flat in Greece', 'Four surprises for first-time renters.', 'athens-alley'),
 ('Myth', '"A one-year lease is one year"', 'For a main residence, the minimum term is three years, even if the contract says less.', 'athens-street'),
 ('Fact', 'The lease is declared to AADE', 'The landlord files it; you accept it online in myAADE.', 'athens-alley'),
 ('Fact', 'You need an AFM first', 'Your tax number is part of the lease declaration.', 'laptop-sea'),
 ('Fact', 'Deposits: commonly 1–2 months', 'Agree in writing how and when it comes back.', 'athens-street'),
 ('Myth', '"Skip the last rent, keep the deposit"', 'Do not. Agree in writing how the deposit is settled.', 'athens-alley'),
 ('Tip', 'Photograph everything on day one', 'Every room, every mark, plus the meter readings.', 'athens-street'),
 ('Free guide', 'Renting a flat in Greece', 'Link in bio: contract checklist, free on our site. Not legal advice.', 'athens-alley'),
], 'A one-year lease that lasts three years? Registering with the tax office? What surprises first-time renters in Greece, and how to be ready.',
 ['#rentingreece', '#athens', '#greece', '#expatlife', '#movingabroad', '#firstapartment'],
 ['Lease declaration: https://www.aade.gr/en/property-rentalstatements',
  'Three-year minimum: https://landager.com/en/property-compliance/greece/national/lease-requirements',
  'Deposits: https://landager.com/en/property-compliance/greece/national/security-deposits'], 'renting-a-flat-in-greece/')

car('17-golden-visa-numbers', 'Golden Visa in numbers', 'Money numbers', [
 ('Money numbers', 'Greece\'s Golden Visa in 2026', 'The property thresholds under Law 5100/2024.', 'santorini-wide'),
 ('Top tier', '€800,000', 'Attica, Thessaloniki, Mykonos, Santorini and islands over 3,100 residents, including Crete.', 'santorini-dome'),
 ('Elsewhere', '€400,000', 'In the rest of Greece.', 'mountain-village'),
 ('Size', 'At least 120 m²', 'One property, in both tiers.', 'athens-alley'),
 ('Exception', '€250,000', 'For converting a commercial building to homes, or restoring a listed building.', 'athens-street'),
 ('No Airbnb', 'Fines from €50,000', 'Short-term letting of the property is not allowed.', 'santorini-wide'),
 ('The permit', '5 years, renewable', 'No minimum stay, and no right to work.', 'crete-rocks'),
 ('Free guide', 'Retiring to Greece, step by step', 'Link in bio. Not legal or investment advice.', 'santorini-wide'),
], '€800,000, €400,000 or €250,000: Greece\'s Golden Visa thresholds, the 120 m² rule and the short-term rental ban, in eight slides.',
 ['#goldenvisa', '#greece', '#realestate', '#residencybyinvestment', '#movingabroad', '#greekproperty'],
 ['IBA overview: https://www.ibanet.org/the-greek-golden-visa-after-2024-2026-overhaul',
  'Zeya newsletter: https://zeya.com/newsletters/greek-golden-visa-regime-conditions-qualifying-property-investments-become-stricter', f'Also: {FS}'], 'retiring-to-greece-2026/')

car('18-first-90-myths', 'First 90 days: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Your first 90 days in Greece', 'The order matters more than the paperwork.', 'cyclades-harbour'),
 ('Myth', '"Open a bank account first"', 'Banks usually ask for your AFM and proof of address. Get those first.', 'athens-street'),
 ('Fact', 'The AFM opens every door', 'Your tax number is needed for the lease and the bank.', 'laptop-sea'),
 ('Fact', 'Apply for it online', 'Through myAADE, then a video call or a tax office visit.', 'laptop-sea'),
 ('Fact', 'A registered lease is proof of address', 'Your landlord declares it; you accept it in myAADE.', 'athens-alley'),
 ('Fact', 'AMKA at a KEP', 'Your social security number, issued in person.', 'mountain-village'),
 ('EU citizens', 'Register after three months', 'In person, with the police service for foreigners where you live.', 'athens-street'),
 ('Free guide', 'Your first 90 days, in order', 'Link in bio: free on our website. Not legal advice.', 'cyclades-harbour'),
], 'Bank first? Not in Greece. AFM, phone, a registered lease, then the bank and AMKA. The order that saves you second trips.',
 ['#movingtogreece', '#greece', '#expatlife', '#movingabroad', '#greekbureaucracy', '#newbeginnings'],
 ['AFM: https://www.gov.gr/en/arxes/anexartete-arkhe-demosion-esodon-aade/anexartete-arkhe-demosion-esodon-aade/apodose-arithmou-phorologikou-metroou-aphm-kai-kleidarithmou-se-phusiko-prosopo',
  'AMKA: https://ypergasias.gov.gr/en/social-security/insured-persons/social-security-registration-number-amka/',
  'Bank documents: https://migration.gov.gr/wp-content/uploads/2023/11/ENGLISH_BROCHURE.pdf',
  'EU registration: https://www.gov.gr/en/sdg/residence/temporary-or-permanent-move/general/obligation-for-citizens-to-register-their-residence-for-periods-exceeding-three-months'], 'first-90-days-in-greece/')

car('19-holidays-quiz', 'Greek holidays 2027 quiz', 'Quiz', [
 ('Quick quiz', 'Greek holidays 2027', 'Guess the date, then swipe. Useful if you are planning a move or a trip.', 'santorini-dome'),
 ('Question 1', 'When is Orthodox Easter 2027?', 'Sunday 2 May.', 'santorini-dome'),
 ('Question 2', 'When is Clean Monday?', '15 March: 48 days before Easter.', 'cyclades-chairs'),
 ('Question 3', 'What happens on 25 March?', 'Independence Day and the Annunciation, both on one day.', 'athens-street'),
 ('Question 4', 'When is Whit Monday 2027?', '21 June, 50 days after Easter.', 'crete-rocks'),
 ('Question 5', 'What is 28 October?', 'Ochi Day, a national holiday.', 'athens-alley'),
 ('Busiest day', '15 August', 'Peak season for ferries and islands. Book early.', 'ferry'),
 ('Free guide', 'All 2027 holidays and what closes', 'Link in bio: free on our website.', 'santorini-dome'),
], 'Orthodox Easter 2027 is on 2 May. Do you know when Clean Monday and Whit Monday fall? Quiz yourself before you plan.',
 ['#greece', '#greekholidays', '#greekeaster', '#travelplanning', '#greekculture', '#visitgreece'],
 ['2027 dates: https://www.timeanddate.com/holidays/greece/2027 ; https://holidaya.gr/en/2027/',
  'Mandatory holidays: https://en.wikipedia.org/wiki/Public_holidays_in_Greece', 'Easter date also computed by us', f'15 August peak: {FS}'], 'greek-public-holidays-2027/')

car('20-island-hopping-myths', 'Island hopping: myths vs facts', 'Myths vs facts', [
 ('Myths vs facts', 'Greek island hopping', 'Why fewer islands make a better trip.', 'cyclades-harbour'),
 ('Myth', '"Five islands in ten days"', 'Two or three islands beat five. You see more by moving less.', 'ferry'),
 ('Fact', 'Three nights per island, minimum', 'Arrival and departure days eat into your time.', 'santorini-wide'),
 ('Fact', 'Stay on one ferry line', 'Crossing between island groups usually means long detours.', 'ferry'),
 ('Fact', 'Wind can cancel ferries', 'Keep your last night near your departure airport.', 'lefkada-boats'),
 ('Route idea', 'Paros, Naxos, Santorini', 'Classic Cyclades in 10–12 days, then fly back to Athens.', 'santorini-dome'),
 ('Route idea', 'Corfu, Lefkada, Kefalonia', 'The Ionian by car in 10 days. Check the Lefkada–Kefalonia ferry date.', 'corfu-boats'),
 ('Free guide', 'Three routes that work', 'Link in bio: island hopping, free on our site.', 'ferry'),
], 'Five islands in ten days sounds great until you spend it in ports. Two or three islands, three nights each. Here is why.',
 ['#islandhopping', '#greekislands', '#greece', '#cyclades', '#travelplanning', '#greecetravel'],
 [f'Rules of thumb and routes: {FS}'], 'greek-island-hopping-three-routes/')

# ---------- checks and output ----------
words = lambda s: len(re.findall(r"\S+", s))
errors = []
assert len(C) == 20, len(C)
out = os.path.join(ROOT, 'docs/social'); os.makedirs(out, exist_ok=True)
index = ['# Social carousels', '', 'Twenty 8-slide carousel scripts for TikTok and Instagram. Each slide: kicker (≤4 words) / headline (≤7 words) / one line (≤18 words) / photo from `src/static/img/`. Generated by `scripts/social.py`, which also checks every length rule.', '', '| # | Carousel | Format |', '|---|---|---|']
for c in C:
    if len(c['slides']) != 8: errors.append(f"{c['slug']}: {len(c['slides'])} slides")
    for i, (k, h, l, img) in enumerate(c['slides'], 1):
        if words(k) > 4: errors.append(f"{c['slug']} s{i} kicker {words(k)}w")
        if words(h) > 7: errors.append(f"{c['slug']} s{i} headline {words(h)}w: {h}")
        if words(l) > 18: errors.append(f"{c['slug']} s{i} line {words(l)}w")
        if img not in IMGS: errors.append(f"{c['slug']} s{i} unknown photo {img}")
    cap = f"{c['caption']} {END} {' '.join(c['tags'])}"
    if len(c['tags']) != 6: errors.append(f"{c['slug']} has {len(c['tags'])} hashtags")
    if words(cap) > 60: errors.append(f"{c['slug']} caption {words(cap)}w")
    md = [f"# {c['title']}", '', f"**Format:** {c['fmt']}  ", f"**Links to:** {SITE}{c['article']}", '', '| Slide | Kicker | Headline | Line | Photo |', '|---|---|---|---|---|']
    for i, (k, h, l, img) in enumerate(c['slides'], 1):
        md.append(f"| {i} | {k} | {h} | {l} | `{img}.jpg` |")
    md += ['', '## Caption', '', cap, '', f"*({words(cap)} words)*", '', '## Sources (do not publish)', ''] + [f"- {s}" for s in c['sources']] + ['']
    open(os.path.join(out, c['slug'] + '.md'), 'w').write('\n'.join(md))
    index.append(f"| {c['slug'][:2]} | [{c['title']}]({c['slug']}.md) | {c['fmt']} |")
open(os.path.join(out, 'README.md'), 'w').write('\n'.join(index) + '\n\nEvery caption ends with "AI characters, written in Greece." and 6 hashtags. Sources at the bottom of each file are for checking, not for posting.\n')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'OK: {len(C)} carousels, all limits met')
