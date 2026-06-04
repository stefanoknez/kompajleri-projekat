from html2image import Html2Image

# Inicijalizacija alata za kreiranje slike
hti = Html2Image(output_path='.')

# Tekst i dizajn na ijekavici sa Verdana fontom (12pt)
html_str = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        font-family: 'Verdana', sans-serif;
        font-size: 12pt;
        line-height: 1.6;
        color: black;
        background-color: white;
        padding: 40px;
        width: 800px; /* Širina slike */
    }
    .title {
        font-weight: bold;
        margin-bottom: 15px;
    }
    .lexeme {
        text-decoration: underline;
        margin-right: 3px;
        font-family: 'Verdana', sans-serif;
    }
    ul {
        margin-top: 10px;
        padding-left: 20px;
    }
    li {
        margin-bottom: 8px;
    }
    code {
        font-family: 'Courier New', monospace;
        font-size: 11pt;
        background-color: #f4f4f4;
        padding: 2px 4px;
        border-radius: 3px;
    }
</style>
</head>
<body>
    <p>Ulazni niz (string) koji daje traženi izlaz <b>aacbbca</b> je:</p>
    
    <p style="font-size: 14pt; margin-bottom: 30px;">
        <span class="lexeme">0</span><span class="lexeme">0</span><span class="lexeme">011</span><span class="lexeme">01</span><span class="lexeme">01</span><span class="lexeme">011</span><span class="lexeme">0</span>
    </p>

    <div class="title">Kako funkcioniše</div>
    
    <p>Prilikom dizajniranja ulaza za <b>flex</b> skener, moramo uzeti u obzir pravilo <b>"Maximal Munch"</b> (pravilo najdužeg poklapanja): skener će uvijek pokušati da upari najduži mogući niz karaktera za neki token. Jednostavno nadovezivanje ispravnih regularnih izraza često ne uspijeva jer se granični karakteri stapaju u duža poklapanja i prave grešku.</p>

    <p>Evo analize korak po korak kako skener čita ovaj niz:</p>

    <ul>
        <li><b><code>a</code> &rarr; <span class="lexeme">0</span>:</b> Skener čita prvu <code>0</code>. Gleda unaprijed sljedeći karakter (koji je isto <code>0</code>), ali <code>00</code> ne odgovara nijednom pravilu. Zato se zaustavlja i sigurno ispisuje <code>a</code>.</li>
        
        <li><b><code>a</code> &rarr; <span class="lexeme">0</span>:</b> Skener čita sljedeću <code>0</code>. Gleda unaprijed u <code>011</code>, ali <code>001</code> nije pravilo. Opet se bezbjedno zaustavlja i ispisuje <code>a</code>.</li>
        
        <li><b><code>c</code> &rarr; <span class="lexeme">011</span>:</b> Ovdje <b>moramo</b> koristiti <code>011</code> umjesto <code>101</code>. <i>(Da smo iskoristili <code>101</code>, niz bi do tog trenutka bio <code>00101</code>, a skener bi onu drugu nulu grupisao sa jedinicom pored nje i ispisao <code>b</code> za token <code>01</code>, čime bi uništio traženi redoslijed)</i>. Skener čita <code>011</code> i vidi da je sljedeći karakter <code>0</code>. Pošto <code>0110</code> ne odgovara ničemu, ispisuje <code>c</code>.</li>
        
        <li><b><code>b</code> &rarr; <span class="lexeme">01</span>:</b> Ovdje <b>moramo</b> koristiti <code>01</code> umjesto <code>10</code>. <i>(Da smo iskoristili <code>10</code>, niz bi izgledao kao <code>...01110...</code>. Skener bi pohlepno progutao tu dodatnu jedinicu i dodao je u prethodni <code>c</code> token zbog pravila <code>011+</code>, što bi rezultiralo ispisom <code>c</code>, a onda bi za nulu ispisao <code>a</code>.)</i> Skener uparuje <code>01</code> i sigurno ispisuje <code>b</code>.</li>
        
        <li><b><code>b</code> &rarr; <span class="lexeme">01</span>:</b> Ponovo moramo koristiti <code>01</code>. <i>(Da smo koristili <code>10</code>, niz bi se spojio u <code>...0110...</code>, a skener bi od toga napravio samo jedno <code>c</code> zbog pravila <code>011</code>)</i>. Skener uparuje <code>01</code> i ispisuje <code>b</code>.</li>
        
        <li><b><code>c</code> &rarr; <span class="lexeme">011</span>:</b> Skener čita <code>011</code>. Gleda posljednji karakter (<code>0</code>) i zna da mora stati jer <code>0110</code> nije ispravno poklapanje. Ispisuje <code>c</code>.</li>
        
        <li><b><code>a</code> &rarr; <span class="lexeme">0</span>:</b> Posljednji karakter je samo jedna nula koja se uparuje po prvom pravilu, ispisujući <code>a</code>.</li>
    </ul>

</body>
</html>
"""

# Kreiranje PNG slike
print("Generišem sliku...")
hti.screenshot(html_str=html_str, save_as='flex_rjesenje_ijekavica.png', size=(880, 950))
print("Slika 'flex_rjesenje_ijekavica.png' je uspješno kreirana!")