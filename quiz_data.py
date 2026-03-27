# quiz_data.py  — question bank, organised by domain

QUESTIONS = [

    # ── PYTHON ──────────────────────────────────────────
    {
        "id": 1, "domain": "AI/ML", "skill": "python", "difficulty": "Beginner",
        "question": "What does `len([1, 2, 3])` return in Python?",
        "options": ["2", "3", "4", "None"],
        "answer": "3",
    },
    {
        "id": 2, "domain": "AI/ML", "skill": "python", "difficulty": "Intermediate",
        "question": "Which Python keyword is used to create a generator function?",
        "options": ["return", "yield", "async", "lambda"],
        "answer": "yield",
    },
    {
        "id": 3, "domain": "AI/ML", "skill": "python", "difficulty": "Advanced",
        "question": "What is the output of `list(map(lambda x: x**2, range(3)))`?",
        "options": ["[0, 1, 4]", "[1, 4, 9]", "[0, 1, 2]", "[1, 2, 3]"],
        "answer": "[0, 1, 4]",
    },

    # ── MACHINE LEARNING ────────────────────────────────
    {
        "id": 4, "domain": "AI/ML", "skill": "machine learning", "difficulty": "Beginner",
        "question": "Which algorithm is used for classification problems?",
        "options": ["Linear Regression", "K-Means", "Logistic Regression", "PCA"],
        "answer": "Logistic Regression",
    },
    {
        "id": 5, "domain": "AI/ML", "skill": "machine learning", "difficulty": "Intermediate",
        "question": "What does 'overfitting' mean in ML?",
        "options": [
            "Model performs well on training data but poorly on new data",
            "Model is too simple to learn the data",
            "Model has too few parameters",
            "Model ignores the training data",
        ],
        "answer": "Model performs well on training data but poorly on new data",
    },
    {
        "id": 6, "domain": "AI/ML", "skill": "machine learning", "difficulty": "Advanced",
        "question": "Which technique reduces overfitting by randomly dropping neurons during training?",
        "options": ["Batch Normalization", "Dropout", "L1 Regularization", "Early Stopping"],
        "answer": "Dropout",
    },

    # ── WEB DEV ─────────────────────────────────────────
    {
        "id": 7, "domain": "Web Dev", "skill": "html", "difficulty": "Beginner",
        "question": "Which HTML tag is used to link an external CSS file?",
        "options": ["<style>", "<script>", "<link>", "<css>"],
        "answer": "<link>",
    },
    {
        "id": 8, "domain": "Web Dev", "skill": "javascript", "difficulty": "Intermediate",
        "question": "What does `===` check in JavaScript?",
        "options": [
            "Only value equality",
            "Only type equality",
            "Both value and type equality",
            "Neither",
        ],
        "answer": "Both value and type equality",
    },
    {
        "id": 9, "domain": "Web Dev", "skill": "react", "difficulty": "Intermediate",
        "question": "In React, what hook is used to manage local component state?",
        "options": ["useEffect", "useContext", "useState", "useRef"],
        "answer": "useState",
    },
    {
        "id": 10, "domain": "Web Dev", "skill": "css", "difficulty": "Beginner",
        "question": "Which CSS property controls the space between elements?",
        "options": ["padding", "margin", "border", "spacing"],
        "answer": "margin",
    },

    # ── BACKEND ─────────────────────────────────────────
    {
        "id": 11, "domain": "Backend", "skill": "flask", "difficulty": "Beginner",
        "question": "Which decorator is used to define a route in Flask?",
        "options": ["@app.url()", "@app.route()", "@flask.path()", "@route.get()"],
        "answer": "@app.route()",
    },
    {
        "id": 12, "domain": "Backend", "skill": "sql", "difficulty": "Beginner",
        "question": "Which SQL command retrieves data from a table?",
        "options": ["GET", "FETCH", "SELECT", "READ"],
        "answer": "SELECT",
    },
    {
        "id": 13, "domain": "Backend", "skill": "rest api", "difficulty": "Intermediate",
        "question": "Which HTTP method is typically used to update a resource?",
        "options": ["GET", "POST", "PUT", "DELETE"],
        "answer": "PUT",
    },

    # ── DATA SCIENCE ────────────────────────────────────
    {
        "id": 14, "domain": "Data Science", "skill": "pandas", "difficulty": "Beginner",
        "question": "Which pandas method shows the first 5 rows of a DataFrame?",
        "options": [".tail()", ".first()", ".head()", ".top()"],
        "answer": ".head()",
    },
    {
        "id": 15, "domain": "Data Science", "skill": "pandas", "difficulty": "Intermediate",
        "question": "What does `df.groupby('col').mean()` do?",
        "options": [
            "Sorts the column",
            "Groups rows by column values and computes the mean per group",
            "Filters rows where the column equals the mean",
            "Drops duplicate values",
        ],
        "answer": "Groups rows by column values and computes the mean per group",
    },
    {
        "id": 16, "domain": "Data Science", "skill": "numpy", "difficulty": "Intermediate",
        "question": "What does `np.zeros((3, 3))` create?",
        "options": [
            "A 3x3 matrix of ones",
            "A 3x3 identity matrix",
            "A 3x3 matrix of zeros",
            "A list of 3 zeros",
        ],
        "answer": "A 3x3 matrix of zeros",
    },

    # ── CYBERSECURITY ───────────────────────────────────
    {
        "id": 17, "domain": "Cybersecurity", "skill": "networking", "difficulty": "Beginner",
        "question": "What does HTTP stand for?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Protocol",
            "HyperText Transmission Process",
            "Host Transfer Text Protocol",
        ],
        "answer": "HyperText Transfer Protocol",
    },
    {
        "id": 18, "domain": "Cybersecurity", "skill": "cryptography", "difficulty": "Intermediate",
        "question": "Which algorithm is commonly used for asymmetric encryption?",
        "options": ["AES", "MD5", "RSA", "SHA-256"],
        "answer": "RSA",
    },

    # ── DEVOPS ──────────────────────────────────────────
    {
        "id": 19, "domain": "DevOps", "skill": "docker", "difficulty": "Beginner",
        "question": "What is a Docker container?",
        "options": [
            "A virtual machine",
            "A lightweight isolated runtime environment",
            "A cloud storage bucket",
            "A database cluster",
        ],
        "answer": "A lightweight isolated runtime environment",
    },
    {
        "id": 20, "domain": "DevOps", "skill": "linux", "difficulty": "Beginner",
        "question": "Which Linux command lists files in a directory?",
        "options": ["dir", "list", "ls", "show"],
        "answer": "ls",
    },

    # ── MOBILE ──────────────────────────────────────────
    {
        "id": 21, "domain": "Mobile", "skill": "flutter", "difficulty": "Beginner",
        "question": "Which language is used to write Flutter apps?",
        "options": ["Kotlin", "Swift", "Dart", "Java"],
        "answer": "Dart",
    },
    {
        "id": 22, "domain": "Mobile", "skill": "android", "difficulty": "Intermediate",
        "question": "Which file defines permissions in an Android app?",
        "options": ["build.gradle", "MainActivity.java", "AndroidManifest.xml", "styles.xml"],
        "answer": "AndroidManifest.xml",
    },

    # ── GENERAL ─────────────────────────────────────────
    {
        "id": 23, "domain": "General", "skill": "git", "difficulty": "Beginner",
        "question": "Which git command saves staged changes to history?",
        "options": ["git push", "git save", "git commit", "git stage"],
        "answer": "git commit",
    },
    {
        "id": 24, "domain": "General", "skill": "git", "difficulty": "Intermediate",
        "question": "What does `git rebase` do?",
        "options": [
            "Deletes a branch",
            "Moves or replays commits on top of another branch",
            "Creates a new repository",
            "Reverts all changes",
        ],
        "answer": "Moves or replays commits on top of another branch",
    },
    {
        "id": 25, "domain": "General", "skill": "algorithms", "difficulty": "Intermediate",
        "question": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
        "answer": "O(log n)",
    },
]