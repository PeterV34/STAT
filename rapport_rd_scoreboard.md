# EU Industrial R&D Investment Scoreboard – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Commission européenne (JRC) : « EU Industrial R&D Investment Scoreboard »**.
Lien : https://iri.jrc.ec.europa.eu/scoreboard

- Chaque édition annuelle classe les **2 000 entreprises qui investissent le plus en R&D dans le monde** (plus de 50 M€ de R&D par an environ). Une ligne correspond à une entreprise.
- Fichier Excel à télécharger gratuitement, sans compte : prendre la dernière édition, onglet de la liste mondiale des 2 000 entreprises.
- Colonnes déjà calculées : R&D, chiffre d'affaires, intensité de R&D, bénéfice d'exploitation, rentabilité, investissements, effectifs, capitalisation boursière, croissances sur un an, pays, secteur.
- Source officielle et citable (Commission européenne).

> Je n'ai pas pu ouvrir le site depuis mon environnement. Les intitulés de colonnes ci-dessous sont des traductions à faire correspondre à ceux du fichier Excel. Si vous pensiez à l'édition de l'an 2000, elle n'existe pas : la première date de 2004. Les « 2000 » désignent ici les 2 000 entreprises classées.

## Problématique

**Titre :** *Taille, pouvoir de marché et concurrence : les déterminants de l'intensité de R&D des 2 000 premières entreprises mondiales.*

**Question :** les grandes entreprises et celles qui ont du pouvoir de marché innovent-elles davantage (hypothèses de Schumpeter) ? La concurrence dans le secteur stimule-t-elle ou freine-t-elle la R&D ? Et pourquoi les entreprises européennes investissent-elles moins en R&D que les américaines ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Innovation, taille des firmes, concurrence (Schumpeter, Arrow, Aghion) |
| ≥ 500 observations | 2 000 entreprises |
| Y continue | Intensité de R&D (R&D / chiffre d'affaires, en %) |
| Plusieurs X sans transformation lourde | 10 X, dont 7 en colonnes brutes |

## Lien avec l'organisation industrielle

L'innovation est un sujet central de l'économie industrielle, avec un débat théorique ancien sur le lien entre structure de marché et R&D.

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Taille (Schumpeter, 1942) | Les grandes firmes amortissent les coûts fixes de la R&D sur plus de ventes et accèdent plus facilement au financement | H1 : effet de la taille sur l'intensité de R&D (positif selon Schumpeter, nul selon Cohen et Klepper) |
| Pouvoir de marché et autofinancement | Les profits élevés financent la R&D, car les banques prêtent mal pour des projets risqués | H2 : rentabilité élevée → plus de R&D |
| Concurrence (Arrow, 1962, contre Aghion et al., 2005) | Arrow : un monopole innove moins (il remplace ses propres rentes). Aghion : relation en U inversé entre concurrence et innovation | H3 : relation en U inversé entre concentration du secteur (HHI) et intensité de R&D |
| Opportunités technologiques | Certains secteurs (pharmacie, logiciels, semi-conducteurs) offrent plus de possibilités d'innover | H4 : forts écarts entre secteurs |
| Écart Europe–États-Unis | L'Europe est spécialisée dans des secteurs moins intensifs en R&D (effet de structure), pas forcément dans des firmes moins innovantes | H5 : l'écart Europe/États-Unis diminue une fois le secteur contrôlé |

## Variables

| Rôle | Variable | Colonne du Scoreboard | Transformation |
| --- | --- | --- | --- |
| Y | Intensité de R&D (%) | R&D intensity | Aucune |
| X1 | Taille (chiffre d'affaires) | Net sales | Logarithme |
| X2 | Taille (effectifs) | Employees | Logarithme |
| X3 | Rentabilité | Profitability (bénéfice d'exploitation / ventes) | Aucune |
| X4 | Intensité d'investissement physique | Capex intensity | Aucune |
| X5 | Croissance des ventes sur un an | One-year sales growth | Aucune |
| X6 | Valorisation boursière (opportunités de croissance) | Market cap / Net sales | Une division |
| X7 | Concentration du secteur (HHI) | Net sales, Industry sector | Parts de ventes dans le secteur, somme des carrés (1 ligne) |
| X8 | HHI au carré | idem | Pour tester le U inversé |
| X9 | Secteur (ICB) | Industry sector | Indicatrices automatiques |
| X10 | Région (UE, États-Unis, Chine, Japon, reste du monde) | Country | Regroupement (1 ligne) |

## Code R

```r
library(readxl)
sb <- read_excel("SB2024_World2000.xlsx", sheet = 1)   # nom du fichier et de l'onglet à adapter
names(sb)                                              # renommer les colonnes utiles ci-dessous

# Exemple après renommage : intensite, ventes, effectifs, rentab, capex_int, croiss, capi, secteur, pays
sb$part   <- ave(sb$ventes, sb$secteur, FUN = function(x) x / sum(x, na.rm = TRUE))
sb$HHI    <- ave(sb$part,   sb$secteur, FUN = function(x) sum(x^2, na.rm = TRUE))
sb$valo   <- sb$capi / sb$ventes
ue        <- c("Germany", "France", "Netherlands", "Sweden", "Italy", "Spain", "Denmark",
               "Finland", "Belgium", "Ireland", "Austria")   # compléter la liste
sb$region <- ifelse(sb$pays %in% ue, "UE",
             ifelse(sb$pays %in% c("US", "China", "Japan"), sb$pays, "Autres"))

modele <- lm(intensite ~ log(ventes) + log(effectifs) + rentab + capex_int + croiss +
               valo + HHI + I(HHI^2) + factor(secteur) + factor(region),
             data = subset(sb, ventes > 0))
summary(modele)
```

Vérifiez l'orthographe des pays (« US » ou « USA ») avec `table(sb$pays)`.

**H5 se teste en deux régressions :** d'abord Y sur la seule région, puis avec les secteurs. Si le coefficient « UE » diminue fortement, l'écart européen vient surtout de la structure sectorielle.

## Statistiques descriptives à présenter

1. Intensité de R&D moyenne par secteur (graphique en barres, du plus au moins intensif).
2. Intensité de R&D moyenne par région, avant et après prise en compte du secteur.
3. Nuage de points de l'intensité de R&D contre le log du chiffre d'affaires.
4. Nuage de points de l'intensité de R&D contre le HHI du secteur, pour visualiser un éventuel U inversé.
5. Part de chaque région dans la R&D totale des 2 000 entreprises.

## Littérature à mobiliser

À vérifier avant de citer.

- Schumpeter, J. (1942), *Capitalism, Socialism and Democracy*.
- Arrow, K. (1962), « Economic Welfare and the Allocation of Resources for Invention », dans *The Rate and Direction of Inventive Activity*, NBER.
- Cohen, W. et Klepper, S. (1996), « A Reprise of Size and R&D », *Economic Journal*.
- Aghion, P., Bloom, N., Blundell, R., Griffith, R. et Howitt, P. (2005), « Competition and Innovation: An Inverted-U Relationship », *Quarterly Journal of Economics*.
- Moncada-Paternò-Castello, P., Ciupagea, C., Smith, K., Tübke, A. et Tubbs, M. (2010), « Does Europe Perform Too Little Corporate R&D? A Comparison of EU and Non-EU Corporate R&D Performance », *Research Policy* (écrit à partir de ce même Scoreboard).
- Cohen, W. (2010), « Fifty Years of Empirical Studies of Innovative Activity and Performance », *Handbook of the Economics of Innovation*, vol. 1.

## Limites à discuter

- **Biais de sélection :** seules les entreprises qui investissent le plus en R&D sont dans la base. On ne peut pas conclure sur les entreprises qui font peu ou pas de R&D.
- **Valeurs extrêmes :** certaines biotechs ont des ventes quasi nulles et une intensité de R&D de plusieurs centaines de %. À exclure ou à plafonner, et à justifier.
- **HHI approximatif :** calculé sur les seules entreprises du Scoreboard et sur des secteurs mondiaux très larges, ce n'est pas une vraie mesure de concentration du marché.
- **Causalité :** la R&D peut aussi expliquer la taille et la rentabilité (causalité inversée).

## Prochaines étapes

- [ ] Télécharger le fichier Excel de la dernière édition et repérer les intitulés exacts des colonnes.
- [ ] Compter les observations complètes pour Y et les 10 X.
- [ ] Faire valider la problématique par votre tuteur, en insistant sur le débat Schumpeter–Arrow–Aghion.
- [ ] Lire Aghion et al. (2005) et Moncada-Paternò-Castello et al. (2010) en premier.
- [ ] Piste d'extension : le JRC publie aussi les éditions passées, ce qui permettrait d'étudier l'évolution sur plusieurs années (fusion de fichiers nécessaire).
