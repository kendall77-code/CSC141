from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def calculate_cost(self):
        pass


class ByWeightItem(Item):
    def __init__(self, name, weight, cost_per_pound):
        super().__init__(name)
        self._weight = float(weight)
        self._cost_per_pound = float(cost_per_pound)

    @property
    def weight(self):
        return self._weight

    @property
    def cost_per_pound(self):
        return self._cost_per_pound

    def calculate_cost(self):
        return self._weight * self._cost_per_pound


class ByQuantityItem(Item):
    def __init__(self, name, quantity, cost_each):
        super().__init__(name)
        self._quantity = int(quantity)
        self._cost_each = float(cost_each)

    @property
    def quantity(self):
        return self._quantity

    @property
    def cost_each(self):
        return self._cost_each

    def calculate_cost(self):
        return self._quantity * self._cost_each


class Grapes(ByWeightItem):
    def __init__(self, weight):
        super().__init__("Grapes", weight, 2.79)


class Bananas(ByWeightItem):
    def __init__(self, weight):
        super().__init__("Bananas", weight, 0.69)


class Oranges(ByQuantityItem):
    def __init__(self, quantity):
        super().__init__("Oranges", quantity, 0.85)


class Cantaloupes(ByQuantityItem):
    def __init__(self, quantity):
        super().__init__("Cantaloupes", quantity, 3.49)


class Order:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def calculate_total(self):
        return sum(item.calculate_cost() for item in self._items)

    def get_items(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)


order = Order()
order.add_item(Grapes(2.5))
order.add_item(Bananas(4.0))
order.add_item(Oranges(6))
order.add_item(Cantaloupes(2))

print("Receipt")
print("-" * 32)

for item in order.get_items():
    print(f"{item.name:<14} ${item.calculate_cost():>7.2f}")

print("-" * 32)
print(f"Total:          ${order.calculate_total():>7.2f}")
print(f"Item count:      {len(order)}")
