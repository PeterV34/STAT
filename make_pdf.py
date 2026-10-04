"""Génère le PDF de dépôt (resume_sp500.pdf) à partir de sortie_console.txt."""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = Path(__file__).parent
FONTS = Path("/usr/share/fonts/truetype")
pdfmetrics.registerFont(TTFont("Sans", FONTS / "liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTS / "liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONTS / "liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTS / "dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic")

INK = colors.HexColor("#1f2933")
ACCENT = colors.HexColor("#1d4e89")
MUTED = colors.HexColor("#5f6b7a")
RULE = colors.HexColor("#d5dbe3")
SHADE = colors.HexColor("#f3f5f8")

body = ParagraphStyle("body", fontName="Sans", fontSize=9.5, leading=13, textColor=INK)
small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=11)
cell = ParagraphStyle("cell", parent=body, fontSize=8.3, leading=10.5)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Sans-Bold")
h1 = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=17, leading=21, textColor=INK)
sub = ParagraphStyle("sub", parent=body, textColor=MUTED, fontSize=9.5)
h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11.5, leading=15, textColor=ACCENT,
                    spaceBefore=10, spaceAfter=4)
mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.6, leading=8.2, textColor=INK)

# ---- Données extraites de la sortie console --------------------------------
console = (ROOT / "sortie_console.txt").read_text(encoding="utf-8")
m = re.search(r"^> summary\(sp\)\n(.*?)\n\n> n_complets", console, re.S | re.M)
summary_sp = m.group(1).rstrip()
n_ok = int(re.search(r"Individus complets\s*:\s*(\d+)", console).group(1))
n_ko = int(re.search(r"Individus incomplets\s*:\s*(\d+)", console).group(1))
n = n_ok + n_ko


def table(rows, widths, header=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), SHADE),
                  ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT)]
    t.setStyle(TableStyle(style))
    return t


def P(text, st=cell):
    return Paragraph(text, st)


story = []
story += [
    Paragraph("Valorisations boursières du S&amp;P 500", h1),
    Spacer(1, 2),
    Paragraph("Dépôt de jeu de données — description et premier résumé statistique (R)", sub),
    Spacer(1, 8),
]

# ---- Chiffres clés ---------------------------------------------------------
kpi = Table(
    [[P(f"<font size=16><b>{n}</b></font><br/>entreprises", cell),
      P(f"<font size=16><b>{n_ok}</b></font><br/>individus complets", cell),
      P(f"<font size=16><b>{n_ko}</b></font><br/>individus incomplets", cell),
      P("<font size=16><b>8 + 4</b></font><br/>variables quanti. + quali.", cell)]],
    colWidths=[4.25 * cm] * 4)
kpi.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SHADE),
    ("LINEBEFORE", (1, 0), (-1, -1), 0.6, colors.white),
    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
]))
story += [kpi]

# ---- Source ----------------------------------------------------------------
story += [Paragraph("1. Source", h2), Paragraph(
    "Jeu de données public <b>« S&amp;P 500 Companies with Financial Information »</b>, "
    "publié sur <b>datahub.io</b> (core/s-and-p-500-companies-financials) et sur GitHub "
    "(datasets/s-and-p-500-companies-financials). Les données financières proviennent de "
    "<b>Yahoo Finance</b>. Une ligne correspond à une entreprise de l'indice. "
    "Chargement direct dans R avec <font name='Mono' size=8>read.csv(url)</font>. "
    "Capitalisation et EBITDA sont exprimés en dollars bruts.", body)]

# ---- Problématique ---------------------------------------------------------
story += [Paragraph("2. Problématique", h2), Paragraph(
    "<i>Les valorisations boursières (P/E, P/B) dépendent-elles du secteur, de la taille de "
    "l'entreprise et de sa politique de dividende ?</i> Le fichier ne contient pas de "
    "rendements boursiers : l'étude porte donc sur les niveaux de valorisation, et non sur "
    "le couple rendement/risque.", body)]

# ---- Individus -------------------------------------------------------------
story += [Paragraph("3. Individus complets et incomplets", h2), Paragraph(
    f"<font name='Mono' size=8>sum(complete.cases(sp))</font> donne <b>{n_ok} individus "
    f"complets</b> sur {n}, soit <b>{n_ko} individus incomplets</b> "
    f"({n_ko / n:.0%}). Les données manquantes ont trois origines :", body), Spacer(1, 3)]
story += [table([
    [P("Origine", cellb), P("Effet", cellb)],
    [P("17 entreprises sans aucune donnée Yahoo (ex. Ansys, Hess, Marathon Oil, "
       "Discover : sorties de l'indice ou rachetées)"),
     P("Toutes les variables numériques manquantes")],
    [P("87 entreprises qui ne versent pas de dividende (Amazon, Adobe, Boeing…)"),
     P("<font name='Mono' size=7.5>Dividend Yield</font> = NA (le fichier ne contient aucun 0)")],
    [P("Bénéfices ou fonds propres négatifs, données non publiées"),
     P("<font name='Mono' size=7.5>Price/Earnings</font> (45 NA), "
       "<font name='Mono' size=7.5>EBITDA</font> (44), "
       "<font name='Mono' size=7.5>Price/Book</font> (20)")],
], [9.2 * cm, 7.8 * cm])]

# ---- Variables -------------------------------------------------------------
story += [Paragraph("4. Description des variables", h2),
          Paragraph("<b>Variables quantitatives</b> (continues, issues du fichier). "
                    "Dans R, <font name='Mono' size=8>read.csv()</font> remplace "
                    "« / » et les espaces par des points.", body), Spacer(1, 3)]
quanti = [
    ("Price", "Price", "Cours de l'action ($)"),
    ("Price/Earnings", "Price.Earnings", "Ratio cours / bénéfice (P/E) — variable expliquée"),
    ("Price/Book", "Price.Book", "Ratio cours / valeur comptable (P/B) — variable expliquée"),
    ("Earnings/Share", "Earnings.Share", "Bénéfice par action ($), peut être négatif"),
    ("Dividend Yield", "Dividend.Yield", "Rendement du dividende (0,02 = 2 %)"),
    ("Market Cap", "Market.Cap", "Capitalisation boursière ($ bruts)"),
    ("EBITDA", "EBITDA", "Excédent brut d'exploitation ($ bruts), peut être négatif"),
    ("Price/Sales", "Price.Sales", "Ratio cours / chiffre d'affaires"),
]
rows = [[P("Variable", cellb), P("Nom dans R", cellb), P("Signification", cellb)]]
rows += [[P(a), P(f"<font name='Mono' size=7.5>{b}</font>"), P(c)] for a, b, c in quanti]
story += [table(rows, [3.2 * cm, 3.4 * cm, 10.4 * cm])]
story += [Spacer(1, 4), Paragraph(
    "Variables d'identification, non analysées : <font name='Mono' size=8>Symbol</font>, "
    "<font name='Mono' size=8>Name</font>, <font name='Mono' size=8>SEC Filings</font> (lien), "
    "<font name='Mono' size=8>52 Week Low</font> / <font name='Mono' size=8>52 Week High</font> "
    "(servent à construire la proximité du plus haut).", small)]

story += [Spacer(1, 6), Paragraph("<b>Variables qualitatives construites</b>", body),
          Spacer(1, 3)]
quali = [
    [P("Variable", cellb), P("Type", cellb), P("Construction", cellb), P("Modalités (effectifs)", cellb)],
    [P("Secteur"), P("Nominale, 11 mod."),
     P("La colonne <font name='Mono' size=7.5>Sector</font> contient en fait la sous-industrie "
       "GICS (127 valeurs) ; regroupement dans les 11 secteurs GICS"),
     P("Industrials 78, Financials 72, Information Technology 69, Health Care 62, "
       "Consumer Discretionary 50, Consumer Staples 38, Real Estate 31, Utilities 31, "
       "Materials 28, Communication Services 22, Energy 22")],
    [P("Dividende"), P("Binaire"),
     P("oui si <font name='Mono' size=7.5>Dividend Yield &gt; 0</font> ; non si rendement absent"),
     P("oui 399 · non 87 · NA 17")],
    [P("Taille"), P("Ordinale, 3 mod."),
     P("Terciles de <font name='Mono' size=7.5>Market Cap</font> avec "
       "<font name='Mono' size=7.5>cut()</font> et <font name='Mono' size=7.5>quantile()</font> ; "
       "seuils ≈ 23,7 et 71,0 Md$"),
     P("petite 162 · moyenne 162 · grande 162 · NA 17")],
    [P("Proche du plus haut"), P("Binaire"),
     P("oui si <font name='Mono' size=7.5>Price &gt; 0,9 × 52 Week High</font>"),
     P("oui 100 · non 386 · NA 17")],
]
story += [table(quali, [2.6 * cm, 2.3 * cm, 6.0 * cm, 6.1 * cm])]
story += [Spacer(1, 4), Paragraph(
    "Ces variables couvrent les 8 situations de test de liaison : quanti/quanti, quali/quali, "
    "quanti/quali à 2 groupes et à 3 groupes ou plus.", small)]

# ---- summary(sp) -----------------------------------------------------------
pre = Preformatted(summary_sp, mono)
box = Table([[pre]], colWidths=[17 * cm])
box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SHADE),
    ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story += [KeepTogether([Paragraph("5. Sortie de summary(sp)", h2), box])]
story += [Spacer(1, 6), Paragraph(
    "À noter : P/E très asymétrique (médiane 22, moyenne 55, max 9 001) et P/B parfois "
    "négatif (fonds propres négatifs). Des tests non paramétriques ou une transformation "
    "logarithmique seront à envisager.", small)]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, "Source : datahub.io — données Yahoo Finance · Script : sp500_depot.R")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(ROOT / "resume_sp500.pdf"), pagesize=A4,
                        leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.7 * cm, bottomMargin=1.8 * cm,
                        title="Valorisations boursières du S&P 500",
                        author="Dépôt de jeu de données")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("OK")
