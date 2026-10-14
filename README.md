<a id="top"></a>

**🌐 Language / Langue :** [🇬🇧 English](#english) · [🇫🇷 Français](#francais)

---

<a id="english"></a>

# 🌊 Wa-Tor: Shark & Fish Ecosystem Simulation

A Python simulation of **Wa-Tor**, a toroidal ocean world (the grid wraps around on itself) where fish and sharks move, reproduce and eat each other. The project contains the object-oriented simulation logic and a **pygame** graphical interface with smooth animations and visual effects.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![pygame](https://img.shields.io/badge/pygame-2.x-green)

---

## 📖 How the simulation works

The world is a square grid whose edges are connected: an entity leaving on the right reappears on the left, and the same goes for top and bottom. On each turn (a "chronon"), every entity acts once.

| | 🐟 Fish | 🦈 Shark |
|---|---|---|
| **Movement** | To a random empty neighbouring cell (up, down, left, right) | To a neighbouring fish if there is one, otherwise to a random empty cell |
| **Food** | None | Eating a fish gives **+5 energy** (maximum 12) |
| **Energy** | Not applicable | Starts at **8**, loses **1 per turn**, the shark dies at 0 |
| **Reproduction** | A baby appears every **8 turns** | A baby appears every **12 turns** |

Sharks play before fish on each turn. The populations therefore evolve in cycles: too many sharks empty the fish population, then the sharks starve, then the fish repopulate the grid.

---

## 🗂️ Project structure

```
.
├── world.py       # Entry point: World class (simulation management) + interface launch
├── grid.py        # Grid class used by world.py
├── fish.py        # Fish class used by world.py
├── shark.py       # Shark class used by world.py
├── interface.py   # pygame graphical interface 
└── README.md
```

- **`world.py`** creates a `Grid` and a `World`, which randomly places the starting fish and sharks, then launches the interface. `World` handles movements, meals and reproduction. A console mode (turn-by-turn grid display) is present in the file but disabled: the `while w.turn < 0` loop never runs. Set a positive limit to enable it, for example `while w.turn < 50`.
- **`interface.py`** is **standalone**: it contains its own `Fish`, `Shark` and `Grid` classes and runs its own simulation (15×15 grid, starting with 45 fish and 18 sharks). It does not reuse the objects from `world.py`, so you can run it on its own.


```bash
pip install pygame
```

The 🐟 and 🦈 emojis use a system font: Segoe UI Emoji (Windows), Apple Color Emoji (macOS) or Noto Color Emoji (Linux). If you can't see them on Linux, install `fonts-noto-color-emoji`.

---

## ▶️ Running

From `world.py` (simulation + interface):

```bash
python world.py
```

Or the interface alone:

```bash
python interface.py
```

---

## 🎮 Controls

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

## 📚 Further reading

Wa-Tor was devised by A. K. Dewdney and presented in *Scientific American* in 1984. It is a classic example of a predator-prey simulation built on simple rules.

---

## 👥 Team

| Person | Contribution |
|---|---| We all worked together; everyone was responsible for their own file, though sometimes assisted by the others.
| **Matisse Guerguet** | Graphical interface (`interface.py`), fish (`fish.py`), helped on `world.py` and `grid.py` |
| **Jocelyne** | `world.py` and `grid.py` |
| **Romain** | Sharks (`shark.py`), helped on `world.py` and `grid.py` |

<sub>[⬆ Back to top / Retour en haut](#top) · [🇫🇷 Version française](#francais)</sub>

---

<a id="francais"></a>

# 🌊 Wa-Tor : simulation d'écosystème requins / poissons

Simulation en Python de **Wa-Tor**, un monde marin en forme de tore (la grille « boucle » sur elle-même) où des poissons et des requins se déplacent, se reproduisent et se mangent. Le projet contient la logique de simulation en programmation orientée objet et une interface graphique **pygame** avec animations et effets visuels.


---

## 📖 Principe de la simulation

Le monde est une grille carrée dont les bords sont reliés : une entité qui sort à droite réapparaît à gauche, et de même en haut et en bas. À chaque tour (« chronon »), chaque entité agit une fois.

| | 🐟 Poisson | 🦈 Requin |
|---|---|---|
| **Déplacement** | Vers une case voisine vide (haut, bas, gauche, droite), au hasard | Vers un poisson voisin s'il y en a un, sinon vers une case vide, au hasard |
| **Nourriture** | Aucune | Mange un poisson : **+5 énergie** (maximum 12) |
| **Énergie** | Sans objet | Démarre à **8**, perd **1 par tour**, le requin meurt à 0 |
| **Reproduction** | Un petit apparaît tous les **8 tours** | Un petit apparaît tous les **12 tours** |

Les requins jouent avant les poissons à chaque tour. Les proportions de poissons et de requins évoluent donc en cycles : trop de requins vident les poissons, puis les requins meurent de faim, puis les poissons repeuplent la grille.

---

## 🗂️ Structure du projet

```
.
├── world.py       # Point d'entrée : classe World (gestion de la simulation) + lancement de l'interface
├── grid.py        # Classe Grid utilisée par world.py
├── fish.py        # Classe Fish utilisée par world.py
├── shark.py       # Classe Shark utilisée par world.py
├── interface.py   # Interface graphique pygame 
└── README.md
```

- **`world.py`** crée une `Grid` et un `World`, qui place au hasard les poissons et les requins de départ, puis lance l'interface. `World` gère les déplacements, les repas et les reproductions. Un mode console (affichage de la grille tour par tour) est présent dans le fichier mais désactivé : la boucle `while w.turn < 0` ne s'exécute jamais. Mets une limite positive pour l'activer, par exemple `while w.turn < 50`.
- **`interface.py`** est **autonome** : il contient ses propres classes `Fish`, `Shark` et `Grid`, et fait tourner sa propre simulation (grille 15×15, 45 poissons et 18 requins au départ). Il ne réutilise pas les objets de `world.py`. Tu peux donc le lancer seul.

---


```bash
pip install pygame
```

Les émojis 🐟 et 🦈 utilisent une police système : Segoe UI Emoji (Windows), Apple Color Emoji (macOS) ou Noto Color Emoji (Linux). Si tu ne les vois pas sous Linux, installe `fonts-noto-color-emoji`.

---

## ▶️ Lancement

Depuis `world.py` (simulation + interface) :

```bash
python world.py
```

Ou l'interface seule :

```bash
python interface.py
```

---

## 🎮 Commandes

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

## 📚 Pour aller plus loin

Wa-Tor a été imaginé par A. K. Dewdney et présenté dans *Scientific American* en 1984. C'est un exemple classique de simulation proie-prédateur à base de règles simples.

---

## 👥 Équipe

| Personne | Contribution |
|---|nous avont tous travaillé ensemble, chacun était responsable de son fichier, mais parfois aider par les autres 
| **Matisse Guerguet** | Interface graphique (`interface.py`), poissons (`fish.py`), aide sur `world.py` et `grid.py` |
| **Jocelyne** | `world.py` et `grid.py` |
| **Romain** | Requins (`shark.py`), aide sur `world.py` et `grid.py` |


<sub>[⬆ Retour en haut / Back to top](#top) · [🇬🇧 English version](#english)</sub>