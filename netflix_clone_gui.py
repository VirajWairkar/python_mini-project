import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QScrollArea, QGridLayout, QFrame, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser


# --- Movie Data ---
movies_data = [
    {"id": 1, "title": "Space Journey", "description": "A crew explores unknown planets.",
     "genres": "Sci-Fi", "moods": ["excited", "thoughtful"],
     "video": "https://www.youtube.com/watch?v=J4QfaZKxB0A"},

    {"id": 2, "title": "Romance in Rome", "description": "Two travellers find love in Rome.",
     "genres": "Romance", "moods": ["romantic", "happy"],
     "video": "https://www.youtube.com/watch?v=EvKphDkU1gY"},

    {"id": 3, "title": "AI Uprising", "description": "A powerful AI questions humanity.",
     "genres": "Thriller", "moods": ["stressed", "thoughtful"],
     "video": "https://www.youtube.com/watch?v=vjF9GgrY9c0"},
]

# --- Helper: Load/Save Users ---
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Netflix Clone Login 🎭")
        self.setFixedSize(800, 600)
        self.initUI()

    def initUI(self):
        # Set gradient background (black → dark red)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#000000"))
        gradient.setColorAt(1.0, QColor("#8B0000"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("🎭 Login to Netflix Clone")
        title.setStyleSheet("font-size: 32px; color: #E50914; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Username field
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(320)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)

        # Password field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(320)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)

        # Login button
        btn = QPushButton("Login / Register")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff1f1f;
            }
        """)
        btn.setFixedWidth(200)
        btn.clicked.connect(self.handle_login)

        layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
            return

        users = load_users()

        # Register new user or check password
        if username not in users:
            users[username] = {"password": password}
            save_users(users)
            QMessageBox.information(self, "Registered", "New account created successfully!")

        elif users[username]["password"] != password:
            QMessageBox.warning(self, "Error", "Incorrect password!")
            return

        # Open main Netflix window
        self.hide()
        self.main_window = NetflixClone(username)
        self.main_window.show()


# --- Netflix Clone Window ---
class NetflixClone(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.users = load_users()
        self.default_poster = "posters/default_poster.jpg"

        self.setWindowTitle(f"Netflix Clone 🎬 - {self.username}")
        self.setGeometry(100, 50, 1200, 800)
        self.setStyleSheet("background-color: #141414; color: white;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        header = QLabel(f"Welcome, {self.username} 🍿")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #E50914; margin: 10px;")
        main_layout.addWidget(header)

        mood_layout = QHBoxLayout()
        mood_label = QLabel("Select your mood: ")
        mood_label.setFont(QFont("Arial", 14))
        self.mood_dropdown = QComboBox()
        self.mood_dropdown.addItems(["All", "happy", "sad", "excited", "thoughtful", "romantic", "stressed"])
        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_dropdown)

        show_btn = QPushButton("Show Movies 🎥")
        show_btn.clicked.connect(self.show_recommendations)
        show_btn.setStyleSheet("background-color: #E50914; padding: 6px 12px; border-radius: 8px;")
        mood_layout.addWidget(show_btn)
        main_layout.addLayout(mood_layout)

        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout()
        self.scroll_content.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
        self.display_movies(movies_data)

    def get_poster(self, title):
        path = f"posters/{title.replace(' ', '_')}.jpg"
        return path if os.path.exists(path) else self.default_poster

    def display_movies(self, movie_list):
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        row, col = 0, 0
        for movie in movie_list:
            frame = QFrame()
            frame.setStyleSheet("background-color: #1E1E1E; border-radius: 10px;")
            vbox = QVBoxLayout()

            poster_label = QLabel()
            pixmap = QPixmap(self.get_poster(movie["title"])).scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            poster_label.setPixmap(pixmap)
            poster_label.setAlignment(Qt.AlignCenter)
            poster_label.mousePressEvent = lambda e, m=movie: self.play_video(m)
            vbox.addWidget(poster_label)

            title_label = QLabel(movie["title"])
            title_label.setFont(QFont("Arial", 12, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            vbox.addWidget(title_label)

            frame.setLayout(vbox)
            self.grid_layout.addWidget(frame, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def show_recommendations(self):
        mood = self.mood_dropdown.currentText().lower()
        if mood == "all":
            filtered = movies_data
        else:
            filtered = [m for m in movies_data if mood in m["moods"]]
        self.display_movies(filtered)

    # --- Movie Player ---

    def play_video(self, movie):
        if "video" not in movie or not movie["video"]:
            QMessageBox.warning(self, "Error", "No video link found for this movie.")
            return

        video_url = movie["video"]

        if video_url.startswith("http"):
            # Open YouTube link in default browser
            webbrowser.open(video_url)
        else:
            # Local MP4 fallback
            if not os.path.exists(video_url):
                QMessageBox.warning(self, "Error", "Trailer file not found.")
                return

            self.player = QWidget()
            self.player.setWindowTitle(f"Playing: {movie['title']}")
            self.player.setGeometry(200, 100, 1000, 600)
            layout = QVBoxLayout()

            self.video_widget = QVideoWidget()
            self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_url)))
            self.media_player.setVideoOutput(self.video_widget)

            layout.addWidget(self.video_widget)

            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.player.close)
            layout.addWidget(close_btn)

            self.player.setLayout(layout)
            self.player.show()
            self.media_player.play()


# --- Run App ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
