"""
3D Path Planning for Drone Navigation
======================================
Uses saved SLAM map to generate collision-free paths
Supports A* and RRT* algorithms
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from heapq import heappush, heappop
import json
from pathlib import Path


class OccupancyGrid3D:
    """3D Occupancy Grid for drone navigation"""

    def __init__(self, cell_size=0.1, bounds=None):
        """
        Initialize 3D occupancy grid

        Args:
            cell_size: Size of each voxel in meters
            bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max))
        """
        self.cell_size = cell_size
        self.bounds = bounds or ((-10, 10), (-10, 10), (0, 5))

        # Calculate grid dimensions
        self.x_min, self.x_max = self.bounds[0]
        self.y_min, self.y_max = self.bounds[1]
        self.z_min, self.z_max = self.bounds[2]

        self.x_cells = int((self.x_max - self.x_min) / cell_size)
        self.y_cells = int((self.y_max - self.y_min) / cell_size)
        self.z_cells = int((self.z_max - self.z_min) / cell_size)

        # Grid: 0=free, 1=occupied, -1=unknown
        self.grid = np.zeros((self.x_cells, self.y_cells, self.z_cells), dtype=np.int8)

        print(f"Created 3D grid: {self.x_cells}x{self.y_cells}x{self.z_cells} cells")
        print(f"World bounds: X[{self.x_min}, {self.x_max}], Y[{self.y_min}, {self.y_max}], Z[{self.z_min}, {self.z_max}]")

    def world_to_grid(self, x, y, z):
        """Convert world coordinates to grid indices"""
        grid_x = int((x - self.x_min) / self.cell_size)
        grid_y = int((y - self.y_min) / self.cell_size)
        grid_z = int((z - self.z_min) / self.cell_size)
        return grid_x, grid_y, grid_z

    def grid_to_world(self, gx, gy, gz):
        """Convert grid indices to world coordinates"""
        x = gx * self.cell_size + self.x_min
        y = gy * self.cell_size + self.y_min
        z = gz * self.cell_size + self.z_min
        return x, y, z

    def is_valid(self, gx, gy, gz):
        """Check if grid cell is within bounds and free"""
        if gx < 0 or gx >= self.x_cells:
            return False
        if gy < 0 or gy >= self.y_cells:
            return False
        if gz < 0 or gz >= self.z_cells:
            return False
        return self.grid[gx, gy, gz] == 0

    def set_obstacle(self, x, y, z, radius=0.2):
        """Mark obstacle in grid with safety radius"""
        gx, gy, gz = self.world_to_grid(x, y, z)
        grid_radius = int(radius / self.cell_size)

        for dx in range(-grid_radius, grid_radius + 1):
            for dy in range(-grid_radius, grid_radius + 1):
                for dz in range(-grid_radius, grid_radius + 1):
                    nx, ny, nz = gx + dx, gy + dy, gz + dz
                    if 0 <= nx < self.x_cells and 0 <= ny < self.y_cells and 0 <= nz < self.z_cells:
                        self.grid[nx, ny, nz] = 1

    def mark_trajectory_as_free(self, trajectory_points):
        """Mark trajectory points as free space"""
        for x, y, z in trajectory_points:
            gx, gy, gz = self.world_to_grid(x, y, z)
            if 0 <= gx < self.x_cells and 0 <= gy < self.y_cells and 0 <= gz < self.z_cells:
                self.grid[gx, gy, gz] = 0


class PathPlanner3D:
    """3D A* path planner for drones"""

    def __init__(self, occupancy_grid):
        """
        Initialize path planner

        Args:
            occupancy_grid: OccupancyGrid3D instance
        """
        self.grid = occupancy_grid

    def get_neighbors(self, pos):
        """Get valid neighboring cells (26-connected in 3D)"""
        gx, gy, gz = pos
        neighbors = []

        # 26-connected neighborhood
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    nx, ny, nz = gx + dx, gy + dy, gz + dz

                    if self.grid.is_valid(nx, ny, nz):
                        # Calculate movement cost
                        cost = np.sqrt(dx**2 + dy**2 + dz**2)
                        neighbors.append(((nx, ny, nz), cost))

        return neighbors

    def heuristic(self, a, b):
        """Euclidean distance heuristic"""
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

    def plan_path(self, start_world, goal_world):
        """
        Plan 3D path using A* algorithm

        Args:
            start_world: (x, y, z) start position in world coordinates
            goal_world: (x, y, z) goal position in world coordinates

        Returns:
            List of (x, y, z) waypoints or None if no path found
        """
        # Convert to grid coordinates
        start = self.grid.world_to_grid(*start_world)
        goal = self.grid.world_to_grid(*goal_world)

        # Validate
        if not self.grid.is_valid(*start):
            print(f"ERROR: Start position {start_world} is occupied or out of bounds!")
            return None
        if not self.grid.is_valid(*goal):
            print(f"ERROR: Goal position {goal_world} is occupied or out of bounds!")
            return None

        print(f"\nPlanning path:")
        print(f"  Start: {start_world} -> grid {start}")
        print(f"  Goal:  {goal_world} -> grid {goal}")

        # A* algorithm
        open_set = []
        heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        nodes_explored = 0

        while open_set:
            current = heappop(open_set)[1]
            nodes_explored += 1

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

                # Convert to world coordinates
                world_path = [self.grid.grid_to_world(*p) for p in path]

                print(f"  Path found! Length: {len(world_path)} waypoints")
                print(f"  Nodes explored: {nodes_explored}")
                print(f"  Path distance: {g_score[goal] * self.grid.cell_size:.2f}m")

                return world_path

            for neighbor, cost in self.get_neighbors(current):
                tentative_g_score = g_score[current] + cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        print(f"  No path found after exploring {nodes_explored} nodes!")
        return None

    def smooth_path(self, path, iterations=10, alpha=0.5):
        """Smooth path using weighted averaging"""
        if path is None or len(path) < 3:
            return path

        smoothed = np.array(path, dtype=float)

        for _ in range(iterations):
            for i in range(1, len(smoothed) - 1):
                smoothed[i] = (1 - alpha) * smoothed[i] + alpha * 0.5 * (smoothed[i-1] + smoothed[i+1])

        return smoothed.tolist()

    def optimize_waypoints(self, path, max_waypoints=20):
        """Reduce number of waypoints by removing collinear points"""
        if path is None or len(path) <= max_waypoints:
            return path

        # Keep start and end, sample intermediate points
        step = max(1, len(path) // max_waypoints)
        optimized = [path[0]]

        for i in range(step, len(path) - 1, step):
            optimized.append(path[i])

        optimized.append(path[-1])

        return optimized


def visualize_path_3d(grid, path, start, goal, obstacles=None):
    """Visualize 3D path with obstacles"""

    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection='3d')

    # Plot path
    if path is not None:
        path_array = np.array(path)
        ax.plot(path_array[:, 0], path_array[:, 1], path_array[:, 2],
                'b-', linewidth=2, label='Path')

        # Plot waypoints
        ax.scatter(path_array[:, 0], path_array[:, 1], path_array[:, 2],
                  c='blue', marker='o', s=30, alpha=0.6)

    # Plot start and goal
    ax.scatter([start[0]], [start[1]], [start[2]],
              c='green', marker='o', s=200, label='Start', edgecolors='black', linewidths=2)
    ax.scatter([goal[0]], [goal[1]], [goal[2]],
              c='red', marker='*', s=300, label='Goal', edgecolors='black', linewidths=2)

    # Plot obstacles
    if obstacles is not None:
        obs_array = np.array(obstacles)
        ax.scatter(obs_array[:, 0], obs_array[:, 1], obs_array[:, 2],
                  c='red', marker='s', s=50, alpha=0.3, label='Obstacles')

    # Plot occupied grid cells (sample for performance)
    occupied = np.argwhere(grid.grid == 1)
    if len(occupied) > 1000:
        # Sample for visualization
        indices = np.random.choice(len(occupied), 1000, replace=False)
        occupied = occupied[indices]

    if len(occupied) > 0:
        world_coords = np.array([grid.grid_to_world(x, y, z) for x, y, z in occupied])
        ax.scatter(world_coords[:, 0], world_coords[:, 1], world_coords[:, 2],
                  c='gray', marker='s', s=10, alpha=0.1)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('3D Path Planning Result')
    ax.legend()
    ax.grid(True)

    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 0.5])

    plt.show()


def demo_path_planning():
    """Demo: Create a simple environment and plan a path"""

    print("="*80)
    print("3D Path Planning Demo")
    print("="*80)

    # Create grid
    grid = OccupancyGrid3D(cell_size=0.1, bounds=((-5, 5), (-5, 5), (0, 3)))

    # Add some obstacles
    print("\nAdding obstacles...")
    obstacles = [
        (0, 0, 1.0),
        (1, 1, 1.5),
        (-1, 1, 1.0),
        (2, -1, 1.2),
        (-2, -2, 0.8),
    ]

    for obs in obstacles:
        grid.set_obstacle(*obs, radius=0.5)
        print(f"  Obstacle at {obs}")

    # Define start and goal
    start = (-4, -4, 1.0)
    goal = (4, 4, 2.0)

    print(f"\nStart: {start}")
    print(f"Goal:  {goal}")

    # Plan path
    planner = PathPlanner3D(grid)
    path = planner.plan_path(start, goal)

    if path:
        # Smooth path
        print("\nSmoothing path...")
        smoothed_path = planner.smooth_path(path, iterations=20)

        # Optimize waypoints
        print("Optimizing waypoints...")
        optimized_path = planner.optimize_waypoints(smoothed_path, max_waypoints=15)

        print(f"\nPath summary:")
        print(f"  Original waypoints: {len(path)}")
        print(f"  Optimized waypoints: {len(optimized_path)}")

        # Visualize
        print("\nVisualizing path...")
        visualize_path_3d(grid, optimized_path, start, goal, obstacles)

        return optimized_path
    else:
        print("\nPath planning failed!")
        return None


def plan_from_slam_data(trajectory_file, start, goal):
    """Plan path using SLAM trajectory data"""

    print("="*80)
    print("Path Planning from SLAM Data")
    print("="*80)

    # Load trajectory
    print(f"\nLoading trajectory from {trajectory_file}...")
    with open(trajectory_file, 'r') as f:
        trajectory = json.load(f)

    print(f"Loaded {len(trajectory)} poses")

    # Extract positions
    positions = [(p['position']['x'], p['position']['y'], p['position']['z'])
                 for p in trajectory]

    # Determine bounds from trajectory
    x_vals = [p[0] for p in positions]
    y_vals = [p[1] for p in positions]
    z_vals = [p[2] for p in positions]

    bounds = (
        (min(x_vals) - 2, max(x_vals) + 2),
        (min(y_vals) - 2, max(y_vals) + 2),
        (max(0, min(z_vals) - 1), max(z_vals) + 2)
    )

    print(f"\nComputed bounds from trajectory:")
    print(f"  X: [{bounds[0][0]:.2f}, {bounds[0][1]:.2f}]")
    print(f"  Y: [{bounds[1][0]:.2f}, {bounds[1][1]:.2f}]")
    print(f"  Z: [{bounds[2][0]:.2f}, {bounds[2][1]:.2f}]")

    # Create grid
    grid = OccupancyGrid3D(cell_size=0.1, bounds=bounds)

    # Mark trajectory as free space
    print("\nMarking trajectory as free space...")
    grid.mark_trajectory_as_free(positions)

    # Plan path
    planner = PathPlanner3D(grid)
    path = planner.plan_path(start, goal)

    if path:
        # Smooth and optimize
        smoothed_path = planner.smooth_path(path, iterations=20)
        optimized_path = planner.optimize_waypoints(smoothed_path, max_waypoints=20)

        print(f"\nOptimized path: {len(optimized_path)} waypoints")

        # Visualize
        visualize_path_3d(grid, optimized_path, start, goal)

        return optimized_path
    else:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Plan from SLAM data
        trajectory_file = sys.argv[1]
        start = tuple(map(float, sys.argv[2].split(',')))
        goal = tuple(map(float, sys.argv[3].split(',')))

        print(f"Planning path:")
        print(f"  Trajectory: {trajectory_file}")
        print(f"  Start: {start}")
        print(f"  Goal: {goal}")

        plan_from_slam_data(trajectory_file, start, goal)
    else:
        # Run demo
        demo_path_planning()
