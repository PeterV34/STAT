# Uber contre Lyft à Boston – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Kaggle : « Uber and Lyft Dataset Boston, MA »**, auteur brllrb.
Lien : https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma

- Fichier : `rideshare_kaggle.csv`, environ 690 000 courses et 57 colonnes (novembre–décembre 2018, Boston).
- Chaque ligne est un prix proposé pour un trajet entre deux quartiers, à un moment donné, pour une gamme de service, avec la météo du moment.
- Pour télécharger : compte Kaggle gratuit, puis bouton « Download » (environ 400 Mo, à ouvrir avec R).

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes ci-dessous sont à vérifier avec `names()`.

## Problématique

**Titre :** *Concurrence en duopole et tarification dynamique : les déterminants du prix des courses de VTC à Boston.*

**Question :** pour un même trajet et une même gamme de service, Uber et Lyft pratiquent-ils des prix différents ? Et comment les prix réagissent-ils aux chocs de demande (heure de pointe, pluie) ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Duopole, discrimination par les prix, tarification dynamique |
| ≥ 500 observations | Environ 690 000 courses |
| Y continue | Prix de la course ($) |
| Plusieurs X sans transformation lourde | 9 X, dont 8 en colonnes brutes |

## Lien avec l'organisation industrielle

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Concurrence en duopole (Bertrand avec produits différenciés) | Deux firmes proches gardent des prix proches, mais la différenciation (marque, réseau de chauffeurs) permet un écart | H1 : écart de prix Uber/Lyft faible à trajet et gamme identiques |
| Discrimination par les prix (versioning) | La firme propose plusieurs versions (partagé, standard, luxe) pour faire payer chaque client selon sa disposition à payer | H2 : les gammes haut de gamme ont un prix bien supérieur à leur surcoût |
| Tarification de pointe | Quand la demande dépasse l'offre de chauffeurs, le prix augmente pour équilibrer le marché | H3 : `surge_multiplier` > 1 → prix plus élevé |
| Chocs de demande | La pluie et les heures de pointe augmentent la demande | H4 : pluie et heures de pointe → prix plus élevés |
| Tarif en deux parties | Prix = prise en charge fixe + prix au mile, donc l'élasticité du prix à la distance est inférieure à 1 | H5 : coefficient de log(distance) entre 0 et 1 |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Prix de la course ($) | `price` | Logarithme |
| X1 | Entreprise (Uber ou Lyft) | `cab_type` | Indicatrice automatique |
| X2 | Gamme de service | `name` | Regroupée en 4 gammes communes (voir code) |
| X3 | Majoration de pointe | `surge_multiplier` | Aucune |
| X4 | Distance (miles) | `distance` | Logarithme |
| X5 | Heure de la journée | `hour` | Indicatrices automatiques |
| X6 | Intensité de la pluie | `precipIntensity` | Aucune |
| X7 | Température | `temperature` | Aucune |
| X8 | Quartier de départ | `source` | Indicatrices automatiques |
| X9 | Quartier d'arrivée | `destination` | Indicatrices automatiques |

**Regroupement des gammes**, pour comparer les deux entreprises à service égal :

| Gamme | Uber | Lyft |
| --- | --- | --- |
| Partagé | UberPool | Shared |
| Standard | UberX, WAV | Lyft |
| Grand véhicule | UberXL | Lyft XL |
| Luxe | Black, Black SUV | Lux, Lux Black, Lux Black XL |

## Code R

```r
vtc <- read.csv("rideshare_kaggle.csv")
names(vtc)
table(vtc$cab_type, vtc$name)        # vérifier les noms des gammes

vtc <- subset(vtc, !is.na(price))    # le produit "Taxi" d'Uber n'a pas de prix

gammes <- c(UberPool = "Partage", Shared = "Partage",
            UberX = "Standard", WAV = "Standard", Lyft = "Standard",
            UberXL = "Grand", `Lyft XL` = "Grand",
            Black = "Luxe", `Black SUV` = "Luxe", Lux = "Luxe",
            `Lux Black` = "Luxe", `Lux Black XL` = "Luxe")
vtc$gamme <- factor(gammes[vtc$name], levels = c("Standard", "Partage", "Grand", "Luxe"))

modele <- lm(log(price) ~ cab_type * gamme + surge_multiplier + log(distance) +
               factor(hour) + precipIntensity + temperature +
               factor(source) + factor(destination), data = vtc)
summary(modele)
```

Le terme `cab_type * gamme` estime l'écart Uber/Lyft dans chaque gamme. Avec Y en logarithme, un coefficient de 0,05 sur `cab_typeUber` signifie qu'Uber est environ 5 % plus cher que Lyft en gamme standard.

**Avec 690 000 observations, presque tous les coefficients seront significatifs.** Commentez surtout leur taille économique (combien de dollars ou de pourcents), pas seulement les étoiles de significativité.

## Statistiques descriptives à présenter

1. Prix moyen et médian par entreprise et par gamme (tableau 2 × 4).
2. Prix moyen par heure de la journée, une courbe pour Uber et une pour Lyft.
3. Distribution de `surge_multiplier` pour chaque entreprise.
4. Prix moyen par temps sec contre par temps de pluie.
5. Nuage de points du prix contre la distance, par gamme.

## Littérature à mobiliser

À vérifier avant de citer.

- Cohen, P., Hahn, R., Hall, J., Levitt, S. et Metcalfe, R. (2016), « Using Big Data to Estimate Consumer Surplus: The Case of Uber », NBER Working Paper.
- Castillo, J. C. (2023), « Who Benefits from Surge Pricing? », *Econometrica*.
- Hall, J., Kendrick, C. et Nosko, C. (2015), « The Effects of Uber's Surge Pricing: A Case Study », document de travail Uber.
- Varian, H. (1989), « Price Discrimination », *Handbook of Industrial Organization*, vol. 1.
- Manuel : Tirole, J. (1988), *The Theory of Industrial Organization*, MIT Press, pour Bertrand avec produits différenciés et la discrimination par les prix.

## Limites à discuter

- **Prix proposés, pas courses réalisées :** on ne sait pas si le client a accepté le prix.
- **Majoration de pointe :** dans cette base, elle semble ne varier que pour Lyft (à vérifier avec `table(vtc$cab_type, vtc$surge_multiplier)`). Si c'est le cas, H3 ne se teste que sur Lyft, ce qu'il faut dire dans le rapport.
- **Une seule ville, deux mois :** les résultats ne se généralisent pas forcément.
- **Pas de quantités :** on observe les prix mais pas les parts de marché, donc on ne peut pas mesurer le pouvoir de marché directement.

## Prochaines étapes

- [ ] Télécharger le fichier sur Kaggle et vérifier les noms de colonnes et des gammes.
- [ ] Vérifier la distribution de `surge_multiplier` par entreprise.
- [ ] Faire valider la problématique par votre tuteur, en insistant sur le duopole et la discrimination par les prix.
- [ ] Lire Cohen et al. (2016) et Castillo (2023) en premier.
