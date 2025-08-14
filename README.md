# 🎯 Bubble Blaster

**Bubble Blaster** is a fast-paced arcade-style shooting game built with **Python** and **PyOpenGL**, where you pilot a tiny spaceship at the bottom of the screen and blast falling bubbles before they hit you.
The game combines precision aiming with quick reflexes — and throws in special red bubbles for bonus points.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [How to Run](#how-to-run)
6. [Gameplay Instructions](#gameplay-instructions)

   * [Controls](#controls)
   * [Objective](#objective)
   * [Special Bubbles](#special-bubbles)
   * [Game Over Conditions](#game-over-conditions)
   * [Scoring](#scoring)
7. [Game Screen Layout](#game-screen-layout)
8. [Development Notes](#development-notes)
9. [Tips and Tricks](#tips-and-tricks)
10. [License](#license)

---

## 📖 Overview

In **Bubble Blaster**, waves of bubbles fall from the top of the screen. You must destroy them by firing bullets from your spaceship before they reach the bottom or collide with you.
Some bubbles are **special red bubbles** that pulse in size — hitting them rewards you with extra points.

Your goal: **Get the highest score possible before the game ends.**

---

## ✨ Features

* 🎯 **Real-time shooting** with smooth animations
* 🔴 **Special bubbles** for bonus points
* 🛑 **Pause, restart, and quit** via on-screen buttons
* 📈 Difficulty scaling — bubbles fall faster as you score higher
* 🖥️ Built with **Midpoint Line** and **Midpoint Circle Drawing Algorithms** for rendering

---

## 🖥️ Requirements

* **Python 3.x**
* **PyOpenGL**
* **PyOpenGL\_accelerate** *(optional, improves performance)*

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bubble-blaster.git
cd bubble-blaster

# Install dependencies
pip install PyOpenGL PyOpenGL_accelerate
```

---

## 🚀 How to Run

```bash
python Bubble_Blaster.py
```

---

## 🎮 Gameplay Instructions

### 🎛️ Controls

| Key / Mouse Action            | Function             |
| ----------------------------- | -------------------- |
| **Spacebar**                  | Fire a bullet upward |
| **A**                         | Move spaceship left  |
| **D**                         | Move spaceship right |
| **Left UI Button (Blue)**     | Restart game         |
| **Right UI Button (Red)**     | Quit game            |
| **Middle UI Button (Orange)** | Pause/Resume game    |

---

### 🎯 Objective

* Destroy falling bubbles **before** they reach your ship or pass the bottom of the screen.
* **Avoid wasting shots** — missed bullets count against you.
* Keep an eye out for **special red bubbles** for bonus points.

---

### 🔴 Special Bubbles

* Appear in **red** and **pulse** in size.
* Worth **5 points** instead of 1.
* Spawn randomly with a **20% chance** after a bubble is destroyed.

---

### 💀 Game Over Conditions

Your game ends when:

1. **3 bubbles** reach the bottom or collide with your spaceship.
2. **3 bullets** miss all bubbles and fly off-screen.

---

### 🏆 Scoring

| Action                 | Points |
| ---------------------- | ------ |
| Destroy normal bubble  | +1     |
| Destroy special bubble | +5     |

---

## 🖼️ Game Screen Layout

```
 -------------------------------------------------
|   [Blue: Restart]   [Orange: Pause]   [Red: Quit]  |
|                                                    |
|              Falling bubbles appear here           |
|                                                    |
|                                                    |
|                                                    |
|                  [Spaceship]                       |
 -------------------------------------------------
```

* **Bubbles** fall from the top at varying positions and speeds.
* Your **spaceship** stays at the bottom and can move left/right.
* UI buttons are at the top for quick control without keyboard.

---

## 🛠️ Development Notes

* Uses **OpenGL.GLUT** for window management and event handling.
* **Midpoint circle** algorithm is used to draw bubbles and bullets.
* **Midpoint line** algorithm is used for UI elements (buttons).
* Bubbles are stored in a list and updated frame-by-frame.
* Collision detection checks for:

  * **Bullet hitting a bubble**
  * **Bubble reaching bottom**
  * **Bubble hitting spaceship**

---

## 💡 Tips and Tricks

* **Aim carefully** — missed bullets bring you closer to game over.
* **Target special bubbles first** for big score jumps.
* The **higher your score**, the faster bubbles fall — plan accordingly.
* **Pause strategically** if overwhelmed.

---

## 📜 License

This project is licensed under the MIT License.
