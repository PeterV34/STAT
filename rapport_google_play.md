# Applications Google Play – Mini-rapport de projet PEA

*8 octobre 2026*

## Où trouver la base

**Kaggle : « Google Play Store Apps »**, auteur Gautham Prakash (gauthamp10).
Lien : https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps

- Fichier : `Google-Playstore.csv`, environ 2,3 millions d'applications et 24 colonnes, collecté en juin 2021.
- Pour télécharger : créer un compte Kaggle gratuit, puis bouton « Download ». Le fichier fait plusieurs centaines de Mo : R le lit sans problème, Excel non.
- Source d'origine à citer : données collectées sur le Google Play Store, mises en ligne sur Kaggle sous licence ouverte.

**Base de secours** (plus petite, mais plus de nettoyage) : Kaggle « Google Play Store Apps » de lava18, environ 10 000 applications (2018). Le prix et les installations y sont du texte (« $4.99 », « 10,000+ ») à convertir.

> Je n'ai pas pu ouvrir Kaggle depuis mon environnement. Les noms de colonnes ci-dessous sont à vérifier avec `names()`.

## Problématique

**Titre :** *Gratuit, gratuit avec publicité ou payant : les déterminants du succès des applications sur le Google Play Store.*

**Question :** sur une plateforme numérique, quel modèle économique (payant, publicité, achats intégrés) attire le plus d'utilisateurs, et quel est le poids de la plateforme elle-même (mise en avant par Google) ?

**Adéquation à la consigne :**

| Critère du PEA | Cette base |
| --- | --- |
| Thème économie industrielle | Marchés bifaces, tarification, pouvoir des plateformes |
| ≥ 500 observations | Environ 2,3 millions (on peut garder un sous-échantillon) |
| Y continue | Nombre d'installations (en logarithme) |
| Plusieurs X sans transformation lourde | 10 X, dont 8 en colonnes brutes |

## Lien avec l'organisation industrielle

| Mécanisme | Ce que prédit la théorie | Hypothèse |
| --- | --- | --- |
| Marchés bifaces | Une plateforme fait payer le côté le moins sensible au prix (les annonceurs) et subventionne l'autre (les utilisateurs) | H1 : applications financées par la publicité → plus d'installations |
| Élasticité-prix et biens numériques | Avec un coût marginal nul, un prix positif réduit fortement la demande | H2 : application payante → beaucoup moins d'installations |
| Discrimination par les prix (freemium) | Les achats intégrés font payer les utilisateurs les plus intéressés, sans exclure les autres | H3 : achats intégrés → plus d'installations |
| Pouvoir de la plateforme | Google, qui contrôle l'accès aux utilisateurs, oriente la demande par ses sélections | H4 : « Editors' Choice » → beaucoup plus d'installations |
| Réputation et information | La note sert de signal de qualité aux consommateurs | H5 : meilleure note → plus d'installations |
| Économies de gamme | Un développeur qui a beaucoup d'applications profite de sa visibilité et de son expérience | H6 : grand portefeuille → plus d'installations |

## Variables

| Rôle | Variable | Colonne | Transformation |
| --- | --- | --- | --- |
| Y | Nombre d'installations | `Maximum Installs` | Logarithme |
| X1 | Application payante | `Free` | Indicatrice (FALSE = payante) |
| X2 | Prix ($) | `Price` | Aucune |
| X3 | Financée par la publicité | `Ad Supported` | Aucune (TRUE/FALSE) |
| X4 | Achats intégrés | `In App Purchases` | Aucune (TRUE/FALSE) |
| X5 | Sélection « Editors' Choice » | `Editors Choice` | Aucune (TRUE/FALSE) |
| X6 | Note moyenne (1 à 5) | `Rating` | Aucune |
| X7 | Catégorie (jeux, éducation…) | `Category` | Indicatrices automatiques |
| X8 | Public visé | `Content Rating` | Indicatrices automatiques |
| X9 | Taille du portefeuille du développeur | `Developer Id` | Nombre d'applications par développeur (1 ligne) |
| X10 | Âge de l'application (années) | `Released` | 2021 − année de sortie (1 ligne) |

## Code R

```r
gp <- read.csv("Google-Playstore.csv")
names(gp)

gp <- subset(gp, Rating.Count >= 10)          # garder les applications notées au moins 10 fois
gp$nb_apps_dev <- ave(gp$Rating, gp$Developer.Id, FUN = length)
gp$age         <- 2021 - as.numeric(substr(gp$Released, nchar(gp$Released) - 3, nchar(gp$Released)))

modele <- lm(log(Maximum.Installs + 1) ~ Free + Price + Ad.Supported + In.App.Purchases +
               Editors.Choice + Rating + factor(Category) + factor(Content.Rating) +
               log(nb_apps_dev) + age, data = gp)
summary(modele)
```

Le format de la date (`Released`, du type « Feb 26, 2020 ») est à vérifier : la ligne `age` extrait les 4 derniers caractères, c'est-à-dire l'année.

## Statistiques descriptives à présenter

1. Répartition des applications : gratuites/payantes, avec/sans publicité, avec/sans achats intégrés.
2. Installations médianes selon le modèle économique (payant, publicité, achats intégrés, aucun).
3. Installations moyennes des applications « Editors' Choice » contre les autres.
4. Nuage de points du log des installations contre la note.
5. Prix moyen des applications payantes par catégorie.

## Littérature à mobiliser

À vérifier avant de citer.

- Rochet, J.-C. et Tirole, J. (2003), « Platform Competition in Two-Sided Markets », *Journal of the European Economic Association*.
- Armstrong, M. (2006), « Competition in Two-Sided Markets », *RAND Journal of Economics*.
- Ghose, A. et Han, S. P. (2014), « Estimating Demand for Mobile Applications in the New Economy », *Management Science*.
- Liu, C. Z., Au, Y. A. et Choi, H. S. (2014), « Effects of Freemium Strategy in the Mobile App Market: An Empirical Study of Google Play », *Journal of Management Information Systems*.

## Limites à discuter

- **Causalité inversée :** une application très installée reçoit plus de notes et a plus de chances d'être sélectionnée par Google.
- **Installations estimées :** `Maximum Installs` est une estimation, pas un chiffre exact.
- **Biais de survie :** seules les applications encore en ligne en 2021 sont observées.
- **Pas de revenus :** on mesure le succès en installations, pas en chiffre d'affaires.

## Prochaines étapes

- [ ] Télécharger le fichier sur Kaggle et vérifier les noms de colonnes.
- [ ] Choisir le filtre (au moins 10 notes, ou une seule catégorie) et compter les observations.
- [ ] Faire valider la problématique par votre tuteur, en insistant sur les marchés bifaces.
- [ ] Lire Rochet et Tirole (2003) et Liu, Au et Choi (2014) en premier.
