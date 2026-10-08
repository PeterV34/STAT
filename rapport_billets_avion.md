# Prix des billets d'avion aux États-Unis – Rapport de projet PEA

*8 octobre 2026*

## Verdict

**C'est la base la plus adaptée à la consigne.** Une ligne correspond à une liaison aérienne (paire de villes) pendant un trimestre. Les mesures de concurrence (parts de marché, présence d'une low-cost) sont déjà des colonnes : il n'y a presque rien à transformer.

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Au cœur du sujet : concentration, pouvoir de marché, entrée des low-cost |
| ≥ 500 observations | Environ 1 000 liaisons par trimestre, soit environ 4 000 sur une année |
| Y continue | Prix moyen du billet |
| Plusieurs X sans transformation lourde | 9 X : des colonnes brutes, deux logarithmes et deux indicatrices |
| Source citable | U.S. Department of Transportation (données officielles) |

**Où trouver les données :**
- Source officielle : data.transportation.gov, « Consumer Airfare Report: Table 1a – All U.S. Airport Pair Markets ».
- Copie Kaggle : « US Airline Flight Routes and Fares 1993-2024 ».

> Je n'ai pas pu télécharger le fichier depuis mon environnement. Les noms de colonnes viennent de ma connaissance de la base : vérifiez-les avec `names()`.

## Problématique

**Titre :** *Concentration du marché et entrée des compagnies low-cost : les déterminants du prix des billets d'avion aux États-Unis (2024).*

**Question :** sur une liaison aérienne, le prix est-il plus élevé quand une compagnie domine le marché, et plus bas quand une compagnie low-cost y est présente ?

## Lien avec l'organisation industrielle

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Pouvoir de marché | Une compagnie dominante peut fixer un prix au-dessus du coût marginal (Cournot, indice de Lerner) | H1 : `large_ms` plus élevé → prix plus élevé |
| Pression concurrentielle des low-cost | L'arrivée d'un concurrent à bas coût discipline les prix en place | H2 : `lf_ms` plus élevé → prix plus bas |
| Effet Southwest | La simple présence de Southwest fait baisser les prix de toute la liaison | H3 : Southwest présente → prix plus bas |
| Coûts | Le coût augmente avec la distance, mais moins que proportionnellement | H4 : élasticité du prix à la distance positive et inférieure à 1 |
| Économies de densité | Les liaisons très fréquentées ont des coûts unitaires plus faibles | H5 : plus de passagers → prix plus bas |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Prix moyen du billet ($) | `fare` | Aucune (ou log) |
| X1 | Part de marché de la compagnie dominante | `large_ms` | Aucune |
| X2 | Part de marché de la compagnie la moins chère | `lf_ms` | Aucune |
| X3 | La dominante est aussi la moins chère | `carrier_lg`, `carrier_low` | Indicatrice (les deux identiques) |
| X4 | Southwest est la compagnie la moins chère | `carrier_low` | Indicatrice (`== "WN"`) |
| X5 | Identité de la compagnie dominante | `carrier_lg` | Indicatrices automatiques |
| X6 | Distance (miles) | `nsmiles` | Logarithme |
| X7 | Passagers par jour | `passengers` | Logarithme |
| X8 | Trimestre | `quarter` | Indicatrices automatiques (saisonnalité) |
| X9 | Ville de départ | `city1` | Indicatrices automatiques (optionnel : aéroports hubs) |

**À ne pas mettre en X :** `fare_lg` et `fare_low`. Ce sont des prix, donc des composantes de Y elles-mêmes.

## Code R

```r
av <- read.csv("US_Airline_Fares.csv")      # nom du fichier à adapter
names(av)
av <- subset(av, Year == 2024)              # une année = coupe transversale, ~4 000 lignes

av$domin_lowcost <- as.integer(av$carrier_lg == av$carrier_low)
av$southwest     <- as.integer(av$carrier_low == "WN")

modele <- lm(log(fare) ~ large_ms + lf_ms + domin_lowcost + southwest +
               factor(carrier_lg) + log(nsmiles) + log(passengers) + factor(quarter),
             data = av)
summary(modele)
```

Avec Y en logarithme, les coefficients se lisent en pourcentage. Par exemple, un coefficient de 0,30 sur `large_ms` signifie qu'une hausse de 10 points de la part de marché de la dominante augmente le prix d'environ 3 %.

## Statistiques descriptives à présenter

1. Distribution du prix et de `large_ms` (histogrammes).
2. Nuage de points du prix contre `large_ms`, avec droite de régression.
3. Prix moyen selon que Southwest est présente ou non, avec un test de différence de moyennes.
4. Prix moyen par compagnie dominante (American, Delta, United, Southwest…).
5. Prix par mile selon la tranche de distance.

## Littérature à mobiliser

À vérifier avant de citer.

- Borenstein, S. (1989), « Hubs and High Fares: Dominance and Market Power in the U.S. Airline Industry », *RAND Journal of Economics*.
- Morrison, S. (2001), « Actual, Adjacent, and Potential Competition: Estimating the Full Effect of Southwest Airlines », *Journal of Transport Economics and Policy*.
- Goolsbee, A. et Syverson, C. (2008), « How Do Incumbents Respond to the Threat of Entry? Evidence from the Major Airlines », *Quarterly Journal of Economics*.
- Brueckner, J., Lee, D. et Singer, E. (2013), « Airline Competition and Domestic US Airfares: A Comprehensive Reappraisal », *Economics of Transportation*.
- Manuel : Tirole, J. (1988), *The Theory of Industrial Organization*, MIT Press, pour Cournot et l'indice de Lerner.

## Limites à discuter

- **Endogénéité :** la concentration dépend elle-même des prix et de la demande. On mesure des corrélations conditionnelles, pas forcément des effets causaux.
- **Concurrence incomplète :** on ne connaît que deux compagnies par liaison (la dominante et la moins chère), pas le nombre total de concurrents.
- **Prix moyens :** ils mélangent toutes les classes et toutes les dates d'achat.
- **Concurrence entre aéroports :** les aéroports voisins d'une même ville (par exemple les trois de New York) se font concurrence, ce que la base ne capte pas.

## Prochaines étapes

- [ ] Télécharger le fichier (data.transportation.gov ou Kaggle) et vérifier les noms de colonnes.
- [ ] Garder une seule année (2024) et compter les lignes complètes.
- [ ] Faire valider la problématique par votre tuteur.
- [ ] Lire Borenstein (1989) et Goolsbee et Syverson (2008) en premier.
