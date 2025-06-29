import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QWidget
import pandas as pd

# Color constants
SIMILARITY_COLOR = '#4caf50'
CORRELATION_COLOR = '#2196f3'
AVG_SIM_COLOR = '#ff5722'
AVG_CORR_COLOR = '#9c27b0'
GRID_COLOR = '#e0e0e0'

class MplCanvas(FigureCanvas):
    """Canvas for matplotlib plots in PyQt5"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class VisualizationWidget(QWidget):
    """Widget for visualizations of file comparison results"""
    def __init__(self, parent=None):
        super(VisualizationWidget, self).__init__(parent)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Add controls for visualization
        control_layout = QHBoxLayout()
        
        # Visualization type selector
        vis_type_label = QLabel("Visualization Type:")
        self.vis_type_combo = QComboBox()
        self.vis_type_combo.addItems([
            "Similarity Bars", 
            "Correlation Heatmap", 
            "Column Comparison"
        ])
        self.vis_type_combo.currentIndexChanged.connect(self.update_visualization)
        
        control_layout.addWidget(vis_type_label)
        control_layout.addWidget(self.vis_type_combo)
        control_layout.addStretch()
        
        self.layout.addLayout(control_layout)
        
        # Canvas for the plot
        self.canvas = MplCanvas(self, width=8, height=6)
        self.layout.addWidget(self.canvas)
        
        # Initialize data
        self.data = {
            'column_names': [],
            'similarity_scores': [],
            'correlation_data': [],
            'avg_score': 0,
            'avg_corr': 0
        }
    
    def update_data(self, data):
        """Update visualization data"""
        self.data = data
        self.update_visualization()
    
    def update_visualization(self):
        """Update the visualization based on selected type"""
        vis_type = self.vis_type_combo.currentText()
        
        # Clear the canvas completely (not just axes)
        self.canvas.figure.clear()
        self.canvas.axes = self.canvas.figure.add_subplot(111)  # Recreate axes
        
        if not self.data['column_names']:
            self.canvas.axes.text(0.5, 0.5, "No data available", 
                                horizontalalignment='center',
                                verticalalignment='center',
                                fontsize=14, color=GRID_COLOR)
            self.canvas.draw()
            return
        
        if vis_type == "Similarity Bars":
            self._draw_similarity_bars()
        elif vis_type == "Correlation Heatmap":
            self._draw_correlation_heatmap()
        elif vis_type == "Column Comparison":
            self._draw_column_comparison()
        elif vis_type == "Similarity Distribution":
            self._draw_similarity_distribution()
        
        self.canvas.draw()

    
    def _draw_similarity_bars(self):
        """Draw bar chart for similarity scores"""
        ax = self.canvas.axes
        column_names = self.data['column_names']
        similarity_scores = self.data['similarity_scores']
        
        if len(similarity_scores) > len(column_names):
            similarity_scores = similarity_scores[:len(column_names)]
        elif len(similarity_scores) < len(column_names):
            column_names = column_names[:len(similarity_scores)]
        
        # Sort by similarity score
        sorted_indices = np.argsort(similarity_scores)
        sorted_names = [column_names[i] for i in sorted_indices]
        sorted_scores = [similarity_scores[i] for i in sorted_indices]
        
        # Create bar chart
        bars = ax.barh(sorted_names, sorted_scores, color=SIMILARITY_COLOR)
        
        # Add a line for average similarity
        avg_score = self.data['avg_score']
        ax.axvline(x=avg_score, color=AVG_SIM_COLOR, linestyle='--', linewidth=2, 
                  label=f'Avg: {avg_score:.2f}%')
        
        # Customize plot
        ax.set_xlabel('Similarity (%)')
        ax.set_ylabel('Columns')
        ax.set_title('Column Similarity Scores')
        ax.set_xlim(0, 100)
        
        # Add values to bars
        for i, v in enumerate(sorted_scores):
            ax.text(v + 1, i, f"{v:.1f}%", va='center', color='black')
        
        ax.legend()
        ax.grid(axis='x', linestyle='--', alpha=0.7, color=GRID_COLOR)
    
    def _draw_correlation_heatmap(self):
        """Draw heatmap for correlation data"""
        ax = self.canvas.axes
        column_names = self.data['column_names']
        correlation_data = self.data['correlation_data']
        
        # If correlation_data is a list (not a matrix), convert to matrix form
        if isinstance(correlation_data, list):
            corr_matrix = np.zeros((len(column_names), len(column_names)))
            for i, corr in enumerate(correlation_data):
                if i < len(column_names):
                    corr_matrix[i, i] = corr
        else:
            corr_matrix = np.array(correlation_data)
            
        # Create heatmap
        im = ax.imshow(corr_matrix, cmap='viridis', vmin=-1, vmax=1)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Correlation')
        
        # Add ticks and labels
        num_columns = min(len(column_names), corr_matrix.shape[0])
        truncated_names = [name[:15] + '...' if len(name) > 15 else name 
                         for name in column_names[:num_columns]]
        
        ax.set_xticks(np.arange(num_columns))
        ax.set_yticks(np.arange(num_columns))
        ax.set_xticklabels(truncated_names, rotation=45, ha='right')
        ax.set_yticklabels(truncated_names)
        
        # Add title
        ax.set_title('Column Correlation Heatmap')
        
        # Annotate cells
        if num_columns <= 10:  # Only annotate if not too crowded
            for i in range(num_columns):
                for j in range(num_columns):
                    if i < corr_matrix.shape[0] and j < corr_matrix.shape[1]:
                        text = ax.text(j, i, f"{corr_matrix[i, j]:.2f}",
                                     ha="center", va="center", 
                                     color="white" if abs(corr_matrix[i, j]) > 0.5 else "black")
    
    def _draw_column_comparison(self):
        """Draw comparative visualization between files"""
        ax = self.canvas.axes
        column_names = self.data['column_names']
        similarity_scores = self.data['similarity_scores']
        correlation_data = self.data['correlation_data']
        
        if len(similarity_scores) > len(column_names):
            similarity_scores = similarity_scores[:len(column_names)]
        elif len(similarity_scores) < len(column_names):
            column_names = column_names[:len(similarity_scores)]
            
        # If correlation_data is a list (not a matrix), use it directly
        if isinstance(correlation_data, list):
            corr_values = correlation_data
            if len(corr_values) > len(column_names):
                corr_values = corr_values[:len(column_names)]
            elif len(corr_values) < len(column_names):
                # Pad with zeros if needed
                corr_values = corr_values + [0] * (len(column_names) - len(corr_values))
        else:
            # If it's a matrix, extract diagonal values
            corr_values = [correlation_data[i][i] if i < len(correlation_data) and i < len(correlation_data[i]) 
                         else 0 for i in range(len(column_names))]
        
        # Create x positions for bars
        x = np.arange(len(column_names))
        width = 0.35
        
        # Create bars
        bars1 = ax.bar(x - width/2, [s for s in similarity_scores], width, label='Similarity (%)', color=SIMILARITY_COLOR)
        bars2 = ax.bar(x + width/2, [c * 100 for c in corr_values], width, label='Correlation (%)', color=CORRELATION_COLOR)
        
        # Customize plot
        ax.set_ylabel('Score (%)')
        ax.set_title('Column Comparison: Similarity vs Correlation')
        ax.set_xticks(x)
        
        # If too many columns, show only a subset of labels
        if len(column_names) > 10:
            step = len(column_names) // 10
            display_indices = range(0, len(column_names), step)
            display_names = [column_names[i] if i < len(column_names) else "" for i in display_indices]
            display_positions = [i for i in display_indices]
            ax.set_xticks(display_positions)
            ax.set_xticklabels(display_names, rotation=45, ha='right')
        else:
            ax.set_xticklabels(column_names, rotation=45, ha='right')
        
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7, color=GRID_COLOR)
        
        # Add average lines
        avg_score = self.data['avg_score']
        avg_corr = self.data['avg_corr'] * 100
        ax.axhline(y=avg_score, color=AVG_SIM_COLOR, linestyle='--', linewidth=1, 
                  label=f'Avg Sim: {avg_score:.2f}%')
        ax.axhline(y=avg_corr, color=AVG_CORR_COLOR, linestyle='--', linewidth=1, 
                  label=f'Avg Corr: {avg_corr:.2f}%')
    
