import heapq
import math
import random
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Patch
import networkx as nx


class StarWarsGalaxy:
    """Holomap of Major Hyperspace Routes in the Star Wars Galaxy"""

    # Hyperspace routes grouped by regions
    ROUTES = {
        "Core Hyperlane": [
            "Coruscant", "Brentaal", "Alderaan",
            "Chandrila", "Kuat", "Hosnian Prime"
        ],
        "Outer Rim Trail": [
            "Tatooine", "Ryloth", "Geonosis",
            "Mandalore", "Florrum", "Lothal"
        ],
        "Mid Rim Corridor": [
            "Kashyyyk", "Felucia", "Batuu",
            "Crait", "Dagobah", "Nal Hutta"
        ]
    }

    # Special crossing hyperspace nodes
    JUNCTIONS = [
        ("Kuat", "Mandalore"),
        ("Felucia", "Geonosis"),
        ("Batuu", "Lothal"),
    ]

    ROUTE_COLORS = {
        "Core Hyperlane": "#00CFFF",      # Cyan-Blue holo line
        "Outer Rim Trail": "#FFAE00",     # Amber hyperspace path
        "Mid Rim Corridor": "#9BFF70",    # Soft green nebula line
    }

    PLANET_SIZES = {
        "Coruscant": 1200,  # capital of the Galaxy
        "Alderaan": 900,
        "Chandrila": 800,
        "Kuat": 850,
        "Hosnian Prime": 700,
        "Brentaal": 600,
        "Tatooine": 500,
        "Ryloth": 450,
        "Geonosis": 400,
        "Mandalore": 550,
        "Florrum": 350,
        "Lothal": 300,
        "Kashyyyk": 750,
        "Felucia": 500,
        "Batuu": 400,
        "Crait": 350,
        "Dagobah": 300,
        "Nal Hutta": 600,
        "junction": 450
    }

    WEIGHTS = {
        # Core Hyperlane
        ("Coruscant", "Brentaal"): 3,
        ("Brentaal", "Alderaan"): 3,
        ("Alderaan", "Chandrila"): 4,
        ("Chandrila", "Kuat"): 5,
        ("Kuat", "Hosnian Prime"): 5,

        # Outer Rim Trail
        ("Tatooine", "Ryloth"): 2,
        ("Ryloth", "Geonosis"): 4,
        ("Geonosis", "Mandalore"): 2,
        ("Mandalore", "Florrum"): 7,
        ("Florrum", "Lothal"): 6,

        # Mid Rim Corridor
        ("Kashyyyk", "Felucia"): 1,
        ("Felucia", "Batuu"): 6,
        ("Batuu", "Crait"): 5,
        ("Crait", "Dagobah"): 4,
        ("Dagobah", "Nal Hutta"): 5,

        # Junctions (transfer hyperspace links)
        ("Kuat", "Mandalore"): 6,
        ("Felucia", "Geonosis"): 5,
        ("Batuu", "Lothal"): 5,
    }

    def __init__(self):
        self.graph = nx.Graph()
        self._construct()

    # GRAPH CONSTRUCTION
    def _construct(self):
        """Build the galactic network graph."""
        for route_name, planets in self.ROUTES.items():
            for a, b in zip(planets, planets[1:]):
                self.graph.add_edge(a, b, route=route_name)

        for p1, p2 in self.JUNCTIONS:
            self.graph.add_edge(p1, p2, route="junction")

        # Add weights
        for (u, v), weight in self.WEIGHTS.items():
            if self.graph.has_edge(u, v):
                self.graph[u][v]["weight"] = weight

    # GRAPH ANALYSIS
    def statistics(self):
        """Return major structural stats about the hyperspace map."""
        degree_map = dict(self.graph.degree())
        central = max(degree_map, key=degree_map.get)

        return {
            "planet_count": self.graph.number_of_nodes(),
            "routes_count": self.graph.number_of_edges(),
            "avg_connections": sum(degree_map.values()) / len(degree_map),
            "density": nx.density(self.graph),
            "is_connected": nx.is_connected(self.graph),
            "main_hub": central,
            "hub_links": degree_map[central],
        }

    # POSITIONING SYSTEM
    def _cosmic_positions(self):
        """
        Spiral galaxy placement with gravitational pull
        for hyperspace transfer pairs so they stay close.
        """
        pos = {}
        arms = len(self.ROUTES)
        arm_spread = 0.45
        noise = 0.25

        # 1. Create raw spiral-arm layout
        for arm_index, (route_name, planets) in enumerate(self.ROUTES.items()):
            for i, planet in enumerate(planets):
                radius = 1.5 + i * 1.3
                angle = (arm_index * (2 * math.pi / arms)) + i * 0.55

                x = radius * math.cos(angle)
                y = radius * math.sin(angle)

                x += random.uniform(-noise, noise) * radius * arm_spread
                y += random.uniform(-noise, noise) * radius * arm_spread

                pos[planet] = (x, y)

        # 2. Apply gravitational pull between junction planets
        for a, b in self.JUNCTIONS:
            if a in pos and b in pos:
                ax, ay = pos[a]
                bx, by = pos[b]

                # midpoint between the two planets
                mid_x = (ax + bx) / 2
                mid_y = (ay + by) / 2

                # pull both planets toward the midpoint
                pull_strength = 0.55

                pos[a] = (
                    ax + (mid_x - ax) * pull_strength,
                    ay + (mid_y - ay) * pull_strength
                )
                pos[b] = (
                    bx + (mid_x - bx) * pull_strength,
                    by + (mid_y - by) * pull_strength
                )

        return pos

    # VISUALIZATION
    def render(self, save=None, highlight_path: list[str] | None = None):
        """Draw Star Wars galactic map without arrows, white background, fixed planet sizes."""

        plt.style.use("default")
        plt.figure(figsize=(14, 14))
        plt.title(
            "Star Wars Galactic Map — Hyperspace Routes",
            fontsize=18,
            color="black",
            fontweight="bold",
        )

        # Show total distance
        if highlight_path and len(highlight_path) > 1:
            total_distance = sum(
                self.graph[u][v].get("weight", 1)
                for u, v in zip(highlight_path[:-1], highlight_path[1:])
            )

            plt.text(
                0.5, 0.98,
                f"Total distance of selected route: {total_distance}",
                transform=plt.gca().transAxes,
                fontsize=12,
                fontweight="bold",
                color="magenta",
                horizontalalignment="center"
            )

        pos = self._cosmic_positions()

        # Planet sizes based on PLANET_SIZES
        planet_sizes = []
        for planet in self.graph.nodes():
            if planet in [j[0] for j in self.JUNCTIONS] or planet in [j[1] for j in self.JUNCTIONS]:
                size = self.PLANET_SIZES["junction"]
            else:
                size = self.PLANET_SIZES.get(planet, 400)
            planet_sizes.append(size)

        # Draw edges
        for u, v, data in self.graph.edges(data=True):
            route = data["route"]
            color = "#555555" if route == "junction" else self.ROUTE_COLORS[route]
            weight = data.get("weight", 1)

            # Glow effect
            nx.draw_networkx_edges(
                self.graph, pos,
                edgelist=[(u, v)],
                width=7, alpha=0.15,
                edge_color=color
            )

            # Main line
            nx.draw_networkx_edges(
                self.graph, pos,
                edgelist=[(u, v)],
                width=2.8, alpha=0.9,
                edge_color=color
            )

            # Show weight
            x = (pos[u][0] + pos[v][0]) / 2
            y = (pos[u][1] + pos[v][1]) / 2
            plt.text(x, y, str(weight), fontsize=8, fontweight="bold", color="#000000",
                     horizontalalignment='center', verticalalignment='center')

        # Draw planets
        nx.draw_networkx_nodes(
            self.graph, pos,
            node_color="#A0C4FF",
            edgecolors="#000000",
            linewidths=1.6,
            node_size=planet_sizes
        )

        # Labels
        nx.draw_networkx_labels(
            self.graph, pos,
            font_size=9,
            font_weight="bold",
            font_color="#000000",
            labels={n:n for n in self.graph.nodes()},
            verticalalignment="center",
            horizontalalignment="center",
        )

        # Highlight a selected path if provided
        if highlight_path and len(highlight_path) > 1:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
            nx.draw_networkx_edges(
                self.graph, pos,
                edgelist=path_edges,
                width=3,
                edge_color="magenta",
                style="solid"
            )

        ax = plt.gca()
        for text in ax.texts:
            text.set_path_effects([pe.Stroke(linewidth=2, foreground="white"), pe.Normal()])

        # Generate Route Legends
        legend_elements = [
            Patch(facecolor=color, edgecolor="black", label=name)
            for name, color in self.ROUTE_COLORS.items()
        ]
        # Junction Legend
        legend_elements.append(Patch(facecolor="#555555", edgecolor="black", label="Junction", linestyle="--"))
        if highlight_path:
            legend_elements.append(Patch(facecolor="magenta", edgecolor="black", label="Selected Route"))

        plt.legend(handles=legend_elements, loc="upper left", fontsize=12)

        plt.axis("off")
        plt.tight_layout()

        if save:
            plt.savefig(save, dpi=220, bbox_inches="tight", facecolor="white")
        plt.show()


class Dijkstra:
    """Dijkstra algorithm for weighted galaxy graph"""

    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def shortest_path(self, start: str, goal: str) -> tuple[list[str], int]:
        distances = {node: float("inf") for node in self.graph.nodes}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes}

        heap = [(0, start)]
        visited = set()

        while heap:
            current_dist, current = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                break

            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                weight = self.graph[current][neighbor].get("weight", 1)
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(heap, (distance, neighbor))

        # Reconstruct path
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = previous[cur]
        path.reverse()
        return path, distances[goal]

    def all_paths(self) -> dict:
        nodes = list(self.graph.nodes)
        results = {}
        for start in nodes:
            results[start] = {}
            for goal in nodes:
                if start != goal:
                    path, distance = self.shortest_path(start, goal)
                    results[start][goal] = {"path": path, "distance": distance}
        return results


if __name__ == "__main__":
    galaxy = StarWarsGalaxy()
    dijkstra = Dijkstra(galaxy.graph)

    stats = galaxy.statistics()
    print("\n🔷 STAR WARS HYPERSPACE NETWORK ANALYSIS 🔷\n")
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    # Available routes
    routes = [
        ("Coruscant", "Dagobah"),
        ("Tatooine", "Kuat"),
        ("Felucia", "Hosnian Prime"),
        ("Kashyyyk", "Alderaan"),
        ("Batuu", "Hosnian Prime"),
    ]

    print("\nChoose a route to highlight:")
    for i, (start, goal) in enumerate(routes, 1):
        print(f"{i}. {start} -> {goal}")
    print("6. None")

    choice = 0
    while choice < 1 or choice > len(routes) + 1:
        try:
            choice = int(input("Enter number (1-6): "))
        except ValueError:
            continue

    path = []
    try:
        start, goal = routes[choice - 1]
        path, distance = dijkstra.shortest_path(start, goal)
        print(f"\nSelected route: {start} -> {goal}")
        print(f"Distance (sum of weights): {distance}")
        print(f"Path: {' -> '.join(path)}")
    except IndexError:
        pass

    galaxy.render(None, path)
