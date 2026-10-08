# Ventes de jeux vidéo – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Kaggle : « Video Game Sales with Ratings »**, auteur Rush Kirubi (rush4ratio).
Lien : https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings

- Fichier : `Video_Games_Sales_as_at_22_Dec_2016.csv`, environ 16 700 lignes (une ligne = un jeu sur une console), données arrêtées en décembre 2016.
- Ventes : estimations du site VGChartz, en millions d'exemplaires. Notes : Metacritic.
- Environ 7 000 lignes ont à la fois les ventes et la note des critiques : c'est l'échantillon de travail, très au-dessus de 500.
- Pour télécharger : compte Kaggle gratuit, puis bouton « Download ». Le fichier est petit (environ 1,5 Mo) et s'ouvre aussi dans Excel.

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes ci-dessous sont à vérifier avec `names()`.

## Problématique

**Titre :** *Intégration verticale et effets de réseau : les déterminants des ventes de jeux vidéo (2000–2016).*

**Question :** les jeux édités par le fabricant de la console (Nintendo sur Wii, Sony sur PlayStation, Microsoft sur Xbox) se vendent-ils mieux que les jeux d'éditeurs indépendants, à qualité égale ? Et quel rôle jouent la taille de l'écosystème de la console et la sortie sur plusieurs consoles ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Intégration verticale, plateformes, effets de réseau, multi-hébergement |
| ≥ 500 observations | Environ 7 000 jeux avec ventes et note |
| Y continue | Ventes mondiales (millions d'exemplaires) |
| Plusieurs X sans transformation lourde | 10 X, dont 6 en colonnes brutes |

## Lien avec l'organisation industrielle

Le jeu vidéo est un **marché biface** : le fabricant de console vend la machine aux joueurs et fait payer une redevance aux éditeurs de jeux. Il est aussi souvent **éditeur lui-même** (intégration verticale).

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Intégration verticale | Le fabricant investit davantage dans ses propres jeux, qui font vendre sa console (biens complémentaires) | H1 : jeu du fabricant → plus de ventes |
| Effets de réseau indirects | Plus une console a de jeux, plus elle attire de joueurs, et inversement | H2 : grand catalogue de la console → plus de ventes par jeu |
| Multi-hébergement | Sortir sur plusieurs consoles élargit le marché mais divise les ventes par version | H3 : effet du nombre de consoles sur les ventes de chaque version |
| Qualité et information | La note des critiques sert de signal de qualité | H4 : meilleure note → plus de ventes |
| Économies d'échelle en marketing | Les grands éditeurs (EA, Activision…) ont plus de moyens de promotion | H5 : grand éditeur → plus de ventes |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Ventes mondiales (millions) | `Global_Sales` | Logarithme |
| X1 | Jeu édité par le fabricant de la console | `Publisher`, `Platform` | Indicatrice (1 ligne, voir code) |
| X2 | Note des critiques (0–100) | `Critic_Score` | Aucune |
| X3 | Nombre de critiques | `Critic_Count` | Aucune (mesure de visibilité) |
| X4 | Note des joueurs (0–10) | `User_Score` | Conversion en nombre (« tbd » → manquant) |
| X5 | Taille du catalogue de la console | `Platform` | Nombre de jeux par console (1 ligne) |
| X6 | Nombre de consoles sur lesquelles sort le jeu | `Name` | Nombre de lignes par jeu (1 ligne) |
| X7 | Taille de l'éditeur | `Publisher` | Nombre de jeux par éditeur (1 ligne) |
| X8 | Genre (action, sport…) | `Genre` | Indicatrices automatiques |
| X9 | Classification d'âge (E, T, M…) | `Rating` | Indicatrices automatiques |
| X10 | Année de sortie | `Year_of_Release` | Indicatrices automatiques (ou continue) |

## Code R

```r
jv <- read.csv("Video_Games_Sales_as_at_22_Dec_2016.csv")
names(jv)

jv$User_Score <- as.numeric(jv$User_Score)            # "tbd" devient NA
jv$Year       <- as.numeric(jv$Year_of_Release)
jv <- subset(jv, Year >= 2000 & !is.na(Critic_Score))

fabricant <- c(Wii = "Nintendo", WiiU = "Nintendo", DS = "Nintendo", `3DS` = "Nintendo",
               GC = "Nintendo", GBA = "Nintendo",
               PS2 = "Sony Computer Entertainment", PS3 = "Sony Computer Entertainment",
               PS4 = "Sony Computer Entertainment", PSP = "Sony Computer Entertainment",
               PSV = "Sony Computer Entertainment",
               XB = "Microsoft Game Studios", X360 = "Microsoft Game Studios",
               XOne = "Microsoft Game Studios")
jv$first_party <- as.integer(jv$Publisher == fabricant[jv$Platform] & !is.na(fabricant[jv$Platform]))

jv$catalogue   <- ave(jv$Global_Sales, jv$Platform,  FUN = length)
jv$nb_consoles <- ave(jv$Global_Sales, jv$Name,      FUN = length)
jv$taille_edit <- ave(jv$Global_Sales, jv$Publisher, FUN = length)

modele <- lm(log(Global_Sales) ~ first_party + Critic_Score + Critic_Count + User_Score +
               log(catalogue) + nb_consoles + log(taille_edit) +
               factor(Genre) + factor(Rating) + factor(Year), data = jv)
summary(modele)
```

Vérifiez dans `table(jv$Publisher)` l'orthographe exacte des noms des trois fabricants.

## Statistiques descriptives à présenter

1. Ventes médianes des jeux du fabricant contre celles des éditeurs indépendants, par console.
2. Part des jeux du fabricant dans les ventes totales de chaque console.
3. Nuage de points des ventes (en log) contre la note des critiques, en distinguant jeux du fabricant et jeux indépendants.
4. Nombre de jeux et ventes moyennes par console (illustration des effets de réseau).
5. Ventes moyennes selon le nombre de consoles sur lesquelles sort le jeu (1, 2, 3, 4 et plus).

## Littérature à mobiliser

À vérifier avant de citer.

- Rochet, J.-C. et Tirole, J. (2003), « Platform Competition in Two-Sided Markets », *Journal of the European Economic Association*.
- Clements, M. et Ohashi, H. (2005), « Indirect Network Effects and the Product Cycle: Video Games in the U.S., 1994–2002 », *Journal of Industrial Economics*.
- Corts, K. et Lederman, M. (2009), « Software Exclusivity and the Scope of Indirect Network Effects in the U.S. Home Video Game Market », *International Journal of Industrial Organization*.
- Lee, R. (2013), « Vertical Integration and Exclusivity in Platform and Two-Sided Markets », *American Economic Review*.
- Landsman, V. et Stremersch, S. (2011), « Multihoming in Two-Sided Markets: An Empirical Inquiry in the Video Game Console Industry », *Journal of Marketing*.

## Limites à discuter

- **Données estimées :** les ventes VGChartz sont des estimations et ne comptent que les ventes physiques (pas le téléchargement).
- **Causalité :** le fabricant choisit peut-être d'éditer lui-même les jeux qu'il sait porteurs (biais de sélection).
- **Catalogue et ventes liés :** une console qui se vend bien attire plus de jeux, ce qui crée une causalité dans les deux sens (c'est le principe même des effets de réseau).
- **Données arrêtées en 2016 :** pas de Switch ni de PS5.

## Prochaines étapes

- [ ] Télécharger le fichier sur Kaggle et vérifier les noms de colonnes et des éditeurs.
- [ ] Compter les observations complètes après le filtre (années 2000 et suivantes, note des critiques renseignée).
- [ ] Faire valider la problématique par votre tuteur, en insistant sur l'intégration verticale et les marchés bifaces.
- [ ] Lire Lee (2013) et Corts et Lederman (2009) en premier : ils traitent exactement de cette question.
