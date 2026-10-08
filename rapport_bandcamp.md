# Ventes Bandcamp – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Kaggle : « 1,000,000 Bandcamp Sales »**, auteur mathurinache.
Lien : https://www.kaggle.com/datasets/mathurinache/1000000-bandcamp-sales

- Environ 1 million de ventes réelles, collectées en 2020 à partir du flux public des ventes de Bandcamp.
- Une ligne = un achat : article acheté, prix minimum fixé par l'artiste, montant réellement payé, devise, pays de l'acheteur, date et heure.
- Pour télécharger : compte Kaggle gratuit, puis bouton « Download ». Le fichier est lourd : à ouvrir avec R, pas Excel.

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes ci-dessous sont ceux que je connais de cette base : vérifiez-les avec `names()`, ainsi que les dates couvertes.

## Problématique

**Titre :** *Prix libre et discrimination par les prix : les déterminants du paiement volontaire sur Bandcamp.*

**Question :** sur Bandcamp, l'artiste fixe un prix minimum et l'acheteur peut payer plus. Qu'est-ce qui pousse un fan à payer au-delà du prix demandé : le type de produit, le niveau du prix minimum, la notoriété de l'artiste, le pays de l'acheteur ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Stratégie de prix, discrimination par les prix, plateformes, désintermédiation |
| ≥ 500 observations | Environ 1 million d'achats |
| Y continue ou 0/1 | Paiement au-delà du prix (0/1) ou montant du dépassement |
| Plusieurs X sans transformation lourde | 9 X, dont 5 en colonnes brutes |

## Lien avec l'organisation industrielle

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Discrimination par les prix au premier degré | Le prix libre laisse chaque acheteur révéler sa disposition à payer : l'artiste capte une partie du surplus des fans les plus attachés | H1 : une part importante des acheteurs paie plus que le minimum |
| Prix de référence | Le prix minimum sert d'ancre : plus il est élevé, moins l'acheteur ajoute | H2 : prix minimum élevé → probabilité de dépassement plus faible |
| Différenciation des produits | Un vinyle ou un t-shirt est un bien rival et coûteux, un fichier numérique non | H3 : le dépassement diffère entre numérique et physique |
| Vente en lot | Acheter plusieurs articles à la fois modifie la disposition à payer pour chacun | H4 : achats groupés → comportement de paiement différent |
| Notoriété et réputation | Les fans paient plus pour soutenir les petits artistes, ou au contraire pour les stars qu'ils admirent | H5 : effet de la popularité de l'artiste (signe à découvrir) |
| Désintermédiation | Bandcamp met l'artiste en vente directe, sans maison de disques : l'acheteur sait que son argent va à l'artiste | Point de discussion, appuyé sur H1 et H5 |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y (principale) | A payé plus que le prix minimum | `amount_paid`, `item_price` | Indicatrice : `amount_paid > item_price` (1 ligne) |
| Y (alternative) | Montant payé en dollars | `amount_paid_usd` | Logarithme |
| X1 | Type d'article (album, morceau, physique) | `item_type` | Indicatrices automatiques |
| X2 | Prix minimum fixé par l'artiste | `item_price` | Logarithme (+1) |
| X3 | Prix minimum nul (pur prix libre) | `item_price` | Indicatrice (1 ligne) |
| X4 | Nombre d'articles achetés en plus | `addl_count` | Aucune |
| X5 | Popularité de l'artiste | `artist_name` | Nombre de ventes de l'artiste dans la base (1 ligne) |
| X6 | Pays de l'acheteur | `country` | Indicatrices automatiques (garder les 15 premiers pays) |
| X7 | Devise | `currency` | Indicatrices automatiques |
| X8 | Heure de l'achat | `utc_date` | Conversion de la date (1 ligne) |
| X9 | Jour de la semaine | `utc_date` | Conversion de la date (1 ligne) |

**Piste bonus : les « Bandcamp Fridays ».** En 2020, Bandcamp a renoncé à sa commission certains vendredis (le 2 octobre 2020 par exemple), pour que tout l'argent aille aux artistes. Si la base couvre l'un de ces jours, une indicatrice « Bandcamp Friday » permet de tester si les fans paient plus quand la plateforme ne prélève rien. C'est un effet très « organisation industrielle » (commission de la plateforme), à vérifier selon les dates du fichier.

## Code R

```r
bc <- read.csv("1000000-bandcamp-sales.csv")
names(bc)
table(bc$item_type)                                      # a = album, t = morceau, p = physique (à vérifier)

bc$depasse      <- as.integer(bc$amount_paid > bc$item_price)
bc$prix_nul     <- as.integer(bc$item_price == 0)
bc$popularite   <- ave(bc$amount_paid, bc$artist_name, FUN = length)
bc$date         <- as.POSIXct(bc$utc_date, origin = "1970-01-01", tz = "UTC")   # format à vérifier
bc$heure        <- as.numeric(format(bc$date, "%H"))
bc$jour         <- weekdays(bc$date)
top_pays        <- names(sort(table(bc$country), decreasing = TRUE))[1:15]
bc$pays         <- ifelse(bc$country %in% top_pays, bc$country, "Autres")

modele <- lm(depasse ~ factor(item_type) + log(item_price + 1) + prix_nul + addl_count +
               log(popularite) + factor(pays) + factor(currency) + factor(heure) + factor(jour),
             data = bc)
summary(modele)

# Robustesse : modèle logit
logit <- glm(depasse ~ factor(item_type) + log(item_price + 1) + prix_nul + addl_count +
               log(popularite) + factor(pays), data = bc, family = binomial)
summary(logit)
```

Le premier modèle est un modèle de probabilité linéaire : un coefficient de 0,05 signifie 5 points de pourcentage de probabilité de dépassement en plus. **Avec un million d'observations, presque tout sera significatif :** commentez surtout la taille des effets.

## Statistiques descriptives à présenter

1. Part des achats payés au-dessus du prix minimum, par type d'article.
2. Distribution du rapport montant payé / prix minimum (combien de fans paient 1,5 fois, 2 fois le prix…).
3. Taux de dépassement par tranche de prix minimum (0, 1–5 $, 5–10 $, plus de 10 $).
4. Taux de dépassement par pays (15 premiers pays).
5. Taux de dépassement selon la popularité de l'artiste (petits, moyens, gros vendeurs).

## Littérature à mobiliser

À vérifier avant de citer.

- Kim, J.-Y., Natter, M. et Spann, M. (2009), « Pay What You Want: A New Participative Pricing Mechanism », *Journal of Marketing*.
- Regner, T. et Barria, J. A. (2009), « Do Consumers Pay Voluntarily? The Case of Online Music », *Journal of Economic Behavior & Organization* (étude du label en ligne Magnatune, très proche de Bandcamp).
- Gneezy, A., Gneezy, U., Nelson, L. et Brown, A. (2010), « Shared Social Responsibility: A Field Experiment in Pay-What-You-Want Pricing and Charitable Giving », *Science*.
- Varian, H. (1989), « Price Discrimination », *Handbook of Industrial Organization*, vol. 1.
- Waldfogel, J. (2018), *Digital Renaissance: What Data and Economics Tell Us about the Future of Popular Culture*, Princeton University Press (désintermédiation et industrie musicale).

## Limites à discuter

- **Pas d'information sur les acheteurs :** on ne connaît ni leur revenu ni leur fidélité à l'artiste.
- **Popularité mesurée dans la base :** le nombre de ventes sur quelques semaines est une mesure imparfaite de la notoriété.
- **Période courte, en pleine crise du Covid :** les concerts étaient annulés, les fans ont pu payer plus que d'habitude pour soutenir les artistes.
- **Devises :** comparer des prix en devises différentes demande d'utiliser `amount_paid_usd` pour les montants.
- **Sélection :** on n'observe que les achats réalisés, pas les fans qui ont renoncé à acheter.

## Prochaines étapes

- [ ] Télécharger le fichier sur Kaggle et vérifier les noms de colonnes, le codage de `item_type` et les dates couvertes.
- [ ] Vérifier si la période inclut un « Bandcamp Friday ».
- [ ] Faire valider la problématique par votre tuteur, en insistant sur la discrimination par les prix et le rôle de la plateforme.
- [ ] Lire Kim, Natter et Spann (2009) et Regner et Barria (2009) en premier.
