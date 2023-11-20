import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

from ..utils.log_manager import get_logger

logger = get_logger(__name__)


class PlotManager:
    def __init__(self, config):
        """
        Initialize a PlotManager object with default plotting attributes.
        """
        self.plot_directory = config.plot_directory
        self.plot_directory.mkdir(parents=True, exist_ok=True)

        self.figsize = (8, 6)
        self.dpi = 300
        self.style = 'default'
        self.grid = True
        self.wide_format = True

        self.apply_matplotlib()

    def apply_matplotlib(self):
        """
        Apply specified attributes to matplotlib plots.
        """
        plt.rcParams['figure.figsize'] = self.figsize
        plt.rcParams['axes.grid'] = self.grid
        plt.rcParams['savefig.dpi'] = self.dpi

    def apply_plotly(self):
        """Anwenden der festgelegten Attribute auf den Plot für Plotly"""
        layout = go.Layout()
        if self.figsize:
            layout.update(dict(width=self.figsize[0], height=self.figsize[1]))
        if self.grid:
            layout.update(dict(showgrid=self.grid))

    def save_plot(self, fig, filename, subdir=None, format='jpg', auto_close=True):
        """
        Save a plot and optionally close it.

        Parameters:
            fig: The figure object to save.
            filename (str): The name of the file.
            subdir (str, optional): The subdirectory in which to save the file.
            format (str, optional): The format to save the figure.
            auto_close (bool, optional): Automatically close the plot after saving. Only for matplotlob.
        """
        dir_path = self.get_dir_path(subdir)

        if isinstance(fig, go.Figure):
            full_path = dir_path / f"{filename}.html"
            pio.write_html(fig, str(full_path))
        else:
            full_path = dir_path / f"{filename}.{format}"
            fig.savefig(str(full_path), dpi=self.dpi)
            if auto_close:
                self.close_plot(fig)

    def close_plot(self, fig):
        """
        Closes the given matplotlib figure.

        Parameters:
            fig (matplotlib.figure.Figure): The figure to close.
        """
        try:
            plt.close(fig)
        except Exception as e:
            logging.error(f"Failed to close plot: {e}")

    def get_dir_path(self, subdir=None):
        """
        Get directory path for saving a plot. Create subdirectory if it doesn't exist.

        Parameters:
            subdir (str, optional): Subdirectory name.

        Returns:
            dir_path (Path): Directory path.
        """
        if subdir:
            dir_path = self.plot_directory / subdir
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            dir_path = self.plot_directory

        return dir_path
