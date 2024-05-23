from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QColorDialog, QSpinBox, QHBoxLayout, 
                             QComboBox, QMessageBox, QDialogButtonBox, QGridLayout, 
                             QCheckBox)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal, Qt
import random
import logging
from utils import generate_maze

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for default values
DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 600
DEFAULT_MAZE_SIZE = 10
DEFAULT_OBSTACLE_DENSITY = 0.3
DEFAULT_HEURISTIC = 'octile'
DEFAULT_COLORS = {
    'start_node_color': '#00FF00',
    'end_node_color': '#FFD700',
    'path_color': '#0000FF',
    'obstacle_color': '#000000',
    'background_color': '#FFFFFF',
    'expanded_node_color': '#808080'  # Add this line
}

DARK_MODE_COLORS = {
    'start_node_color': '#00FF00',
    'end_node_color': '#FFD700',
    'path_color': '#0000FF',
    'obstacle_color': '#000000',
    'background_color': '#1E1E1E',
    'expanded_node_color': '#808080'  # Add this line
}

class SettingsMenu(QDialog):
    settings_updated = pyqtSignal(dict)
    menu_closed = pyqtSignal()


    def __init__(self, parent=None):
        """
        Initialize the SettingsMenu dialog.
        """
        super(SettingsMenu, self).__init__(parent)
        logging.debug("Initializing SettingsMenu")
        self.mazeArray = []
        self.setWindowTitle('Settings Menu')
        self.layout = QVBoxLayout(self)
        
        # Window size configuration
        self.setupWindowSizeConfig()

        # Dark mode configuration
        self.setupDarkModeConfig()

        # Color configuration
        self.setupColorConfig()

        # Maze configuration
        self.setupMazeConfig()
        self.insertMazeButton = QPushButton("Insert Maze")
        self.insertMazeButton.clicked.connect(self.insertMaze)
        self.layout.addWidget(self.insertMazeButton)

        # Heuristic configuration
        self.setupHeuristicConfig()
        self.setupRandomMazeConfig()

        # Save button
        self.saveButton = QPushButton("Save Settings")
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)
        self.rejected.connect(self.useDefaultSettings)

        # Apply dark mode by default
        self.applyDarkMode(True)
        self.rejected.connect(self.useDefaultSettings)
        self.accepted.connect(self.on_accepted)


    def on_accepted(self):
        """Emit the menu_closed signal when the dialog is accepted."""
        self.menu_closed.emit()


    def setupRandomMazeConfig(self):
        """
        Setup configuration for random maze settings.
        """
        self.randomMazeLayout = QHBoxLayout()
        self.randomMazeCheckBox = QCheckBox("Random Maze")
        self.randomMazeCheckBox.stateChanged.connect(self.randomMazeCheckBoxLogic)
        self.randomMazeCheckBox.setChecked(True)
        self.randomMazeLayout.addWidget(self.randomMazeCheckBox)
        self.layout.addLayout(self.randomMazeLayout)

    def randomMazeCheckBoxLogic(self):
        """
        Logic for handling random maze checkbox state changes.
        """
        logging.debug("RandomMazeCheckBox toggled")
        if self.randomMazeCheckBox.isChecked():
            self.insertMazeButton.hide()
            self.obstacleDensityLabel.show()
            self.obstacleDensityLineEdit.show()
        else:
            self.obstacleDensityLabel.hide()
            self.obstacleDensityLineEdit.hide()
            self.insertMazeButton.show()

    def insertMaze(self):
        """
        Open dialog to insert a custom maze.
        """
        logging.debug("Inserting maze")
        self.mazeCells = {}
        try:
            maze_size = int(self.MazeSizeLineEdit.text())
            if maze_size <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Set maze size before inserting the maze.")
            return

        self.mazeDialog = QDialog(self)
        self.mazeDialog.setWindowTitle("Insert Maze")
        layout = QGridLayout(self.mazeDialog)

        for row in range(maze_size):
            for col in range(maze_size):
                cellButton = QPushButton()
                cellButton.setCheckable(True)
                cellButton.setStyleSheet("background-color: white; border: 1px solid #ccc;")
                cellButton.toggled.connect(lambda checked, row=row, col=col: self.updateMazeCell(row, col, checked))
                layout.addWidget(cellButton, row, col)
                self.mazeCells[(row, col)] = cellButton

        self.mazeArray = [[0 for _ in range(maze_size)] for _ in range(maze_size)]

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.mazeDialog.accept)
        buttonBox.rejected.connect(self.mazeDialog.reject)
        layout.addWidget(buttonBox, maze_size, 0, 1, maze_size)

        self.mazeDialog.setLayout(layout)
        self.mazeDialog.exec_()

    def updateMazeCell(self, row, col, checked):
        """
        Update the state of a maze cell.
        """
        if checked:
            self.mazeCells[(row, col)].setStyleSheet("background-color: black; border: 1px solid #ccc;")
            self.mazeArray[row][col] = 1
        else:
            self.mazeCells[(row, col)].setStyleSheet("background-color: white; border: 1px solid #ccc;")
            self.mazeArray[row][col] = 0

    def setupWindowSizeConfig(self):
        """
        Setup configuration for window size settings.
        """
        logging.debug("Setting up window size config")
        self.sizeLayout = QHBoxLayout()

        self.widthLabel = QLabel("Window Width:")
        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setRange(100, 2000)
        self.widthSpinBox.setValue(DEFAULT_WINDOW_WIDTH)
        self.widthSpinBox.setButtonSymbols(QSpinBox.NoButtons)  # Remove up and down arrows
        self.sizeLayout.addWidget(self.widthLabel)
        self.sizeLayout.addWidget(self.widthSpinBox)

        self.heightLabel = QLabel("Window Height:")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setRange(100, 2000)
        self.heightSpinBox.setValue(DEFAULT_WINDOW_HEIGHT)
        self.heightSpinBox.setButtonSymbols(QSpinBox.NoButtons)  # Remove up and down arrows
        self.sizeLayout.addWidget(self.heightLabel)
        self.sizeLayout.addWidget(self.heightSpinBox)

        self.layout.addLayout(self.sizeLayout)


    def setupDarkModeConfig(self):
        """
        Setup configuration for dark mode settings.
        """
        logging.debug("Setting up dark mode config")
        self.darkModeLayout = QHBoxLayout()
        self.darkModeCheckBox = QCheckBox("Dark Mode")
        self.darkModeCheckBox.setChecked(True)
        self.darkModeCheckBox.stateChanged.connect(self.toggleDarkMode)
        self.darkModeLayout.addWidget(self.darkModeCheckBox)
        self.layout.addLayout(self.darkModeLayout)

    def toggleDarkMode(self, state):
        """
        Toggle dark mode based on the checkbox state.
        """
        logging.debug("Toggling dark mode")
        dark_mode = state == Qt.Checked
        self.applyDarkMode(dark_mode)

    def applyDarkMode(self, enabled):
        """
        Apply dark mode styles to the dialog.
        """
        if enabled:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLineEdit, QSpinBox, QComboBox, QCheckBox {
                    background-color: #3C3C3C;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton {
                    background-color: #4C4C4C;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #5C5C5C;
                }
            """)
            self.colorSettings.update(DARK_MODE_COLORS)
        else:
            self.setStyleSheet("")
            self.colorSettings.update(DEFAULT_COLORS)
        self.updateColorSwatches()

    def updateColorSwatches(self):
        """
        Update the color swatches based on the current color settings.
        """
        for color_key, default_color in self.colorSettings.items():
            swatch = self.findChild(QLabel, color_key)
            if swatch:
                swatch.setStyleSheet(f"background-color: {default_color}; border: 1px solid #555555;")

    def setupColorConfig(self):
        """
        Setup configuration for color settings.
        """
        logging.debug("Setting up color config")
        self.colorConfigLayout = QGridLayout()
        self.colorSettings = DARK_MODE_COLORS.copy()

        row = 0
        col = 0
        for color_key, default_color in self.colorSettings.items():
            self.createColorPicker(color_key, default_color, row, col)
            col += 1
            if col == 3:  # Adjust swatches per row
                col = 0
                row += 1

        self.layout.addLayout(self.colorConfigLayout)


    def createColorPicker(self, color_key, default_color, row, col):
        """
        Create a color picker for a given color setting.

        Args:
            color_key (str): The key for the color setting.
            default_color (str): The default color value.
            row (int): The row in the grid layout.
            col (int): The column in the grid layout.
        """
        label = QLabel(f"{color_key.replace('_', ' ').title()}:")
        swatch = QLabel()
        swatch.setObjectName(color_key)
        swatch.setStyleSheet(f"background-color: {default_color}; border: 1px solid #555555;")
        swatch.setFixedSize(50, 20)
        swatch.mousePressEvent = lambda event, key=color_key, sw=swatch: self.openColorDialog(key, sw)
        colorLayout = QHBoxLayout()
        colorLayout.addWidget(label)
        colorLayout.addWidget(swatch)
        self.colorConfigLayout.addLayout(colorLayout, row, col)

    def openColorDialog(self, color_key, swatch):
        """
        Open a color dialog to select a color for a given setting.

        Args:
            color_key (str): The key for the color setting.
            swatch (QLabel): The swatch label to update with the selected color.
        """
        logging.debug(f"Opening color dialog for {color_key}")
        color = QColorDialog.getColor(QColor(swatch.styleSheet().split(': ')[1].split(';')[0]))
        if color.isValid():
            self.colorSettings[color_key] = color.name()
            swatch.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555555;")

    def setupMazeConfig(self):
        """
        Setup configuration for maze settings.
        """
        logging.debug("Setting up maze config")
        self.MazeSizeLayout = QHBoxLayout()
        self.MazeSizeLabel = QLabel("Maze Size:")
        self.MazeSizeLineEdit = QLineEdit()
        self.MazeSizeLineEdit.setPlaceholderText("Enter Maze size (e.g., 10)")
        self.MazeSizeLineEdit.setToolTip("Enter the size of the maze (e.g., 10 for a 10x10 maze)")
        self.MazeSizeLayout.addWidget(self.MazeSizeLabel)
        self.MazeSizeLayout.addWidget(self.MazeSizeLineEdit)

        self.obstacleDensityLayout = QHBoxLayout()
        self.obstacleDensityLabel = QLabel("Obstacle Density:")
        self.obstacleDensityLineEdit = QLineEdit()
        self.obstacleDensityLineEdit.setPlaceholderText("Enter obstacle density (0 to 1)")
        self.obstacleDensityLineEdit.setToolTip("Enter the obstacle density as a float between 0 and 1")
        self.obstacleDensityLayout.addWidget(self.obstacleDensityLabel)
        self.obstacleDensityLayout.addWidget(self.obstacleDensityLineEdit)

        self.startPointLayout = QHBoxLayout()
        self.startPointLabel = QLabel("Start Point (x,y):")
        self.startPointLineEdit = QLineEdit()
        self.startPointLineEdit.setPlaceholderText("Enter start point (e.g., 0,0)")
        self.startPointLineEdit.setToolTip("Enter the start point coordinates (e.g., 0,0)")
        self.startPointLayout.addWidget(self.startPointLabel)
        self.startPointLayout.addWidget(self.startPointLineEdit)

        self.endPointLayout = QHBoxLayout()
        self.endPointLabel = QLabel("End Point (x,y):")
        self.endPointLineEdit = QLineEdit()
        self.endPointLineEdit.setPlaceholderText("Enter end point (e.g., 9,9)")
        self.endPointLineEdit.setToolTip("Enter the end point coordinates (e.g., 9,9)")
        self.endPointLayout.addWidget(self.endPointLabel)
        self.endPointLayout.addWidget(self.endPointLineEdit)

        self.layout.addLayout(self.MazeSizeLayout)
        self.layout.addLayout(self.obstacleDensityLayout)
        self.layout.addLayout(self.startPointLayout)
        self.layout.addLayout(self.endPointLayout)

    def setupHeuristicConfig(self):
        """
        Setup configuration for heuristic settings.
        """
        logging.debug("Setting up heuristic config")
        self.heuristicLayout = QHBoxLayout()
        self.heuristicLabel = QLabel("Heuristic:")
        self.heuristicComboBox = QComboBox()
        self.heuristicComboBox.addItem("Octile Distance", "octile")
        self.heuristicComboBox.addItem("Euclidean Distance", "euclidean")
        self.heuristicLayout.addWidget(self.heuristicLabel)
        self.heuristicLayout.addWidget(self.heuristicComboBox)
        self.layout.addLayout(self.heuristicLayout)

    def validateInputs(self):
        """
        Validate all user inputs in the settings dialog.

        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
        logging.debug("Validating inputs")
        valid = True

        # Validate Maze Size
        maze_size = self.validateMazeSize()
        if maze_size is None:
            valid = False

        # Validate Obstacle Density
        if self.randomMazeCheckBox.isChecked():
            obstacle_density = self.validateObstacleDensity()
            if obstacle_density is None:
                valid = False

        # Validate Start and End Points
        start_point, end_point = self.validateStartEndPoints(maze_size)
        if start_point is None or end_point is None:
            valid = False

        return valid

    def validateMazeSize(self):
        """
        Validate the maze size input.

        Returns:
            int: The maze size if valid, None otherwise.
        """
        try:
            maze_size = int(self.MazeSizeLineEdit.text())
            if maze_size <= 0:
                raise ValueError("Maze size must be a positive integer.")
            return maze_size
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Maze Size Error: {e}")
            return None

    def validateObstacleDensity(self):
        """
        Validate the obstacle density input.

        Returns:
            float: The obstacle density if valid, None otherwise.
        """
        try:
            obstacle_density = float(self.obstacleDensityLineEdit.text())
            if obstacle_density < 0 or obstacle_density > 1:
                raise ValueError("Obstacle Density must be a float between 0 and 1.")
            return obstacle_density
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Obstacle Density Error: {e}")
            return None

    def validateStartEndPoints(self, maze_size):
        """
        Validate the start and end point inputs.

        Args:
            maze_size (int): The size of the maze.

        Returns:
            tuple: The start and end points if valid, None otherwise.
        """
        try:
            start_point = tuple(map(int, self.startPointLineEdit.text().split(',')))
            end_point = tuple(map(int, self.endPointLineEdit.text().split(',')))
            
            if not (0 <= start_point[0] < maze_size and 0 <= start_point[1] < maze_size):
                raise ValueError("Start point is out of bounds.")
            if not (0 <= end_point[0] < maze_size and 0 <= end_point[1] < maze_size):
                raise ValueError("End point is out of bounds.")
            
            if start_point == end_point:
                raise ValueError("Start point and end point cannot be the same.")
            
            return start_point, end_point
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Start/End Point Error: {e}")
            return None, None

    def useDefaultSettings(self):
        logging.debug("Using default settings")
        default_settings = {
            'window_width': DEFAULT_WINDOW_WIDTH,
            'window_height': DEFAULT_WINDOW_HEIGHT,
            'Maze_size': DEFAULT_MAZE_SIZE,
            'start_point': (0, 0),
            'end_point': (DEFAULT_MAZE_SIZE - 1, DEFAULT_MAZE_SIZE - 1),
            'obstacle_density': DEFAULT_OBSTACLE_DENSITY,
            'heuristic': DEFAULT_HEURISTIC,
            'start_node_color': DARK_MODE_COLORS['start_node_color'],
            'end_node_color': DARK_MODE_COLORS['end_node_color'],
            'path_color': DARK_MODE_COLORS['path_color'],
            'obstacle_color': DARK_MODE_COLORS['obstacle_color'],
            'background_color': DARK_MODE_COLORS['background_color'],
            'expanded_node_color': DARK_MODE_COLORS['expanded_node_color'],  # Add this line
            'maze': generate_maze(DEFAULT_MAZE_SIZE, DEFAULT_OBSTACLE_DENSITY),
        }
        self.settings_updated.emit(default_settings)

    def MazeSetter(self):
        """
        Set the maze based on user settings.

        Returns:
            list: A 2D list representing the maze.
        """
        logging.debug("Setting maze")
        if self.randomMazeCheckBox.isChecked():
            maze_size = int(self.MazeSizeLineEdit.text())
            obstacle_density = float(self.obstacleDensityLineEdit.text())
            self.mazeArray = generate_maze(maze_size, obstacle_density)
        return self.mazeArray

    def saveSettings(self):
        logging.debug("Saving settings")
        if not self.validateInputs():
            return

        start_point = tuple(map(int, self.startPointLineEdit.text().split(',')))
        end_point = tuple(map(int, self.endPointLineEdit.text().split(',')))

        settings = {
            'window_width': self.widthSpinBox.value(),
            'window_height': self.heightSpinBox.value(),
            'Maze_size': int(self.MazeSizeLineEdit.text()),
            'start_point': start_point,
            'end_point': end_point,
            'heuristic': self.heuristicComboBox.currentData(),
            'start_node_color': self.colorSettings['start_node_color'],
            'end_node_color': self.colorSettings['end_node_color'],
            'path_color': self.colorSettings['path_color'],
            'obstacle_color': self.colorSettings['obstacle_color'],
            'background_color': self.colorSettings['background_color'],
            'expanded_node_color': self.colorSettings['expanded_node_color'],
            'maze': self.MazeSetter(),
        }
        if self.randomMazeCheckBox.isChecked():
            obstacle_density = float(self.obstacleDensityLineEdit.text())
            settings.update({'obstacle_density': obstacle_density})
        self.settings_updated.emit(settings)
        self.accept()  # Close the settings menu


