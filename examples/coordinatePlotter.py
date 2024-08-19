import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
from collections import deque
import threading

class CoordinatePlotter:
    def __init__(self, x_range=(-10, 10), y_range=(-10, 10), figsize=(7, 7), grid=True, point_style='o', dpi=100, max_points=300):
        """
        CoordinatePlotter class is designed to plot incoming two-dimensional coordinates on a graph in real-time.

        :param x_range: Range of x-axis, tuple (min, max)
        :param y_range: Range of y-axis, tuple (min, max)
        :param figsize: Size of the figure, tuple (width, height)
        :param grid: Boolean to determine if the grid should be displayed
        :param point_style: Style of the points, matplotlib style code
        :param dpi: Pixel density
        :param max_points: Maximum number of points to display
        """
        self.x_range = x_range
        self.y_range = y_range
        self.figsize = figsize
        self.grid = grid
        self.point_style = point_style
        self.dpi = dpi
        self.max_points = max_points
        self.coordinates = deque(maxlen=max_points)  # Use deque to hold coordinates with a maximum length
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        self.points, = self.ax.plot([], [], self.point_style)
        self.lock = threading.Lock()  # Lock to prevent data races
        self.setup_plot()

    def setup_plot(self):
        """Sets up the initial configuration of the plot."""
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim(self.y_range)
        if self.grid:
            self.ax.grid(True, linestyle='--', linewidth=0.5, color='gray')

    def update_plot(self, frame):
        """
        Updates the plot. Draws the latest incoming coordinate data.

        :param frame: Index of the coordinate data (not used, but required)
        """
        with self.lock:  # Lock during access
            if self.coordinates:
                x_data, y_data = zip(*self.coordinates)
                self.points.set_data(x_data, y_data)
        return self.points,

    def add_coordinate(self, x, y):
        """
        Adds a new coordinate to the queue.

        :param x: x-coordinate
        :param y: y-coordinate
        """
        with self.lock:  # Lock during access
            self.coordinates.append((x, y))

    def animate(self, update_interval=10):
        """
        Starts the animation and continuously updates as new data arrives.

        :param update_interval: Time between each frame (milliseconds)
        """
        anim = animation.FuncAnimation(
            self.fig,
            self.update_plot,
            interval=update_interval,
            blit=True,
            cache_frame_data=False  # Disable caching of frame data
        )
        plt.show()
        
    def __enter__(self):
        print('CoordinatePlotter INIT')
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('CoordinatePlotter EXIT')


""" RANDOM COORDINATE PLOT TEST """
"""
with CoordinatePlotter(x_range=(-10, 10), y_range=(-10, 10), max_points=50) as plotter:
	def simulate_real_time_data(plotter, duration=400):
		start_time = time.time()
		while time.time() - start_time < duration:
			x, y = random.uniform(-10, 10), random.uniform(-10, 10)
			plotter.add_coordinate(x, y)
			time.sleep(0.5)

	# Create a thread to start the real-time data simulation
	thread = threading.Thread(target=simulate_real_time_data, args=(plotter,))
	thread.start()

	# Start the animation
	plotter.animate(update_interval = 1)

	# Wait for the thread (Optional, you can remove it if you want the main program to continue)
	thread.join()
"""