import os
import re

examples_db = {
    # First batch
    "Zealous": [
        "The zealous volunteers worked late into the night to prepare the shelter.",
        "She was a zealous supporter of environmental conservation initiatives."
    ],
    "Harmonious": [
        "The team worked in a harmonious manner to complete the project ahead of schedule.",
        "The music was a harmonious blend of traditional and modern instruments."
    ],
    "Gregarious": [
        "Dolphins are gregarious animals that live and hunt in close-knit social groups.",
        "Being gregarious by nature, he made friends easily at the new university."
    ],
    "Jovial": [
        "The festive atmosphere put everyone in a jovial and celebratory mood.",
        "Our host was a jovial man who welcomed us with a warm smile and hearty laugh."
    ],
    "Jubilant": [
        "The crowd was jubilant when the home team scored the winning goal in the final second.",
        "Researchers were jubilant after achieving a major breakthrough in their cancer study."
    ],
    "Judicious": [
        "A judicious use of resources helped the startup survive its first critical year.",
        "The judge's judicious decision was praised by legal experts from both sides."
    ],
    "Wholesome": [
        "The organic farm provides fresh and wholesome vegetables to the local community.",
        "Spending a weekend hiking in the mountains was a wholesome family experience."
    ],
    "Wanderlust": [
        "Her strong sense of wanderlust led her to travel to over forty countries.",
        "Looking at the travel brochure reawakened my dormant wanderlust."
    ],
    "Wisdom": [
        "The elders passed down their wisdom to the younger generation through storytelling.",
        "It is wisdom to know when to speak and when to remain silent."
    ],
    "Bizarre": [
        "The detective investigated a bizarre case that seemed to defy all logical explanation.",
        "We experienced some bizarre weather conditions, including snow in the middle of summer."
    ],
    "Tenacious": [
        "With a tenacious grip, the climber refused to let go of the rocky ledge.",
        "Her tenacious defense of human rights won her international recognition."
    ],
    "Tranquil": [
        "The house overlooked a tranquil lake surrounded by quiet pine forests.",
        "She meditated every morning to maintain a tranquil state of mind throughout the day."
    ],
    "Compassion": [
        "The nurse showed great compassion toward the suffering patients under her care.",
        "Driven by compassion, the community raised funds to help the family rebuild their house."
    ],
    "Captivate": [
        "The magician's incredible illusions managed to captivate the entire audience.",
        "Her beautiful voice and emotional performance captivated the music judges."
    ],
    "Delightful": [
        "We spent a delightful evening chatting by the fireplace with our old friends.",
        "The restaurant served a delightful dessert made of fresh strawberries and cream."
    ],
    "Nostalgic": [
        "Hearing the old song made him feel nostalgic about his high school days.",
        "The antique shop was filled with items that evoked a nostalgic feeling."
    ],
    "Notable": [
        "There has been a notable improvement in his grades since he started studying daily.",
        "The museum displays several notable paintings from the Renaissance era."
    ],
    "Nurture": [
        "Teachers strive to nurture the talents and creativity of all their students.",
        "It is important to nurture young seedlings by watering them regularly."
    ],
    "Frugal": [
        "By living a frugal lifestyle, she was able to save enough money to buy a house.",
        "He prepared a frugal but delicious meal using simple ingredients from his pantry."
    ],
    "Knowledgeable": [
        "The museum guide was highly knowledgeable about the history of the ancient ruins.",
        "If you want to start a business, consult with someone knowledgeable in the field."
    ],
    "Kinship": [
        "Spending time together in the wilderness fostered a deep sense of kinship among the group.",
        "She felt a strong kinship with fellow artists who shared her creative vision."
    ],
    "Knack": [
        "He has a natural knack for languages and learned to speak Spanish in just three months.",
        "Fixing broken clocks was a unique knack that he inherited from his grandfather."
    ],
    "Pivotal": [
        "The signing of the treaty was a pivotal moment in the history of the two nations.",
        "Her mentorship played a pivotal role in the success of my academic career."
    ],
    "Quaint": [
        "The tourists stayed in a quaint cottage with a thatched roof and a lovely garden.",
        "We walked down the cobblestone streets of a quaint medieval village."
    ],
    "Quintessential": [
        "A red telephone box is a quintessential symbol of British culture.",
        "He is the quintessential gentleman, always polite, helpful, and well-mannered."
    ],
    "Majestic": [
        "The majestic snow-capped peaks of the Himalayas rose high into the blue sky.",
        "An eagle soaring gracefully above the canyon is a truly majestic sight."
    ],
    "Meticulous": [
        "The researcher kept meticulous records of every step in the scientific experiment.",
        "The dressmaker paid meticulous attention to every single stitch of the gown."
    ],
    "Mindful": [
        "We must be mindful of our environmental impact and reduce plastic waste.",
        "Being mindful of his health, he exercised daily and ate balanced meals."
    ],
    "Xenial": [
        "The hosts welcomed the weary travelers with warm and xenial hospitality.",
        "Their xenial attitude made the international students feel at home immediately."
    ],
    "Xenobiotic": [
        "The laboratory tested how the liver metabolizes various xenobiotic substances.",
        "Marine biologists are studying the long-term effects of xenobiotic pollutants on fish."
    ],
    "Astonish": [
        "The magician's ability to levitate objects astonished everyone in the room.",
        "It astonished me that they managed to finish the massive project in just a weekend."
    ],
    "Eloquent": [
        "The president delivered an eloquent speech that inspired millions of citizens.",
        "His eloquent arguments persuaded the jury to reach a quick verdict."
    ],
    "Lucid": [
        "The teacher gave a lucid explanation of a very complex mathematical formula.",
        "Despite his advanced age, he remained lucid and remembered historical events clearly."
    ],
    "Lucrative": [
        "Investing in real estate turned out to be a highly lucrative venture for them.",
        "She left her teaching job to pursue a more lucrative career in software engineering."
    ],
    "Luminous": [
        "The watch hands were coated with luminous paint so they could be read in the dark.",
        "The night sky was filled with luminous stars reflecting on the calm lake surface."
    ],
    "Resilient": [
        "The resilient economy quickly bounced back after the severe winter storm.",
        "He is a resilient individual who overcame many hardships early in life."
    ],
    "Relentless": [
        "The relentless rain caused minor flooding in the lower parts of the town.",
        "The detective's relentless pursuit of the truth finally solved the cold case."
    ],
    
    # Second batch (only one placeholder example present in the file)
    "Benevolent": [
        "The benevolent donor provided scholarships for dozens of underprivileged students.",
        "She was known throughout the town for her benevolent nature and charity work."
    ],
    "Bewilder": [
        "The complex instructions on the exam paper served to bewilder the students.",
        "The sudden changes in the project requirements bewildered the development team."
    ],
    "Genuine": [
        "The painting was verified as a genuine masterpiece by Leonardo da Vinci.",
        "He showed a genuine interest in learning about different cultures."
    ],
    "Grateful": [
        "The rescued hikers were extremely grateful to the search and rescue team.",
        "I am deeply grateful for all the support my family has given me."
    ],
    "Versatile": [
        "Eggplants are a versatile ingredient that can be baked, grilled, or roasted.",
        "He is a versatile actor who can transition smoothly from comedy to intense drama."
    ],
    "Vibrant": [
        "The local market was filled with vibrant colors and lively music.",
        "She has a vibrant personality that brightens up any room she enters."
    ],
    "Vigilant": [
        "Security guards must remain vigilant to detect any suspicious activity in the building.",
        "Parents need to be vigilant about their children's online safety."
    ],
    "Zenith": [
        "At the zenith of his career, the singer won three Grammy awards in one night.",
        "The sun reached its zenith in the sky, casting short shadows on the ground."
    ],
    "Candid": [
        "During the interview, the politician gave a candid response about his past mistakes.",
        "We took a few candid photographs of the children playing in the garden."
    ],
    "Tangible": [
        "The new policies brought tangible benefits, including a 15% increase in employment.",
        "There was a tangible sense of excitement in the air before the concert started."
    ],
    "Spontaneous": [
        "The crowd erupted into spontaneous applause at the end of the beautiful speech.",
        "We took a spontaneous road trip to the coast last weekend."
    ],
    "Obligation": [
        "Citizens have a moral obligation to help those in need within their community.",
        "She fulfilled her financial obligations by paying off her student loans early."
    ],
    "Outstanding": [
        "The student was honored with an award for her outstanding academic achievements.",
        "He has a few outstanding bills that need to be paid by the end of the month."
    ],
    "Nuance": [
        "A good translator must understand the subtle nuances of both languages.",
        "The actor's performance captured every nuance of the character's complex emotions."
    ],
    "Daunting": [
        "Climbing Mount Everest is a daunting task that requires months of preparation.",
        "Facing the board of directors was a daunting prospect for the young manager."
    ],
    "Diligent": [
        "Through diligent study and practice, she became a master pianist.",
        "The diligent detectives spent weeks analyzing evidence to solve the mystery."
    ],
    "Flawless": [
        "The gymnast executed a flawless routine, scoring a perfect ten.",
        "Her spoken English is flawless and sounds just like a native speaker."
    ],
    "Formidable": [
        "The champion boxer faced a formidable opponent in the championship match.",
        "The mountain range presented a formidable barrier to the early explorers."
    ],
    "Yearn": [
        "Living far away from home, she yearned to see her family and friends again.",
        "The prisoners yearned for freedom and a chance to rebuild their lives."
    ],
    "Inspiring": [
        "The teacher gave an inspiring lecture that motivated students to pursue research.",
        "Overcoming her physical challenges to run the marathon was an inspiring story."
    ],
    "Impeccable": [
        "He was dressed in an impeccable suit for the formal dinner party.",
        "Her manners are impeccable, always showing respect and kindness to everyone."
    ],
    "Pragmatic": [
        "We need to take a pragmatic approach to solve this budget deficit.",
        "She is a pragmatic decision-maker who focuses on practical results."
    ],
    "Profound": [
        "The book had a profound impact on my understanding of human nature.",
        "The sudden loss of his mentor left him in a state of profound sadness."
    ],
    "Persuade": [
        "He managed to persuade his parents to let him study art instead of law.",
        "Advertisements try to persuade consumers to buy products they may not need."
    ],
    "Humble": [
        "Despite his immense wealth, he lived in a humble cottage in the countryside.",
        "She was very humble about her achievements, always sharing credit with her team."
    ],
    "Hesitant": [
        "He was hesitant to sign the contract before consulting with his lawyer.",
        "She gave a hesitant reply, unsure if she was ready for the responsibility."
    ],
    "Hilarious": [
        "The comedian told a hilarious joke that had the entire audience laughing out loud.",
        "We spent the evening watching a hilarious comedy movie together."
    ],
    "Empathy": [
        "Listening actively is a key way to show empathy toward someone who is struggling.",
        "He felt deep empathy for the refugees who had lost their homes."
    ],
    "Enthusiastic": [
        "The children were enthusiastic about the upcoming field trip to the science museum.",
        "She received an enthusiastic welcome from her new colleagues on her first day."
    ],
    "Essential": [
        "Water and nutritious food are essential for maintaining good physical health.",
        "It is essential to double-check your calculations before submitting the report."
    ],
    "Logical": [
        "There is a logical explanation for why the experiment did not produce the expected results.",
        "He presented a logical argument that was easy for everyone to follow."
    ],
    "Ubiquitous": [
        "Smartphones have become ubiquitous in modern society, used by people of all ages.",
        "The coffee shop chain has a ubiquitous presence, with outlets on almost every corner."
    ],
    "Unique": [
        "Every person's fingerprint is unique and can be used for identification.",
        "The museum contains a unique collection of ancient coins from around the world."
    ],
    "Uplifting": [
        "The choir sang an uplifting song that brought joy to everyone in the audience.",
        "Reading inspiring success stories is a very uplifting experience."
    ]
}

def fix_markdown_files():
    markdown_dir = os.path.join("public", "markdown")
    if not os.path.exists(markdown_dir):
        print(f"Directory {markdown_dir} not found!")
        return

    files = [f for f in os.listdir(markdown_dir) if f.endswith(".md")]
    
    for filename in files:
        filepath = os.path.join(markdown_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        modified = False
        sections = content.split("## ")
        new_sections = [sections[0]]
        
        for sec in sections[1:]:
            lines = sec.split("\n")
            header = lines[0]
            word_match = re.search(r"^[0-9]+:\s*([A-Za-z\-]+)", header)
            if not word_match:
                word_match = re.search(r"^Word:\s*([A-Za-z\-]+)", header)
                
            if word_match:
                word = word_match.group(1).capitalize()
                if word in examples_db:
                    ex1, ex2 = examples_db[word]
                    
                    # Track index of example matching (since we may replace either 1st, 2nd, or both)
                    # Let's count how many examples we have replaced
                    ex_lines_indices = []
                    for i, line in enumerate(lines):
                        if "shows how it works" in line or "made the meaning very clear" in line or re.search(r"^\s*\d+\.\s*One example sentence", line) or re.search(r"^\s*\d+\.\s*The use of", line):
                            ex_lines_indices.append(i)
                    
                    if len(ex_lines_indices) == 2:
                        # Replace both
                        indent = len(lines[ex_lines_indices[0]]) - len(lines[ex_lines_indices[0]].lstrip())
                        lines[ex_lines_indices[0]] = " " * indent + "1. " + ex1
                        lines[ex_lines_indices[1]] = " " * indent + "2. " + ex2
                        modified = True
                    elif len(ex_lines_indices) == 1:
                        # Replace whichever single one is present. Typically it's the second example (the "use of")
                        idx = ex_lines_indices[0]
                        indent = len(lines[idx]) - len(lines[idx].lstrip())
                        # If the line contains "2." or is the second item, use ex2, otherwise ex1
                        if "2. " in lines[idx] or "made the meaning very clear" in lines[idx]:
                            lines[idx] = " " * indent + "2. " + ex2
                        else:
                            lines[idx] = " " * indent + "1. " + ex1
                        modified = True
            
            new_sections.append("\n".join(lines))
            
        if modified:
            new_content = "## ".join(new_sections)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Fixed placeholders in {filename}")

if __name__ == "__main__":
    fix_markdown_files()
