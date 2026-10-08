# Dataset S&P 500 (Kaggle) – Adéquation aux consignes du PEA

*8 octobre 2026*

## Ce qu'exigent les consignes

La base doit permettre d'expliquer **une variable Y** par **plusieurs X**, sur **au moins 500 observations**, dans le thème de l'**économie industrielle** (concurrence, structures de marché, prix, stratégies des firmes).

| Critère du PEA | Exigence |
| --- | --- |
| Thème | Économie industrielle, « de près ou de loin » |
| Observations | ≥ 500 individus (firmes, ménages, pays) |
| Y | Quantitative continue ou binaire 0/1 |
| X | Plusieurs déterminants, justifiés par la littérature académique |
| Analyse | Statistiques descriptives + économétrie |
| Argumentation | D'économiste, pas une simple description de faits |

Modèle de titre proposé par le cours : « Les déterminants de [Y], en [pays], en [année] ».

## Le dataset Kaggle et le verdict

**Oui, il peut convenir, mais de justesse sur le nombre d'observations.** Il s'agit d'une coupe transversale de ~500 entreprises du S&P 500, avec des colonnes directement utilisables comme Y et X (seulement des logs, une division ou des indicatrices de secteur à créer).

| Dataset | Fichier utile | Lignes | Colonnes exploitables |
| --- | --- | --- | --- |
| [S&P 500 Stocks (daily updated), andrewmvd](https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks) — recommandé | sp500_companies.csv | ~502 | Sector, Industry, Currentprice, Marketcap, Ebitda, Revenuegrowth, Fulltimeemployees, Country, State, Weight |
| [S&P 500 Companies with Financial Information, paytonfisher](https://www.kaggle.com/datasets/paytonfisher/sp-500-companies-with-financial-information) | financials.csv | ~505 | Sector, Price, Price/Earnings, Dividend Yield, Earnings/Share, 52 Week Low/High, Market Cap, EBITDA, Price/Sales, Price/Book |

Le fichier andrewmvd contient aussi sp500_stocks.csv (prix journaliers). À éviter ici : en tirer des rendements ou une volatilité demande justement des transformations lourdes.

**Points forts.** Unité = la firme, ce qui colle au thème. Variables propres, déjà calculées, licence ouverte. Aucune fusion nécessaire si on reste dans un seul fichier.

**Limite principale.** 502–505 lignes, c'est à peine au-dessus du seuil de 500. L'EBITDA est souvent manquant pour les banques et assurances : après suppression des valeurs manquantes, l'échantillon peut tomber sous 500. À faire valider par votre tuteur dès maintenant.

## Problématique 1 — Les grandes firmes croissent-elles moins vite ?

**Titre :** Les déterminants de la croissance du chiffre d'affaires des firmes du S&P 500 : un test de la loi de Gibrat. Fichier : andrewmvd, sp500_companies.csv.

**Lien avec le thème.** La loi de Gibrat (croissance indépendante de la taille) est un classique de l'économie industrielle. Littérature à chercher : Evans (1987), Hall (1987), Sutton (1997, *Journal of Economic Literature*).

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Croissance du chiffre d'affaires | Revenuegrowth | Aucune |
| X1 | Taille (valeur boursière) | Marketcap | Logarithme |
| X2 | Taille (effectifs) | Fulltimeemployees | Logarithme |
| X3 | Rentabilité | Ebitda | Aucune (ou log si > 0) |
| X4 | Secteur d'activité | Sector | Indicatrices (automatique dans R) |
| X5 | Siège hors des États-Unis | Country | Indicatrice 0/1 |

**Hypothèse testée.** Si le coefficient de log(Marketcap) est négatif et significatif, la loi de Gibrat est rejetée : les petites firmes croissent plus vite.

**Avantage.** C'est la problématique qui demande le moins de transformations, et Y est une colonne brute.

## Problématique 2 — Qu'est-ce qui explique les rentes de marché des firmes ?

**Titre :** Les déterminants du ratio Price/Book des firmes du S&P 500, mesure approchée du pouvoir de marché. Fichier : paytonfisher, financials.csv.

**Lien avec le thème.** Un ratio valeur de marché / valeur comptable élevé (proche du q de Tobin) signale des rentes durables, donc du pouvoir de marché. Littérature : Lindenberg et Ross (1981, *Journal of Business*), Montgomery et Wernerfelt (1988, *RAND Journal of Economics*).

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Valorisation / rentes | Price/Book | Aucune (log conseillé) |
| X1 | Taille | Market Cap | Logarithme |
| X2 | Rentabilité | Earnings/Share | Aucune |
| X3 | Marge implicite | Price/Sales | Aucune |
| X4 | Politique de distribution | Dividend Yield | Aucune |
| X5 | Secteur d'activité | Sector | Indicatrices (automatique dans R) |

**Hypothèse testée.** Les firmes plus grandes et plus rentables ont un Price/Book plus élevé, et l'effet du secteur reste significatif à taille donnée.

**Point d'attention.** Price/Book est négatif ou extrême pour quelques firmes à fonds propres négatifs : il faudra les signaler ou les exclure, et le dire dans le rapport. Les données datent d'environ 2018.

## Problématique 3 — La rentabilité dépend-elle du secteur ou de la firme ?

**Titre :** Les déterminants de la rentabilité par salarié des firmes du S&P 500 : effet secteur contre effet taille. Fichier : andrewmvd, sp500_companies.csv.

**Lien avec le thème.** Le paradigme Structure–Comportement–Performance prédit que la rentabilité dépend surtout de la structure du marché (le secteur). Littérature : Bain (1951), Schmalensee (1985, *American Economic Review*, « Do Markets Differ Much? »), Rumelt (1991).

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | EBITDA par salarié | Ebitda, Fulltimeemployees | Une division (puis log) |
| X1 | Secteur d'activité | Sector | Indicatrices (automatique dans R) |
| X2 | Taille | Marketcap | Logarithme |
| X3 | Croissance | Revenuegrowth | Aucune |
| X4 | Siège hors des États-Unis | Country | Indicatrice 0/1 |

**Hypothèse testée.** Les indicatrices de secteur expliquent une part importante de la variance de Y (comparer le R² avec et sans Sector), comme chez Schmalensee.

**Point d'attention.** Seule transformation : une division de deux colonnes. Les banques (EBITDA manquant) sortent de l'échantillon, ce qui réduit n.

## Recommandation et points de vigilance

**Choix conseillé : la problématique 1 (loi de Gibrat).** Y et X sont des colonnes brutes, la littérature est abondante et le lien avec l'économie industrielle est direct.

- [ ] Faire valider à votre tuteur un échantillon d'environ 500 firmes, potentiellement un peu moins après retrait des valeurs manquantes.
- [ ] Télécharger le fichier, compter les lignes complètes pour Y et les X retenus, et noter la date d'extraction (le dataset andrewmvd est mis à jour quotidiennement).
- [ ] Citer la source d'origine des données (Yahoo Finance via Kaggle) dans la présentation de la base.
- [ ] Vérifier chaque référence académique avant de la citer, comme l'exige la consigne sur l'IA.

**Limites à discuter dans le rapport.** Biais de sélection (seulement les plus grandes firmes américaines), coupe transversale à une seule date, causalité non établie (ex. la rentabilité peut causer la taille).

**Sources consultées.** Diaporama « PEA – Séance d'intro » (TSE, 2026/2027). Les colonnes et les nombres de lignes des datasets viennent d'un miroir de recherche ; les pages Kaggle elles-mêmes n'ont pas pu être ouvertes depuis cet environnement, donc vérifiez-les en téléchargeant les fichiers.
