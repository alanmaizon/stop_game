# **Stop! Game - Singleplayer Version**

## **Table of Contents**
1. [Introduction](#introduction)
2. [About the Game](#about-the-game)
3. [ER Diagram](#er-diagram)
4. [Features](#features)
5. [How to Play](#how-to-play)
6. [Contribute](#contribute)
7. [User Stories](#user-stories)
8. [Test Cases](#test-cases)
9. [Debugging](#debugging)
10. [Resources](#resources)

---

## **Introduction**

**Stop!** is a Django-based single-player word game where users compete against the clock to generate words for predefined categories that match a randomly chosen letter. The project demonstrates the use of Django's key features, including models, views, templates, form handling, and database integration.

The primary goal is to highlight Django’s potential for building scalable web applications while delivering an engaging word game experience.

---

## **About the Game**

Stop! is a digital adaptation of the classic pen-and-paper game. It challenges players’ vocabulary and creativity by requiring quick thinking under time constraints. The game is perfect for building your vocabulary while competing against yourself.

---

## **ER Diagram**

Here’s the **Entity-Relationship Diagram** for the game, created using **Mermaid**:

```mermaid
erDiagram
    User {
        int id PK
        string username
        string email
        string password
    }

    Player {
        int id PK
        int user_id FK
        int score
    }

    Round {
        int id PK
        char letter
        bool is_active
        datetime created_at
    }

    Category {
        int id PK
        string name
        datetime created_at
    }

    Submission {
        int id PK
        int player_id FK
        int round_id FK
        int category_id FK
        string word
        bool is_valid
        string validation_message
        bool score_calculated
    }

    WordSubmission {
        int id PK
        int player_id FK
        string word
        string status
        string feedback
    }

    ValidAnswer {
        int id PK
        int category_id FK
        string word
    }

    User ||--o{ Player : "has"
    Player ||--o{ Submission : "makes"
    Player ||--o{ WordSubmission : "suggests"
    Round ||--o{ Submission : "includes"
    Category ||--o{ Submission : "has"
    Category ||--o{ ValidAnswer : "contains"
```

---

## **Features**

### **Gameplay Features**
1. **Game Rounds**:
   - Start a round with a randomly generated letter.
   - Timer set for 60 seconds to challenge the player.
   - Submit words for categories such as "Animal," "Country," and "Food."

2. **Word Validation**:
   - Words are validated in real-time against a database of valid answers.
   - Validation checks include:
     - Does the word start with the correct letter?
     - Is the word valid for the chosen category?

3. **Results Page**:
   - Displays all submissions for the round.
   - Shows points earned for valid and unique words.
   - Tracks cumulative player scores.

4. **Suggest a New Word**:
   - Players can suggest words for categories.
   - Admins can approve/reject suggestions to expand the game’s word database.
   - Players earn bonus points for approved suggestions.

5. **Responsive Design**:
   - User-friendly interface styled with Bootstrap.
   - Optimized for mobile, tablet, and desktop devices.

6. **Dark Mode**:
   - A toggle to switch between light and dark themes for better accessibility.

---

## **How to Play**

The rules are simple:
1. Start a round with a randomly chosen letter.
2. Fill in categories like "Animal," "Country," and "Food" with words starting with that letter.
3. Press "Submit" before the timer runs out.
4. See your score and evaluate your performance on the results page!

---

## **Contribute**

Players can contribute to the game by suggesting new words:
1. Submit words that are missing from the current database.
2. Admins review and approve the suggestions.
3. Earn bonus points for every approved word.

---

## **User Stories**

### **Player Stories**
- **As a player**, I want to start a new game round with a randomly generated letter and see a timer, so I can compete against myself.
- **As a player**, I want to submit words for categories like "Animal," "Country," "Food," etc., to earn points.
- **As a player**, I want to see detailed results after a game round to evaluate my performance.
- **As a player**, I want to suggest a new word and earn bonus points if it is approved by an admin.

### **Admin Stories**
- **As an admin**, I want to review and validate submissions to ensure they follow the rules of the game.
- **As an admin**, I want to approve or reject player-submitted words, expanding the database of valid answers.

### **Developer/Academic Focus**
- **As a developer**, I want to showcase the use of Django's features (models, views, templates, form handling, and database queries) in building a web application.
- **As a professor/reviewer**, I want to evaluate the proper use of Django as a framework to structure and manage this application.

---

## **Test Cases**

Here are test cases to validate the core functionality of the game:

### **1. Game Round**
- **Test Case 1**: Start a new round and verify that a random letter is generated and displayed.
- **Test Case 2**: Ensure the timer counts down correctly and stops at 0.
- **Test Case 3**: Verify that categories load dynamically on the game screen.

### **2. Word Submission**
- **Test Case 1**: Validate words starting with the correct letter are accepted.
- **Test Case 2**: Verify that invalid words (e.g., incorrect starting letter or invalid category) are rejected with proper error messages.
- **Test Case 3**: Ensure duplicate submissions are flagged and do not receive points.

### **3. Results Page**
- **Test Case 1**: Confirm that the player’s score is displayed correctly.
- **Test Case 2**: Verify that unique valid words receive bonus points.
- **Test Case 3**: Ensure cumulative player scores update properly in the database.

### **4. Word Suggestions**
- **Test Case 1**: Allow players to suggest words and verify that they appear in the admin’s review panel.
- **Test Case 2**: Confirm that approved suggestions add to the valid answers database.
- **Test Case 3**: Verify that players earn bonus points for approved words.

---

## **Debugging**

### **Debugging Techniques**
1. **Logging**:
   - Use Django’s `logging` module to track word validation results and submission statuses:
     ```python
     logger.debug(f"Validating word: {word}, Category: {category_name}")
     ```

2. **Django Debug Toolbar**:
   - Install and configure the **Django Debug Toolbar** to monitor database queries and page rendering times:
     ```bash
     pip install django-debug-toolbar
     ```

3. **Browser DevTools**:
   - Inspect the user interface for responsiveness and layout issues.
   - Use the **Console** to debug JavaScript functions (e.g., dark mode toggle).

4. **Test Database**:
   - Use Django’s test database to run isolated tests on models and views:
     ```bash
     python manage.py test
     ```

5. **Handle Exceptions Gracefully**:
   - Add `try/except` blocks for database operations to prevent application crashes:
     ```python
     try:
         round = Round.objects.get(id=round_id)
     except Round.DoesNotExist:
         return JsonResponse({'error': 'Round not found'}, status=404)
     ```

---

## **Resources**

### **Tools and Libraries**
- **Django**: Framework for backend logic and database handling.
- **Bootstrap**: Frontend framework for styling and responsiveness.
- **SQLite**: Lightweight database for development.
- **Mermaid**: For generating the ER diagram.

### **References**
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Mermaid Documentation](https://mermaid.js.org/)

---

## Module 5 - UCD PA - Alan Maizon
**[Github (Public Repository)](https://github.com/alanmaizon/stop_game/)**


