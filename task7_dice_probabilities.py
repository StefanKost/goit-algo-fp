import random
import os
import matplotlib.pyplot as plt

# Directory for saving results
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")

# Theoretical probabilities for sums of two dice
THEORETICAL_PROB = {
    total: count / 36
    for total, count in zip(range(2, 13), [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])
}


def roll_two_dice(trials: int) -> dict:
    """Simulate rolling two dice a number of times."""
    outcomes = {i: 0 for i in range(2, 13)}
    for _ in range(trials):
        dice_sum = random.randint(1, 6) + random.randint(1, 6)
        outcomes[dice_sum] += 1
    return {k: v / trials for k, v in outcomes.items()}


def print_probability_table(probabilities: dict):
    """Print comparison table of Monte Carlo vs theoretical probabilities."""
    header = f"{'Sum':<6}{'Monte Carlo (%)':<20}{'Theoretical (%)':<18}{'Difference'}"
    print(header)
    print("-" * len(header))
    for s in range(2, 13):
        mc = probabilities[s] * 100
        th = THEORETICAL_PROB[s] * 100
        diff = abs(mc - th)
        print(f"{s:<6}{mc:<20.2f}{th:<18.2f}{diff:.4f}")


def plot_probabilities(probabilities: dict, trials: int, file_path: str):
    """Plot Monte Carlo and theoretical probabilities."""
    sums = list(range(2, 13))
    mc_vals = [probabilities[s] * 100 for s in sums]
    th_vals = [THEORETICAL_PROB[s] * 100 for s in sums]

    plt.figure(figsize=(9, 5))
    plt.plot(sums, mc_vals, marker='o', label="Monte Carlo")
    plt.plot(sums, th_vals, linestyle='--', marker='s', label="Theoretical")
    plt.title(f"Dice Roll Probabilities ({trials:,} rolls)")
    plt.xlabel("Sum")
    plt.ylabel("Probability (%)")
    plt.xticks(sums)
    plt.grid(alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    trial_counts = [1_000, 10_000, 100_000, 1_000_000]

    print("Monte Carlo Simulation of Two Dice Rolls")
    print("=" * 55)

    for n in trial_counts:
        probs = roll_two_dice(n)
        output_file = os.path.join(ASSETS_FOLDER, f"dice_probs_{n}.png")
        plot_probabilities(probs, n, output_file)
        print(f"Plot saved: assets/dice_probs_{n}.png")

    # Detailed comparison for 1,000,000 rolls
    print("\nComparison table for 100,000 rolls:\n")
    final_probs = roll_two_dice(100_000)
    print_probability_table(final_probs)
