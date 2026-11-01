// Photo catalogue. Source files live in src/static/img/<name>.jpg (Unsplash licence).
// alt: plain description of what is in the photo (never claims a place the file name does not name).
// pos: crop focus when the photo is cut to 16:9 (sharp position: centre, top, bottom, left, right…).
export const images = {
  'athens-alley': { alt: 'A narrow paved lane between pastel-coloured houses with balconies and potted plants' },
  'athens-street': { alt: 'A sunny cobbled street lined with yellow and cream houses with green shutters' },
  coffee: { alt: 'Coffee being poured from a small pot into a cup on a wooden counter, next to an iced coffee', pos: 'centre' },
  'corfu-boats': { alt: 'Turquoise water with small boats along a jetty and a tiny island with a white chapel' },
  'crete-rocks': { alt: 'A wide bay of shallow turquoise water and white sand below a rocky headland' },
  'cyclades-chairs': { alt: 'A whitewashed lane with café chairs stacked outside and lanterns hanging overhead', pos: 'centre' },
  'cyclades-harbour': { alt: 'A small harbour with a wide concrete quay and white houses on the hillside' },
  ferry: { alt: 'A red ferry moored in a calm harbour beside a stone breakwater, with white houses on the hills' },
  'greek-inscription': { alt: 'Ancient Greek letters carved into a block of stone' },
  'laptop-sea': { alt: 'A person working on a laptop on a sunny terrace above rooftops and the sea', pos: 'centre' },
  'lefkada-bay': { alt: 'A view over red-roofed houses to a calm bay dotted with small green islands' },
  'lefkada-beach': { alt: 'A long beach at the foot of steep wooded cliffs, seen from high above the sea', pos: 'centre' },
  'lefkada-boats': { alt: 'Clear turquoise water in a bay, with boats and a village on the green hillside behind' },
  'lefkada-cliff': { alt: 'A pebble beach at the foot of a tall, pale cliff, with small waves breaking' },
  'lefkada-green': { alt: 'A curve of white beach and bright blue sea below a high pale cliff, with a yacht offshore' },
  'mountain-village': { alt: 'Old stone houses with slate roofs and wooden balconies in a green mountain village', pos: 'centre' },
  'santorini-dome': { alt: 'Whitewashed buildings and blue church domes above a deep blue sea', pos: 'centre' },
  'santorini-wide': { alt: 'Whitewashed and pastel houses stacked on a cliff above a deep blue sea' },
  'taverna-chairs': { alt: 'A shady taverna terrace with tables and chairs under the trees', pos: 'bottom' },
  'taverna-tables': { alt: 'Blue tables and chairs in a stone courtyard under a white awning, with flowering plants' },
};

// Stand-in cover photo for each guide's product card.
export const guideCovers = {
  retire: 'coffee',
  nomad: 'laptop-sea',
  islands: 'santorini-dome',
  eat: 'taverna-chairs',
  phrases: 'cyclades-chairs',
  flashcards: 'athens-street',
  first90: 'cyclades-harbour',
  renting: 'athens-alley',
  alphabet: 'greek-inscription',
};
