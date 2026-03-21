/** Translated quest titles, descriptions and objective labels for EN, FR, AR. */
type QuestT = { title: string; description: string; objectives: Record<string, string> };
export const QUEST_LOCALES: Record<'en' | 'fr' | 'ar', Record<string, QuestT>> = {

  // ── ENGLISH ───────────────────────────────────────────────────────────────
  en: {
    q_starter_delivery: {
      title: 'The First Delivery',
      description: 'Yusuf the courier has a flat tyre. Help him deliver three parcels.',
      objectives: {
        talk_yusuf:   'Talk to Yusuf the courier',
        deliver_done: 'Help Yusuf with the deliveries',
      },
    },
    q_fabric_quest: {
      title: 'Fabric for Nora',
      description: "Fatima's niece Nora is getting married next month. She needs beautiful fabric from Stunt Solderie.",
      objectives: {
        get_fabric:     'Pick up the fabric from Mrs. Baert (Indian Boutique, nr.137)',
        deliver_fabric: 'Bring the fabric to Fatima',
      },
    },
    q_flour_shortage: {
      title: 'Baker Without Flour',
      description: 'Omar has no flour left for the morning shift. Get flour from Budget Market.',
      objectives: {
        buy_flour:     'Buy flour at Budget Market (nr.326)',
        deliver_flour: 'Bring the flour to Omar',
      },
    },
    q_oud_string: {
      title: "Reza's Broken String",
      description: "Reza's oud has a broken string. He can't play until you find one at Mimoun.",
      objectives: {
        find_string: 'Find an oud string at Mimoun (nr.239)',
        give_reza:   'Give the string to Reza',
      },
    },
    q_signatures: {
      title: 'Signatures Against Eviction',
      description: 'A property speculator threatens to buy three buildings and evict residents. Collect 5 signatures for the petition.',
      objectives: {
        sig_fatima: 'Signature from Fatima',
        sig_omar:   'Signature from Omar',
        sig_reza:   'Signature from Reza',
        sig_baert:  'Signature from Mrs. Baert',
        sig_aziz:   'Signature from Aziz (elder)',
      },
    },
    q_beno_repair: {
      title: 'Broken Bakfiets',
      description: 'Your bakfiets is damaged. Ben at Costermans Cycling Sports (nr.332) can repair it.',
      objectives: {
        visit_beno:  'Go to Costermans Cycling Sports (nr.332)',
        repair_done: 'Pay for the repair (20 coins)',
      },
    },
    q_bulldozer_fight: {
      title: 'The Bulldozer Bureaucrat',
      description: 'The property speculator stands before the three buildings. With the petition and neighbourhood support you can confront him.',
      objectives: {
        enter_zone3:      'Go to Borger Hub (nr.284)',
        defeat_bulldozer: 'Defeat the Bureau-Bulldozer',
      },
    },
    q_geest_88: {
      title: "The Ghost of '88",
      description: "A dark ghost from the '80s appears on Turnhoutsebaan. He cannot be defeated by force — only by sharing a table.",
      objectives: {
        find_geest:  "Find the Ghost of '88",
        pacify_geest: "Defeat the Ghost with 'Samen Aan Tafel' (not with attacks)",
      },
    },
    q_mayor_meeting: {
      title: 'District Chair El Osri',
      description: 'Mariam El Osri wants to speak to you about a big plan for Turnhoutsebaan.',
      objectives: {
        meet_mayor: 'Speak with District Chair El Osri',
      },
    },
    q_faction_moroccan: {
      title: 'The Moroccan Association',
      description: 'The Moroccan community association is still hesitating. Fatima can persuade them — but you must first persuade her.',
      objectives: {
        convince_fatima_faction: 'Convince Fatima to contact the association',
      },
    },
    q_faction_turkish: {
      title: 'The Turkish Social Club',
      description: "Tine knows the chairman of the Turkish social club. She'll say yes if you approach her in the right spirit.",
      objectives: {
        talk_tine_faction: 'Talk to Tine about the Turkish social club',
      },
    },
    q_faction_flemish: {
      title: 'Bar Leon at Krugerplein',
      description: "The Flemish regulars at Bar Leon are sceptical. Mrs. Baert is the key — she's respected by both sides.",
      objectives: {
        talk_baert_faction: 'Ask Mrs. Baert to persuade Bar Leon',
      },
    },
    q_faction_art: {
      title: "Borgerhub Artists' Collective",
      description: 'The artists at Borgerhub want to participate — but only if De Roma also joins.',
      objectives: {
        link_roma_borgerhub: "Link De Roma's spirit to Borgerhub",
      },
    },
    q_faction_school: {
      title: 'The Neighbourhood School',
      description: "Hamza's school wants to participate but the headmaster is worried about order. Hamza can persuade him.",
      objectives: {
        talk_hamza_school: 'Talk to Hamza about his school',
      },
    },
    q_faction_mosque: {
      title: 'De-Koepel Mosque',
      description: 'The imam of De-Koepel Mosque wants the table to also be an iftar moment. He will say yes after your promise.',
      objectives: {
        talk_imam: 'Talk to the imam of De-Koepel Mosque (Stenenbrug 11)',
      },
    },
    q_faction_frituur: {
      title: 'Frituur de Tram',
      description: 'Frituur de Tram wants to fry 7000 bags of chips. They need your help ordering enough potatoes.',
      objectives: {
        order_fries: 'Help Frituur de Tram with the bulk order',
      },
    },
  },

  // ── FRANÇAIS ──────────────────────────────────────────────────────────────
  fr: {
    q_starter_delivery: {
      title: 'La Première Livraison',
      description: 'Yusuf le livreur a un pneu crevé. Aide-le à livrer trois colis.',
      objectives: {
        talk_yusuf:   'Parle à Yusuf le livreur',
        deliver_done: 'Aide Yusuf avec les livraisons',
      },
    },
    q_fabric_quest: {
      title: 'Le Tissu pour Nora',
      description: 'La nièce de Fatima, Nora, se marie le mois prochain. Elle a besoin de beau tissu de Stunt Solderie.',
      objectives: {
        get_fabric:     'Récupère le tissu chez Madame Baert (Indian Boutique, nr.137)',
        deliver_fabric: 'Apporte le tissu à Fatima',
      },
    },
    q_flour_shortage: {
      title: 'Boulanger Sans Farine',
      description: "Omar n'a plus de farine pour le service du matin. Achète de la farine chez Budget Market.",
      objectives: {
        buy_flour:     'Achète de la farine chez Budget Market (nr.326)',
        deliver_flour: 'Apporte la farine à Omar',
      },
    },
    q_oud_string: {
      title: 'La Corde Cassée de Reza',
      description: "L'oud de Reza a une corde cassée. Il ne peut pas jouer jusqu'à ce que tu en trouves une.",
      objectives: {
        find_string: 'Trouve une corde de oud chez Mimoun (nr.239)',
        give_reza:   'Donne la corde à Reza',
      },
    },
    q_signatures: {
      title: "Signatures Contre l'Expulsion",
      description: "Un spéculateur immobilier menace d'acheter trois propriétés et d'expulser les résidents. Collecte 5 signatures.",
      objectives: {
        sig_fatima: 'Signature de Fatima',
        sig_omar:   "Signature d'Omar",
        sig_reza:   'Signature de Reza',
        sig_baert:  'Signature de Madame Baert',
        sig_aziz:   "Signature d'Aziz (ancien)",
      },
    },
    q_beno_repair: {
      title: 'Bakfiets Cassé',
      description: 'Ton bakfiets est endommagé. Ben chez Costermans Wielersport (nr.332) peut le réparer.',
      objectives: {
        visit_beno:  'Va chez Costermans Wielersport (nr.332)',
        repair_done: 'Paie pour la réparation (20 pièces)',
      },
    },
    q_bulldozer_fight: {
      title: 'Le Bureaucrate-Bulldozer',
      description: "Le spéculateur immobilier se tient devant les trois propriétés. Avec la pétition et le soutien du quartier, tu peux l'affronter.",
      objectives: {
        enter_zone3:      'Va à Borger Hub (nr.284)',
        defeat_bulldozer: 'Bats le Bureau-Bulldozer',
      },
    },
    q_geest_88: {
      title: "Le Fantôme de '88",
      description: "Un esprit sombre des années '80 apparaît sur la Turnhoutsebaan. Il ne peut être vaincu par la force — seulement en partageant une table.",
      objectives: {
        find_geest:   "Trouve le Fantôme de '88",
        pacify_geest: "Bats le Fantôme avec 'Samen Aan Tafel' (pas avec des attaques)",
      },
    },
    q_mayor_meeting: {
      title: "Présidente de District El Osri",
      description: "Mariam El Osri veut te parler d\u2019un grand projet pour la Turnhoutsebaan.",
      objectives: {
        meet_mayor: "Parle avec la Présidente de District El Osri",
      },
    },
    q_faction_moroccan: {
      title: "L\u2019Association Marocaine",
      description: "L\u2019association communautaire marocaine hésite encore. Fatima peut les convaincre — mais tu dois d\u2019abord la convaincre, elle.",
      objectives: {
        convince_fatima_faction: "Convaincs Fatima de contacter l\u2019association",
      },
    },
    q_faction_turkish: {
      title: "Le Club Social Turc",
      description: "Tine connaît le président du club social turc. Elle dira oui si tu l\u2019approches dans le bon esprit.",
      objectives: {
        talk_tine_faction: "Parle à Tine du club social turc",
      },
    },
    q_faction_flemish: {
      title: 'Bar Leon au Krugerplein',
      description: 'Les habitués flamands de Bar Leon sont sceptiques. Madame Baert est la clé — elle est respectée des deux côtés.',
      objectives: {
        talk_baert_faction: 'Demande à Madame Baert de convaincre Bar Leon',
      },
    },
    q_faction_art: {
      title: "Collectif d'Artistes Borgerhub",
      description: "Les artistes de Borgerhub veulent participer — mais seulement si De Roma participe aussi.",
      objectives: {
        link_roma_borgerhub: "Lie l'esprit de De Roma à Borgerhub",
      },
    },
    q_faction_school: {
      title: "L'École du Quartier",
      description: "L'école de Hamza veut participer mais le directeur est soucieux de l'ordre. Hamza peut le convaincre.",
      objectives: {
        talk_hamza_school: 'Parle à Hamza de son école',
      },
    },
    q_faction_mosque: {
      title: 'Mosquée De-Koepel',
      description: "L'imam de la Mosquée De-Koepel veut que la table soit aussi un moment d'iftar. Il dira oui après ta promesse.",
      objectives: {
        talk_imam: "Parle à l'imam de la Mosquée De-Koepel (Stenenbrug 11)",
      },
    },
    q_faction_frituur: {
      title: 'Frituur de Tram',
      description: 'Frituur de Tram veut faire frire 7000 portions de frites. Ils ont besoin de ton aide pour commander assez de pommes de terre.',
      objectives: {
        order_fries: 'Aide Frituur de Tram avec la grosse commande',
      },
    },
  },

  // ── العربية ───────────────────────────────────────────────────────────────
  ar: {
    q_starter_delivery: {
      title: 'أول تسليم',
      description: 'يوسف الساعي لديه إطار مثقوب. ساعده في تسليم ثلاثة طرود.',
      objectives: {
        talk_yusuf:   'تحدث مع يوسف الساعي',
        deliver_done: 'ساعد يوسف في التسليمات',
      },
    },
    q_fabric_quest: {
      title: 'قماش نورا',
      description: 'ابنة أخت فاطمة نورا ستتزوج الشهر القادم. تحتاج إلى قماش جميل من Stunt Solderie.',
      objectives: {
        get_fabric:     'اجلب القماش من السيدة بيرت (Indian Boutique، رقم 137)',
        deliver_fabric: 'أوصل القماش إلى فاطمة',
      },
    },
    q_flour_shortage: {
      title: 'خباز بلا دقيق',
      description: 'عمر ليس لديه دقيق لوردية الصباح. اشتر دقيقًا من Budget Market.',
      objectives: {
        buy_flour:     'اشتر دقيقًا من Budget Market (رقم 326)',
        deliver_flour: 'أوصل الدقيق إلى عمر',
      },
    },
    q_oud_string: {
      title: 'وتر ريزا المكسور',
      description: 'عود ريزا لديه وتر مكسور. لا يمكنه العزف حتى تجد واحدًا.',
      objectives: {
        find_string: 'ابحث عن وتر عود عند ميمون (رقم 239)',
        give_reza:   'أعط الوتر لريزا',
      },
    },
    q_signatures: {
      title: 'توقيعات ضد الإخلاء',
      description: 'مضارب عقاري يهدد بشراء ثلاثة عقارات وطرد السكان. اجمع 5 توقيعات للعريضة.',
      objectives: {
        sig_fatima: 'توقيع فاطمة',
        sig_omar:   'توقيع عمر',
        sig_reza:   'توقيع ريزا',
        sig_baert:  'توقيع السيدة بيرت',
        sig_aziz:   'توقيع عزيز (شيخ الحي)',
      },
    },
    q_beno_repair: {
      title: 'عربة مكسورة',
      description: 'عربتك تالفة. بن في Costermans Wielersport (رقم 332) يمكنه إصلاحها.',
      objectives: {
        visit_beno:  'اذهب إلى Costermans Wielersport (رقم 332)',
        repair_done: 'ادفع مقابل الإصلاح (20 عملة)',
      },
    },
    q_bulldozer_fight: {
      title: 'البيروقراطي البلدوزر',
      description: 'المضارب العقاري يقف أمام العقارات الثلاثة. مع العريضة ودعم الحي يمكنك مواجهته.',
      objectives: {
        enter_zone3:      'اذهب إلى Borger Hub (رقم 284)',
        defeat_bulldozer: 'اهزم البيروقراطي البلدوزر',
      },
    },
    q_geest_88: {
      title: 'شبح الثمانينيات',
      description: 'شبح مظلم من الثمانينيات يظهر في تورنهاوتسيبان. لا يمكن هزيمته بالقوة — فقط بمشاركة الطعام.',
      objectives: {
        find_geest:   "ابحث عن شبح '88",
        pacify_geest: "اهزم الشبح بـ 'ساميناان تافيل' (لا بالهجمات)",
      },
    },
    q_mayor_meeting: {
      title: 'رئيسة المقاطعة العسري',
      description: 'مريم العسري تريد التحدث إليك عن خطة كبيرة لتورنهاوتسيبان.',
      objectives: {
        meet_mayor: 'تحدث مع رئيسة المقاطعة العسري',
      },
    },
    q_faction_moroccan: {
      title: 'الجمعية المغربية',
      description: 'جمعية المجتمع المغربي لا تزال تتردد. فاطمة يمكنها إقناعهم — لكن يجب أن تقنعها أنت أولًا.',
      objectives: {
        convince_fatima_faction: 'أقنع فاطمة للتواصل مع الجمعية',
      },
    },
    q_faction_turkish: {
      title: 'النادي الاجتماعي التركي',
      description: 'تين تعرف رئيس النادي الاجتماعي التركي. ستقول نعم إذا اقتربت منها بالروح الصحيحة.',
      objectives: {
        talk_tine_faction: 'تحدث مع تين عن النادي الاجتماعي التركي',
      },
    },
    q_faction_flemish: {
      title: 'Bar Leon في Krugerplein',
      description: 'زبائن Bar Leon الفلمنكيون متشككون. السيدة بيرت هي المفتاح — كلا الطرفين يحترمانها.',
      objectives: {
        talk_baert_faction: 'اطلب من السيدة بيرت إقناع Bar Leon',
      },
    },
    q_faction_art: {
      title: 'مجموعة فنانين Borgerhub',
      description: 'الفنانون في Borgerhub يريدون المشاركة — لكن فقط إذا شارك De Roma أيضًا.',
      objectives: {
        link_roma_borgerhub: 'ربط روح De Roma بـ Borgerhub',
      },
    },
    q_faction_school: {
      title: 'مدرسة الحي',
      description: 'مدرسة حمزة تريد المشاركة لكن المدير قلق على النظام. حمزة يمكنه إقناعه.',
      objectives: {
        talk_hamza_school: 'تحدث مع حمزة عن مدرسته',
      },
    },
    q_faction_mosque: {
      title: 'مسجد القبة',
      description: 'إمام مسجد القبة يريد أن تكون الطاولة أيضًا لحظة إفطار. سيقول نعم بعد وعدك.',
      objectives: {
        talk_imam: 'تحدث مع إمام مسجد القبة (Stenenbrug 11)',
      },
    },
    q_faction_frituur: {
      title: 'Frituur de Tram',
      description: 'Frituur de Tram يريد قلي 7000 كيس بطاطس. يحتاجون مساعدتك في طلب كميات كافية.',
      objectives: {
        order_fries: 'ساعد Frituur de Tram في الطلبية الكبيرة',
      },
    },
  },
};
