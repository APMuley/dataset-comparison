import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, 
                           QTabWidget, QTextEdit, QScrollArea, QFrame, QSplitter,
                           QStatusBar, QGroupBox, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

# Import your existing calculation modules
from open_nc_file import val2val
from cat_sim import jaccard_similarity
from master import entryPoint, generate_comparison_score


import matplotlib
matplotlib.use('Qt5Agg')  # Must be set before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from visualization_code import VisualizationWidget

# Worker thread for calculations
class CalculationWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, file1, file2, order):
        super().__init__()
        self.file1 = file1
        self.file2 = file2
        self.order = order
        
    def run(self):
        try:
            avg_score, corr_list = entryPoint(self.file1, self.file2, self.order)
            avg_corr = sum(corr_list) / len(corr_list) if corr_list else 0
            
            df = pd.read_csv(self.file1)
            column_names = list(df.columns)
            result = generate_comparison_score(column_names, self.order)
            
            self.finished.emit({
                'avg_score': avg_score,
                'corr_list': corr_list,
                'avg_corr': avg_corr,
                'column_names': column_names,
                'similarity_scores': result[0],
                'correlation_data': result[1]
            })
        except Exception as e:
            self.error.emit(str(e))


class ModernFileComparator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced File Comparator")
        self.setMinimumSize(900, 700)
        
        # Set application style
        self.set_application_style()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create header
        self.create_header(main_layout)
        
        # Create content in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        # Create input section
        self.create_input_section(scroll_layout)
        
        # Create results section
        self.create_results_section(scroll_layout)
        
        # Create button section
        self.create_button_section(scroll_layout)
        
        # Add stretching space at the bottom
        scroll_layout.addStretch()
        
        # Set the scroll content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Add progress bar to status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(150)
        self.progress_bar.setMaximumHeight(15)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def set_application_style(self):
        """Set application-wide styling"""
        # Set color palette
        palette = QPalette()
        
        # Background colors
        palette.setColor(QPalette.Window, QColor("#f5f5f5"))
        palette.setColor(QPalette.WindowText, QColor("#212121"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#e8f5e9"))
        
        # Foreground colors
        palette.setColor(QPalette.Text, QColor("#212121"))
        palette.setColor(QPalette.Button, QColor("#4caf50"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        
        # Accent colors
        palette.setColor(QPalette.Highlight, QColor("#2e7d32"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        
        QApplication.setPalette(palette)
        
        # Set stylesheet for custom styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QLabel {
                color: #212121;
            }
            
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton#secondary {
                background-color: #ffffff;
                color: #4caf50;
                border: 1px solid #4caf50;
            }
            
            QPushButton#secondary:hover {
                background-color: #e8f5e9;
            }
            
            QLineEdit {
                padding: 6px;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                background-color: white;
            }
            
            QLineEdit:read-only {
                background-color: #f5f5f5;
            }
            
            QComboBox {
                padding: 6px;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                background-color: white;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2e7d32;
            }
            
            QTabWidget::pane {
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e8f5e9;
                color: #212121;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-top: 3px solid #2e7d32;
                color: #2e7d32;
                font-weight: bold;
            }
            
            QStatusBar {
                background-color: #2e7d32;
                color: white;
            }
            
            QTextEdit {
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #a5d6a7;
                selection-color: #212121;
            }
            
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 12px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                min-height: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
    
    def create_header(self, layout):
        """Create application header"""
        header_layout = QHBoxLayout()
        
        # App title
        app_title = QLabel("Advanced File Comparator")
        app_title.setFont(QFont('Arial', 18, QFont.Bold))
        app_title.setStyleSheet("color: #2e7d32;")
        
        header_layout.addWidget(app_title)
        header_layout.addStretch()
        
        # Add header layout to main layout
        layout.addLayout(header_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #4caf50;")
        layout.addWidget(separator)
    
    def create_input_section(self, layout):
        """Create input section with file selections and options"""
        input_group = QGroupBox("Input Files")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(15)
        
        # File 1 selection
        file1_layout = QHBoxLayout()
        file1_label = QLabel("File 1:")
        file1_label.setMinimumWidth(60)
        self.file1_input = QLineEdit()
        self.file1_input.setPlaceholderText("Select first CSV file...")
        file1_browse = QPushButton("Browse")
        file1_browse.clicked.connect(lambda: self.browse_file(self.file1_input))
        
        file1_layout.addWidget(file1_label)
        file1_layout.addWidget(self.file1_input)
        file1_layout.addWidget(file1_browse)
        input_layout.addLayout(file1_layout)
        
        # File 2 selection
        file2_layout = QHBoxLayout()
        file2_label = QLabel("File 2:")
        file2_label.setMinimumWidth(60)
        self.file2_input = QLineEdit()
        self.file2_input.setPlaceholderText("Select second CSV file...")
        file2_browse = QPushButton("Browse")
        file2_browse.clicked.connect(lambda: self.browse_file(self.file2_input))
        
        file2_layout.addWidget(file2_label)
        file2_layout.addWidget(self.file2_input)
        file2_layout.addWidget(file2_browse)
        input_layout.addLayout(file2_layout)
        
        # Order matters option
        order_layout = QHBoxLayout()
        order_label = QLabel("Order Matters:")
        order_label.setMinimumWidth(60)
        self.order_combo = QComboBox()
        self.order_combo.addItems(["Yes", "No"])
        
        order_layout.addWidget(order_label)
        order_layout.addWidget(self.order_combo)
        order_layout.addStretch()
        input_layout.addLayout(order_layout)
        
        layout.addWidget(input_group)
    
    def create_results_section(self, layout):
        """Create results section with summary and detail tabs"""
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        
        # Summary results
        summary_layout = QHBoxLayout()
        
        # Average score
        avg_score_layout = QHBoxLayout()
        avg_score_label = QLabel("Average Score:")
        self.avg_score_input = QLineEdit()
        self.avg_score_input.setReadOnly(True)
        
        avg_score_layout.addWidget(avg_score_label)
        avg_score_layout.addWidget(self.avg_score_input)
        
        # Average correlation
        avg_corr_layout = QHBoxLayout()
        avg_corr_label = QLabel("Average Correlation:")
        self.avg_corr_input = QLineEdit()
        self.avg_corr_input.setReadOnly(True)
        
        avg_corr_layout.addWidget(avg_corr_label)
        avg_corr_layout.addWidget(self.avg_corr_input)
        
        # Add to summary layout
        summary_layout.addLayout(avg_score_layout)
        summary_layout.addLayout(avg_corr_layout)
        
        results_layout.addLayout(summary_layout)
        
        # Create tab widget for detailed results
        self.result_tabs = QTabWidget()
        
        # Similarity details tab
        self.similarity_text = QTextEdit()
        self.similarity_text.setReadOnly(True)
        self.result_tabs.addTab(self.similarity_text, "Similarity Details")
        
        # Correlation details tab
        self.correlation_text = QTextEdit()
        self.correlation_text.setReadOnly(True)
        self.result_tabs.addTab(self.correlation_text, "Correlation Details")
        
        # Add visualization tab with the new visualization widget
        from visualization_code import VisualizationWidget
        self.visualization_widget = VisualizationWidget()
        self.result_tabs.addTab(self.visualization_widget, "Visualization")
        
        results_layout.addWidget(self.result_tabs)
        layout.addWidget(results_group)
    
    def create_button_section(self, layout):
        """Create buttons for actions"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondary")
        self.clear_button.clicked.connect(self.clear_inputs)
        
        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.calculate_button)
        
        layout.addLayout(button_layout)
    
    def browse_file(self, line_edit):
        """Open file dialog to select a CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            line_edit.setText(file_path)
            self.status_bar.showMessage(f"Selected file: {os.path.basename(file_path)}")
    
    def calculate(self):
        """Start calculation in a separate thread"""
        file1 = self.file1_input.text()
        file2 = self.file2_input.text()
        
        if not file1 or not file2:
            QMessageBox.warning(self, "Warning", "Please select both input files.")
            return
        
        # Show progress indication
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage("Calculating...")
        self.calculate_button.setEnabled(False)
        
        # Set up worker thread
        order = 0 if self.order_combo.currentText() == "Yes" else 1
        self.worker = CalculationWorker(file1, file2, order)
        self.worker.finished.connect(self.handle_results)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def handle_results(self, results):
        """Process calculation results"""
        # Update result fields
        avg_score = results.get('avg_score')
        avg_corr = results.get('avg_corr')
        
        if avg_score is not None:
            self.avg_score_input.setText(f"{avg_score:.2f}")
            self.avg_corr_input.setText(f"{avg_corr:.4f}")
            
            # Clear previous results
            self.similarity_text.clear()
            self.correlation_text.clear()
            
            # Update similarity details
            column_names = results.get('column_names', [])
            similarity_scores = results.get('similarity_scores', [])
            
            for i, score in enumerate(similarity_scores):
                if i < len(column_names):
                    self.similarity_text.append(f"{column_names[i]}: {score:.2f}%")
            
            # Update correlation details
            corr_list = results.get('corr_list', [])
            
            for i, corr in enumerate(corr_list):
                col_name = column_names[i] if i < len(column_names) else f"Column {i+1}"
                self.correlation_text.append(f"{col_name}: {corr:.2f}")
            
            # Update visualization with the data
            visualization_data = {
                'column_names': column_names,
                'similarity_scores': similarity_scores,
                'correlation_data': corr_list,
                'avg_score': avg_score,
                'avg_corr': avg_corr
            }
            self.visualization_widget.update_data(visualization_data)
            
            self.status_bar.showMessage("Calculation complete")
        else:
            self.status_bar.showMessage("Calculation failed")
        
        # Reset UI state
        self.progress_bar.setVisible(False)
        self.calculate_button.setEnabled(True)
    
    def handle_error(self, error_msg):
        """Handle calculation errors"""
        QMessageBox.critical(self, "Error", f"An error occurred during calculation:\n{error_msg}")
        self.status_bar.showMessage("Calculation failed")
        self.progress_bar.setVisible(False)
        self.calculate_button.setEnabled(True)
    
    def clear_inputs(self):
        """Clear all inputs and results"""
        self.file1_input.clear()
        self.file2_input.clear()
        self.avg_score_input.clear()
        self.avg_corr_input.clear()
        self.similarity_text.clear()
        self.correlation_text.clear()
        self.order_combo.setCurrentIndex(0)
        self.status_bar.showMessage("Ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernFileComparator()
    window.show()
    sys.exit(app.exec_())