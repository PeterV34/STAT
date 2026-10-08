# Dataset S&P 500 (Kaggle) – Adéquation aux consignes du PEA

*8 octobre 2026 — version 2 : 8 à 10 variables explicatives par problématique*

## Ce qu'exigent les consignes

La base doit permettre d'expliquer **une variable Y** par **plusieurs X**, sur **au moins 500 observations**, dans le thème de l'**économie industrielle** (concurrence, structures de marché, prix, stratégies des firmes).

| Critère du PEA | Exigence |
| --- | --- |
| Thème | Économie industrielle, « de près ou de loin » |
| Observations | ≥ 500 individus (firmes, ménages, pays) |
| Y | Quantitative continue ou binaire 0/1 |
| X | « Plusieurs » déterminants, justifiés par la littérature académique |
| Analyse | Statistiques descriptives + économétrie |

La consigne ne fixe pas de nombre minimum de X. Avec ~500 firmes, 8 à 10 X (plus les indicatrices de secteur) reste raisonnable. Au-delà, chaque variable ajoutée fait perdre des observations à cause des valeurs manquantes.

## Le point bloquant : le nombre d'observations

**Avec le fichier que vous utilisez déjà (constituents-financials, le même que le Kaggle « paytonfisher »), on n'atteint pas 500 firmes.** Je l'ai recalculé à partir du fichier :

| Étape | Firmes restantes |
| --- | --- |
| Fichier brut | 503 |
| Firmes avec des données (17 lignes vides) | 486 |
| Firmes avec EBITDA renseigné | 459 |
| Modèle de la problématique 3 ci-dessous (9 X) | 427 |
| Modèle de la problématique 2 ci-dessous (9 X, P/B > 0) | 399 |

Votre propre sortie console le confirme : 350 individus complets sur 503. **Plus on ajoute de X, plus n baisse.** Il faut donc soit faire accepter ~430 firmes par votre tuteur, soit changer de base (voir la dernière section).

## Comment avoir plus de X sans transformations compliquées

Toutes les variables ajoutées ci-dessous se construisent en **une ligne de R** : une division, un test, ou un regroupement par sous-industrie.

```r
sp$CA      <- sp$Market.Cap / sp$Price.Sales           # chiffre d'affaires
sp$Marge   <- sp$EBITDA / sp$CA                         # marge EBITDA (indice de Lerner approché)
sp$Rend    <- sp$EBITDA / sp$Market.Cap                 # rentabilité rapportée à la valeur
sp$Vol     <- (sp$X52.Week.High - sp$X52.Week.Low) / sp$Price   # volatilité sur 1 an
sp$Part    <- ave(sp$CA, sp$Sector, FUN = function(x) x / sum(x, na.rm = TRUE))      # part de marché dans la sous-industrie
sp$HHI     <- ave(sp$Part, sp$Sector, FUN = function(x) sum(x^2, na.rm = TRUE))      # concentration (Herfindahl)
sp$Nfirmes <- ave(sp$CA, sp$Sector, FUN = length)       # nombre de concurrents dans la sous-industrie
```

La colonne `Sector` de votre fichier est en réalité la sous-industrie GICS (127 modalités). C'est un avantage : on peut y calculer des **parts de marché** et un **indice de concentration (HHI)**, les deux variables centrales de l'économie industrielle. Limite à écrire dans le rapport : ces parts ne portent que sur les firmes du S&P 500, pas sur tout le marché.

## Problématique 1 — Les grandes firmes croissent-elles moins vite ?

**Titre :** Les déterminants de la croissance du chiffre d'affaires des firmes du S&P 500 : un test de la loi de Gibrat. Fichier : Kaggle andrewmvd, sp500_companies.csv (seul fichier qui contient `Revenuegrowth`).

**Littérature :** Evans (1987), Hall (1987), Sutton (1997, *Journal of Economic Literature*).

| Rôle | Variable | Colonne | Construction |
| --- | --- | --- | --- |
| Y | Croissance du chiffre d'affaires | Revenuegrowth | Aucune |
| X1 | Taille (valeur boursière) | Marketcap | Logarithme |
| X2 | Taille (effectifs) | Fulltimeemployees | Logarithme |
| X3 | Rentabilité | Ebitda / Marketcap | Une division |
| X4 | Productivité du travail | Ebitda / Fulltimeemployees | Une division |
| X5 | Part de marché dans l'industrie | Marketcap, Industry | Une ligne `ave()` |
| X6 | Concentration de l'industrie (HHI) | Marketcap, Industry | Une ligne `ave()` |
| X7 | Nombre de concurrents | Industry | Une ligne `ave()` |
| X8 | Cotée au NASDAQ (vs NYSE) | Exchange | Indicatrice 0/1 |
| X9 | Siège hors des États-Unis | Country | Indicatrice 0/1 |
| X10 | Secteur d'activité | Sector | Indicatrices (automatique dans R) |

**Hypothèse testée.** Coefficient de log(Marketcap) négatif et significatif → la loi de Gibrat est rejetée. X5 à X7 testent si la structure de marché freine la croissance.

**Attention :** n'utilisez pas `Weight` en plus de `Marketcap` (c'est la même information), ni X1 et X2 si elles sont trop corrélées (vérifier la corrélation).

## Problématique 2 — Qu'est-ce qui explique les rentes de marché des firmes ?

**Titre :** Les déterminants du ratio Price/Book des firmes du S&P 500, mesure approchée du pouvoir de marché. Fichier : votre fichier constituents-financials.

**Littérature :** Lindenberg et Ross (1981, *Journal of Business*), Montgomery et Wernerfelt (1988, *RAND Journal of Economics*).

| Rôle | Variable | Colonne | Construction |
| --- | --- | --- | --- |
| Y | Valorisation / rentes | Price.Book | Logarithme (exclure P/B ≤ 0 : 32 firmes) |
| X1 | Taille | Market.Cap | Logarithme |
| X2 | Rentabilité par action | Earnings.Share | Aucune |
| X3 | Rentabilité rapportée à la valeur | EBITDA / Market.Cap | Une division |
| X4 | Marge EBITDA | EBITDA / CA | Deux divisions |
| X5 | Verse un dividende | Dividend.Yield | Indicatrice (déjà dans votre script) |
| X6 | Volatilité sur 1 an | 52 Week High, Low, Price | Une ligne |
| X7 | Part de marché dans la sous-industrie | CA, Sector | Une ligne `ave()` |
| X8 | Concentration de la sous-industrie (HHI) | CA, Sector | Une ligne `ave()` |
| X9 | Secteur GICS (11 modalités) | Secteur | Déjà dans votre script |

Échantillon estimé : **~400 firmes**. Je n'ai pas mis Price/Earnings ni Price/Sales en X : ce sont, comme Y, des ratios de valorisation (le modèle serait presque tautologique).

## Problématique 3 — Le pouvoir de marché augmente-t-il les marges ?

**Titre :** Concentration, part de marché et marges des firmes du S&P 500 : un test du paradigme Structure–Comportement–Performance. Fichier : votre fichier constituents-financials.

**Littérature :** Bain (1951), Schmalensee (1985, *American Economic Review*, « Do Markets Differ Much? »), Demsetz (1973, *Journal of Law and Economics*), Rumelt (1991).

| Rôle | Variable | Colonne | Construction |
| --- | --- | --- | --- |
| Y | Marge EBITDA (indice de Lerner approché) | EBITDA / CA | Deux divisions |
| X1 | Concentration de la sous-industrie (HHI) | CA, Sector | Une ligne `ave()` |
| X2 | Part de marché de la firme | CA, Sector | Une ligne `ave()` |
| X3 | Nombre de concurrents | Sector | Une ligne `ave()` |
| X4 | Taille | Market.Cap | Logarithme |
| X5 | Verse un dividende | Dividend.Yield | Indicatrice (déjà dans votre script) |
| X6 | Volatilité sur 1 an | 52 Week High, Low, Price | Une ligne |
| X7 | Valorisation (opportunités de croissance) | Price.Book | Logarithme |
| X8 | Rentabilité par action | Earnings.Share | Aucune |
| X9 | Secteur GICS (11 modalités) | Secteur | Déjà dans votre script |

Échantillon estimé : **~427 firmes**. C'est la problématique la plus « économie industrielle » : elle oppose Bain (la concentration crée des marges via la collusion) à Demsetz (les firmes efficaces gagnent à la fois des parts de marché et des marges). Si X2 est significative mais pas X1, l'explication par l'efficacité l'emporte.

## Recommandation

**Le meilleur sujet, et celui qui a le plus de X : la problématique 3**, avec le fichier que vous avez déjà nettoyé. Mais elle donne ~430 firmes, sous le seuil de 500.

- [ ] Montrer à votre tuteur le tableau des effectifs ci-dessus et demander si ~430 firmes est acceptable.
- [ ] Si non : chercher une base de **toutes les firmes cotées aux États-Unis** (environ 4 000), pas seulement le S&P 500. Piste à vérifier : le dataset Kaggle « 200+ Financial Indicators of US stocks (2014-2018) » (auteur cnic92), qui contiendrait plus de 200 colonnes déjà calculées (croissance, marges, R&D, secteur…). Je n'ai pas pu confirmer qu'il existe ni ses colonnes depuis cet environnement : vérifiez sur Kaggle.
- [ ] Vérifier chaque référence académique avant de la citer, comme l'exige la consigne sur l'IA.

**Limites à discuter dans le rapport.** Biais de sélection (seulement les plus grandes firmes américaines), coupe transversale à une seule date, parts de marché calculées sur le seul S&P 500, causalité non établie.

**Sources.** Diaporama « PEA – Séance d'intro » (TSE, 2026/2027). Effectifs calculés sur [constituents-financials.csv](https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/main/data/constituents-financials.csv). Les colonnes du fichier andrewmvd viennent d'un résultat de recherche ; la page Kaggle n'a pas pu être ouverte depuis cet environnement.
