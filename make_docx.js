// Génère depot_sp500.docx (dossier de dépôt Moodle) à partir de sortie_console.txt
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, AlignmentType, LineRuleType, PageBreak, BorderStyle, ShadingType, LevelFormat, Footer, PageNumber,
} = require("docx");

const console_txt = fs.readFileSync(path.join(__dirname, "sortie_console.txt"), "utf8");
const summary = console_txt.match(/^> summary\(sp\)\n([\s\S]*?)\n\n> n_complets/m)[1].replace(/\s+$/, "");
const nOk = +console_txt.match(/Individus complets\s*:\s*(\d+)/)[1];
const nKo = +console_txt.match(/Individus incomplets\s*:\s*(\d+)/)[1];
const n = nOk + nKo;

const FONT = "Calibri";
const MONO = "Courier New";

const p = (runs, opts = {}) =>
  new Paragraph({ spacing: { after: 120, line: 276 }, alignment: AlignmentType.JUSTIFIED, ...opts,
    children: (Array.isArray(runs) ? runs : [runs]).map(r => typeof r === "string" ? new TextRun(r) : r) });
const b = t => new TextRun({ text: t, bold: true });
const i = t => new TextRun({ text: t, italics: true });
const code = t => new TextRun({ text: t, font: MONO, size: 20 });
const bullet = runs => p(runs, { numbering: { reference: "puces", level: 0 }, spacing: { after: 60 } });
const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });

const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows) {
  const total = widths.reduce((a, c) => a + c, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((row, ri) => new TableRow({
      tableHeader: ri === 0,
      children: row.map((txt, ci) => new TableCell({
        borders,
        width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { fill: "D9D9D9", type: ShadingType.CLEAR, color: "auto" } : undefined,
        margins: { top: 40, bottom: 40, left: 90, right: 90 },
        children: [new Paragraph({ children: [new TextRun({ text: txt, bold: ri === 0, size: 20 })] })],
      })),
    })),
  });
}

const children = [
  // En-tête "étudiant"
  p([b("NOM Prénom")], { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
  p("Groupe : ……", { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
  p("Statistiques — Dépôt du jeu de données", { alignment: AlignmentType.LEFT, spacing: { after: 360 } }),

  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: "Présentation du jeu de données", bold: true, size: 32 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
    children: [new TextRun({ text: "Les entreprises du S&P 500 et leurs indicateurs financiers", italics: true, size: 24 })] }),

  h1("1. Source des données"),
  p(["Nous avons choisi le jeu de données public ", i("« S&P 500 Companies with Financial Information »"),
     ", disponible sur le site datahub.io (jeu « core/s-and-p-500-companies-financials ») ainsi que sur GitHub. ",
     "Les données financières proviennent de ", b("Yahoo Finance"), "."]),
  p(["Chaque ligne du fichier correspond à une entreprise de l'indice S&P 500. Le fichier est chargé directement dans R, sans téléchargement manuel :"]),
  p([code('sp <- read.csv("https://datahub.io/core/s-and-p-500-companies-financials/_r/-/data/constituents-financials.csv")')],
    { alignment: AlignmentType.LEFT }),
  p(["Remarque : la capitalisation boursière et l'EBITDA sont donnés en dollars (et non en milliards de dollars)."]),

  h1("2. Problématique"),
  p([b("Les valorisations boursières (P/E, P/B) dépendent-elles du secteur, de la taille de l'entreprise et de sa politique de dividende ?")]),
  p(["Le fichier ne contient pas de rendements boursiers. Nous nous intéressons donc aux niveaux de valorisation des entreprises ",
     "(ratio cours/bénéfice et ratio cours/valeur comptable) plutôt qu'à la relation entre rendement et risque."]),

  h1("3. Individus complets et incomplets"),
  p([`Le fichier contient ${n} entreprises et 14 colonnes. La commande `, code("sum(complete.cases(sp))"),
     ` donne `, b(`${nOk} individus complets`), `, il y a donc `, b(`${nKo} individus incomplets`),
     ` (environ ${Math.round(100 * nKo / n)} %).`]),
  p("En regardant les valeurs manquantes, nous avons identifié trois causes :"),
  bullet(["17 entreprises n'ont aucune donnée financière (par exemple Ansys, Hess ou Discover Financial, qui ont été rachetées ou sont sorties de l'indice) ;"]),
  bullet(["104 entreprises n'ont pas de rendement du dividende : pour 87 d'entre elles, c'est parce qu'elles ne versent pas de dividende (Amazon, Adobe, Boeing…), car le fichier ne contient jamais la valeur 0 ;"]),
  bullet(["certains ratios manquent lorsque le bénéfice ou les capitaux propres sont négatifs (Price/Earnings : 45 NA, EBITDA : 44 NA, Price/Book : 20 NA)."]),

  h1("4. Description des variables"),
  new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4.1 Variables quantitatives")] }),
  p(["Toutes ces variables sont quantitatives continues. Dans R, ", code("read.csv()"),
     " remplace les « / » et les espaces des noms de colonnes par des points."]),
  table([2200, 2000, 4826], [
    ["Variable", "Nom dans R", "Signification"],
    ["Price", "Price", "Cours de l'action (en $)"],
    ["Price/Earnings", "Price.Earnings", "Ratio cours / bénéfice (P/E)"],
    ["Price/Book", "Price.Book", "Ratio cours / valeur comptable (P/B)"],
    ["Earnings/Share", "Earnings.Share", "Bénéfice par action (en $), peut être négatif"],
    ["Dividend Yield", "Dividend.Yield", "Rendement du dividende (0,02 = 2 %)"],
    ["Market Cap", "Market.Cap", "Capitalisation boursière (en $)"],
    ["EBITDA", "EBITDA", "Excédent brut d'exploitation (en $), peut être négatif"],
    ["Price/Sales", "Price.Sales", "Ratio cours / chiffre d'affaires"],
  ]),
  p(""),
  p(["Les autres colonnes servent à identifier les entreprises (Symbol, Name, SEC Filings) ou à construire une variable qualitative (52 Week Low, 52 Week High)."]),

  new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("4.2 Variables qualitatives")] }),
  p("Nous avons construit quatre variables qualitatives à partir du fichier :"),
  table([1700, 1500, 3226, 2600], [
    ["Variable", "Type", "Construction", "Modalités (effectifs)"],
    ["Secteur", "Qualitative nominale", "Regroupement des 127 sous-industries de la colonne Sector dans les 11 secteurs GICS",
      "Industrials (78), Financials (72), Information Technology (69), Health Care (62), Consumer Discretionary (50), Consumer Staples (38), Real Estate (31), Utilities (31), Materials (28), Communication Services (22), Energy (22)"],
    ["Dividende", "Qualitative binaire", "Oui si Dividend Yield > 0, non si le rendement est absent", "oui (399), non (87), NA (17)"],
    ["Taille", "Qualitative ordinale", "Terciles de Market Cap avec cut() et quantile() (seuils : environ 23,7 et 71 milliards $)",
      "petite (162), moyenne (162), grande (162), NA (17)"],
    ["Proche du plus haut", "Qualitative binaire", "Oui si Price > 90 % du 52 Week High", "oui (100), non (386), NA (17)"],
  ]),
  p(""),
  p(["Remarque sur le secteur : contrairement à ce que laisse penser son nom, la colonne ", code("Sector"),
     " contient la sous-industrie (127 modalités, souvent moins de 5 entreprises chacune). Nous l'avons regroupée en 11 secteurs pour avoir des effectifs suffisants."]),
  p(["Avec ces variables, nous pourrons étudier des liaisons quantitative/quantitative, qualitative/qualitative et quantitative/qualitative (à 2 groupes et à 3 groupes ou plus)."]),

  new Paragraph({ children: [new PageBreak()] }),
  h1("5. Sortie de summary(sp)"),
  ...summary.split("\n").map(line => new Paragraph({ keepNext: true, keepLines: true,
    spacing: { after: 0, before: 0, line: 190, lineRule: LineRuleType.EXACT },
    children: [new TextRun({ text: line, font: MONO, size: 15 })] })),
  p("", { spacing: { after: 120 } }),
  p(["On remarque que le P/E est très dissymétrique (médiane 22,3 mais moyenne 55,2 et maximum 9 001) et que le P/B peut être négatif. ",
     "Il faudra en tenir compte dans le choix des tests."]),
];

const doc = new Document({
  creator: "Étudiant",
  title: "Dépôt jeu de données S&P 500",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: "1F3864" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: "2F5496" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "puces", levels: [{ level: 0, format: LevelFormat.BULLET, text: "–",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1134, bottom: 1134, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(path.join(__dirname, "depot_sp500.docx"), buf);
  console.log("OK");
});
