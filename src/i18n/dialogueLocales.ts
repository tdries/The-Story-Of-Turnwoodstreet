/** Per-locale dialogue text overlays (NL = original dialogue.json, not duplicated here).
 *  Format: locale → dialogueId → stepIndex → { text?, choices? }
 *  Steps with no text (effects-only) are represented as empty objects {}.
 *  choices[] maps 1-to-1 to the choice array in dialogue.json by index.
 */

export type DialogueStep = { text?: string; choices?: string[] };
export type DialogueLocale = Record<string, DialogueStep[]>;

export const DIALOGUE_LOCALES: Record<'en' | 'fr' | 'ar', DialogueLocale> = {

  // ── ENGLISH ───────────────────────────────────────────────────────────────
  en: {
    fatima_intro: [
      { text: "Salam! Are you new on Turnhoutsebaan? Welcome to the most beautiful street in Antwerp." },
      { text: "I've lived here for 22 years. My father came as a guest worker in '72. He worked in the textile factory." },
      { text: "Now my niece Nora runs a hammam school further down the street. She's getting married next month — but she still needs fabric for her dress.", choices: ["I can get that fabric for you.", "Where can I find fabric?"] },
    ],
    fatima_fabric_accept: [
      { text: "That would be wonderful! Mrs. Baert at Indian Boutique — nr.137 — always has nice remnants. Tell her I sent you." },
    ],
    fatima_fabric_hint: [
      { text: "Indian Boutique! Number 137. Open since 1985. Mrs. Baert knows every fabric. She's Flemish, but her best customers are Moroccan — she understands us." },
    ],
    fatima_after_fabric: [
      { text: "The fabric! Shukran, shukran! Nora will be so happy." },
      { text: "You're a good person. The neighbourhood needs people like you. If you ever need help — I'm here." },
    ],
    fatima_post_trust: [
      { text: "Have you heard that a speculator wants to buy three properties? Everyone is worried." },
      { text: "Omar the baker also has problems — he has no flour left for tomorrow morning. Maybe you can help?" },
    ],
    fatima_faction: [
      { text: "Samen Aan Tafel... yes. If everyone joins, then yes. I'll call the Moroccan association." },
    ],
    omar_bakker: [
      { text: "Khobz? Msemmen? Fresh from five this morning! My oven never stops on Turnhoutsebaan." },
      { text: "During Ramadan I sometimes bake until midnight. Then the whole neighbourhood is at my door." },
      { text: "Have you heard about the 2-kilometre table? We baked bread for 7000 people." },
    ],
    omar_flour_request: [
      { text: "Aiwa, big problem! My supplier is sick. No flour for tomorrow. Budget Market has it — but I can't leave the shop.", choices: ["I'll get it for you.", "How much flour?"] },
    ],
    omar_flour_thanks: [
      { text: "Barakallahu fik! Budget Market, nr.326. Two 5-kilo bags. Just say it's for Omar." },
    ],
    omar_flour_detail: [
      { text: "Two bags, 5 kilos each. Good quality flour — type 45 if they have it. Budget Market, nr.326." },
    ],
    omar_flour_done: [
      { text: "The flour! Perfect. Here — harira and baklava for you. And if you ever need bread: free, always." },
    ],
    stunt_baert: [
      { text: "Stunt Solderie, open since '85! I've seen the whole neighbourhood change." },
      { text: "It used to be a Flemish working-class neighbourhood. Now I hear five languages when I open my door." },
      { text: "But you know? My best customers are the Moroccan women. They know fabrics better than anyone." },
    ],
    stunt_baert_fabric: [
      { text: "For Fatima's niece! Of course. I had already set a piece aside — I knew she'd send someone." },
      { text: "Tell Fatima the fabric is a gift from Stunt Solderie. After all these years." },
    ],
    stunt_baert_signature: [
      { text: "A petition? Against that speculator? Hand it over. I'll sign first. My shop has been here for 40 years." },
    ],
    stunt_baert_faction: [
      { text: "Bar Leon? Those guys aren't easy. But if I go and explain what it's about... they know me. I'll do it." },
    ],
    reza_music: [
      { text: "Psst. Do you hear that? Those sounds come from De Roma. Every week something different — gnawa, jazz, rap." },
      { text: "Paul McCartney once played here. Really. Turnhoutsebaan 286, August '72." },
      { text: "My oud has a broken string. If you find one at Mimoun, nr.239, I'll play a song for you tonight.", choices: ["I'll look for that string for you.", "Tell me more about De Roma."] },
    ],
    reza_oud_accept: [
      { text: "Mimoun, nr.239 — further down the street. They sometimes have music accessories. Ask about strings for an oud." },
    ],
    reza_de_roma_lore: [
      { text: "De Roma is Art Deco, 1927. Alphonse Pauwels built it for 2000 people. After years of vacancy, saved by 400 volunteers in 2003." },
      { text: "Now gnawa from Marrakech, hip-hop from Borgerhout, jazz from everywhere. THAT is Turnhoutsebaan." },
    ],
    reza_oud_found: [
      { text: "The string... perfect. Wait." },
      { text: "*plays* ... Do you hear that? That is the language of this street. You understand it now too." },
    ],
    reza_signature: [
      { text: "That speculator? I know him. He wants to buy my studio too. Here's my signature, and those of my two neighbours." },
    ],
    yusuf_delivery: [
      { text: "No no no! Flat tyre and 12 more parcels! Sir, madam — can you help me?", choices: ["I'll help you with the last three.", "Where do they need to go?"] },
    ],
    yusuf_delivery_accept: [
      { text: "Really? Great! Parcel 1 → nr.170 (Patisserie Aladdin). Parcel 2 → nr.137 (Indian Boutique). Parcel 3 → nr.284 (Borger Hub). Please!" },
    ],
    yusuf_delivery_info: [
      { text: "Nr.170, nr.137 and nr.284. Three addresses, one street. Not far! I'll give you a tram ticket as a reward." },
    ],
    yusuf_delivery_done: [
      { text: "Everything delivered? Fantastic! Here — a tram ticket. May your bakfiets never get a flat tyre." },
    ],
    hamza_marbles: [
      { text: "Yo! Marbles? Always. But I want to ask something — for school. Do you know what the Reuzenpoort is?" },
      { text: "Our teacher says it's a historic gate. But why is it here on Turnhoutsebaan?" },
    ],
    hamza_school_faction: [
      { text: "The school joining Samen Aan Tafel? I'll ask Miss De Smedt. She's cool, she'll definitely say yes." },
    ],
    aziz_signature: [
      { text: "I've been here for 40 years. I've seen how they first excluded us, then tolerated us, and now maybe... accepted us." },
      { text: "My signature? Yes. For this street I'll sign anything." },
    ],
    fatima_signature: [
      { text: "A petition! Finally. Hand it over. Name, address and date — done. Now go to Omar, Reza, Mrs. Baert and Aziz." },
    ],
    omar_signature: [
      { text: "That speculator? He tried to buy my bakery last year too. Here — signature. And take a roll with you." },
    ],
    tine_faction: [
      { text: "Ah, Samen Aan Tafel! I've known the chairman of the Turkish social club for 20 years. If you ask and I support it — he'll say yes." },
    ],
    kid_marbles: [
      { text: "Yo! Want to play marbles? I always win but it's boring if there's no one to play against." },
      { text: "My grandma says the police used to patrol here all the time. Now there's a café. Better, right?" },
    ],
    delivery_rush: [
      { text: "No no no, not now! My bakfiets has a flat tyre and I still have 12 parcels to deliver!" },
      { text: "If you help me with the last three, I'll give you a tram ticket. Deal?" },
    ],
    reuzenpoort_blocked: [
      { text: "The gate remains closed to strangers. First speak with Fatima at the start of the street." },
    ],
    de_roma_blocked: [
      { text: "The door of De Roma only opens for those who understand the language of the street. Find Reza's oud string." },
    ],
    deurne_blocked: [
      { text: "The border guard asks for your papers. Defeat the Bulldozer-Bureaucrat and carry his permit." },
    ],
    reuzenpoort_legend: [
      { text: "The Reuzenpoort dates from 1713. They built it for the Reuzenhouse — long before the town hall stood here." },
      { text: "In 1833 they demolished the Reuzenhouse for the new town hall of Josephus Hoefnagels. But the gate remained." },
      { text: "Borgerhout was independent for centuries. Only on 1 January 1983 did we become Antwerp. Many still regret that." },
    ],
    de_roma_keeper: [
      { text: "This building is Art Deco, built in 1927. Alphonse Pauwels designed it for 2000 spectators." },
      { text: "After years of vacancy, we were saved in 2003 by Paul Schyvens and 400 volunteers." },
      { text: "Tonight: gnawa music from Marrakech. Tomorrow: hip-hop from Borgerhout. Always welcome." },
    ],
    de_roma_concert: [
      { text: "Reza is playing on stage tonight. Thanks to you. Thanks to the string you found." },
      { text: "*plays oud* This song is called 'Turnhoutsebaan'. I wrote it for everyone here." },
    ],
    district_mayor: [
      { text: "Good afternoon. I am Mariam El Osri, district chair of Borgerhout." },
      { text: "I've heard what you've done — the fabric, the petition, the string. This street needs you." },
      { text: "I'm organising Samen Aan Tafel: 2-kilometre table, 7000 people, Easter and Iftar together. But I need 7 factions. Will you help?", choices: ["Yes. I'm in.", "Tell me more."] },
    ],
    mayor_briefing: [
      { text: "Good. Seven factions: Moroccan association, Turkish club, Bar Leon, Borgerhub, the school, the mosque and Frituur de Tram. One by one." },
    ],
    mayor_explains: [
      { text: "April 2024. 2 kilometres. Easter and Iftar on the same day. 7000 seats. All of Turnhoutsebaan at the table. Real history." },
    ],
    imam_mosque: [
      { text: "Peace. I've heard about your table. If the iftar meal is respected — if there's no alcohol next to our plates — we'll join.", choices: ["I promise. We'll arrange separate zones.", "How do you envision that?"] },
    ],
    imam_agreed: [
      { text: "Alhamdulillah. The mosque joins. A shared meal shifts a judgment." },
    ],
    imam_explains: [
      { text: "A separate section: halal, no alcohol, but next to the others. Not apart. Together but respectful." },
    ],
    frituur_faction: [
      { text: "7000 bags of fries? That's... a lot of potatoes. But if you arrange the order at the wholesaler, we'll join.", choices: ["I'll arrange the order.", "How much does that cost?"] },
    ],
    frituur_agreed: [
      { text: "Great! Fries with Andalous for 7000 people. That'll go down in history." },
    ],
    frituur_cost: [
      { text: "Five coins for the deposit. Then we'll sort the rest." },
    ],
    borgerhub_faction: [
      { text: "An artists' collective at Samen Aan Tafel? If De Roma is also joining — absolutely. Art and community belong together." },
    ],
    geest_van_88_encounter: [
      { text: "Borgerokko! This is our neighbourhood! You don't belong here!" },
      { text: "The Ghost of '88 cannot be defeated by force. Use 'Samen Aan Tafel' in the battle." },
    ],
    geest_van_88_defeated: [
      { text: "I... I've never... all these years... sat at the table with..." },
      { text: "*slowly fades* ...enjoy your meal." },
    ],
  },

  // ── FRANÇAIS ──────────────────────────────────────────────────────────────
  fr: {
    fatima_intro: [
      { text: "Salam! Tu es nouveau sur la Turnhoutsebaan? Bienvenue dans la plus belle rue d'Anvers." },
      { text: "Ça fait 22 ans que j'habite ici. Mon père est arrivé comme travailleur immigré en '72. Il travaillait dans l'usine textile." },
      { text: "Maintenant, ma nièce Nora dirige une école de hammam plus loin. Elle se marie le mois prochain — mais il lui manque encore du tissu pour sa robe.", choices: ["Je peux aller chercher ce tissu.", "Où puis-je trouver du tissu?"] },
    ],
    fatima_fabric_accept: [
      { text: "Ce serait merveilleux! Madame Baert à l'Indian Boutique — nr.137 — a toujours de beaux restes. Dis-lui que je t'envoie." },
    ],
    fatima_fabric_hint: [
      { text: "Indian Boutique! Numéro 137. Ouvert depuis 1985. Madame Baert connaît chaque tissu. Elle est Flamande, mais ses meilleures clientes sont Marocaines — elle nous comprend." },
    ],
    fatima_after_fabric: [
      { text: "Le tissu! Shukran, shukran! Nora sera tellement heureuse." },
      { text: "Tu es une bonne personne. Le quartier a besoin de gens comme toi. Si tu as jamais besoin d'aide — je suis là." },
    ],
    fatima_post_trust: [
      { text: "Tu as entendu qu'un spéculateur veut acheter trois propriétés? Tout le monde est inquiet." },
      { text: "Omar le boulanger a aussi des problèmes — il n'a plus de farine pour demain matin. Tu peux peut-être aider?" },
    ],
    fatima_faction: [
      { text: "Samen Aan Tafel... oui. Si tout le monde participe, alors oui. Je vais appeler l'association marocaine." },
    ],
    omar_bakker: [
      { text: "Khobz? Msemmen? Frais depuis cinq heures ce matin! Mon four ne s'arrête jamais sur la Turnhoutsebaan." },
      { text: "Pendant le Ramadan, je fais parfois la cuisson jusqu'à minuit. Tout le quartier est à ma porte." },
      { text: "Tu as entendu parler de la table de 2 kilomètres? Nous avons fait du pain pour 7000 personnes." },
    ],
    omar_flour_request: [
      { text: "Aiwa, grand problème! Mon fournisseur est malade. Pas de farine pour demain. Budget Market en a — mais je ne peux pas quitter la boutique.", choices: ["Je vais en chercher.", "Combien de farine?"] },
    ],
    omar_flour_thanks: [
      { text: "Barakallahu fik! Budget Market, nr.326. Deux sacs de 5 kilos. Dis que c'est pour Omar." },
    ],
    omar_flour_detail: [
      { text: "Deux sacs, 5 kilos chacun. Farine de bonne qualité — type 45 s'ils en ont. Budget Market, nr.326." },
    ],
    omar_flour_done: [
      { text: "La farine! Parfait. Tiens — harira et baklava pour toi. Et si tu as jamais besoin de pain: gratuit, toujours." },
    ],
    stunt_baert: [
      { text: "Stunt Solderie, ouvert depuis '85! J'ai vu tout le quartier changer." },
      { text: "Avant c'était un quartier ouvrier flamand. Maintenant j'entends cinq langues quand j'ouvre ma porte." },
      { text: "Mais tu sais? Mes meilleures clientes sont les femmes marocaines. Elles connaissent les tissus mieux que personne." },
    ],
    stunt_baert_fabric: [
      { text: "Pour la nièce de Fatima! Bien sûr. J'avais déjà mis un morceau de côté — je savais qu'elle enverrait quelqu'un." },
      { text: "Dis à Fatima que le tissu est un cadeau de Stunt Solderie. Après toutes ces années." },
    ],
    stunt_baert_signature: [
      { text: "Une pétition? Contre ce spéculateur? Donne. Je signe en premier. Ma boutique est ici depuis 40 ans." },
    ],
    stunt_baert_faction: [
      { text: "Bar Leon? Ces gars-là ne sont pas faciles. Mais si j'y vais et explique ce que c'est... ils me connaissent. Je le fais." },
    ],
    reza_music: [
      { text: "Psst. Tu entends ça? Ces sons viennent de De Roma. Chaque semaine quelque chose de différent — gnawa, jazz, rap." },
      { text: "Paul McCartney a joué ici une fois. Vraiment. Turnhoutsebaan 286, août '72." },
      { text: "Mon oud a une corde cassée. Si tu en trouves une chez Mimoun, nr.239, je joue une chanson pour toi ce soir.", choices: ["Je vais chercher cette corde.", "Parle-moi de De Roma."] },
    ],
    reza_oud_accept: [
      { text: "Mimoun, nr.239 — plus loin dans la rue. Ils ont parfois des accessoires musicaux. Demande des cordes pour un oud." },
    ],
    reza_de_roma_lore: [
      { text: "De Roma est Art Déco, 1927. Alphonse Pauwels l'a construit pour 2000 personnes. Après des années d'abandon, sauvé par 400 bénévoles en 2003." },
      { text: "Maintenant gnawa de Marrakech, hip-hop de Borgerhout, jazz de partout. C'est ÇA la Turnhoutsebaan." },
    ],
    reza_oud_found: [
      { text: "La corde... parfaite. Attends." },
      { text: "*joue* ... Tu entends ça? C'est la langue de cette rue. Toi aussi tu la comprends maintenant." },
    ],
    reza_signature: [
      { text: "Ce spéculateur? Je le connais. Il veut aussi acheter mon studio. Voici ma signature, et celles de mes deux voisins." },
    ],
    yusuf_delivery: [
      { text: "Non non non! Crevaison et encore 12 colis! Monsieur, madame — vous pouvez m'aider?", choices: ["Je t'aide avec les trois derniers.", "Où doivent-ils aller?"] },
    ],
    yusuf_delivery_accept: [
      { text: "Vraiment? Super! Colis 1 → nr.170 (Patisserie Aladdin). Colis 2 → nr.137 (Indian Boutique). Colis 3 → nr.284 (Borger Hub). S'il vous plaît!" },
    ],
    yusuf_delivery_info: [
      { text: "Nr.170, nr.137 et nr.284. Trois adresses, une rue. Pas loin! Je te donne un ticket de tram en récompense." },
    ],
    yusuf_delivery_done: [
      { text: "Tout livré? Fantastique! Tiens — un ticket de tram. Que ton bakfiets n'ait jamais de crevaison." },
    ],
    hamza_marbles: [
      { text: "Yo! Des billes? Toujours. Mais je veux aussi demander quelque chose — pour l'école. Tu sais ce qu'est la Reuzenpoort?" },
      { text: "Notre prof dit que c'est une porte historique. Mais pourquoi est-elle ici sur la Turnhoutsebaan?" },
    ],
    hamza_school_faction: [
      { text: "L'école participer au Samen Aan Tafel? Je vais demander à Mademoiselle De Smedt. Elle est cool, elle dit sûrement oui." },
    ],
    aziz_signature: [
      { text: "Je suis ici depuis 40 ans. J'ai vu comment ils nous ont d'abord exclus, puis tolérés, et maintenant peut-être... acceptés." },
      { text: "Ma signature? Oui. Pour cette rue, je signe tout." },
    ],
    fatima_signature: [
      { text: "Une pétition! Enfin. Donne. Nom, adresse et date — voilà. Va maintenant voir Omar, Reza, Madame Baert et Aziz." },
    ],
    omar_signature: [
      { text: "Ce spéculateur? L'an dernier il a aussi essayé d'acheter ma boulangerie. Tiens — signature. Et prends un petit pain." },
    ],
    tine_faction: [
      { text: "Ah, Samen Aan Tafel! Je connais le président du club social turc depuis 20 ans. Si tu demandes et que je soutiens — il dit oui." },
    ],
    kid_marbles: [
      { text: "Yo! Tu veux jouer aux billes? Je gagne toujours mais c'est ennuyeux s'il n'y a personne contre qui jouer." },
      { text: "Ma grand-mère dit que la police patrouillait toujours ici avant. Maintenant il y a un café. Mieux, non?" },
    ],
    delivery_rush: [
      { text: "Non non non, pas maintenant! Mon bakfiets a une crevaison et j'ai encore 12 colis à livrer!" },
      { text: "Si tu m'aides avec les trois derniers, je te donne un ticket de tram. Marché conclu?" },
    ],
    reuzenpoort_blocked: [
      { text: "La porte reste fermée aux étrangers. Parle d'abord avec Fatima au début de la rue." },
    ],
    de_roma_blocked: [
      { text: "La porte de De Roma ne s'ouvre que pour ceux qui comprennent la langue de la rue. Trouve la corde d'oud de Reza." },
    ],
    deurne_blocked: [
      { text: "Le garde-frontière demande vos papiers. Bats le Bureaucrate-Bulldozer et porte son permis." },
    ],
    reuzenpoort_legend: [
      { text: "La Reuzenpoort date de 1713. Ils l'ont construite pour le Reuzenhaus — bien avant que la mairie s'installe ici." },
      { text: "En 1833, ils ont démoli le Reuzenhaus pour la nouvelle mairie de Josephus Hoefnagels. Mais la porte est restée." },
      { text: "Borgerhout était indépendant pendant des siècles. Ce n'est que le 1er janvier 1983 que nous sommes devenus Anvers. Beaucoup le regrettent encore." },
    ],
    de_roma_keeper: [
      { text: "Ce bâtiment est Art Déco, construit en 1927. Alphonse Pauwels l'a conçu pour 2000 spectateurs." },
      { text: "Après des années d'abandon, nous avons été sauvés en 2003 par Paul Schyvens et 400 bénévoles." },
      { text: "Ce soir: musique gnawa de Marrakech. Demain: hip-hop de Borgerhout. Toujours bienvenu." },
    ],
    de_roma_concert: [
      { text: "Reza joue ce soir sur scène. Grâce à toi. Grâce à la corde que tu as trouvée." },
      { text: "*joue de l'oud* Cette chanson s'appelle 'Turnhoutsebaan'. Je l'ai écrite pour tout le monde ici." },
    ],
    district_mayor: [
      { text: "Bonjour. Je suis Mariam El Osri, présidente de district de Borgerhout." },
      { text: "J'ai entendu ce que tu as fait — le tissu, la pétition, la corde. Cette rue a besoin de toi." },
      { text: "J'organise Samen Aan Tafel: 2 kilomètres de table, 7000 personnes, Pâques et Iftar ensemble. Mais j'ai besoin de 7 factions. Tu veux aider?", choices: ["Oui. Je participe.", "Dis m'en plus."] },
    ],
    mayor_briefing: [
      { text: "Bien. Sept factions: association marocaine, club turc, Bar Leon, Borgerhub, l'école, la mosquée et Frituur de Tram. Une par une." },
    ],
    mayor_explains: [
      { text: "Avril 2024. 2 kilomètres. Pâques et Iftar le même jour. 7000 sièges. Toute la Turnhoutsebaan à table. Histoire réelle." },
    ],
    imam_mosque: [
      { text: "Paix. J'ai entendu parler de votre table. Si le repas d'iftar est respecté — s'il n'y a pas d'alcool à côté de nos assiettes — nous participons.", choices: ["Je le promets. Nous arrangerons des zones séparées.", "Comment vous imaginez-vous ça?"] },
    ],
    imam_agreed: [
      { text: "Alhamdulillah. La mosquée participe. Un repas partagé fait bouger un jugement." },
    ],
    imam_explains: [
      { text: "Une section séparée: halal, pas d'alcool, mais à côté des autres. Pas à part. Ensemble mais respectueux." },
    ],
    frituur_faction: [
      { text: "7000 portions de frites? C'est... beaucoup de pommes de terre. Mais si tu organises la commande chez le grossiste, nous participons.", choices: ["Je règle la commande.", "Combien ça coûte?"] },
    ],
    frituur_agreed: [
      { text: "Super! Frites sauce Andalouse pour 7000 personnes. Ça entrera dans l'histoire." },
    ],
    frituur_cost: [
      { text: "Cinq pièces pour l'acompte. Ensuite on s'occupe du reste." },
    ],
    borgerhub_faction: [
      { text: "Un collectif d'artistes au Samen Aan Tafel? Si De Roma participe aussi — absolument. Art et communauté vont ensemble." },
    ],
    geest_van_88_encounter: [
      { text: "Borgerokko! C'est notre quartier! Vous n'avez rien à faire ici!" },
      { text: "Le Fantôme de '88 ne peut pas être vaincu par la force. Utilisez 'Samen Aan Tafel' dans la bataille." },
    ],
    geest_van_88_defeated: [
      { text: "Je... je n'ai jamais... toutes ces années... été à table avec..." },
      { text: "*disparaît lentement* ...bon appétit." },
    ],
  },

  // ── العربية ───────────────────────────────────────────────────────────────
  ar: {
    fatima_intro: [
      { text: "سلام! هل أنت جديد في تورنهاوتسيبان؟ مرحبًا بك في أجمل شارع في أنتويرب." },
      { text: "أنا أعيش هنا منذ 22 سنة. والدي جاء كعامل مهاجر في '72. كان يعمل في مصنع النسيج." },
      { text: "الآن ابنة أختي نورا تدير مدرسة حمام أبعد في الشارع. ستتزوج الشهر القادم — لكنها لا تزال بحاجة إلى قماش لفستانها.", choices: ["أستطيع إحضار ذلك القماش لك.", "أين أجد القماش؟"] },
    ],
    fatima_fabric_accept: [
      { text: "سيكون ذلك رائعًا! السيدة بيرت في Indian Boutique — رقم 137 — لديها دائمًا بقايا جميلة. أخبرها أنني أرسلتك." },
    ],
    fatima_fabric_hint: [
      { text: "Indian Boutique! رقم 137. مفتوح منذ 1985. السيدة بيرت تعرف كل قماش. هي فلمنكية، لكن أفضل زبائنها مغاربة — هي تفهمنا." },
    ],
    fatima_after_fabric: [
      { text: "القماش! شكرًا، شكرًا! نورا ستكون سعيدة جدًا." },
      { text: "أنت إنسان طيب. الحي يحتاج إلى أشخاص مثلك. إذا احتجت يومًا مساعدة — أنا هنا." },
    ],
    fatima_post_trust: [
      { text: "هل سمعت أن مضاربًا يريد شراء ثلاثة عقارات؟ الجميع قلقون." },
      { text: "عمر الخباز لديه مشاكل أيضًا — ليس لديه دقيق لصباح الغد. ربما يمكنك المساعدة؟" },
    ],
    fatima_faction: [
      { text: "ساميناان تافيل... نعم. إذا انضم الجميع، فنعم. سأتصل بالجمعية المغربية." },
    ],
    omar_bakker: [
      { text: "خبز؟ مسمن؟ طازج من الساعة الخامسة هذا الصباح! فرني لا يتوقف أبدًا في تورنهاوتسيبان." },
      { text: "خلال رمضان أحيانًا أخبز حتى منتصف الليل. ثم يكون الحي كله أمام بابي." },
      { text: "هل سمعت عن طاولة الكيلومترين؟ خبزنا خبزًا لـ 7000 شخص." },
    ],
    omar_flour_request: [
      { text: "أيوا، مشكلة كبيرة! موردي مريض. لا دقيق لغد. Budget Market لديهم — لكنني لا أستطيع مغادرة المحل.", choices: ["سأحضره لك.", "كم من الدقيق؟"] },
    ],
    omar_flour_thanks: [
      { text: "بارك الله فيك! Budget Market، رقم 326. كيسان من 5 كيلو. قل فقط إنه لعمر." },
    ],
    omar_flour_detail: [
      { text: "كيسان، 5 كيلو كل منهما. دقيق جيد الجودة — نوع 45 إن كان متاحًا. Budget Market، رقم 326." },
    ],
    omar_flour_done: [
      { text: "الدقيق! ممتاز. تفضل — حريرة وبقلاوة لك. وإذا احتجت خبزًا يومًا: مجانًا، دائمًا." },
    ],
    stunt_baert: [
      { text: "Stunt Solderie، مفتوح منذ '85! رأيت الحي كله يتغير." },
      { text: "كان هذا حيًّا عماليًّا فلمنكيًّا. الآن أسمع خمس لغات عندما أفتح بابي." },
      { text: "لكن تعرف؟ أفضل زبائني هن النساء المغربيات. يعرفن الأقمشة أكثر من أي شخص آخر." },
    ],
    stunt_baert_fabric: [
      { text: "لابنة أخت فاطمة! بالطبع. كنت قد أبقيت قطعة جانبًا — علمت أنها ستُرسل أحدًا." },
      { text: "أخبري فاطمة أن القماش هدية من Stunt Solderie. بعد كل هذه السنين." },
    ],
    stunt_baert_signature: [
      { text: "عريضة؟ ضد ذلك المضارب؟ هاتها. أنا أول من يوقع. محلي هنا منذ 40 سنة." },
    ],
    stunt_baert_faction: [
      { text: "Bar Leon؟ هؤلاء الرجال ليسوا سهلين. لكن إذا ذهبت وشرحت ما الأمر... يعرفونني. سأفعل ذلك." },
    ],
    reza_music: [
      { text: "بسست. هل تسمع ذلك؟ تلك الأصوات تأتي من De Roma. كل أسبوع شيء مختلف — جنوى، جاز، راب." },
      { text: "بول مكارتني عزف هنا مرة. حقًّا. Turnhoutsebaan 286، أغسطس '72." },
      { text: "عودي لها وتر مكسور. إذا وجدت واحدًا عند ميمون، رقم 239، سأعزف لك أغنية الليلة.", choices: ["سأبحث عن ذلك الوتر لك.", "أخبرني أكثر عن De Roma."] },
    ],
    reza_oud_accept: [
      { text: "ميمون، رقم 239 — أبعد في الشارع. لديهم أحيانًا إكسسوارات موسيقية. اسأل عن أوتار للعود." },
    ],
    reza_de_roma_lore: [
      { text: "De Roma هو Art Deco، 1927. بناه ألفونس باولز لـ 2000 شخص. بعد سنوات من الإهمال، أُنقذ بواسطة 400 متطوع في 2003." },
      { text: "الآن جنوى من مراكش، هيب هوب من بورغيرهاوت، جاز من كل مكان. هذا هو تورنهاوتسيبان." },
    ],
    reza_oud_found: [
      { text: "الوتر... مثالي. انتظر." },
      { text: "*يعزف* ... هل تسمع ذلك؟ هذه لغة هذا الشارع. أنت أيضًا تفهمها الآن." },
    ],
    reza_signature: [
      { text: "ذلك المضارب؟ أعرفه. يريد شراء استوديوي أيضًا. هذا توقيعي، وتوقيعا جاري." },
    ],
    yusuf_delivery: [
      { text: "لا لا لا! إطار مثقوب و12 طردًا بعد! سيدي، سيدتي — هل يمكنكم مساعدتي؟", choices: ["سأساعدك في الثلاثة الأخيرة.", "أين يجب أن تذهب؟"] },
    ],
    yusuf_delivery_accept: [
      { text: "حقًّا؟ رائع! الطرد 1 ← رقم 170 (Patisserie Aladdin). الطرد 2 ← رقم 137 (Indian Boutique). الطرد 3 ← رقم 284 (Borger Hub). من فضلك!" },
    ],
    yusuf_delivery_info: [
      { text: "رقم 170، رقم 137، ورقم 284. ثلاثة عناوين، شارع واحد. ليس بعيدًا! سأعطيك تذكرة ترام كمكافأة." },
    ],
    yusuf_delivery_done: [
      { text: "تم التسليم كله؟ رائع! تفضل — تذكرة ترام. عسى عربتك لا تتعطل أبدًا." },
    ],
    hamza_marbles: [
      { text: "يو! كرات الرخام؟ دائمًا. لكن أريد أيضًا أن أسأل شيئًا — للمدرسة. هل تعرف ما هي Reuzenpoort؟" },
      { text: "أستاذتنا تقول إنها بوابة تاريخية. لكن لماذا هي هنا في تورنهاوتسيبان؟" },
    ],
    hamza_school_faction: [
      { text: "المدرسة تشارك في ساميناان تافيل؟ سأسأل الأستاذة De Smedt. إنها رائعة، ستقول نعم بالتأكيد." },
    ],
    aziz_signature: [
      { text: "أنا هنا منذ 40 سنة. رأيت كيف استبعدونا أولًا، ثم تحملونا، والآن ربما... يقبلوننا." },
      { text: "توقيعي؟ نعم. لهذا الشارع سأوقع أي شيء." },
    ],
    fatima_signature: [
      { text: "عريضة! أخيرًا. هاتها. الاسم والعنوان والتاريخ — تمام. اذهب الآن إلى عمر، وريزا، والسيدة بيرت، وعزيز." },
    ],
    omar_signature: [
      { text: "ذلك المضارب؟ حاول العام الماضي أيضًا شراء مخبزي. تفضل — توقيع. وخذ خبزًا معك." },
    ],
    tine_faction: [
      { text: "آه، ساميناان تافيل! أعرف رئيس النادي الاجتماعي التركي منذ 20 سنة. إذا طلبت أنت وأنا دعمت — سيقول نعم." },
    ],
    kid_marbles: [
      { text: "يو! تريد لعب كرات الرخام؟ أنا دائمًا أفوز لكن الأمر ممل إن لم يكن هناك أحد للعب ضده." },
      { text: "جدتي تقول إن الشرطة كانت تتجول هنا دائمًا. الآن هناك مقهى. أفضل، أليس كذلك؟" },
    ],
    delivery_rush: [
      { text: "لا لا لا، ليس الآن! عربتي لها إطار مثقوب ولا يزال لدي 12 طردًا لتسليمها!" },
      { text: "إذا ساعدتني في الثلاثة الأخيرة، سأعطيك تذكرة ترام. اتفاق؟" },
    ],
    reuzenpoort_blocked: [
      { text: "البوابة تبقى مغلقة للغرباء. تحدث أولًا مع فاطمة في بداية الشارع." },
    ],
    de_roma_blocked: [
      { text: "باب De Roma يفتح فقط لمن يفهم لغة الشارع. ابحث عن وتر عود ريزا." },
    ],
    deurne_blocked: [
      { text: "حارس الحدود يطلب أوراقك. اهزم البيروقراطي البلدوزر واحمل تصريحه." },
    ],
    reuzenpoort_legend: [
      { text: "Reuzenpoort يعود إلى عام 1713. بُني لـ Reuzenhaus — قبل وجود البلدية بزمن طويل." },
      { text: "في 1833 هدموا Reuzenhaus لبلدية Josephus Hoefnagels الجديدة. لكن البوابة بقيت." },
      { text: "بورغيرهاوت كانت مستقلة لقرون. فقط في 1 يناير 1983 أصبحنا أنتويرب. كثيرون لا يزالون يأسفون على ذلك." },
    ],
    de_roma_keeper: [
      { text: "هذا المبنى Art Deco، بُني عام 1927. صممه ألفونس باولز لـ 2000 متفرج." },
      { text: "بعد سنوات من الإهمال، أُنقذنا عام 2003 بواسطة بول شيفنز و400 متطوع." },
      { text: "الليلة: موسيقى جنوى من مراكش. الغد: هيب هوب من بورغيرهاوت. أهلًا دائمًا." },
    ],
    de_roma_concert: [
      { text: "ريزا يعزف الليلة على المسرح. بفضلك. بفضل الوتر الذي وجدته." },
      { text: "*يعزف العود* هذه الأغنية تسمى 'تورنهاوتسيبان'. كتبتها للجميع هنا." },
    ],
    district_mayor: [
      { text: "مساء الخير. أنا مريم العسري، رئيسة مقاطعة بورغيرهاوت." },
      { text: "سمعت عما فعلته — القماش، والعريضة، والوتر. هذا الشارع يحتاج إليك." },
      { text: "أنظم ساميناان تافيل: طاولة بكيلومترين، 7000 شخص، عيد الفصح والإفطار معًا. لكن أحتاج إلى 7 فصائل. هل تريد المساعدة؟", choices: ["نعم. أنا معك.", "أخبرني أكثر."] },
    ],
    mayor_briefing: [
      { text: "حسنًا. سبع فصائل: الجمعية المغربية، النادي التركي، Bar Leon، Borgerhub، المدرسة، المسجد، وFrituur de Tram. واحدة تلو الأخرى." },
    ],
    mayor_explains: [
      { text: "أبريل 2024. كيلومتران. عيد الفصح والإفطار في نفس اليوم. 7000 مقعد. تورنهاوتسيبان كلها على الطاولة. تاريخ حقيقي." },
    ],
    imam_mosque: [
      { text: "سلام. سمعت عن طاولتكم. إذا تم احترام وجبة الإفطار — إذا لم يكن هناك كحول بجانب صحوننا — سنشارك.", choices: ["أعدك. سنخصص مناطق منفصلة.", "كيف تتصور ذلك؟"] },
    ],
    imam_agreed: [
      { text: "الحمد لله. المسجد يشارك. وجبة مشتركة تزيل حكمًا." },
    ],
    imam_explains: [
      { text: "قسم منفصل: حلال، بدون كحول، لكن بجانب الآخرين. ليس منفصلًا. معًا لكن باحترام." },
    ],
    frituur_faction: [
      { text: "7000 كيس بطاطس؟ هذا... كثير من البطاطس. لكن إذا رتبت الطلبية عند تاجر الجملة، سنشارك.", choices: ["سأرتب الطلبية.", "كم يكلف ذلك؟"] },
    ],
    frituur_agreed: [
      { text: "رائع! بطاطس بصلصة الأندلس لـ 7000 شخص. سيُسجَّل ذلك في التاريخ." },
    ],
    frituur_cost: [
      { text: "خمسة عملات للدفعة الأولى. ثم سنرتب الباقي." },
    ],
    borgerhub_faction: [
      { text: "مجموعة فنية في ساميناان تافيل؟ إذا شارك De Roma أيضًا — بالتأكيد. الفن والمجتمع ينتميان معًا." },
    ],
    geest_van_88_encounter: [
      { text: "بورغيروكو! هذا حينا! أنتم لا تنتمون هنا!" },
      { text: "شبح '88 لا يمكن هزيمته بالقوة. استخدم 'ساميناان تافيل' في المعركة." },
    ],
    geest_van_88_defeated: [
      { text: "أنا... لم أجلس يومًا... طوال هذه السنوات... على الطاولة مع..." },
      { text: "*يختفي ببطء* ...بالهناء والشفاء." },
    ],
  },
};
