# Frais des fonds d'investissement américains – Rapport de projet PEA

*8 octobre 2026 — version complète, 20 variables explicatives*

---

## 1. Résumé

**Problématique :** *Différenciation, coûts de recherche et pouvoir de marché : les déterminants des frais de gestion des fonds d'investissement américains.*

**Données :** environ 23 000 fonds communs de placement américains (Kaggle, « US Funds dataset from Yahoo Finance », données Morningstar, 2021).

**Variable expliquée :** frais annuels nets du fonds (*expense ratio*, en % de l'encours).

**Variables explicatives :** 20 variables organisées autour de 6 mécanismes d'organisation industrielle : économies d'échelle, pouvoir de marché des sociétés de gestion, coûts de recherche et distribution, discrimination par les prix, différenciation réelle (gestion active ou passive), qualité.

**Méthode :** statistiques descriptives, puis moindres carrés ordinaires (MCO) avec effets fixes de catégorie et erreurs standard regroupées par société de gestion.

---

## 2. Où trouver la base

**Kaggle : « US Funds dataset from Yahoo Finance »**, auteur Stefano Leone (stefanoleone992).
Lien : https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs

| Élément | Détail |
| --- | --- |
| Fichier à utiliser | `MutualFunds.csv` (le fichier `ETFs.csv` peut servir d'extension) |
| Observations | Environ 23 000 fonds (une ligne = une catégorie de parts d'un fonds) |
| Colonnes | Près de 300 : frais, encours, notes Morningstar, performances, risque, composition du portefeuille |
| Origine des données | Yahoo Finance, qui reprend les données de Morningstar |
| Date | Collecte vers 2021 (à vérifier dans la description Kaggle) |
| Accès | Gratuit, compte Kaggle nécessaire |
| Version européenne | « European Funds dataset from Morningstar », même auteur, pour une comparaison |

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes viennent de ma connaissance de la base : le code de la section 7 vérifie automatiquement lesquels existent.

---

## 3. Problématique et motivation

### 3.1 Le paradoxe

Un fonds indiciel S&P 500 détient les mêmes 500 actions dans les mêmes proportions que tous les autres fonds indiciels S&P 500. C'est un produit **quasi homogène**. Avec une concurrence à la Bertrand, les frais devraient converger vers le coût marginal de gestion, très faible.

Or les frais des fonds varient du simple au décuple, y compris parmi les fonds indiciels (Hortaçsu et Syverson, 2004). **Pourquoi la concurrence ne fait-elle pas baisser les prix sur ce marché ?**

### 3.2 Question de recherche

> Quels facteurs expliquent les écarts de frais entre fonds d'investissement : la taille, la marque de la société de gestion, la vente par des intermédiaires, la discrimination entre catégories de clients, ou la qualité réelle de la gestion ?

### 3.3 Pourquoi c'est de l'économie industrielle

| Question d'organisation industrielle | Ce qu'on teste ici |
| --- | --- |
| Concurrence en prix avec produits homogènes (Bertrand) | Les frais convergent-ils pour des produits identiques ? |
| Coûts de recherche (Stigler, 1961 ; Diamond, 1971) | Les épargnants mal informés paient-ils plus cher ? |
| Différenciation des produits | La différenciation est-elle réelle (gestion active) ou fictive (fonds qui copient l'indice) ? |
| Discrimination par les prix | Un même fonds est-il vendu plus cher aux petits épargnants ? |
| Économies d'échelle | Les gros fonds sont-ils moins chers ? |
| Pouvoir de marché et marque | Les grandes sociétés de gestion facturent-elles une prime ? |

### 3.4 Intérêt du sujet

- Les frais sont le principal déterminant de la performance nette des épargnants sur le long terme.
- Le régulateur américain (SEC) encadre les frais de commercialisation (règle 12b-1, 1980) ; le sujet a une dimension de politique de la concurrence et de protection du consommateur.
- En France et en Europe, le débat sur les frais de l'épargne (assurance-vie, PEA, épargne retraite) est très actuel : on peut s'en servir dans l'introduction.

---

## 4. Revue de littérature

À vérifier une par une avant de citer (consigne sur l'IA).

| Référence | Apport | Résultat principal |
| --- | --- | --- |
| Hortaçsu, A. et Syverson, C. (2004), « Product Differentiation, Search Costs, and Competition in the Mutual Fund Industry: A Case Study of S&P 500 Index Funds », *Quarterly Journal of Economics* | **Article central.** Explique la dispersion des frais entre fonds indiciels par les coûts de recherche et une différenciation non financière (services, marque) | Les coûts de recherche des épargnants expliquent une large part de la dispersion des prix |
| Choi, J., Laibson, D. et Madrian, B. (2010), « Why Does the Law of One Price Fail? An Experiment on Index Mutual Funds », *Review of Financial Studies* | Expérience : même informés, les investisseurs ne minimisent pas les frais | Les épargnants accordent trop de poids aux performances passées |
| Gil-Bazo, J. et Ruiz-Verdú, P. (2009), « The Relation between Price and Performance in the Mutual Fund Industry », *Journal of Finance* | Lien entre frais et performance ajustée du risque | Les fonds les plus chers ont une **moins bonne** performance : le prix n'est pas un signal de qualité |
| Khorana, A., Servaes, H. et Tufano, P. (2009), « Mutual Fund Fees Around the World », *Review of Financial Studies* | Comparaison internationale des frais | Frais plus bas pour les gros fonds et les grandes familles (économies d'échelle) |
| Bergstresser, D., Chalmers, J. et Tufano, P. (2009), « Assessing the Costs and Benefits of Brokers in the Mutual Fund Industry », *Review of Financial Studies* | Fonds vendus par des intermédiaires | Les fonds vendus via courtiers sont plus chers sans être meilleurs |
| Cremers, M. et Petajisto, A. (2009), « How Active Is Your Fund Manager? A New Measure That Predicts Performance », *Review of Financial Studies* | Mesure de la gestion réellement active | Beaucoup de fonds « actifs » copient en fait l'indice (*closet indexing*) |
| Tirole, J. (1988), *The Theory of Industrial Organization*, MIT Press | Cadre théorique | Bertrand, différenciation, coûts de recherche, discrimination par les prix |

---

## 5. Cadre théorique et hypothèses

| Mécanisme | Ce que prédit la théorie | Hypothèse | Variables concernées |
| --- | --- | --- | --- |
| **Économies d'échelle** | La gestion a des coûts fixes (équipe, recherche, conformité) amortis sur un encours plus grand | **H1** : encours élevé → frais plus bas | X1, X2 |
| **Pouvoir de marché et marque** | Une société de gestion connue vend sa réputation et peut facturer une prime ; à l'inverse, une grande famille peut mutualiser ses coûts | **H2** : effet de la taille de la société de gestion (signe à déterminer) | X3, X4 |
| **Coûts de recherche et distribution** | Les fonds vendus par des intermédiaires visent des épargnants moins informés, qui comparent peu | **H3** : frais d'entrée, de sortie et de commercialisation élevés → frais de gestion plus élevés | X5, X6, X7 |
| **Discrimination par les prix** | Un même fonds est décliné en parts pour petits épargnants (chères) et pour gros clients (bon marché) | **H4** : investissement minimum élevé → frais plus bas | X8 |
| **Différenciation réelle ou fictive** | La gestion active coûte plus cher. Mais un fonds qui copie l'indice tout en facturant une gestion active exerce un pouvoir de marché | **H5** : fonds indiciel, faible rotation → frais plus bas ; **H5 bis** : à rotation égale, R² élevé (copie de l'indice) ne réduit pas les frais | X9, X10, X11, X12 |
| **Qualité et signal** | Si le marché était efficient, les fonds plus chers devraient offrir une meilleure performance | **H6** : alpha et Sharpe sans lien (ou lien négatif) avec les frais, mais note Morningstar positive | X13 à X17 |
| **Capital humain** | Un gérant expérimenté peut facturer davantage | **H7** : ancienneté du gérant → frais plus élevés | X18 |

---

## 6. Variables

### 6.1 Variable expliquée

| Variable | Colonne | Remarque |
| --- | --- | --- |
| **Y : frais annuels nets (%)** | `fund_annual_report_net_expense_ratio` | Vérifier l'unité : 0,75 (en %) ou 0,0075 (en fraction) |
| Y alternative 1 : frais relatifs | `fund_annual_report_net_expense_ratio` − `category_annual_report_net_expense_ratio` | Écart à la moyenne de la catégorie : le fonds est-il cher face à ses concurrents directs ? |
| Y alternative 2 : frais bruts | `fund_prospectus_gross_expense_ratio` | Avant les remises accordées par le gestionnaire |

### 6.2 Les 20 variables explicatives

| # | Variable | Colonne source | Construction | Mécanisme | Signe attendu |
| --- | --- | --- | --- | --- | --- |
| X1 | Taille du fonds | `total_net_assets` | Logarithme | Économies d'échelle | − |
| X2 | Âge du fonds (années) | `inception_date` | 2021 − année de création | Économies d'échelle, réputation | − |
| X3 | Part de marché de la société de gestion | `fund_family`, `total_net_assets` | Encours de la famille / encours total (1 ligne) | Pouvoir de marché | ? |
| X4 | Nombre de fonds de la société de gestion | `fund_family` | Comptage par famille (1 ligne), logarithme | Gamme, économies de gamme | ? |
| X5 | Frais d'entrée maximum | `fund_max_front_end_sales_load` | Aucune (0 si manquant, à justifier) | Coûts de recherche, distribution | + |
| X6 | Frais de sortie maximum | `fund_max_deferred_sales_load` | Aucune (0 si manquant) | Coûts de changement | + |
| X7 | Frais de commercialisation (12b-1) | `fund_max_12b1_fee` | Aucune (0 si manquant) | Distribution | + |
| X8 | Investissement minimum | `initial_investment` | Logarithme (+1) | Discrimination par les prix | − |
| X9 | Fonds indiciel | `fund_long_name` | Indicatrice : nom contenant « Index » (1 ligne) | Gestion passive | − |
| X10 | Rotation du portefeuille | `annual_holdings_turnover` | Aucune | Intensité de gestion active | + |
| X11 | Poids des 10 premières lignes | `top10_holdings_total_assets` | Aucune | Concentration du portefeuille, gestion active | + |
| X12 | R² par rapport à l'indice (3 ans) | `fund_r_squared_3years` | Aucune | Copie de l'indice (différenciation fictive) | − (si marché efficient) |
| X13 | Note Morningstar globale | `morningstar_overall_rating` | Aucune (1 à 5) | Signal de qualité perçue | + |
| X14 | Alpha (3 ans) | `fund_alpha_3years` | Aucune | Qualité réelle de la gestion | 0 ou − |
| X15 | Ratio de Sharpe (3 ans) | `fund_sharpe_ratio_3years` | Aucune | Rendement ajusté du risque | 0 ou − |
| X16 | Volatilité (3 ans) | `fund_stdev_3years` | Aucune | Risque du fonds | + |
| X17 | Bêta (3 ans) | `fund_beta_3years` | Aucune | Exposition au marché | ? |
| X18 | Ancienneté du gérant (années) | `management_start_date` | 2021 − année d'arrivée | Capital humain | + |
| X19 | Part investie en actions | `asset_stocks` | Aucune | Type de produit (les actions coûtent plus cher à gérer que les obligations) | + |
| X20 | Catégorie Morningstar | `fund_category` | Effets fixes (automatique dans R) | Comparer des fonds comparables | — |

**Variables écartées volontairement :**
- `fund_return_3years` et `morningstar_return_rating` : trop corrélées avec l'alpha et la note globale.
- `size_type` et `investment_type` : déjà contenues dans `fund_category` (par exemple « Large Growth »).
- `fund_prospectus_net_expense_ratio` : presque identique à Y.

---

## 7. Préparation des données en R

```r
library(sandwich)   # erreurs standard regroupées
library(lmtest)

fd <- read.csv("MutualFunds.csv")

# ---- 1. Vérifier les colonnes ----------------------------------------------
cols <- c("fund_symbol", "fund_long_name", "fund_family",
          "fund_annual_report_net_expense_ratio", "category_annual_report_net_expense_ratio",
          "fund_prospectus_gross_expense_ratio",
          "total_net_assets", "inception_date",
          "fund_max_front_end_sales_load", "fund_max_deferred_sales_load", "fund_max_12b1_fee",
          "initial_investment", "annual_holdings_turnover", "top10_holdings_total_assets",
          "fund_r_squared_3years", "morningstar_overall_rating", "fund_alpha_3years",
          "fund_sharpe_ratio_3years", "fund_stdev_3years", "fund_beta_3years",
          "management_start_date", "asset_stocks", "fund_category")
setdiff(cols, names(fd))          # doit être vide ; sinon chercher avec grep("mot", names(fd), value = TRUE)
fd <- fd[, intersect(cols, names(fd))]

# ---- 2. Variable expliquée -------------------------------------------------
fd$Y      <- fd$fund_annual_report_net_expense_ratio
summary(fd$Y)                      # vérifier l'unité (% ou fraction)
fd$Y_rel  <- fd$Y - fd$category_annual_report_net_expense_ratio

# ---- 3. Variables construites ----------------------------------------------
annee <- function(d) as.numeric(substr(d, 1, 4))          # format AAAA-MM-JJ à vérifier

fd$log_tna      <- log(fd$total_net_assets)
fd$age          <- 2021 - annee(fd$inception_date)
enc_famille     <- ave(fd$total_net_assets, fd$fund_family, FUN = function(x) sum(x, na.rm = TRUE))
fd$part_famille <- enc_famille / sum(fd$total_net_assets, na.rm = TRUE)
fd$nb_fonds_fam <- ave(fd$Y, fd$fund_family, FUN = length)
fd$indiciel     <- as.integer(grepl("index", fd$fund_long_name, ignore.case = TRUE))
fd$anc_gerant   <- 2021 - annee(fd$management_start_date)
fd$log_minimum  <- log(fd$initial_investment + 1)

# Frais de distribution : une valeur manquante signifie souvent "pas de frais" (à vérifier)
for (v in c("fund_max_front_end_sales_load", "fund_max_deferred_sales_load", "fund_max_12b1_fee"))
  fd[[v]][is.na(fd[[v]])] <- 0

# ---- 4. Échantillon de travail ---------------------------------------------
fd <- subset(fd, total_net_assets > 0 & !is.na(Y))
nrow(fd)                           # nombre d'observations
colSums(is.na(fd))                 # valeurs manquantes par variable
```

---

## 8. Statistiques descriptives à présenter

| # | Tableau ou graphique | Ce qu'il montre | Hypothèse |
| --- | --- | --- | --- |
| 1 | Tableau : moyenne, médiane, écart-type, min, max des 20 X et de Y | Présentation de la base | — |
| 2 | Histogramme des frais | Dispersion des prix | Paradoxe |
| 3 | **Frais min, médian et max parmi les seuls fonds indiciels** | La loi du prix unique ne tient pas pour un produit homogène | Paradoxe central |
| 4 | Frais moyens par décile d'encours | Économies d'échelle | H1 |
| 5 | Frais moyens des 10 plus grandes sociétés de gestion (Vanguard, Fidelity, BlackRock…) | Effet de la marque | H2 |
| 6 | Frais moyens selon que le fonds a des frais d'entrée ou non | Coûts de recherche | H3 |
| 7 | Frais moyens par tranche d'investissement minimum | Discrimination par les prix | H4 |
| 8 | Nuage de points : frais contre R², fonds actifs seulement | Fonds qui copient l'indice | H5 bis |
| 9 | Nuage de points : frais contre alpha | Les fonds chers sont-ils meilleurs ? | H6 |
| 10 | Matrice de corrélation des X | Repérer la colinéarité | — |

```r
summary(fd[, c("Y", "log_tna", "age", "part_famille", "indiciel", "fund_alpha_3years")])
hist(fd$Y, breaks = 100, main = "Distribution des frais", xlab = "Frais annuels nets")
tapply(fd$Y, fd$indiciel, quantile, probs = c(0, .1, .5, .9, 1), na.rm = TRUE)
plot(fd$fund_alpha_3years, fd$Y, pch = ".", xlab = "Alpha 3 ans", ylab = "Frais")
round(cor(fd[, c("log_tna", "age", "fund_alpha_3years", "fund_sharpe_ratio_3years",
                 "fund_r_squared_3years", "morningstar_overall_rating")], use = "complete.obs"), 2)
```

---

## 9. Stratégie économétrique

### 9.1 Modèle principal

```latex
\text{Frais}_i = \beta_0 + \sum_{k=1}^{19} \beta_k X_{k,i} + \gamma_{\text{cat}(i)} + \varepsilon_i
```

où *i* est le fonds et γ un effet fixe par catégorie Morningstar (X20). Les effets fixes comparent chaque fonds aux fonds de la même catégorie : un fonds d'actions américaines de grandes entreprises n'est comparé qu'à ses semblables.

### 9.2 Modèles emboîtés (à présenter dans un même tableau)

| Modèle | Variables | Objectif |
| --- | --- | --- |
| M1 | X1, X2, X20 | Économies d'échelle seules |
| M2 | M1 + X3, X4 | Ajout du pouvoir de marché des sociétés de gestion |
| M3 | M2 + X5 à X8 | Ajout de la distribution et de la discrimination par les prix |
| M4 | M3 + X9 à X12 | Ajout de la gestion active ou passive |
| M5 (complet) | M4 + X13 à X19 | Ajout de la qualité et des contrôles |

```r
m1 <- lm(Y ~ log_tna + age + factor(fund_category), data = fd)
m2 <- update(m1, . ~ . + part_famille + log(nb_fonds_fam))
m3 <- update(m2, . ~ . + fund_max_front_end_sales_load + fund_max_deferred_sales_load +
                         fund_max_12b1_fee + log_minimum)
m4 <- update(m3, . ~ . + indiciel + annual_holdings_turnover + top10_holdings_total_assets +
                         fund_r_squared_3years)
m5 <- update(m4, . ~ . + morningstar_overall_rating + fund_alpha_3years + fund_sharpe_ratio_3years +
                         fund_stdev_3years + fund_beta_3years + anc_gerant + asset_stocks)

# Erreurs standard regroupées par société de gestion
coeftest(m5, vcov = vcovCL(m5, cluster = ~ fund_family))
```

Pour un tableau propre des 5 modèles côte à côte : package `stargazer` ou `modelsummary`.

### 9.3 Tests de robustesse

| Test | Pourquoi |
| --- | --- |
| Y = frais relatifs (`Y_rel`) | Vérifier que les résultats ne viennent pas des écarts entre catégories |
| Y = log des frais | Réduire l'effet des valeurs extrêmes, lecture en % |
| Fonds indiciels seulement | Reproduire Hortaçsu et Syverson sur un produit homogène |
| Retirer X14 ou X15 | Alpha et Sharpe sont corrélés : vérifier la stabilité des coefficients |
| Garder une seule part par fonds (la moins chère) | Éviter de compter plusieurs fois le même portefeuille |

### 9.4 Points de vigilance économétriques

- **Colinéarité :** alpha, Sharpe et note Morningstar sont corrélés ; X3 et X4 aussi. Vérifier avec `car::vif(m5)` (VIF supérieur à 10 = problème).
- **Hétéroscédasticité :** probable (les petits fonds ont des frais plus dispersés) ; les erreurs standard regroupées la corrigent.
- **Observations non indépendantes :** plusieurs parts d'un même fonds et plusieurs fonds d'une même société, d'où le regroupement par `fund_family`.
- **Taille de l'échantillon :** avec des milliers d'observations, presque tout sera significatif : commenter la **taille économique** des coefficients (par exemple : « doubler l'encours réduit les frais de 0,05 point »).

---

## 10. Résultats attendus

| Hypothèse | Résultat attendu d'après la littérature | Interprétation |
| --- | --- | --- |
| H1 Échelle | Coefficient négatif de log(encours) | Les gros fonds partagent leurs coûts fixes |
| H2 Marque | Ambigu : les très grandes familles (Vanguard) sont bon marché, les marques « premium » chères | Deux modèles économiques coexistent |
| H3 Distribution | Coefficients positifs des frais d'entrée et 12b-1 | Les épargnants conseillés par un intermédiaire paient plus |
| H4 Discrimination | Coefficient négatif de l'investissement minimum | Les gros clients paient moins pour le même produit |
| H5 Gestion | Fonds indiciels nettement moins chers | La gestion passive coûte moins |
| H5 bis Copie d'indice | R² élevé sans baisse de frais | Différenciation fictive = pouvoir de marché |
| H6 Qualité | Alpha non significatif ou négatif | Le prix n'est pas un signal de qualité (Gil-Bazo et Ruiz-Verdú) |

---

## 11. Limites à discuter

- **Causalité inversée :** les fonds peu chers attirent davantage d'épargne. L'encours (X1) dépend donc en partie des frais, ce qui biaise son coefficient.
- **Biais de survie :** les fonds fermés ou fusionnés avant 2021, souvent les moins performants, ont disparu de la base.
- **Indicatrice « indiciel » approximative :** repérée par le mot « Index » dans le nom.
- **Une seule date :** coupe transversale ; impossible d'étudier l'évolution des frais dans le temps.
- **Pas de données sur les épargnants :** on ne connaît ni leur niveau d'information ni leur revenu ; les coûts de recherche sont mesurés indirectement (frais de distribution).
- **Données agrégées par Yahoo Finance :** quelques erreurs de saisie possibles ; repérer les valeurs aberrantes (frais supérieurs à 5 %, encours nuls).

---

## 12. Plan du rapport final (conforme à la consigne du PEA)

| Partie | Contenu | Pages indicatives |
| --- | --- | --- |
| Introduction | Le paradoxe des fonds indiciels, chiffres clés, question de recherche | 2–3 |
| Revue de littérature | Hortaçsu et Syverson, Gil-Bazo et Ruiz-Verdú, Khorana et al., Cremers et Petajisto | 4–5 |
| Présentation de la base | Source, observations, Y, les 20 X, tableau de statistiques | 3–4 |
| Statistiques descriptives | Les 10 tableaux et graphiques de la section 8, comparés à la littérature | 5–6 |
| Économétrie | Modèles M1 à M5, robustesse, interprétation | 6–8 |
| Conclusion | Réponse à la question, limites, implications pour la régulation | 1–2 |
| Bibliographie | Références vérifiées | 1 |

Total : 30 pages maximum, graphiques et bibliographie compris.

---

## 13. Prochaines étapes

- [ ] Télécharger `MutualFunds.csv` sur Kaggle.
- [ ] Lancer le code de la section 7 : vérifier les colonnes (`setdiff`), l'unité des frais et le format des dates.
- [ ] Compter les observations complètes pour Y et les 20 X.
- [ ] Faire valider la problématique et la liste des variables par votre tuteur.
- [ ] Lire Hortaçsu et Syverson (2004) et Gil-Bazo et Ruiz-Verdú (2009) en premier.
- [ ] Rédiger l'introduction et la revue de littérature avant le rapport intermédiaire (24 janvier).
