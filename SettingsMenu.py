from PyQt5.QtWidgets import QApplication,QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QSpinBox, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QMessageBox, QInputDialog,QDialogButtonBox,QGridLayout,QCheckBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal,QEvent
import random


class SettingsMenu(QDialog):
    settings_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(SettingsMenu, self).__init__(parent)
        self.mazeArray = []
        self.setWindowTitle('Settings Menu')
        self.layout = QVBoxLayout(self)
        # Window size configuration
        self.setupWindowSizeConfig()

        # Color configuration
        self.setupColorConfig()

        # Maze configuration
        self.setupMazeConfig()
        self.insertMazeButton = QPushButton("Insert Maze")
        self.insertMazeButton.clicked.connect(self.insertMaze)
        self.layout.addWidget(self.insertMazeButton)


        # Heuristic configuration
        self.setupHeuristicConfig()  # Add this line
        self.setupRandomMazeConfig()


        # Save button
        self.saveButton = QPushButton("Save Settings")
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)
        self.rejected.connect(self.useDefaultSettings)

    def setupRandomMazeConfig(self):
        self.randomMazeLayout = QHBoxLayout()
        self.randomMazeCheckBox = QCheckBox("Random Maze")
        self.randomMazeCheckBox.stateChanged.connect(self.randomMazeCheckBoxLogic)
        self.randomMazeCheckBox.setChecked(True)
        self.randomMazeLayout.addWidget(self.randomMazeCheckBox)
        self.layout.addLayout(self.randomMazeLayout)
    
    def randomMazeCheckBoxLogic(self):
        # Check if the checkbox is checked
        if self.randomMazeCheckBox.isChecked():
            self.insertMazeButton.hide()
            self.obstacleDensityLabel.show()
            self.obstacleDensityLineEdit.show()

            # Hide the button if checkbox is checked
        else:
            # Show the button if checkbox is not checked
            self.obstacleDensityLabel.hide()
            self.obstacleDensityLineEdit.hide()
            self.insertMazeButton.show()


    def insertMaze(self):
        # Existing code to get maze_size...
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
                cellButton.setStyleSheet("background-color: white;")  # Default color
                cellButton.toggled.connect(lambda checked, row=row, col=col: self.updateMazeCell(row, col, checked))
                layout.addWidget(cellButton, row, col)
                self.mazeCells[(row, col)] = cellButton

        self.mazeArray = [[0 for _ in range(maze_size)] for _ in range(maze_size)]  # Initialize the 2D list

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.mazeDialog.accept)
        buttonBox.rejected.connect(self.mazeDialog.reject)
        layout.addWidget(buttonBox, maze_size, 0, 1, maze_size)

        self.mazeDialog.setLayout(layout)
        self.mazeDialog.exec_()



    def updateMazeCell(self, row, col, checked):
        if checked:
            self.mazeCells[(row, col)].setStyleSheet("background-color: black;")
            self.mazeArray[row][col] = 1
        else:
            self.mazeCells[(row, col)].setStyleSheet("background-color: white;")
            self.mazeArray[row][col] = 0

    def setupWindowSizeConfig(self):
        self.sizeLayout = QHBoxLayout()
        self.widthLabel = QLabel("Window Width:")
        self.widthSpinBox = QSpinBox()
        self.widthSpinBox.setRange(100, 2000)
        self.widthSpinBox.setValue(600)  # Default value
        self.sizeLayout.addWidget(self.widthLabel)
        self.sizeLayout.addWidget(self.widthSpinBox)

        self.heightLabel = QLabel("Window Height:")
        self.heightSpinBox = QSpinBox()
        self.heightSpinBox.setRange(100, 2000)
        self.heightSpinBox.setValue(600)  # Default value
        self.sizeLayout.addWidget(self.heightLabel)
        self.sizeLayout.addWidget(self.heightSpinBox)

        self.layout.addLayout(self.sizeLayout)

    def setupColorConfig(self):
        self.colorConfigLayout = QHBoxLayout()  # Change to QHBoxLayout for side-by-side layout

        self.colorSettings = {
            'start_node_color': '#00FF00',  # Default green
            'end_node_color': '#FFD700',  # Default gold
            'path_color': '#0000FF',  # Default blue
            'obstacle_color': '#000000',  # Default black
            'background_color': '#FFFFFF'  # Default white
        }

        for color_key, default_color in self.colorSettings.items():
            label = QLabel(f"{color_key.replace('_', ' ').title()}:")
            swatch = QLabel()
            swatch.setStyleSheet(f"background-color: {default_color};")
            swatch.setFixedSize(50, 20)
            swatch.mousePressEvent = lambda event, key=color_key, sw=swatch: self.openColorDialog(key, sw)
            self.colorConfigLayout.addWidget(label)
            self.colorConfigLayout.addWidget(swatch)

        self.layout.addLayout(self.colorConfigLayout)  # Add the color configuration layout to the dialog's layout
    def openColorDialog(self, color_key, swatch):
        color = QColorDialog.getColor(QColor(swatch.styleSheet().split(': ')[1].split(';')[0]))
        if color.isValid():
            self.colorSettings[color_key] = color.name()
            swatch.setStyleSheet(f"background-color: {color.name()};")
    def setupMazeConfig(self):
        # Maze Size Configuration
        self.MazeSizeLayout = QHBoxLayout()
        self.MazeSizeLabel = QLabel("Maze Size:")
        self.MazeSizeLineEdit = QLineEdit()
        self.MazeSizeLineEdit.setPlaceholderText("Enter Maze size (e.g., 10)")
        self.MazeSizeLayout.addWidget(self.MazeSizeLabel)
        self.MazeSizeLayout.addWidget(self.MazeSizeLineEdit)

        # Obstacle Density Configuration
        self.obstacleDensityLayout = QHBoxLayout()
        self.obstacleDensityLabel = QLabel("Obstacle Density:")
        self.obstacleDensityLineEdit = QLineEdit()
        self.obstacleDensityLineEdit.setPlaceholderText("Enter obstacle density (0 to 1)")
        self.obstacleDensityLayout.addWidget(self.obstacleDensityLabel)
        self.obstacleDensityLayout.addWidget(self.obstacleDensityLineEdit)

        # Start and End Points Configuration
        self.startPointLayout = QHBoxLayout()
        self.startPointLabel = QLabel("Start Point (x,y):")
        self.startPointLineEdit = QLineEdit()
        self.startPointLineEdit.setPlaceholderText("Enter start point (e.g., 0,0)")
        self.startPointLayout.addWidget(self.startPointLabel)
        self.startPointLayout.addWidget(self.startPointLineEdit)

        self.endPointLayout = QHBoxLayout()
        self.endPointLabel = QLabel("End Point (x,y):")
        self.endPointLineEdit = QLineEdit()
        self.endPointLineEdit.setPlaceholderText("Enter end point (e.g., 9,9)")
        self.endPointLayout.addWidget(self.endPointLabel)
        self.endPointLayout.addWidget(self.endPointLineEdit)

        # Adding to main layout
        self.layout.addLayout(self.MazeSizeLayout)
        self.layout.addLayout(self.obstacleDensityLayout)
        self.layout.addLayout(self.startPointLayout)
        self.layout.addLayout(self.endPointLayout)

    def generate_maze(self,size, obstacle_density):
        print("Generating maze")
        maze = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if random.uniform(0, 1) < obstacle_density:
                    maze[i][j] = 1
        print(maze)
        return maze

    def setupHeuristicConfig(self):
        self.heuristicLayout = QHBoxLayout()
        self.heuristicLabel = QLabel("Heuristic:")
        self.heuristicComboBox = QComboBox()
        # Populate the combo box with heuristic options
        self.heuristicComboBox.addItem("Euclidean Distance", "euclidean")
        self.heuristicComboBox.addItem("Octile Distance", "octile")
        # Add the components to the layout
        self.heuristicLayout.addWidget(self.heuristicLabel)
        self.heuristicLayout.addWidget(self.heuristicComboBox)
        # Add the heuristic layout to the main layout
        self.layout.addLayout(self.heuristicLayout)


    def validateInputs(self):
        # Validate Maze Size
        try:
            Maze_size = int(self.MazeSizeLineEdit.text())
            if Maze_size <= 0:
                raise ValueError("Maze size must be a positive integer.")
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Maze Size Error: {e}")
            return False

        # Validate Obstacle Density
        try:
            obstacle_density = float(self.obstacleDensityLineEdit.text())
        except ValueError as e:
            if not (0 <= obstacle_density <= 1):
                QMessageBox.critical(self, "Input Error", "Obstacle Density must be a float between 0 and 1.")
                obstacle_density = 0.3  # Set to default value if validation fails


        # Validate Start and End Points
        try:
            start_point = tuple(map(int, self.startPointLineEdit.text().split(',')))
            end_point = tuple(map(int, self.endPointLineEdit.text().split(',')))
            if not (0 <= start_point[0] < Maze_size and 0 <= start_point[1] < Maze_size):
                raise ValueError("Start point is out of bounds.")
            if not (0 <= end_point[0] < Maze_size and 0 <= end_point[1] < Maze_size):
                raise ValueError("End point is out of bounds.")
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Start/End Point Error: {e}")
            return False

        return True  # All validations passed


    def useDefaultSettings(self):
        default_settings = {
            'window_width': 600,
            'window_height': 600,
            'Maze_size': 10,
            'start_point': (0, 0),
            'end_point': (9, 9),
            'obstacle_density': 0.3,
            'heuristic': 'octile',  # Assuming 'euclidean' is the default heuristic
            'start_node_color': '#00FF00',  # Default green
            'end_node_color': '#FFD700',  # Default gold
            'path_color': '#0000FF',  # Default blue
            'obstacle_color': '#000000',  # Default black
            'background_color': '#FFFFFF',  # Default white
            'maze': self.generate_maze(10, 0.1),  # Default 10x10 maze with 0.3 obstacle density
        }
        self.settings_updated.emit(default_settings)

    def MazeSetter(self):
        if self.randomMazeCheckBox.isChecked():
            maze_size = int(self.MazeSizeLineEdit.text())
            obstacle_density = float(self.obstacleDensityLineEdit.text())
            self.mazeArray = self.generate_maze(maze_size, obstacle_density)
        else:
            self.mazeArray = self.mazeArray
        return self.mazeArray

    def saveSettings(self):
        if not self.validateInputs():
            return  # Stop saving if validation fails

        start_point = tuple(map(int, self.startPointLineEdit.text().split(',')))
        end_point = tuple(map(int, self.endPointLineEdit.text().split(',')))
        obstacle_density = float(self.obstacleDensityLineEdit.text())

        settings = {
            'window_width': self.widthSpinBox.value(),
            'window_height': self.heightSpinBox.value(),
            'Maze_size': int(self.MazeSizeLineEdit.text()),
            'start_point': start_point,
            'end_point': end_point,
            'obstacle_density': obstacle_density,
            'heuristic': self.heuristicComboBox.currentData(),
            # Color settings
            'start_node_color': getattr(self, 'start_node_color', '#00FF00'),  # Default green
            'end_node_color': getattr(self, 'end_node_color', '#FFD700'),  # Default red
            'path_color': getattr(self, 'path_color', '#0000FF'),  # Default blue
            'obstacle_color': getattr(self, 'obstacle_color', '#000000'),  # Default black
            'background_color': getattr(self, 'background_color', '#FFFFFF'),  # Default white
            'maze': self.MazeSetter(),
        }
        self.settings_updated.emit(settings)
        self.accept()