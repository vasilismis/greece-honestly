// Site-wide settings and the guide catalogue.
// SITE_URL and BASE_PATH can be overridden with environment variables at build time,
// e.g. for a custom domain: SITE_URL=https://www.example.com BASE_PATH=/ npm run build

export const site = {
  name: 'Greece, Honestly',
  tagline: 'Practical English-language guides for visiting and moving to Greece.',
  description:
    'Practical, plain-English guides for people visiting or moving to Greece: residence, tax, islands, food and the language.',
  url: (process.env.SITE_URL || 'https://vasilismis.github.io').replace(/\/+$/, ''),
  basePath: normaliseBase(process.env.BASE_PATH ?? '/greece-honestly/'),
  lang: 'en-GB',
  shopUrl: 'https://payhip.com/GreeceHonestly',
  // Leave empty until the founder adds a contact address. When set, it appears on the Privacy and About pages.
  contactEmail: process.env.CONTACT_EMAIL || '',
  lastChecked: 'November 2026',
  footerNote:
    'Greece, Honestly is presented by AI-generated characters. Guides are written with AI tools and checked in Greece. General information, not legal, tax or medical advice.',
};

function normaliseBase(b) {
  let s = b.trim();
  if (!s.startsWith('/')) s = '/' + s;
  if (!s.endsWith('/')) s += '/';
  return s;
}

// key → guide. "price" is shown as-is; "format" is used in the call-to-action box.
export const guides = {
  retire: { name: 'Retire in Greece 2026', price: '€12', url: 'https://payhip.com/b/vrQHk', format: 'PDF' },
  nomad: { name: 'Digital Nomad in Greece 2026', price: '€9', url: 'https://payhip.com/b/Eniwq', format: 'PDF' },
  islands: { name: 'Which Greek Island? 35 islands compared', price: '€7', url: 'https://payhip.com/b/MiE5C', format: 'PDF' },
  eat: { name: 'What to Eat in Greece: the taverna menu decoder', price: '€7', url: 'https://payhip.com/b/9avjp', format: 'PDF' },
  phrases: { name: 'Survival Greek: 150 phrases + audio', price: 'see shop', url: 'https://payhip.com/b/7oGHa', format: 'PDF + audio' },
  flashcards: { name: 'Survival Greek Flashcards', price: '€5', url: 'https://payhip.com/b/EIdK0', format: 'PDF' },
  first90: { name: 'Your First 90 Days in Greece', price: 'see shop', url: 'https://payhip.com/b/PT5D7', format: 'PDF' },
  renting: { name: "Renting in Greece: the tenant's kit", price: 'see shop', url: 'https://payhip.com/b/d2DGi', format: 'PDF' },
  alphabet: { name: 'FREE Greek Alphabet Cheat Sheet', price: 'free', url: 'https://payhip.com/b/pY9Ot', format: 'PDF' },
};

// Order and grouping on the Guides page.
export const guideGroups = [
  { title: 'Moving to Greece', keys: ['retire', 'nomad', 'first90', 'renting'] },
  { title: 'Travelling in Greece', keys: ['islands', 'eat'] },
  { title: 'Learning some Greek', keys: ['phrases', 'flashcards', 'alphabet'] },
];
