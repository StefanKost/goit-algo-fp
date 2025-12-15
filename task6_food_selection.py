ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


def greedy_algorithm(items, budget):
    # Sort by ratio descending
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True
    )

    selected = []
    total_cost = 0
    total_calories = 0

    for name, info in sorted_items:
        if total_cost + info["cost"] <= budget:
            selected.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]

    return selected, total_calories


def dynamic_programming(items, budget):
    food_names = list(items.keys())
    num_items = len(food_names)

    table = [[0] * (budget + 1) for _ in range(num_items + 1)]

    for item_index in range(1, num_items + 1):
        food_name = food_names[item_index - 1]
        food_cost = items[food_name]["cost"]
        food_calories = items[food_name]["calories"]

        for money in range(budget + 1):
            without_this_food = table[item_index - 1][money]

            if food_cost <= money:
                remaining_money = money - food_cost
                with_this_food = table[item_index - 1][remaining_money] + food_calories
            else:
                with_this_food = 0

            table[item_index][money] = max(without_this_food, with_this_food)

    selected = []
    remaining_budget = budget
    for item_index in range(num_items, 0, -1):
        calories_with_item = table[item_index][remaining_budget]
        calories_without_item = table[item_index - 1][remaining_budget]

        if calories_with_item != calories_without_item:
            food_name = food_names[item_index - 1]
            selected.append(food_name)
            remaining_budget -= items[food_name]["cost"]

    return selected, table[num_items][budget]


if __name__ == "__main__":
    balance = 115

    print("-" * 55)
    print(f"Balance: {balance}")
    print("-" * 55)

    greedy_items, greedy_cal = greedy_algorithm(ITEMS, balance)
    print(f"\nGreedy Algorithm:")
    print(f" -> Food: {greedy_items}")
    print(f" -> Total calories: {greedy_cal}")
    print(f" -> Cost: {sum(ITEMS[i]['cost'] for i in greedy_items)}")

    dp_items, dp_cal = dynamic_programming(ITEMS, balance)
    print(f"\nDynamic Programming:")
    print(f" -> Food: {dp_items}")
    print(f" -> Total calories: {dp_cal}")
    print(f" -> Cost: {sum(ITEMS[i]['cost'] for i in dp_items)}")