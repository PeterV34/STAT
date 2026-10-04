# =====================================================================
#  S&P 500 Companies with Financial Information
#  Source : datahub.io (core/s-and-p-500-companies-financials),
#           données financières issues de Yahoo Finance
#  Problématique : les valorisations boursières (P/E, P/B) dépendent-elles
#  du secteur, de la taille de l'entreprise et de sa politique de dividende ?
# =====================================================================

url <- "https://datahub.io/core/s-and-p-500-companies-financials/_r/-/data/constituents-financials.csv"
# Miroir GitHub du même fichier, si datahub ne répond pas
url_github <- "https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/main/data/constituents-financials.csv"

sp <- tryCatch(read.csv(url), error = function(e) read.csv(url_github))

# ---- 1. Structure ----------------------------------------------------
dim(sp)
names(sp)      # vérifiez les noms de colonnes
summary(sp)    # la sortie demandée pour le dépôt

# ---- 2. Individus complets / incomplets ------------------------------
n_complets   <- sum(complete.cases(sp))
n_incomplets <- sum(!complete.cases(sp))
cat("Individus complets   :", n_complets, "\n")
cat("Individus incomplets :", n_incomplets, "\n")
colSums(is.na(sp))   # valeurs manquantes par variable

# ---- 3. Variables qualitatives construites ---------------------------
# 3a. Secteur : la colonne `Sector` contient en réalité la sous-industrie
#     GICS (127 modalités). On la regroupe dans les 11 secteurs GICS.
gics <- list(
  "Communication Services" = c("Advertising", "Broadcasting", "Cable & Satellite",
    "Integrated Telecommunication Services", "Interactive Home Entertainment",
    "Interactive Media & Services", "Movies & Entertainment", "Publishing",
    "Wireless Telecommunication Services"),
  "Consumer Discretionary" = c("Apparel Retail", "Apparel, Accessories & Luxury Goods",
    "Automobile Manufacturers", "Automotive Parts & Equipment", "Automotive Retail",
    "Broadline Retail", "Casinos & Gaming", "Computer & Electronics Retail",
    "Consumer Electronics", "Distributors", "Footwear", "Home Furnishings",
    "Home Improvement Retail", "Homebuilding", "Hotels, Resorts & Cruise Lines",
    "Leisure Products", "Other Specialty Retail", "Restaurants"),
  "Consumer Staples" = c("Agricultural Products & Services", "Brewers",
    "Consumer Staples Merchandise Retail", "Distillers & Vintners", "Drug Retail",
    "Food Distributors", "Food Retail", "Household Products", "Packaged Foods & Meats",
    "Personal Care Products", "Soft Drinks & Non-alcoholic Beverages", "Tobacco"),
  "Energy" = c("Integrated Oil & Gas", "Oil & Gas Equipment & Services",
    "Oil & Gas Exploration & Production", "Oil & Gas Refining & Marketing",
    "Oil & Gas Storage & Transportation"),
  "Financials" = c("Asset Management & Custody Banks", "Consumer Finance",
    "Diversified Banks", "Financial Exchanges & Data", "Insurance Brokers",
    "Investment Banking & Brokerage", "Life & Health Insurance", "Multi-Sector Holdings",
    "Multi-line Insurance", "Property & Casualty Insurance", "Regional Banks",
    "Reinsurance", "Transaction & Payment Processing Services"),
  "Health Care" = c("Biotechnology", "Health Care Distributors", "Health Care Equipment",
    "Health Care Facilities", "Health Care Services", "Health Care Supplies",
    "Health Care Technology", "Life Sciences Tools & Services", "Managed Health Care",
    "Pharmaceuticals"),
  "Industrials" = c("Aerospace & Defense", "Agricultural & Farm Machinery",
    "Air Freight & Logistics", "Building Products", "Cargo Ground Transportation",
    "Construction & Engineering",
    "Construction Machinery & Heavy Transportation Equipment",
    "Data Processing & Outsourced Services", "Diversified Support Services",
    "Electrical Components & Equipment", "Environmental & Facilities Services",
    "Heavy Electrical Equipment", "Human Resource & Employment Services",
    "Industrial Conglomerates", "Industrial Machinery & Supplies & Components",
    "Passenger Airlines", "Passenger Ground Transportation", "Rail Transportation",
    "Research & Consulting Services", "Trading Companies & Distributors"),
  "Information Technology" = c("Application Software", "Communications Equipment",
    "Electronic Components", "Electronic Equipment & Instruments",
    "Electronic Manufacturing Services", "Internet Services & Infrastructure",
    "IT Consulting & Other Services", "Semiconductor Materials & Equipment",
    "Semiconductors", "Systems Software", "Technology Distributors",
    "Technology Hardware, Storage & Peripherals"),
  "Materials" = c("Commodity Chemicals", "Construction Materials", "Copper",
    "Fertilizers & Agricultural Chemicals", "Gold", "Industrial Gases",
    "Metal, Glass & Plastic Containers",
    "Paper & Plastic Packaging Products & Materials", "Specialty Chemicals", "Steel"),
  "Real Estate" = c("Data Center REITs", "Health Care REITs", "Hotel & Resort REITs",
    "Industrial REITs", "Multi-Family Residential REITs", "Office REITs",
    "Other Specialized REITs", "Real Estate Services", "Retail REITs",
    "Self-Storage REITs", "Single-Family Residential REITs", "Telecom Tower REITs",
    "Timber REITs"),
  "Utilities" = c("Electric Utilities", "Gas Utilities",
    "Independent Power Producers & Energy Traders", "Multi-Utilities",
    "Water Utilities")
)
correspondance <- setNames(rep(names(gics), lengths(gics)), unlist(gics))
sp$Secteur <- factor(correspondance[sp$Sector])
cat("Sous-industries non classées :", sum(is.na(sp$Secteur)), "\n")
table(sp$Secteur)

# 3b. Dividende : oui si Dividend Yield > 0. Le fichier ne contient aucun 0 :
#     une entreprise sans dividende a un rendement manquant (NA). On code donc
#     NA -> "non", sauf pour les 17 entreprises sans aucune donnée Yahoo.
sans_donnees <- is.na(sp$Price)
sp$Dividende <- factor(ifelse(!is.na(sp$Dividend.Yield) & sp$Dividend.Yield > 0,
                              "oui", "non"), levels = c("non", "oui"))
sp$Dividende[sans_donnees] <- NA
table(sp$Dividende, useNA = "ifany")

# 3c. Taille : terciles de la capitalisation (variable ordinale)
sp$Taille <- cut(sp$Market.Cap,
                 breaks = quantile(sp$Market.Cap, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE),
                 labels = c("petite", "moyenne", "grande"),
                 include.lowest = TRUE, ordered_result = TRUE)
quantile(sp$Market.Cap, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE) / 1e9   # en milliards $
table(sp$Taille, useNA = "ifany")

# 3d. Proximité du plus haut annuel : Price > 90 % du 52 Week High
sp$ProcheHaut <- factor(ifelse(sp$Price > 0.9 * sp$X52.Week.High, "oui", "non"),
                        levels = c("non", "oui"))
table(sp$ProcheHaut, useNA = "ifany")

# ---- 4. Résumé des variables d'étude ---------------------------------
summary(sp[, c("Price", "Price.Earnings", "Earnings.Share", "Dividend.Yield",
               "Market.Cap", "EBITDA", "Price.Sales", "Price.Book",
               "Secteur", "Dividende", "Taille", "ProcheHaut")])
