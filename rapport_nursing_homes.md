# Base CMS « Nursing Home Provider Information » – Rapport de projet PEA

*8 octobre 2026*

## Verdict

**La base convient très bien aux consignes, et beaucoup mieux que le S&P 500.** Elle compte environ 14 700 maisons de retraite américaines (≥ 500 largement), une centaine de colonnes déjà calculées, et presque toutes les variables explicatives s'utilisent telles quelles.

| Critère du PEA | S&P 500 (Kaggle) | CMS Nursing Home Provider Information |
| --- | --- | --- |
| ≥ 500 observations | Non : 427 à 486 firmes exploitables | Oui : ~14 700 établissements |
| Y quantitative continue ou 0/1 | Oui | Oui (heures de soins, notes, amendes) |
| Plusieurs X, sans transformation lourde | Peu de X, la plupart à calculer | 12 X, dont 9 en colonnes brutes |
| Thème économie industrielle | Indirect | Direct : propriété, chaînes, concentration, concurrence par la qualité |
| Source citable | Kaggle | Agence fédérale américaine (CMS), données officielles |

**Où trouver les données.** [data.cms.gov – Nursing Home Provider Information](https://data.cms.gov/provider-data/dataset/4pq5-n9py), bouton « Download » (fichier `NH_ProviderInfo_<mois><année>.csv`). Une copie existe aussi sur Kaggle. Notez la date du fichier : la base est mise à jour chaque mois.

> Je n'ai pas pu télécharger le fichier depuis mon environnement (site bloqué). Les noms de colonnes ci-dessous viennent de ma connaissance des versions récentes : vérifiez-les avec `names()` après téléchargement, ils changent parfois légèrement.

## La problématique retenue

**Titre :** *Propriété, chaînes et concentration du marché : les déterminants de la qualité des soins dans les maisons de retraite américaines.*

**Question :** à prix largement réglementés, les maisons de retraite à but lucratif, appartenant à une chaîne ou installées sur un marché local concentré fournissent-elles moins de qualité, mesurée par les heures de personnel soignant par résident ?

C'est la problématique qui exploite le mieux la base : elle utilise les colonnes les plus riches (propriété, chaîne, taille, effectifs, gravité des patients, localisation) et chaque X correspond à un mécanisme d'organisation industrielle.

## Pourquoi c'est de l'organisation industrielle

Le marché des maisons de retraite est un cas d'école de **concurrence imparfaite avec prix réglementés**. Environ 60 % des résidents sont financés par Medicaid, dont le tarif est fixé par chaque État. Les établissements ne peuvent donc pas vraiment se concurrencer sur le prix : **ils se concurrencent (ou non) sur la qualité**, et le personnel soignant est leur principal coût et leur principale dimension de qualité.

| Mécanisme d'organisation industrielle | Ce que prédit la théorie | Variable de la base | Hypothèse |
| --- | --- | --- | --- |
| **Forme de propriété** (but lucratif vs non lucratif) | Quand la qualité est difficile à observer par les familles (« échec du contrat »), une firme qui maximise son profit a intérêt à réduire la qualité non observable. Le non-lucratif sert de garantie. | Ownership Type | H1 : à but lucratif → moins d'heures de soins |
| **Structure multi-établissements** (chaînes) | Économies d'échelle, standardisation, mais aussi pression des actionnaires sur les coûts et contournement de la réputation locale. | Affiliated Entity ID | H2 : effet des chaînes, croissant avec la taille de la chaîne |
| **Concentration du marché local** (HHI) | Avec prix fixés, plus de concurrents → la qualité devient la seule arme pour attirer les patients privés et Medicare. Un marché concentré relâche cette pression. | Comté + nombre de lits | H3 : HHI élevé → moins d'heures de soins |
| **Excès de demande** (taux d'occupation) | Un établissement plein n'a pas besoin d'attirer des patients par la qualité (pouvoir de marché de capacité). | Résidents / lits | H4 : occupation élevée → moins de qualité |
| **Changement de propriétaire** | Les rachats (souvent par des fonds d'investissement) s'accompagnent de réductions de coûts. | Provider Changed Ownership in Last 12 Months | H5 : rachat récent → moins d'heures |

## Variable expliquée

**Y = `Reported Total Nurse Staffing Hours per Resident per Day`** : heures totales de personnel soignant (infirmiers + aides-soignants) par résident et par jour. Colonne brute, continue, sans transformation. Elle se lit directement : « un résident reçoit en moyenne X heures de soins par jour ». C'est aussi la mesure de qualité la plus utilisée dans la littérature, car elle est objective (déclarée via les fiches de paie), contrairement aux notes.

**Variables expliquées alternatives** (tests de robustesse, mêmes X) :
- `Overall Rating` codée en 0/1 (1 si 4 ou 5 étoiles) → régression logit/probit.
- `Total nursing staff turnover` (rotation du personnel).
- `Number of Fines` ou une indicatrice « au moins une amende ».

## Variables explicatives

| X | Variable | Colonne CMS | Construction | Mécanisme |
| --- | --- | --- | --- | --- |
| X1 | But lucratif | Ownership Type | Indicatrice (commence par « For profit ») | H1 |
| X2 | Public | Ownership Type | Indicatrice (commence par « Government ») ; référence = non lucratif | H1 |
| X3 | Appartient à une chaîne | Affiliated Entity ID | Indicatrice (colonne non vide) | H2 |
| X4 | Taille de la chaîne | Affiliated Entity ID | Nombre d'établissements de la même chaîne (1 ligne) | H2 |
| X5 | Taille de l'établissement | Number of Certified Beds | Logarithme | Économies d'échelle |
| X6 | Taux d'occupation | Average Number of Residents per Day / Number of Certified Beds | Une division | H4 |
| X7 | Concentration du marché local (HHI) | Number of Certified Beds, State, County/Parish | Parts de lits dans le comté, somme des carrés (1 ligne) | H3 |
| X8 | Part de marché locale | idem | Lits / lits du comté (1 ligne) | Pouvoir de marché individuel |
| X9 | Gravité des patients | Nursing Case-Mix Index | Aucune | Contrôle : des patients plus lourds exigent plus de soins |
| X10 | Rachat récent | Provider Changed Ownership in Last 12 Months | Indicatrice Y/N | H5 |
| X11 | Situé dans un hôpital | Provider Resides in Hospital | Indicatrice Y/N | Intégration verticale |
| X12 | Résidence multi-niveaux (CCRC) | Continuing Care Retirement Community | Indicatrice Y/N | Différenciation |
| X13 | État | State | Effets fixes (automatique dans R) | Contrôle : tarif Medicaid et normes propres à chaque État |

**X9 et X13 sont essentiels** : sans eux, on confondrait l'effet de la propriété avec le fait que certains établissements accueillent des patients plus lourds, ou sont situés dans des États plus généreux.

## Construction des variables en R

Tout se fait en une ligne par variable.

```r
nh <- read.csv("NH_ProviderInfo_Oct2026.csv", check.names = FALSE)   # nom du fichier à adapter
names(nh)   # vérifier les noms de colonnes

nh$Y          <- nh$`Reported Total Nurse Staffing Hours per Resident per Day`
nh$lucratif   <- as.integer(grepl("^For profit", nh$`Ownership Type`))
nh$public     <- as.integer(grepl("^Government", nh$`Ownership Type`))
nh$chaine     <- as.integer(!is.na(nh$`Affiliated Entity ID`) & nh$`Affiliated Entity ID` != "")
nh$taille_ch  <- ifelse(nh$chaine == 1, ave(nh$chaine, nh$`Affiliated Entity ID`, FUN = length), 1)
nh$lits       <- nh$`Number of Certified Beds`
nh$occupation <- nh$`Average Number of Residents per Day` / nh$lits
nh$comte      <- paste(nh$State, nh$`County/Parish`)
nh$part       <- ave(nh$lits, nh$comte, FUN = function(x) x / sum(x, na.rm = TRUE))
nh$HHI        <- ave(nh$part, nh$comte, FUN = function(x) sum(x^2, na.rm = TRUE))
nh$rachat     <- as.integer(nh$`Provider Changed Ownership in Last 12 Months` == "Y")
nh$hopital    <- as.integer(nh$`Provider Resides in Hospital` == "Y")
nh$ccrc       <- as.integer(nh$`Continuing Care Retirement Community` == "Y")
nh$casemix    <- nh$`Nursing Case-Mix Index`

modele <- lm(Y ~ lucratif + public + chaine + log(taille_ch) + log(lits) + occupation +
               HHI + part + casemix + rachat + hopital + ccrc + factor(State), data = nh)
summary(modele)
```

## Spécification économétrique

```latex
Y_i = \beta_0 + \beta_1 \text{Lucratif}_i + \beta_2 \text{Public}_i + \beta_3 \text{Chaine}_i + \beta_4 \log(\text{TailleChaine}_i) + \beta_5 \log(\text{Lits}_i) + \beta_6 \text{Occupation}_i + \beta_7 \text{HHI}_c + \beta_8 \text{Part}_i + \beta_9 \text{CaseMix}_i + \gamma' Z_i + \delta_{\text{Etat}} + \varepsilon_i
```

où *i* est l'établissement, *c* son comté, *Z* les indicatrices de contrôle (rachat, hôpital, CCRC) et δ les effets fixes État. Erreurs standard à regrouper par comté si votre tuteur le demande (`sandwich::vcovCL`).

Résultats attendus d'après la littérature : β1 < 0 (but lucratif), β3 < 0 (chaînes), β7 < 0 (concentration), β6 < 0 (occupation), β9 > 0 (gravité).

## Statistiques descriptives à présenter

1. Moyenne de Y par type de propriété (lucratif / non lucratif / public) et test de différence de moyennes.
2. Moyenne de Y selon l'appartenance à une chaîne, et selon la taille de la chaîne (1, 2–10, 11–50, > 50 établissements).
3. Nuage de points Y contre HHI du comté, avec droite de régression.
4. Répartition des établissements par type de propriété (environ 70 % à but lucratif aux États-Unis, à vérifier dans vos données).
5. Tableau de corrélations entre les X, pour repérer la colinéarité (taille, part de marché et HHI notamment).

## Littérature à mobiliser

À vérifier une par une avant de les citer (consigne sur l'IA).

- **Théorie du non-lucratif et échec du contrat :** Hansmann, H. (1980), « The Role of Nonprofit Enterprise », *Yale Law Journal*.
- **Qualité et prix réglementés :** Gertler, P. (1989), « Subsidies, Quality, and the Regulation of Nursing Homes », *Journal of Public Economics*. Nyman, J. (1985), sur l'excès de demande et la qualité, *Journal of Health Economics*.
- **Propriété et qualité :** Hirth, R. (1999), « Consumer Information and Competition between Nonprofit and For-profit Nursing Homes », *Journal of Health Economics*. Harrington, C. et al. (2001), « Does Investor Ownership of Nursing Homes Compromise the Quality of Care? », *American Journal of Public Health*.
- **Concurrence entre lucratif et non lucratif :** Grabowski, D. et Hirth, R. (2003), « Competitive Spillovers across Non-profit and For-profit Nursing Homes », *Journal of Health Economics*.
- **Rachats par des fonds d'investissement :** Gupta, A., Howell, S., Yannelis, C. et Gupta, A., « Owner Incentives and Performance in Healthcare: Private Equity Investment in Nursing Homes » (NBER, puis *Review of Financial Studies*).
- **Manuel d'organisation industrielle** pour le HHI et la concurrence par la qualité : Tirole, J. (1988), *The Theory of Industrial Organization*, MIT Press.

## Limites à discuter

- **Causalité :** les établissements à but lucratif peuvent s'installer là où les patients sont moins solvables. Le contrôle par le case-mix et l'État réduit, sans supprimer, ce biais de sélection.
- **Marché = comté :** une définition approximative du marché pertinent (certains comtés sont immenses, d'autres minuscules). Un comté avec un seul établissement a HHI = 1.
- **HHI calculé en lits**, pas en chiffre d'affaires (non disponible).
- **Données d'une seule date** (coupe transversale) ; les établissements très récents ont des valeurs manquantes.
- **Contexte américain** : le financement Medicaid/Medicare est spécifique ; la comparaison avec les EHPAD français (débat Orpea, 2022) peut motiver l'introduction.

## Deux problématiques de secours (même base)

| Problématique | Y | Différence avec la principale |
| --- | --- | --- |
| Rotation du personnel et pouvoir de monopsone local | Total nursing staff turnover | Concentration des employeurs dans le comté (marché du travail) |
| Sanctions réglementaires et forme de propriété | Indicatrice « au moins une amende » (Number of Fines > 0) | Logit/probit ; ajout de Number of Substantiated Complaints |

## Prochaines étapes

- [ ] Télécharger le fichier sur data.cms.gov et vérifier les noms de colonnes avec `names()`.
- [ ] Compter les observations complètes pour Y et les 13 X (attendu : plus de 13 000).
- [ ] Faire valider la problématique par votre tuteur, en insistant sur l'angle organisation industrielle (propriété, chaînes, concentration).
- [ ] Lire Grabowski et Hirth (2003) et Gupta et al. en premier : ils utilisent ces mêmes données CMS.
