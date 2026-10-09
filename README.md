# 🦈 Wa-Tor 🐟

**Simulation proies / prédateurs · Predator / prey simulation**


[🇬🇧 English](#-english) · [🇫🇷 Français](#-français)



---

## 🇬🇧 English

> Ecosystem simulation in Python (object-oriented programming): fish and sharks live on a toroidal world, where the edges wrap around.

### 🌊 How it works

| | Creature | Behaviour |
|---|---|---|
| 🐟 | **Fish** | Moves to a free neighbouring cell and reproduces after `fish_reproduction_time` cycles. |
| 🦈 | **Shark** *(inherits from Fish)* | Eats neighbouring fish to regain energy, loses energy every cycle, dies at 0 and reproduces after `shark_reproduction_time` cycles. |
| 🧱 | **Grid** | The `width` x `height` toroidal grid that stores the cells. |
| 🌍 | **World** | Runs the simulation and updates every creature at each cycle. |

### 📁 Files

| File | Content |
|---|---|
| `world.py` | World class |
| `grid.py` | Grid class |
| `fish.py` | Fish class |
| `shark.py` | Shark class |

### ▶️ Running

Run the main file `world.py` with Python.


### 👥 Members

| Member | Contribution |
|---|---|
| **Matisse** | fish class & help for grid and world |
| **Romain** | shark class & help for grid and world |
| **Joyceline** | world & grid |

---

## 🇫🇷 Français

> Simulation d'écosystème en Python (programmation orientée objet) : des poissons et des requins évoluent dans un monde torique, dont les bords sont reliés entre eux.

### 🌊 Fonctionnement

| | Créature | Comportement |
|---|---|---|
| 🐟 | **Poisson** (fish) | Se déplace sur une case voisine libre et se reproduit après `fish_reproduction_time` cycles. |
| 🦈 | **Requin** (shark, hérite de Poisson) | Mange les poissons voisins pour regagner de l'énergie, perd de l'énergie à chaque cycle, meurt à 0 et se reproduit après `shark_reproduction_time` cycles. |
| 🧱 | **Grille** (grid) | La grille torique de `width` x `height` qui stocke les cases. |
| 🌍 | **Monde** (world) | Lance la simulation et met à jour chaque créature à chaque cycle. |

### 📁 Fichiers

| Fichier | Contenu |
|---|---|
| `world.py` | classe World |
| `grid.py` | classe Grid |
| `fish.py` | classe Fish |
| `shark.py` | classe Shark |

### ▶️ Exécution

Lancer le fichier principal `world.py` avec Python.

### 👥 Membres

| Membre | Contribution |
|---|---|
| **Matisse** | classe fish et aide pour grid et world |
| **Romain** | classe shark et aide pour grid et world |
| **Joyceline** | world et grid |