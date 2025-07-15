"""
Character generation system for the Warhammer Fantasy Tavern Simulator
Contains the 17 unique NPCs with detailed backgrounds and faction-specific traits
"""

from typing import List, Dict
from .character import Character
from .enums import Faction, CharacterClass, Skill

class CharacterGenerator:
    """Generates the 17 unique NPCs for the tavern simulator"""
    
    def __init__(self):
        self.unique_characters = self._create_unique_characters()
    
    def get_all_characters(self) -> List[Character]:
        """Get all 17 unique characters"""
        return list(self.unique_characters.values())
    
    def get_character_by_name(self, name: str) -> Character:
        """Get a specific character by name"""
        return self.unique_characters.get(name)
    
    def _create_unique_characters(self) -> Dict[str, Character]:
        """Create all 17 unique characters with detailed backgrounds"""
        characters = {}
        
        # 1. Grimm Ironbeard - Dwarf Warrior
        characters["Grimm Ironbeard"] = Character(
            name="Grimm Ironbeard",
            faction=Faction.DWARF,
            character_class=CharacterClass.WARRIOR,
            age=156,
            gender="Male",
            appearance="A stocky dwarf with a magnificent braided beard adorned with iron rings. Wears chainmail and carries a massive two-handed axe.",
            distinctive_features="Iron rings in beard, battle scars on arms, missing left pinky finger",
            backstory="A veteran of the War of Vengeance, Grimm has spent decades fighting greenskins in the World's Edge Mountains. He came to the tavern seeking respite from endless warfare.",
            motivation="To find peace after a lifetime of war, but struggles with civilian life",
            secrets=["Has nightmares about fallen comrades", "Secretly fears he's too old to fight effectively"],
            personality_traits=["Gruff but honorable", "Protective of innocents", "Distrusts magic users", "Values craftsmanship"],
            likes=["Good ale", "Well-made weapons", "Stories of valor", "Honest work"],
            dislikes=["Elves", "Cowardice", "Shoddy craftsmanship", "Being called short"],
            greeting_phrases=[
                "By Grungni's hammer, what brings you here?",
                "The ale better be worth the coin, manling.",
                "I've fought orcs tougher than you look.",
                "Sit, but don't expect me to be chatty."
            ],
            faction_specific_phrases=[
                "The Ancestor Gods watch over us.",
                "A grudge remembered is a grudge avenged.",
                "Khazad! Khazad ai-mênu!",
                "The Book of Grudges grows heavy."
            ]
        )
        
        # 2. Lady Elara Brightblade - High Elf Noble
        characters["Lady Elara Brightblade"] = Character(
            name="Lady Elara Brightblade",
            faction=Faction.HIGH_ELF,
            character_class=CharacterClass.NOBLE,
            age=234,
            gender="Female",
            appearance="Tall and graceful with silver hair and piercing blue eyes. Wears elegant robes with subtle magical enchantments.",
            distinctive_features="Silver hair that seems to shimmer, a small scar on her left temple, carries an ornate staff",
            backstory="A minor noble from Ulthuan who came to the Old World to study human culture and magic. She finds the experience both fascinating and appalling.",
            motivation="To understand the 'lesser races' and report back to the Phoenix King's court",
            secrets=["Is actually a spy for Ulthuan", "Has developed genuine affection for some humans"],
            personality_traits=["Arrogant but curious", "Intellectually superior", "Secretly lonely", "Fascinated by human emotion"],
            likes=["Fine wine", "Intellectual discourse", "Ancient lore", "Beautiful art"],
            dislikes=["Crude behavior", "Loud noises", "Dwarfs", "Being ignored"],
            greeting_phrases=[
                "How... quaint. I suppose you'll do for conversation.",
                "I trust you can speak without shouting?",
                "Your customs are most... interesting.",
                "Do try not to disappoint me entirely."
            ],
            faction_specific_phrases=[
                "By Asuryan's light...",
                "The winds of magic whisper of change.",
                "Such crude understanding of the mystical arts.",
                "In Ulthuan, we would handle this differently."
            ]
        )
        
        # 3. Brother Marcus - Empire Priest
        characters["Brother Marcus"] = Character(
            name="Brother Marcus",
            faction=Faction.EMPIRE,
            character_class=CharacterClass.PRIEST,
            age=45,
            gender="Male",
            appearance="A middle-aged man with kind eyes and calloused hands. Wears simple brown robes with Sigmar's hammer pendant.",
            distinctive_features="Burn scar on right hand from holy ritual, always carries a worn prayer book",
            backstory="A former soldier who found faith after surviving a chaos incursion. Now travels the Empire offering spiritual guidance to common folk.",
            motivation="To bring Sigmar's light to the darkest corners of the Empire",
            secrets=["Struggles with doubt about his faith", "Once killed a man in cold blood before finding religion"],
            personality_traits=["Compassionate", "Patient", "Haunted by past", "Protective of the innocent"],
            likes=["Helping others", "Simple pleasures", "Prayer", "Acts of kindness"],
            dislikes=["Chaos cultists", "Cruelty", "Excessive drinking", "Blasphemy"],
            greeting_phrases=[
                "Sigmar's blessings upon you, friend.",
                "May I offer you comfort in these troubled times?",
                "The light of faith guides us all.",
                "Peace be with you, traveler."
            ],
            faction_specific_phrases=[
                "Sigmar protects the faithful.",
                "The Empire stands strong against darkness.",
                "By hammer and faith, we endure.",
                "The twin-tailed comet shows the way."
            ]
        )
        
        # 4. Slytha Shadowstep - Wood Elf Scout
        characters["Slytha Shadowstep"] = Character(
            name="Slytha Shadowstep",
            faction=Faction.WOOD_ELF,
            character_class=CharacterClass.SCOUT,
            age=89,
            gender="Female",
            appearance="Lithe and quick with forest-green clothing and intricate tattoos. Moves with predatory grace.",
            distinctive_features="Leaf-pattern tattoos on arms, always barefoot, carries a longbow",
            backstory="Exiled from Athel Loren for questioning the Wild Hunt's brutality. Now wanders the Old World, torn between two worlds.",
            motivation="To find her place between the wild forest and civilized world",
            secrets=["Killed her own cousin during the Wild Hunt", "Can speak to forest spirits"],
            personality_traits=["Fierce and independent", "Distrusts civilization", "Quick to anger", "Protective of nature"],
            likes=["Open spaces", "Natural beauty", "Archery", "Wild animals"],
            dislikes=["Cities", "Pollution", "Cages", "Unnecessary killing"],
            greeting_phrases=[
                "The forest whispers of your approach.",
                "You smell of stone and smoke.",
                "What brings you to my path, groundling?",
                "Speak quickly, I have little patience."
            ],
            faction_specific_phrases=[
                "The Wild Hunt rides eternal.",
                "Orion's horn calls to the faithful.",
                "The forest remembers all debts.",
                "Kurnous guide my arrows true."
            ]
        )
        
        # 5. Sir Gaston de Montfort - Bretonnian Knight
        characters["Sir Gaston de Montfort"] = Character(
            name="Sir Gaston de Montfort",
            faction=Faction.BRETONNIAN,
            character_class=CharacterClass.NOBLE,
            age=28,
            gender="Male",
            appearance="Tall and handsome with perfectly groomed mustache. Wears fine clothes and carries himself with noble bearing.",
            distinctive_features="Elaborate mustache, family crest ring, always impeccably dressed",
            backstory="A knight errant seeking glory and adventure. His quest brought him far from Bretonnia, but he maintains his chivalric ideals.",
            motivation="To prove his worth and earn his spurs as a Knight of the Realm",
            secrets=["Is terrified of failing his quest", "Has never actually been in a real battle"],
            personality_traits=["Chivalrous", "Naive", "Brave but inexperienced", "Romantic idealist"],
            likes=["Tales of chivalry", "Beautiful ladies", "Honor", "Fine horses"],
            dislikes=["Cowardice", "Dishonor", "Peasant food", "Being mocked"],
            greeting_phrases=[
                "Good morrow, fair citizen!",
                "Honor and glory guide my steps!",
                "A knight's duty is never done!",
                "Might I regale you with tales of valor?"
            ],
            faction_specific_phrases=[
                "For the Lady and Bretonnia!",
                "Chivalry demands no less!",
                "The Grail Knights inspire us all!",
                "Honor above all else!"
            ]
        )
        
        # 6. Pip Greenhill - Halfling Merchant
        characters["Pip Greenhill"] = Character(
            name="Pip Greenhill",
            faction=Faction.HALFLING,
            character_class=CharacterClass.MERCHANT,
            age=52,
            gender="Male",
            appearance="A rotund halfling with curly hair and a perpetual smile. Wears a colorful vest and carries multiple pouches.",
            distinctive_features="Always eating something, has seven different pouches, missing tooth from bar fight",
            backstory="A traveling merchant from the Moot who specializes in rare spices and comfort foods. His jovial nature hides a sharp business mind.",
            motivation="To become the most successful halfling merchant outside the Moot",
            secrets=["Smuggles illegal goods occasionally", "Has a gambling addiction"],
            personality_traits=["Cheerful", "Greedy", "Sociable", "Cunning"],
            likes=["Good food", "Profit", "Gossip", "Comfortable beds"],
            dislikes=["Empty stomachs", "Bad deals", "Violence", "Waste"],
            greeting_phrases=[
                "Well met, friend! Care to see my wares?",
                "A good meal makes everything better!",
                "Business is good when everyone's happy!",
                "Have you heard the latest news from the road?"
            ],
            faction_specific_phrases=[
                "The Moot's finest, guaranteed!",
                "A halfling's word is his bond!",
                "Nothing beats home cooking!",
                "The Elder's wisdom guides good business!"
            ]
        )
        
        # 7. Captain Isabella Torretti - Tilean Mercenary
        characters["Captain Isabella Torretti"] = Character(
            name="Captain Isabella Torretti",
            faction=Faction.TILEAN,
            character_class=CharacterClass.SOLDIER,
            age=34,
            gender="Female",
            appearance="A weathered woman with olive skin and numerous scars. Wears practical leather armor and carries multiple weapons.",
            distinctive_features="Scar across left cheek, gold tooth, always armed",
            backstory="Former captain of a mercenary company that was destroyed by Skaven. Now works alone, seeking revenge and coin.",
            motivation="To rebuild her company and get revenge on the Skaven who destroyed it",
            secrets=["Sole survivor of her company's massacre", "Has a price on her head in Tilea"],
            personality_traits=["Pragmatic", "Ruthless", "Loyal to friends", "Haunted by loss"],
            likes=["Good wine", "Reliable weapons", "Honest pay", "Competent allies"],
            dislikes=["Skaven", "Betrayal", "Incompetence", "Cheap wine"],
            greeting_phrases=[
                "You hiring, or just drinking?",
                "Coin talks louder than words.",
                "I've seen worse places than this.",
                "What's the job, and what's the pay?"
            ],
            faction_specific_phrases=[
                "Myrmidia guide my blade!",
                "In Tilea, we settle debts with steel.",
                "The city-states breed the best soldiers.",
                "Gold and glory, in that order."
            ]
        )
        
        # 8. Yuki Snowblossom - Nipponese Monk (Rare visitor)
        characters["Yuki Snowblossom"] = Character(
            name="Yuki Snowblossom",
            faction=Faction.NIPPONESE,
            character_class=CharacterClass.SCHOLAR,
            age=26,
            gender="Female",
            appearance="Small and graceful with black hair in an elaborate style. Wears flowing silk robes and moves with fluid precision.",
            distinctive_features="Elaborate hair ornaments, silk fan, moves like a dancer",
            backstory="A scholar-monk from distant Nippon studying foreign cultures and martial arts. Her presence in the Old World is extremely rare.",
            motivation="To master foreign fighting techniques and bring knowledge back to Nippon",
            secrets=["Is actually a spy for her clan", "Practices forbidden martial arts"],
            personality_traits=["Mysterious", "Disciplined", "Curious", "Honor-bound"],
            likes=["Learning", "Tea ceremony", "Martial arts", "Poetry"],
            dislikes=["Rudeness", "Ignorance", "Disorder", "Loud noises"],
            greeting_phrases=[
                "Honorable greetings, foreign friend.",
                "Your customs are most intriguing.",
                "May harmony guide our meeting.",
                "I seek knowledge of your ways."
            ],
            faction_specific_phrases=[
                "The ancestors watch over us.",
                "Balance in all things.",
                "The way of the warrior is death.",
                "Honor is sharper than any blade."
            ]
        )
        
        # 9. Dmitri Volkov - Kislev Ice Guard
        characters["Dmitri Volkov"] = Character(
            name="Dmitri Volkov",
            faction=Faction.KISLEV,
            character_class=CharacterClass.SOLDIER,
            age=31,
            gender="Male",
            appearance="A tall, broad-shouldered man with a thick beard and fur-lined coat. Bears the scars of countless battles against Chaos.",
            distinctive_features="Frost-blue eyes, bear claw necklace, always cold to the touch",
            backstory="A veteran of the Ice Guard who survived the siege of Praag. Haunted by what he saw, he travels south seeking warmer lands and peace.",
            motivation="To forget the horrors of Chaos and find a place where winter doesn't mean death",
            secrets=["Witnessed daemonic possession of his captain", "Has minor ice magic abilities"],
            personality_traits=["Stoic", "Melancholic", "Protective", "Superstitious"],
            likes=["Vodka", "Warm fires", "Simple food", "Honest folk"],
            dislikes=["Chaos symbols", "Cold weather", "Loud noises", "Weakness"],
            greeting_phrases=[
                "The cold follows me everywhere.",
                "You have not seen true winter, southerner.",
                "Drink with me, the night is long.",
                "The bear spirits guide my path."
            ],
            faction_specific_phrases=[
                "Ursun protect us from the dark.",
                "The Tzarina's will be done.",
                "Ice and iron, that's all we need.",
                "The north remembers its debts."
            ]
        )

        # 10. Ragnar Bloodaxe - Norse Raider
        characters["Ragnar Bloodaxe"] = Character(
            name="Ragnar Bloodaxe",
            faction=Faction.NORSE,
            character_class=CharacterClass.WARRIOR,
            age=29,
            gender="Male",
            appearance="A massive man with wild blonde hair and ritual scars. Wears furs and carries a massive two-handed axe.",
            distinctive_features="Ritual scars on chest, wolf pelt cloak, braided beard with bone ornaments",
            backstory="A Norse raider who grew tired of endless warfare and seeks to prove himself in single combat rather than raids.",
            motivation="To die gloriously in battle and earn a place in the halls of his ancestors",
            secrets=["Secretly fears he's a coward", "Dreams of a peaceful life but can't admit it"],
            personality_traits=["Violent", "Honor-bound", "Boastful", "Surprisingly philosophical"],
            likes=["Combat", "Strong drink", "Epic tales", "Worthy opponents"],
            dislikes=["Cowardice", "Weak beer", "Backing down", "Chaos worship"],
            greeting_phrases=[
                "Face me in combat, if you dare!",
                "The gods hunger for blood and glory!",
                "I smell fear on you, southling!",
                "Drink with me or fight me!"
            ],
            faction_specific_phrases=[
                "The All-Father watches!",
                "Blood for the Blood God... wait, wrong god.",
                "The ravens circle overhead.",
                "Death in battle is the greatest honor!"
            ]
        )

        # 11. Hassan al-Rashid - Arabyan Merchant
        characters["Hassan al-Rashid"] = Character(
            name="Hassan al-Rashid",
            faction=Faction.ARABYAN,
            character_class=CharacterClass.MERCHANT,
            age=43,
            gender="Male",
            appearance="A well-dressed man with dark skin and an elaborate turban. His clothes are fine silk and he carries himself with dignity.",
            distinctive_features="Jeweled turban, ornate curved dagger, speaks with exotic accent",
            backstory="A wealthy spice merchant from Araby who travels the Old World seeking rare goods and new markets.",
            motivation="To establish a trading empire spanning from Araby to the Empire",
            secrets=["Smuggles magical artifacts", "Is fleeing creditors in Araby"],
            personality_traits=["Charming", "Calculating", "Generous", "Secretive"],
            likes=["Fine goods", "Negotiation", "Exotic foods", "Beautiful things"],
            dislikes=["Poor quality", "Rushed deals", "Prejudice", "Cold weather"],
            greeting_phrases=[
                "Peace be upon you, honored friend.",
                "Perhaps we can do business together?",
                "The desert winds brought me here.",
                "I have wonders from distant lands!"
            ],
            faction_specific_phrases=[
                "By the Prophet's beard!",
                "The desert teaches patience.",
                "Araby's treasures are beyond compare.",
                "The djinn whisper of profit."
            ]
        )

        # 12. Li Wei - Cathayan Scholar
        characters["Li Wei"] = Character(
            name="Li Wei",
            faction=Faction.CATHAYAN,
            character_class=CharacterClass.SCHOLAR,
            age=67,
            gender="Male",
            appearance="An elderly man with a long white beard and traditional robes. Carries scrolls and writing materials.",
            distinctive_features="Long white beard, jade amulet, always writing in a journal",
            backstory="An elderly scholar from Grand Cathay studying the barbarian lands of the west. His wisdom is vast but his patience limited.",
            motivation="To document the strange customs of western barbarians for the Dragon Emperor",
            secrets=["Is actually much older than he appears", "Practices ancient magic"],
            personality_traits=["Wise", "Condescending", "Patient", "Observant"],
            likes=["Knowledge", "Tea", "Quiet contemplation", "Proper etiquette"],
            dislikes=["Ignorance", "Rudeness", "Waste", "Loud behavior"],
            greeting_phrases=[
                "Greetings, western barbarian.",
                "Your customs are... primitive.",
                "I observe much in your simple ways.",
                "The Dragon Emperor's wisdom guides me."
            ],
            faction_specific_phrases=[
                "The Celestial Dragon watches all.",
                "In Cathay, we have a saying...",
                "The Middle Kingdom endures.",
                "Harmony must be maintained."
            ]
        )

        # 13. Gunther Steinhammer - Empire Craftsman
        characters["Gunther Steinhammer"] = Character(
            name="Gunther Steinhammer",
            faction=Faction.EMPIRE,
            character_class=CharacterClass.CRAFTSMAN,
            age=38,
            gender="Male",
            appearance="A sturdy man with calloused hands and soot-stained apron. His arms are muscled from years at the forge.",
            distinctive_features="Burn scars on arms, leather apron, always carries hammer",
            backstory="A master blacksmith from Nuln who travels seeking rare metals and techniques. His work is renowned throughout the Empire.",
            motivation="To create the perfect weapon and earn recognition as the greatest smith alive",
            secrets=["Uses dwarf techniques learned in secret", "His masterwork was stolen by rivals"],
            personality_traits=["Perfectionist", "Proud", "Hardworking", "Stubborn"],
            likes=["Fine craftsmanship", "Good steel", "Honest work", "Recognition"],
            dislikes=["Shoddy work", "Laziness", "Thieves", "Magic weapons"],
            greeting_phrases=[
                "I can tell good steel by its ring.",
                "A craftsman's work speaks for itself.",
                "You need something forged?",
                "Quality takes time, friend."
            ],
            faction_specific_phrases=[
                "Sigmar guide my hammer!",
                "The Empire's steel is the finest!",
                "A good blade serves its master well.",
                "Honest work builds the realm."
            ]
        )

        # 14. Mordecai the Learned - Empire Wizard
        characters["Mordecai the Learned"] = Character(
            name="Mordecai the Learned",
            faction=Faction.EMPIRE,
            character_class=CharacterClass.WIZARD,
            age=52,
            gender="Male",
            appearance="A thin man with wild grey hair and ink-stained fingers. Wears robes covered in mystical symbols.",
            distinctive_features="Wild grey hair, multiple spell component pouches, constantly muttering",
            backstory="A Grey Wizard of the Empire who studies the nature of Chaos corruption. His research has made him paranoid and secretive.",
            motivation="To understand and combat Chaos corruption before it spreads",
            secrets=["Has been exposed to Chaos corruption", "Conducts illegal magical experiments"],
            personality_traits=["Paranoid", "Brilliant", "Obsessive", "Secretive"],
            likes=["Ancient lore", "Magical theory", "Solitude", "Complex puzzles"],
            dislikes=["Interruptions", "Ignorance", "Chaos symbols", "Bright lights"],
            greeting_phrases=[
                "The winds of magic are restless tonight.",
                "I sense... disturbances in the aethyr.",
                "Knowledge is the only true power.",
                "Beware the shadows, they have eyes."
            ],
            faction_specific_phrases=[
                "The Colleges teach discipline.",
                "Magic serves the Empire's needs.",
                "Chaos must be understood to be defeated.",
                "The Grey Wind shows hidden truths."
            ]
        )

        # 15. Thane Thorek Grudgebearer - Dwarf Noble
        characters["Thane Thorek Grudgebearer"] = Character(
            name="Thane Thorek Grudgebearer",
            faction=Faction.DWARF,
            character_class=CharacterClass.NOBLE,
            age=203,
            gender="Male",
            appearance="An imposing dwarf with elaborate braided beard and rich clothing. Carries himself with absolute authority.",
            distinctive_features="Golden beard rings, clan insignia, ornate warhammer",
            backstory="A Thane of Clan Grudgebearer who seeks to settle ancient grudges. His presence commands respect from all dwarfs.",
            motivation="To restore his clan's honor and settle all outstanding grudges",
            secrets=["His clan is nearly bankrupt", "He's the last of his bloodline"],
            personality_traits=["Authoritative", "Traditional", "Proud", "Burden of leadership"],
            likes=["Clan honor", "Ancient traditions", "Grudge settling", "Respect"],
            dislikes=["Dishonor", "Elves", "Broken oaths", "Disrespect"],
            greeting_phrases=[
                "I am Thane Thorek, show proper respect!",
                "The Book of Grudges grows heavy.",
                "Speak your business, I have little time.",
                "Honor demands satisfaction."
            ],
            faction_specific_phrases=[
                "The ancestors watch and judge!",
                "A grudge unpaid is honor lost!",
                "Khazad-Dûm! The dwarfs are coming!",
                "By Grungni's forge, I swear it!"
            ]
        )

        # 16. Valdric the Witch Hunter - Empire Witch Hunter
        characters["Valdric the Witch Hunter"] = Character(
            name="Valdric the Witch Hunter",
            faction=Faction.WITCH_HUNTER,
            character_class=CharacterClass.WITCH_HUNTER,
            age=41,
            gender="Male",
            appearance="A grim man in black leather with cold eyes. Carries blessed weapons and holy symbols.",
            distinctive_features="Burn scar on neck, silver holy symbols, always armed with blessed weapons",
            backstory="A fanatical Witch Hunter who has dedicated his life to purging Chaos corruption. His methods are extreme but effective.",
            motivation="To purge all Chaos corruption from the world, no matter the cost",
            secrets=["His sister was a chaos cultist he had to execute", "Struggles with his own dark thoughts"],
            personality_traits=["Fanatical", "Ruthless", "Dedicated", "Haunted"],
            likes=["Purity", "Justice", "Confession", "Holy symbols"],
            dislikes=["Chaos", "Magic users", "Corruption", "Weakness"],
            greeting_phrases=[
                "I smell corruption on the wind.",
                "Confess your sins, heretic!",
                "Sigmar's light reveals all truth.",
                "The guilty will burn!"
            ],
            faction_specific_phrases=[
                "Sigmar's hammer strikes the wicked!",
                "Burn the heretic! Kill the mutant!",
                "The Emperor protects the faithful!",
                "Confession cleanses the soul!"
            ]
        )

        # 17. Sasha the Shadowdancer - Cultist (Hidden)
        characters["Sasha the Shadowdancer"] = Character(
            name="Sasha the Shadowdancer",
            faction=Faction.CULTIST,
            character_class=CharacterClass.ROGUE,
            age=27,
            gender="Female",
            appearance="A beautiful woman with dark hair and mesmerizing eyes. Dresses to blend in with common folk.",
            distinctive_features="Hypnotic violet eyes, small chaos star tattoo hidden on wrist, silver tongue",
            backstory="A Slaanesh cultist who infiltrates taverns to corrupt the innocent. She hides her true nature behind charm and beauty.",
            motivation="To spread corruption and gather souls for her dark master",
            secrets=["Is a chaos cultist", "Has corrupted several people already", "Plans to corrupt the entire tavern"],
            personality_traits=["Seductive", "Manipulative", "Charming", "Utterly corrupt"],
            likes=["Corruption", "Pleasure", "Manipulation", "Beautiful things"],
            dislikes=["Purity", "Witch Hunters", "Resistance", "Ugly things"],
            greeting_phrases=[
                "Hello there, handsome stranger.",
                "Care to share a drink with a lonely girl?",
                "You look like you need some... company.",
                "I know ways to make the evening interesting."
            ],
            faction_specific_phrases=[
                "Pleasure is the only truth.",
                "Why deny yourself what you desire?",
                "The Dark Prince offers such gifts...",
                "Pain and pleasure are one."
            ]
        )

        return characters
