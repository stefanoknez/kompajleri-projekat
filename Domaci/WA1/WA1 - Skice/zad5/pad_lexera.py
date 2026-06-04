import os
from PIL import Image, ImageDraw, ImageFont

# 1. Kreiranje bijele slike
img = Image.new('RGB', (1000, 650), color='white')
draw = ImageDraw.Draw(img)

# 2. Putanja do fonta
font_path = "/System/Library/Fonts/Supplemental/Verdana.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"

# Povećane veličine fonta
try:
    f_reg = ImageFont.truetype(font_path, 18)    # Tekst tijela
    f_title = ImageFont.truetype(font_bold_path, 24) # Naslovi
except:
    f_reg = ImageFont.load_default()
    f_title = ImageFont.load_default()

# 3. Ispis naslova
draw.text((40, 40), "Zašto Greedy matching zakazuje", fill="black", font=f_title)

# 4. Vizuelizacija ispravne tokenizacije
draw.text((40, 100), "Teoretski ispravna podjela (aab = a + ab):", fill="black", font=f_reg)
lexemes = ["a", "ab"]
x, y = 40, 140
for lex in lexemes:
    draw.text((x, y), lex, fill="black", font=f_title)
    w = draw.textlength(lex, font=f_title)
    draw.line([(x, y + 32), (x + w, y + 32)], fill="black", width=3)
    x += w + 20

# 5. Tekstualno objašnjenje
objasnjenje = (
    "Reg. izraz: (a+|ab) | Ulazni string: 'aab'\n\n"
    "1. Greedy korak (Pozicija 0): Algoritam traži najduži meč.\n"
    "   'a+' matchuje 'aa', dok 'ab' ne matchuje (jer su prva dva slova 'aa').\n"
    "   Maximal Munch uzima 'aa' kao prvi token.\n\n"
    "2. Ostatak stringa: Na traci ostaje 'b'.\n\n"
    "3. Fatalna greška: Skener pokušava matchovati 'b' pravilima 'a+' i 'ab'.\n"
    "   Nijedno ne odgovara, pa lekser prijavljuje grešku i puca.\n\n"
    "Suština: Pohlepni algoritam je pojeo jedno 'a' previše, a to 'a'\n"
    "je bilo neophodno kao 'sidro' za početak drugog tokena 'ab'."
)
draw.text((40, 220), objasnjenje, fill="black", font=f_reg)

# 6. Snimanje
img.save('maximal_munch_failure.png')
print("Slika 'maximal_munch_failure.png' je uspješno kreirana sa uvećanim fontom!")