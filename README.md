<a id="top"></a>

**🌐 Language / Langue :** [🇬🇧 English](#english) · [🇫🇷 Français](#francais)

---

<a id="english"></a>

# 🌊 Wa-Tor: Shark & Fish Ecosystem Simulation

A Python simulation of **Wa-Tor**, a toroidal ocean world (the grid wraps around on itself) where fish and sharks move, reproduce and eat each other. The project contains the object-oriented simulation logic, a **console version** launched by `Main.py`, and a **pygame** graphical version launched by `interface.py`, with smooth animations and visual effects.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![pygame](https://img.shields.io/badge/pygame-2.x-green)

---

## 📖 How the simulation works

The world is a square grid whose edges are connected: an entity leaving on the right reappears on the left, and the same goes for top and bottom. On each turn (a "chronon"), every entity acts once.

| | 🐟 Fish | 🦈 Shark |
|---|---|---|
| **Movement** | To a random empty neighbouring cell (up, down, left, right) | To a neighbouring fish if there is one, otherwise to a random empty cell |
| **Food** | None | Eating a fish gives **+7 energy** (maximum 16) |
| **Energy** | Not applicable | Starts at **16**, loses **1 per turn**, the shark dies at 0 |
| **Reproduction** | A baby appears every **8 turns** | A baby appears every **12 turns** |

Sharks play before fish on each turn. The populations therefore evolve in cycles: too many sharks empty the fish population, then the sharks starve, then the fish repopulate the grid.

---

## 🗂️ Project structure

```
.
├── main.py              # Entry point: launches the simulation in the console
├── interface.py         # Launches the graphical version of the simulation (pygame)
├── config.ini           # File with principal var
├── requierement.txt     # Python dependencies
├── classes/
│   ├── world.py         # World class (simulation management)
│   ├── grid.py          # Grid class used by world.py
│   ├── fish.py          # Fish class used by world.py
│   └── shark.py         # Shark class used by world.py
└── README.md
```

- **`Main.py`** launches the simulation in the console (turn-by-turn grid display). It creates a `Grid` and a `World`, which randomly places the starting fish and sharks.
- **`world.py`** contains the `World` class, which handles movements, meals and reproduction.
- **`interface.py`** launches the **graphical version** of the simulation. 
---

## ⚙️ Installation

```bash
pip install pygame-ce 
```
Or
```bash
pip install -r requirements.txt 
```

`pygame` is only needed for the graphical version (`interface.py`). The console version (`Main.py`) does not need it.

The 🐟 and 🦈 emojis use a system font: Segoe UI Emoji (Windows), Apple Color Emoji (macOS) or Noto Color Emoji (Linux). If you can't see them on Linux, install `fonts-noto-color-emoji`.

---

## ▶️ Running

Console version (`Main.py`):

```bash
python Main.py
```

Graphical version (`interface.py`):

```bash
python interface.py
```

---

## 🎮 Controls

These controls apply to the graphical version (`interface.py`).

| Key | Action |
|---|---|
| `Space` | Pause / resume (animations and effects freeze too) |
| `↑` | Speed up the simulation |
| `↓` | Slow down the simulation |
| `E` | Toggle visual effects on/off |
| `F11` | Toggle fullscreen / window |
| `Esc` | Quit |

---

## 🖥️ Interface

- **Game window**: the 15×15 grid, with a sea animated by waves.
- **Shark energy**: a badge at the bottom right of each shark shows its energy (red when it is 3 or lower).
- **Dashboard**: turn number, fish and shark populations, simulation speed, prey and predator density, FPS and a reminder of the controls.
- **Smooth movement**: each entity glides from one cell to the next instead of jumping, including when it crosses a grid edge. Eaten fish and dead sharks fade out.
- **Visual effects** (decorative only, they never affect the simulation):
  - a sailboat crossing the sea with a V-shaped foam wake;
  - rising bubbles;
  - sun glints;
  - drifting cloud shadows;
  - ripples in the water where a fish is eaten (pinkish when a shark starves).
- **Performance**: emojis, sea tiles, energy badges and dashboard elements are pre-rendered or cached, and the frame rate is capped.

---

## 🔧 Settings

All values are at the top of `interface.py`, except `logic_delay`.

| Constant | Purpose | Default |
|---|---|---|
| `CELL_SIZE` | Cell size in pixels | `50` |
| `GRID_SIZE` | Number of cells per side | `15` |
| `TARGET_FPS` | Frame rate cap | `60` |
| `EMOJI_RATIO` | Emoji size relative to a cell | `0.6` |
| `START_FULLSCREEN` | Start in fullscreen | `True` |
| `logic_delay` (in `launch_interface`) | Number of frames between two turns: the higher it is, the slower the simulation | `14` |

With `TARGET_FPS = 60` and `logic_delay = 14`, the simulation advances about 4 turns per second. If you change `TARGET_FPS`, also replace the `60` in `60//logic_delay` in the dashboard so the displayed speed stays correct.

---

## 🧠 Technical notes

- The grid is a **torus**: neighbours are computed with a modulo on the grid size.
- The simulation **logic** (turns, movement, meals, reproduction) is separate from the **display**: animations and effects only read the grid state and never modify it.
- For the animation, each entity remembers its cell at the start of the turn, and the display interpolates between that cell and the current one according to how far the turn has progressed.

---

## 👥 Team

We all worked together; everyone was responsible for their own file, though sometimes assisted by the others.

| Person | Contribution |
|---|---|
| **Matisse** | Graphical interface (`interface.py`) and fish (`fish.py`); helped on `world.py` and `grid.py`; also wrote the README |
| **Romain** | Sharks (`shark.py`); helped on `world.py` and `grid.py` |
| **Jocelyne** | `world.py`, `grid.py` and `config.ini`; helped on fish (`fish.py`) and sharks (`shark.py`) |

<sub>[⬆ Back to top / Retour en haut](#top) · [🇫🇷 Version française](#francais)</sub>

---

<a id="francais"></a>

# 🌊 Wa-Tor : simulation d'écosystème requins / poissons

Simulation en Python de **Wa-Tor**, un monde marin en forme de tore (la grille « boucle » sur elle-même) où des poissons et des requins se déplacent, se reproduisent et se mangent. Le projet contient la logique de simulation en programmation orientée objet, une **version console** lancée par `Main.py` et une version graphique **pygame** lancée par `interface.py`, avec animations et effets visuels.


---

## 📖 Principe de la simulation

Le monde est une grille carrée dont les bords sont reliés : une entité qui sort à droite réapparaît à gauche, et de même en haut et en bas. À chaque tour (« chronon »), chaque entité agit une fois.

| | 🐟 Poisson | 🦈 Requin |
|---|---|---|
| **Déplacement** | Vers une case voisine vide (haut, bas, gauche, droite), au hasard | Vers un poisson voisin s'il y en a un, sinon vers une case vide, au hasard |
| **Nourriture** | Aucune | Mange un poisson : **+7 énergie** (maximum 16) |
| **Énergie** | Sans objet | Démarre à **16**, perd **1 par tour**, le requin meurt à 0 |
| **Reproduction** | Un petit apparaît tous les **8 tours** | Un petit apparaît tous les **12 tours** |

Les requins jouent avant les poissons à chaque tour. Les proportions de poissons et de requins évoluent donc en cycles : trop de requins vident les poissons, puis les requins meurent de faim, puis les poissons repeuplent la grille.

---

## 🗂️ Structure du projet

```
.
├── main.py              # Point d'entrée : lance la simulation dans la console
├── interface.py         # Lance la version graphique de la simulation (pygame)
├── config.ini           # Fichier avec les variables principales
├── requierement.txt     # Dépendances Python
├── classes/
│   ├── world.py         # Classe World (gestion de la simulation)
│   ├── grid.py          # Classe Grid utilisée par world.py
│   ├── fish.py          # Classe Fish utilisée par world.py
│   └── shark.py         # Classe Shark utilisée par world.py
└── README.md
```

- **`Main.py`** lance la simulation dans la console (affichage de la grille tour par tour). Il crée une `Grid` et un `World`, qui place au hasard les poissons et les requins de départ.
- **`world.py`** contient la classe `World`, qui gère les déplacements, les repas et les reproductions.
- **`interface.py`** lance la **version graphique** de la simulation. 

---

## ⚙️ Installation

```bash
pip install pygame-ce 
```
Ou
```bash
pip install -r requirements.txt 
```

`pygame` n'est nécessaire que pour la version graphique (`interface.py`). La version console (`Main.py`) n'en a pas besoin.

Les émojis 🐟 et 🦈 utilisent une police système : Segoe UI Emoji (Windows), Apple Color Emoji (macOS) ou Noto Color Emoji (Linux). Si tu ne les vois pas sous Linux, installe `fonts-noto-color-emoji`.

---

## ▶️ Lancement

Version console (`Main.py`) :

```bash
python Main.py
```

Version graphique (`interface.py`) :

```bash
python interface.py
```

---

## 🎮 Commandes

Ces commandes s'appliquent à la version graphique (`interface.py`).

| Touche | Action |
|---|---|
| `Espace` | Pause / reprise (les animations et les effets se figent aussi) |
| `↑` | Accélérer la simulation |
| `↓` | Ralentir la simulation |
| `E` | Activer / désactiver les effets visuels |
| `F11` | Plein écran / fenêtre |
| `Échap` | Quitter |

---

## 🖥️ Interface

- **Fenêtre de jeu** : la grille de 15×15 cases, avec une mer animée par des vagues.
- **Énergie des requins** : une pastille en bas à droite de chaque requin affiche son énergie (rouge quand elle est à 3 ou moins).
- **Tableau de bord** : numéro du tour, populations de poissons et de requins, vitesse de la simulation, densité de proies et de prédateurs, FPS et rappel des touches.
- **Déplacements fluides** : chaque entité glisse d'une case à l'autre au lieu de sauter, y compris quand elle traverse un bord de la grille. Les poissons mangés et les requins morts disparaissent en fondu.
- **Effets visuels** (décoratifs, sans effet sur la simulation) :
  - un voilier qui traverse la mer avec un sillage d'écume en V ;
  - des bulles qui remontent ;
  - des reflets du soleil ;
  - des ombres de nuages qui dérivent ;
  - des ondes dans l'eau là où un poisson est mangé (rosées quand un requin meurt de faim).
- **Performance** : émojis, cases de mer, bulles d'énergie et éléments du tableau de bord sont pré-rendus ou mis en cache, et les FPS sont limités.

---

## 🔧 Réglages

Toutes les valeurs sont en haut de `interface.py`, sauf `logic_delay`.

| Constante | Rôle | Valeur par défaut |
|---|---|---|
| `CELL_SIZE` | Taille d'une case en pixels | `50` |
| `GRID_SIZE` | Nombre de cases par côté | `15` |
| `TARGET_FPS` | Limite d'images par seconde | `60` |
| `EMOJI_RATIO` | Taille des émojis par rapport à une case | `0.6` |
| `START_FULLSCREEN` | Démarrer en plein écran | `True` |
| `logic_delay` (dans `launch_interface`) | Nombre d'images entre deux tours : plus il est grand, plus la simulation est lente | `14` |

Avec `TARGET_FPS = 60` et `logic_delay = 14`, la simulation avance d'environ 4 tours par seconde. Si tu changes `TARGET_FPS`, remplace aussi le `60` dans `60//logic_delay` du tableau de bord pour que la vitesse affichée reste juste.

---

## 🧠 Notes techniques

- La grille est un **tore** : les voisins sont calculés avec un modulo sur la taille de la grille.
- La **logique** de la simulation (tours, déplacements, repas, reproductions) est séparée de l'**affichage** : les animations et les effets ne lisent que l'état de la grille et ne le modifient jamais.
- Pour l'animation, chaque entité mémorise sa case au début du tour et l'affichage interpole entre cette case et la case actuelle selon l'avancement du tour.

---

## 👥 Équipe

Nous avons tous travaillé ensemble, chacun était responsable de son fichier, mais parfois aidé par les autres.

| Personne | Contribution |
|---|---|
| **Matisse** | Interface graphique (`interface.py`) et poissons (`fish.py`) ; aide sur `world.py` et `grid.py` ; a aussi rédigé le README |
| **Romain** | Requins (`shark.py`) ; aide sur `world.py` et `grid.py` |
| **Jocelyne** | `world.py`, `grid.py` et `config.ini` ; aide sur les poissons (`fish.py`) et les requins (`shark.py`) |


<sub>[⬆ Retour en haut / Back to top](#top) · [🇬🇧 English version](#english)</sub>