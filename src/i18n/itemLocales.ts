/** Translated item name + description for EN, FR, AR (NL = original items.json). */
export const ITEM_LOCALES: Record<'en' | 'fr' | 'ar', Record<string, { name: string; description: string }>> = {

  en: {
    mint_tea:       { name: 'Mint Tea',               description: 'Fresh Moroccan mint tea. Restores some HP.' },
    smoske:         { name: 'Smoske',                 description: 'A filled roll from Boulangerie Karimi. +8 HP.' },
    friet:          { name: 'Fries with Andalous',    description: 'Crispy and good. +12 HP.' },
    baklava:        { name: 'Baklava',                description: 'Sweet honey pastry from the Moroccan baker. +6 HP.' },
    harira:         { name: 'Harira',                 description: 'Traditional Moroccan soup. +15 HP.' },
    permit_doc:     { name: 'Permit',                 description: 'An official document from city hall. Required for certain quests.' },
    reuzenpoort_key:{ name: 'Reuzenpoort Key',        description: 'Opens the historic Reuzenpoort at Turnhoutsebaan 110.' },
    tram_ticket:    { name: 'Tram Ticket',            description: 'A valid ticket for De Lijn tram 10. Travel to Deurne or Wijnegem.' },
    fabric_bolt:    { name: 'Fabric Roll (Stunt)',    description: "A fabric remnant from Stunt Solderie, Turnhoutsebaan 74. For Fatima's dress." },
    oud_string:     { name: 'Oud String',             description: "A spare string for Reza's oud. Fragile." },
    samen_flyer:    { name: 'Samen Aan Tafel Flyer',  description: 'Flyer for the big iftar event on Turnhoutsebaan. 7000 seats.' },
  },

  fr: {
    mint_tea:       { name: 'Thé à la Menthe',        description: 'Thé à la menthe marocaine fraîche. Récupère des PV.' },
    smoske:         { name: 'Smoske',                 description: 'Un sandwich garni de la Boulangerie Karimi. +8 PV.' },
    friet:          { name: 'Frites Sauce Andalouse', description: 'Croustillant et bon. +12 PV.' },
    baklava:        { name: 'Baklava',                description: 'Pâtisserie au miel du boulanger marocain. +6 PV.' },
    harira:         { name: 'Harira',                 description: 'Soupe marocaine traditionnelle. +15 PV.' },
    permit_doc:     { name: 'Permis',                 description: 'Un document officiel de la mairie. Nécessaire pour certaines quêtes.' },
    reuzenpoort_key:{ name: 'Clé de la Reuzenpoort', description: 'Ouvre la Reuzenpoort historique à Turnhoutsebaan 110.' },
    tram_ticket:    { name: 'Ticket de Tram',         description: 'Un ticket valide pour le tram De Lijn 10. Voyage vers Deurne ou Wijnegem.' },
    fabric_bolt:    { name: 'Rouleau de Tissu',       description: 'Un reste de tissu de Stunt Solderie, Turnhoutsebaan 74. Pour la robe de Fatima.' },
    oud_string:     { name: 'Corde de Oud',           description: "Une corde de rechange pour le oud de Reza. Fragile." },
    samen_flyer:    { name: 'Flyer Samen Aan Tafel',  description: "Flyer pour le grand événement d'iftar sur la Turnhoutsebaan. 7000 sièges." },
  },

  ar: {
    mint_tea:       { name: 'شاي النعناع',            description: 'شاي نعناع مغربي طازج. يستعيد بعض الصحة.' },
    smoske:         { name: 'سموسكه',                 description: 'خبز محشو من Boulangerie Karimi. +8 ص.ح.' },
    friet:          { name: 'بطاطس بصلصة الأندلس',   description: 'مقرمش ولذيذ. +12 ص.ح.' },
    baklava:        { name: 'بقلاوة',                 description: 'حلوى العسل من الخباز المغربي. +6 ص.ح.' },
    harira:         { name: 'حريرة',                  description: 'حساء مغربي تقليدي. +15 ص.ح.' },
    permit_doc:     { name: 'رخصة',                   description: 'وثيقة رسمية من البلدية. مطلوبة لبعض المهام.' },
    reuzenpoort_key:{ name: 'مفتاح Reuzenpoort',      description: 'يفتح Reuzenpoort التاريخية في Turnhoutsebaan 110.' },
    tram_ticket:    { name: 'تذكرة ترام',             description: 'تذكرة صالحة لترام De Lijn 10. سافر إلى Deurne أو Wijnegem.' },
    fabric_bolt:    { name: 'لفة قماش (Stunt)',       description: 'بقايا قماش من Stunt Solderie، Turnhoutsebaan 74. لفستان فاطمة.' },
    oud_string:     { name: 'وتر عود',                description: 'وتر احتياطي لعود ريزا. هش.' },
    samen_flyer:    { name: 'نشرة ساميناان تافيل',    description: 'نشرة لحفل الإفطار الكبير في تورنهاوتسيبان. 7000 مقعد.' },
  },
};
