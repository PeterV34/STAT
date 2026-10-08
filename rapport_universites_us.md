# Universités américaines (College Scorecard) – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**U.S. Department of Education : « College Scorecard »**.
Lien : https://collegescorecard.ed.gov/data

- Fichier : `Most-Recent-Cohorts-Institution.csv` (données les plus récentes, une ligne par établissement), environ 6 500 établissements et plus de 3 000 colonnes.
- Téléchargement gratuit, sans compte. Une documentation (« Data Dictionary », fichier Excel) explique chaque colonne.
- Copies disponibles sur Kaggle (rechercher « College Scorecard »), mais la source officielle est plus à jour.

> Je n'ai pas pu ouvrir le site depuis mon environnement. Les noms de colonnes ci-dessous sont ceux du dictionnaire de données que je connais : vérifiez-les avec `names()` et le Data Dictionary.

## Problématique

**Titre :** *But lucratif, sélectivité et qualité : les déterminants du prix des études dans les universités américaines.*

**Question :** à qualité de formation égale, les universités à but lucratif font-elles payer plus cher ? Les établissements très sélectifs exercent-ils un pouvoir de marché sur les prix ? Et le prix reflète-t-il la qualité réelle (diplomation, salaires des diplômés) ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Forme de propriété, pouvoir de marché, prix et qualité, discrimination par les prix |
| ≥ 500 observations | ~2 000 établissements délivrant surtout des licences (bachelor), après filtre |
| Y continue | Prix net moyen payé par les étudiants ($ par an) |
| Plusieurs X sans transformation lourde | 12 X, dont 11 en colonnes brutes |
| Qualité des X | Données administratives fédérales, mesures objectives |

## Lien avec l'organisation industrielle

L'enseignement supérieur américain est un marché où coexistent trois formes de propriété (public, privé non lucratif, privé lucratif), où la qualité est difficile à observer avant d'acheter, et où les prix affichés diffèrent fortement des prix réellement payés.

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Forme de propriété (Hansmann, 1980) | Quand la qualité est difficile à observer, une firme à but lucratif peut facturer cher une qualité faible ; le non-lucratif sert de garantie | H1 : à but lucratif → prix plus élevé à qualité égale |
| Pouvoir de marché par la sélectivité | Les places dans les universités sélectives sont rares : elles peuvent fixer des prix élevés | H2 : taux d'admission faible → prix plus élevé |
| Signal de qualité | Le prix reflète la qualité de la formation, mesurée par la diplomation et les salaires | H3 : diplomation et salaires élevés → prix plus élevé |
| Discrimination par les prix (bourses) | Les universités affichent un prix élevé puis accordent des réductions selon le revenu : chaque étudiant paie selon sa capacité | H4 : écart prix affiché / prix net plus grand dans le privé non lucratif |
| Économies d'échelle | Les coûts fixes (bâtiments, bibliothèques) sont amortis sur plus d'étudiants | H5 : effectifs élevés → prix plus bas |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Prix net moyen ($/an) | `NPT4_PUB` (public), `NPT4_PRIV` (privé) | Réunies en une seule colonne (1 ligne) |
| Y (alternative) | Frais de scolarité affichés | `TUITIONFEE_OUT` | Aucune |
| X1 | Statut (public / privé non lucratif / privé lucratif) | `CONTROL` | Indicatrices automatiques |
| X2 | Taux d'admission (sélectivité) | `ADM_RATE` | Aucune |
| X3 | Taux de diplomation en 6 ans | `C150_4` | Aucune |
| X4 | Salaire médian des anciens étudiants 10 ans après l'entrée | `MD_EARN_WNE_P10` | Logarithme |
| X5 | Effectifs de premier cycle | `UGDS` | Logarithme |
| X6 | Salaire mensuel moyen des enseignants | `AVGFACSAL` | Aucune |
| X7 | Part d'enseignants à temps plein | `PFTFAC` | Aucune |
| X8 | Part d'étudiants boursiers (revenus modestes) | `PCTPELL` | Aucune |
| X9 | Établissement religieux | `RELAFFIL` | Indicatrice (non vide) |
| X10 | Type de zone (grande ville, banlieue, rural…) | `LOCALE` | Indicatrices automatiques |
| X11 | Région | `REGION` | Indicatrices automatiques |
| X12 | Nombre d'établissements dans l'État (concurrence) | `STABBR` | Comptage par État (1 ligne) |

`SAT_AVG` (score moyen au SAT des admis) est une autre bonne mesure de sélectivité, mais beaucoup d'établissements ne la renseignent pas (admission sans test) : à utiliser seulement en robustesse.

## Code R

```r
us <- read.csv("Most-Recent-Cohorts-Institution.csv", na.strings = c("NULL", "PrivacySuppressed", "NA"))
names(us)[1:50]

us <- subset(us, PREDDEG == 3)                     # établissements délivrant surtout des licences (bachelor)

us$prix_net   <- ifelse(us$CONTROL == 1, us$NPT4_PUB, us$NPT4_PRIV)
us$statut     <- factor(us$CONTROL, levels = 1:3,
                        labels = c("Public", "Prive non lucratif", "Prive lucratif"))
us$religieux  <- as.integer(!is.na(us$RELAFFIL))
us$nb_etat    <- ave(us$UGDS, us$STABBR, FUN = length)

modele <- lm(prix_net ~ statut + ADM_RATE + C150_4 + log(MD_EARN_WNE_P10) + log(UGDS) +
               AVGFACSAL + PFTFAC + PCTPELL + religieux + log(nb_etat) +
               factor(LOCALE) + factor(REGION), data = us)
summary(modele)
```

Les valeurs « NULL » et « PrivacySuppressed » (données masquées pour protéger les étudiants) sont lues comme manquantes grâce à `na.strings`.

## Statistiques descriptives à présenter

1. Prix net moyen et frais affichés moyens selon le statut (tableau 3 × 2) : l'écart entre les deux mesure la discrimination par les bourses.
2. Nuage de points du prix net contre le salaire médian des anciens étudiants, une couleur par statut (le prix reflète-t-il la qualité ?).
3. Nuage de points du prix net contre le taux d'admission.
4. Taux de diplomation et salaires médians moyens selon le statut.
5. Répartition des établissements par statut et par région.

## Littérature à mobiliser

À vérifier avant de citer.

- Hansmann, H. (1980), « The Role of Nonprofit Enterprise », *Yale Law Journal*.
- Winston, G. (1999), « Subsidies, Hierarchy and Peers: The Awkward Economics of Higher Education », *Journal of Economic Perspectives*.
- Epple, D., Romano, R. et Sieg, H. (2006), « Admission, Tuition, and Financial Aid Policies in the Market for Higher Education », *Econometrica*.
- Deming, D., Goldin, C. et Katz, L. (2012), « The For-Profit Postsecondary School Sector: Nimble Critters or Agile Predators? », *Journal of Economic Perspectives*.
- Cellini, S. et Goldin, C. (2014), « Does Federal Student Aid Raise Tuition? New Evidence on For-Profit Colleges », *American Economic Journal: Economic Policy*.
- Hoxby, C. (2009), « The Changing Selectivity of American Colleges », *Journal of Economic Perspectives*.

## Limites à discuter

- **Causalité :** les salaires des diplômés reflètent aussi le niveau des étudiants admis (effet de sélection), pas seulement la qualité de la formation.
- **Marché = État :** la concurrence entre universités est en partie nationale ; le nombre d'établissements dans l'État est une mesure approximative.
- **Valeurs manquantes :** les établissements à but lucratif renseignent moins souvent le taux d'admission (admission ouverte). Vérifier combien d'observations restent par statut.
- **Prix net moyen :** il cache de fortes différences entre étudiants selon leur revenu.

## Prochaines étapes

- [ ] Télécharger le fichier et le Data Dictionary, vérifier les noms de colonnes.
- [ ] Compter les observations complètes par statut après le filtre (`PREDDEG == 3`).
- [ ] Faire valider la problématique par votre tuteur, en insistant sur la forme de propriété et la discrimination par les prix.
- [ ] Lire Deming, Goldin et Katz (2012) et Epple, Romano et Sieg (2006) en premier.
