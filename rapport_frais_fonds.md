# Frais des fonds d'investissement américains – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Kaggle : « US Funds dataset from Yahoo Finance »**, auteur Stefano Leone (stefanoleone992).
Lien : https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs

- Fichiers : `MutualFunds.csv` (environ 23 000 fonds communs de placement) et `ETFs.csv` (environ 2 000 ETF), collectés sur Yahoo Finance (données Morningstar), environ 2021.
- Près de 300 colonnes : frais, encours, notes Morningstar, performances, risque, composition du portefeuille.
- Pour télécharger : compte Kaggle gratuit, puis bouton « Download » (quelques dizaines de Mo).
- Le même auteur publie une version européenne (« European Funds dataset from Morningstar »), utile pour comparer.

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes ci-dessous sont à vérifier avec `names()`.

## Problématique

**Titre :** *Différenciation, réputation et pouvoir de marché : les déterminants des frais de gestion des fonds d'investissement américains.*

**Question :** pourquoi des fonds qui vendent un produit très proche (par exemple, plusieurs fonds répliquant le même indice) facturent-ils des frais si différents ? Est-ce la qualité, la taille, la marque de la société de gestion, ou l'ignorance des épargnants ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Concurrence en prix, différenciation, coûts de recherche, discrimination par les prix |
| ≥ 500 observations | Environ 23 000 fonds |
| Y continue | Frais annuels (% de l'encours) |
| Plusieurs X sans transformation lourde | 11 X, dont 8 en colonnes brutes |

## Lien avec l'organisation industrielle

Le fonds d'investissement est un produit quasi homogène : un fonds indiciel S&P 500 en vaut un autre. Avec une concurrence à la Bertrand, les frais devraient tous être au niveau du coût. Ce n'est pas le cas, et la théorie propose plusieurs explications.

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Économies d'échelle | La gestion a des coûts fixes : un gros fonds peut facturer moins par euro géré | H1 : encours élevé → frais plus bas |
| Coûts de recherche des épargnants | Comparer les fonds est coûteux ; les épargnants mal informés paient plus cher (Hortaçsu et Syverson, 2004) | H2 : fonds vendus via des intermédiaires (frais d'entrée) → frais plus élevés |
| Marque et différenciation | Une grande société de gestion vend sa réputation, pas seulement sa performance | H3 : grande famille de fonds → frais différents à qualité égale |
| Signal de qualité | Une bonne note Morningstar permet de facturer plus | H4 : meilleure note → frais plus élevés |
| Discrimination par les prix | Un même fonds est vendu en plusieurs « parts » (A, C, institutionnelle) à des prix différents selon le client | H5 : parts pour particuliers → frais plus élevés |
| Gestion active ou passive | La gestion active coûte plus cher mais ne surperforme pas toujours | H6 : fonds indiciel → frais beaucoup plus bas |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Frais annuels nets (%) | `fund_annual_report_net_expense_ratio` | Aucune |
| X1 | Taille du fonds (encours) | `total_net_assets` | Logarithme |
| X2 | Taille de la société de gestion | `fund_family` | Nombre de fonds par famille (1 ligne) |
| X3 | Fonds indiciel | `fund_long_name` | Indicatrice : nom contenant « Index » (1 ligne) |
| X4 | Note Morningstar (1 à 5) | `morningstar_overall_rating` | Aucune |
| X5 | Frais d'entrée maximum (vente par intermédiaire) | `fund_max_front_end_sales_load` | Aucune |
| X6 | Frais de distribution (12b-1) | `fund_max_12b1_fee` | Aucune |
| X7 | Rotation du portefeuille | `annual_holdings_turnover` | Aucune |
| X8 | Âge du fonds (années) | `inception_date` | 2021 − année de création (1 ligne) |
| X9 | Investissement minimum | `initial_investment` | Logarithme (+1) |
| X10 | Performance sur 3 ans | `fund_return_3years` | Aucune |
| X11 | Catégorie (actions US, obligations…) | `fund_category` | Indicatrices automatiques |

**X9 mesure la discrimination par les prix :** un investissement minimum élevé signale une part réservée aux gros clients, qui paient moins de frais.

## Code R

```r
fd <- read.csv("MutualFunds.csv")
names(fd)

fd$Y           <- fd$fund_annual_report_net_expense_ratio
fd$taille_fam  <- ave(fd$Y, fd$fund_family, FUN = length)
fd$indiciel    <- as.integer(grepl("Index", fd$fund_long_name, ignore.case = TRUE))
fd$age         <- 2021 - as.numeric(substr(fd$inception_date, 1, 4))   # format AAAA-MM-JJ à vérifier

modele <- lm(Y ~ log(total_net_assets) + log(taille_fam) + indiciel +
               morningstar_overall_rating + fund_max_front_end_sales_load +
               fund_max_12b1_fee + annual_holdings_turnover + age +
               log(initial_investment + 1) + fund_return_3years +
               factor(fund_category),
             data = subset(fd, total_net_assets > 0))
summary(modele)
```

Vérifiez l'unité de Y : les frais peuvent être stockés en pourcentage (0,75) ou en fraction (0,0075).

## Statistiques descriptives à présenter

1. Distribution des frais : histogramme, moyenne, écart entre le 10e et le 90e centile.
2. **Le paradoxe central :** frais minimum, médian et maximum parmi les seuls fonds indiciels S&P 500 (produits quasi identiques).
3. Frais moyens par tranche d'encours (petits, moyens, gros fonds).
4. Frais moyens selon la note Morningstar.
5. Frais moyens des 10 plus grandes sociétés de gestion (Vanguard, Fidelity, BlackRock…).

## Littérature à mobiliser

À vérifier avant de citer.

- Hortaçsu, A. et Syverson, C. (2004), « Product Differentiation, Search Costs, and Competition in the Mutual Fund Industry: A Case Study of S&P 500 Index Funds », *Quarterly Journal of Economics*.
- Khorana, A., Servaes, H. et Tufano, P. (2009), « Mutual Fund Fees Around the World », *Review of Financial Studies*.
- Gil-Bazo, J. et Ruiz-Verdú, P. (2009), « The Relation between Price and Performance in the Mutual Fund Industry », *Journal of Finance*.
- Choi, J., Laibson, D. et Madrian, B. (2010), « Why Does the Law of One Price Fail? An Experiment on Index Mutual Funds », *Review of Financial Studies*.
- Manuel : Tirole, J. (1988), *The Theory of Industrial Organization*, MIT Press, pour la différenciation, les coûts de recherche et la discrimination par les prix.

## Limites à discuter

- **Plusieurs lignes par fonds :** un même fonds apparaît souvent avec plusieurs parts (A, C, institutionnelle). Les observations ne sont pas indépendantes ; on peut le signaler, ou regrouper les erreurs standard par fonds.
- **Causalité :** les fonds peu chers attirent plus d'épargne, donc l'encours dépend aussi des frais (causalité inversée sur X1).
- **Biais de survie :** les fonds fermés avant 2021 ont disparu de la base.
- **Indicatrice « indiciel » approximative :** repérée par le mot « Index » dans le nom, ce qui peut manquer quelques fonds.

## Prochaines étapes

- [ ] Télécharger `MutualFunds.csv` et vérifier les noms de colonnes et l'unité des frais.
- [ ] Compter les observations complètes pour Y et les 11 X.
- [ ] Faire valider la problématique par votre tuteur, en insistant sur le paradoxe des fonds indiciels (produit homogène, prix différents).
- [ ] Lire Hortaçsu et Syverson (2004) en premier : c'est exactement votre question.
