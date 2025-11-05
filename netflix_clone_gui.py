import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QScrollArea, QGridLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# --- Movie Dataset ---
movies_data = [
    {"id": 1, "title": "Space Journey", "description": "A crew explores unknown planets. Sci-fi adventure with AI and aliens.", "genres": "Sci-Fi | Adventure", "cast": "A. Star, B. Nova", "moods": ["excited", "thoughtful"]},
    {"id": 2, "title": "Romance in Rome", "description": "Two travellers find love in the streets of Rome.", "genres": "Romance | Drama", "cast": "C. Heart, D. Smile", "moods": ["romantic", "happy"]},
    {"id": 3, "title": "AI Uprising", "description": "A powerful AI questions humanity. Thriller about ethics of technology.", "genres": "Sci-Fi | Thriller", "cast": "E. Code, F. Logic", "moods": ["thoughtful", "stressed"]},
    {"id": 4, "title": "Comedy Campus", "description": "College friends pull pranks and learn about life.", "genres": "Comedy", "cast": "G. Jester, H. Wit", "moods": ["happy", "bored"]},
    {"id": 5, "title": "Lost in Time", "description": "A scientist accidentally travels back in time and tries to return.", "genres": "Sci-Fi | Drama", "cast": "I. Clock, J. Past", "moods": ["thoughtful", "excited"]},
    {"id": 6, "title": "Family Ties", "description": "A family drama about reconnecting after years apart.", "genres": "Drama", "cast": "K. Home, L. Bond", "moods": ["sad", "thoughtful"]},
    {"id": 7, "title": "Stand-Up Night", "description": "A stand-up comedian faces life on stage — laughs and tears.", "genres": "Comedy | Drama", "cast": "M. Mic, N. Laugh", "moods": ["happy", "thoughtful"]},
    {"id": 8, "title": "Heist High", "description": "A clever crew plans a heist that goes hilariously wrong.", "genres": "Crime | Comedy", "cast": "O. Sleuth, P. Trick", "moods": ["excited", "happy"]},
    {"id": 9, "title": "Quiet River", "description": "A slow, introspective film about choices and consequences.", "genres": "Drama", "cast": "Q. Calm, R. Reflect", "moods": ["sad", "thoughtful"]},
    {"id": 10, "title": "Midnight Runner", "description": "Fast-paced action as a courier races against the clock.", "genres": "Action | Thriller", "cast": "S. Dash, T. Bolt", "moods": ["excited", "stressed"]},
]

# --- UI Class ---
class NetflixClone(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Netflix Clone 🎬")
        self.setGeometry(100, 50, 1200, 800)
        self.setStyleSheet("background-color: #141414; color: white;")
        
        self.default_poster = "posters/default_poster.jpg"
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header
        title = QLabel("🎬 Netflix Clone")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #E50914; margin: 10px;")
        main_layout.addWidget(title)

        # Mood dropdown
        mood_layout = QHBoxLayout()
        mood_label = QLabel("Select your mood: ")
        mood_label.setFont(QFont("Arial", 14))
        mood_label.setStyleSheet("margin-right: 10px;")

        self.mood_dropdown = QComboBox()
        self.mood_dropdown.addItems(["All", "happy", "sad", "excited", "thoughtful", "romantic", "bored", "stressed"])
        self.mood_dropdown.setStyleSheet("font-size: 14px; padding: 6px;")

        show_btn = QPushButton("Show Recommendations 🍿")
        show_btn.clicked.connect(self.show_recommendations)
        show_btn.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                border-radius: 10px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B20710;
            }
        """)

        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_dropdown)
        mood_layout.addWidget(show_btn)
        main_layout.addLayout(mood_layout)

        # Scrollable area for movies
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.scroll_content.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
        self.display_movies(movies_data)

    def get_poster_path(self, title):
        path = f"posters/{title.replace(' ', '_')}.jpg"
        if not os.path.exists(path):
            return self.default_poster
        return path

    def display_movies(self, movie_list):
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add posters
        row, col = 0, 0
        for movie in movie_list:
            frame = QFrame()
            frame.setStyleSheet("background-color: #1E1E1E; border-radius: 10px;")
            vbox = QVBoxLayout()

            poster_label = QLabel()
            poster_label.setAlignment(Qt.AlignCenter)
            poster_path = self.get_poster_path(movie["title"])
            pixmap = QPixmap(poster_path).scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            poster_label.setPixmap(pixmap)
            vbox.addWidget(poster_label)

            title_label = QLabel(movie["title"])
            title_label.setFont(QFont("Arial", 12, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(title_label)

            desc_label = QLabel(movie["description"])
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("color: #BBBBBB; font-size: 11px; padding: 4px;")
            vbox.addWidget(desc_label)

            frame.setLayout(vbox)
            self.grid_layout.addWidget(frame, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def show_recommendations(self):
        selected_mood = self.mood_dropdown.currentText().lower()
        if selected_mood == "all":
            filtered = movies_data
        else:
            filtered = [m for m in movies_data if selected_mood in m["moods"]]
        self.display_movies(filtered)

# --- Run App ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetflixClone()
    window.show()
    sys.exit(app.exec_())
