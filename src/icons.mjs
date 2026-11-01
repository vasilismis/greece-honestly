// Small inline line icons (24×24, stroke = currentColor). Decorative: always rendered with aria-hidden.
const p = {
  plane: '<path d="M2 16l20-6-3-3-7 2-5-5-2 1 3 6-4 1-2-2-1 1z"/><path d="M3 21h18"/>',
  bus: '<rect x="4" y="3" width="16" height="15" rx="2"/><path d="M4 11h16M8 18v3M16 18v3"/><circle cx="8" cy="14.5" r="1"/><circle cx="16" cy="14.5" r="1"/>',
  car: '<path d="M3 13l2-6h14l2 6v5H3z"/><path d="M3 13h18"/><circle cx="7.5" cy="16" r="1.2"/><circle cx="16.5" cy="16" r="1.2"/><path d="M5 18v2M19 18v2"/>',
  boat: '<path d="M3 15h18l-3 5H6z"/><path d="M12 3v12M12 4l6 9h-6"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  wind: '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h16a3 3 0 1 1-3 3M3 16h8"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  euro: '<path d="M17 6a7 7 0 1 0 0 12"/><path d="M4 10h9M4 14h9"/>',
  percent: '<path d="M5 19L19 5"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  doc: '<path d="M6 2h8l5 5v15H6z"/><path d="M14 2v5h5M9 13h7M9 17h7"/>',
  home: '<path d="M3 11l9-8 9 8"/><path d="M5 10v11h14V10"/><path d="M10 21v-6h4v6"/>',
  phone: '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
  bank: '<path d="M3 9l9-6 9 6"/><path d="M4 21h16M6 10v8M10 10v8M14 10v8M18 10v8"/>',
  id: '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2.5"/><path d="M13 10h6M13 14h4"/>',
  health: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
  pin: '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
  food: '<path d="M7 2v20M4 2v6a3 3 0 0 0 6 0V2"/><path d="M17 22V2c-2 2-3 5-3 9h3"/>',
  chat: '<path d="M4 4h16v12H8l-4 4z"/>',
  check: '<path d="M4 12l5 5L20 6"/>',
  shield: '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  leaf: '<path d="M5 19c0-9 6-15 15-15 0 9-6 15-15 15z"/><path d="M5 19L14 10"/>',
};

export const iconNames = Object.keys(p);

export function icon(name, cls = 'icon') {
  if (!p[name]) throw new Error(`unknown icon "${name}". Available: ${iconNames.join(', ')}`);
  return `<svg class="${cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${p[name]}</svg>`;
}
