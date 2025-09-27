# Dokumentace pro Plánovač pro Divoké Kmeny

## Úvod

Toto je dokumentace pro webovou stránku [plemiona-planer.pl](https://plemiona-planer.pl) – ambiciózní projekt pro [plemiona.pl](https://plemiona.pl), který začal v lednu 2020 po aktualizaci hry na verzi 8.192 v listopadu 2019. Aktualizace zavedla možnost pro administrátory kmenů sbírat data o hráčích a jejich jednotkách.

- [1. Testovací svět](./first_steps/index.md) - sekce věnovaná prozkoumání stránky bez nutnosti cokoli instalovat nebo dokonce mít aktivní herní účet. Umožňuje plánovat akce ve speciálně připraveném Testovacím světě.
- [2. Instalace potřebných skriptů](./scripts/army_and_defence_collection.md) - pro použití ve skutečném světě a plánování akcí pro skutečný kmen je nutný skript pro sběr dat z kmene (volitelně druhý skript pomáhá posílat zprávy hráčům).
- [3. Průvodci](./primary/write_outline_targets.md) - 6 rozšířených článků na konkrétní témata související s plánováním akcí.
- [4. Pokročilé](./primary/write_outline_targets.md) - popis všech záložek a možností v hlavní záložce "Plánovač".

## Otázky a odpovědi

### O stránce

> Co je tato stránka a pro koho je a není určena?

Tato stránka je určena pro **administrátory kmenů** a jejich koordinátory útoků, kteří mají přístup k datům hráčů. Pomocí kmenových dat, zadáváním cílů akcí a úpravou nastavení může koordinátor vygenerovat osnovu akce a poslat cíle hráčům (prostřednictvím odkazu na stránku nebo přímo v herní zprávě). Matematika použitá na stránce a mnoho možností umožňují plánovat prakticky jakoukoli akci v jakékoli fázi hry, což šetří čas plánovače.

> Co plemiona-planer NENÍ?

NENÍ to nelegální nástroj, herní bot ani žádný skript, který automatizuje herní akce. Stránka se NEPŘIPOJUJE ke hře za žádným jiným účelem než pro získávání veřejně dostupných dat o světě. NIKDY nebudete požádáni o své herní heslo!

### Platby

> Je plemiona-planer placený?

Stránka je zdarma. Můžete si však zakoupit předplatné prémiového účtu, které umožňuje plánovat více než 40 cílů v jedné osnově a poskytuje přístup k nevyužitým datům z dříve plánovaných akcí (pro použití v budoucích akcích). Nejsou žádné rozdíly ve funkčnosti, kvalitě algoritmu ani rychlosti. Tento model pomáhá udržovat službu a poplatek lze rozdělit mezi členy kmene. Není potřeba více než jeden účet na kmen, s výjimkou případů **zjevných!** problémů se sdílením účtu. Stránka nenese odpovědnost za ztráty způsobené neoprávněným přístupem, krádeží účtu nebo sdílením hesel s protivníky. Majitel účtu by měl zvážit pro a proti, než dá své heslo třetí straně.

> Jak je možné, že kód aplikace je otevřený a dostupný na GitHubu?
>
> Proč platit za předplatné, když mohu kód používat zdarma?

Jsem zastáncem [open-source softwaru](https://opensource.com/resources/what-open-source)! Je pravda, že se můžete rozhodnout neplatit a používat kód stránky a výsledek let práce mnoha oddaných uživatelů. Zdarma, a tak to i zůstane :) Odráží to také mou důvěru v bezpečnost a matematiku použitou při plánování – není co skrývat. Pohodlí plánování z jakéhokoli místa a online přístup k výsledkům plánování pro členy kmene je však neocenitelné. Nastavení vlastních serverů vyžaduje specializované znalosti, značné náklady a průběžnou údržbu, aktualizace atd. Poplatek za předplatné také pokrývá čas potřebný na opravu chyb, pomoc uživatelům s problémy nebo psaní nových funkcí. To vše by nebylo možné bez podpory uživatelů. Děkuji všem, kteří tento projekt podporují.

### Data

> Jsou moje data v bezpečí?

Stránka je online od poloviny roku 2020. Během této doby nedošlo k žádnému bezpečnostnímu incidentu. Současný obchodní model udržuje servery v chodu. Data zadaná uživateli jsou jejich odpovědností a nikdy nebudou prodána ani sdílena s třetími stranami.

> Mohu ve vašem Plánovači vytvářet osnovy bez přístupu k datům kmene?

Ne, poskytnutí dat je vyžadováno. Musíte být ve vedení kmene a jeho členové musí povolit příslušná nastavení pro sdílení dat. Existuje testovací svět, kde si můžete stránku vyzkoušet bez přístupu k datům kmene.

### Osnova

> Ahoj, proč Plánovač nerozplánuje všechny mé útočné jednotky? Myslím, že jsem v nastavení všechno změnil, ale stále nechává 2,7k útočných jednotek nevyužitých…

Důvodů může být mnoho, hlavně nastavení akce v záložce [1. Dostupné jednotky a popis tabulky](./advanced/1_available_troops_and_table.md), jako je přeskočení některých vesnic na frontě nebo vzdálených vesnic u okraje. Méně často je to kvůli [3. Parametrům osnovy](./advanced/3_outline_parameters.md). Plánovač plně nekontroluje nepromyšlené parametry a **povoluje chyby**. Například pokud nastavení fronty naznačuje, že celý kmen je na frontě, ale uživatel nastaví útočné jednotky pouze ze zálohy, aplikace takovou akci naplánuje, i když žádná útočná jednotka nebude zahrnuta.

### Noční bonus

> Jak funguje algoritmus, aby se co nejvíce vyhnul nočním útokům?

Rozsah přirozených čísel 0-23, kde 0-7 má nejhorší skóre = 1, okraje rozsahu mají skóre = 2 a zcela "bezpečné" hodiny mají skóre = 3, vše zabaleno v modulu 24. [Kód zde](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

Toto se musí provést pro každý cíl individuálně přes všechny spojenecké vesnice, nejprve se vypočítá vzdálenost v polích.

### Skripty

> Ahoj, úplně nerozumím, jak funguje skript pro odesílání cílů. Po instalaci na lištu nástrojů se v rozhraní kmenů nic neděje.

Viz [Skript pro odesílání zpráv](./scripts/sending_messages.md). Jedná se o **prohlížečový skript**, nikoli pro herní lištu nástrojů. Používá se v novém zobrazení zprávy, pokud jsou v URL adrese speciálně přidané parametry. [Zkontrolujte bod 11 v záložce s výsledky](./first_steps/step_7_results_tab.md).

### Právní informace a licence

> Mohu použít kód plemiona-planer z GitHubu?

Ano! Můžete dělat cokoli v rámci **licence Apache 2.0** – nastavit si Plánovač lokálně, používat forky a sami je nasazovat. Můžete použít kód zkopírovaný z repozitáře GitHub pro své nástroje (pod licencí Apache 2.0, což znamená BEZ odstranění hlavičky licence). NESOUHLASÍM s vydáváním se za značku plemiona-planer.pl, používáním loga rafsaf.pl nebo mého jména v zásadách ochrany osobních údajů v produktech nebo projektech založených na plemiona-planer.pl.
