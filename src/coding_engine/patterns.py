from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type
from dataclasses import dataclass


@dataclass
class PatternInfo:
    name: str
    category: str
    description: str
    use_cases: List[str]
    template: str


class DesignPattern(ABC):
    @abstractmethod
    def get_info(self) -> PatternInfo:
        pass

    @abstractmethod
    def generate_code(self, **kwargs) -> str:
        pass


class Singleton(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Singleton",
            category="Creational",
            description="Ensures a class has only one instance and provides a global point of access to it.",
            use_cases=[
                "Database connections",
                "Configuration managers",
                "Logging services",
            ],
            template="""class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance"""
        )

    def generate_code(self, **kwargs) -> str:
        class_name = kwargs.get("class_name", "Singleton")
        thread_safe = kwargs.get("thread_safe", False)

        if thread_safe:
            return f"""import threading

class {class_name}:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance"""
        else:
            return f"""class {class_name}:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance"""


class FactoryMethod(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Factory Method",
            category="Creational",
            description="Defines an interface for creating an object, but lets subclasses decide which class to instantiate.",
            use_cases=[
                "UI component creation",
                "Document generators",
                "Plugin systems",
            ],
            template="""class Product(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteProduct(Product):
    def operation(self):
        return "ConcreteProduct operation"

class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        pass

    def some_operation(self):
        return self.factory_method().operation()

class ConcreteCreator(Creator):
    def factory_method(self) -> Product:
        return ConcreteProduct()"""
        )

    def generate_code(self, **kwargs) -> str:
        product_name = kwargs.get("product_name", "Product")
        creator_name = kwargs.get("creator_name", "Creator")
        num_products = kwargs.get("num_products", 2)

        products = "\n".join([
            f"""class ConcreteProduct{i}({product_name}):
    def operation(self):
        return "ConcreteProduct{i} operation\""""
            for i in range(1, num_products + 1)
        ])

        creators = "\n".join([
            f"""class ConcreteCreator{i}(Creator):
    def factory_method(self) -> {product_name}:
        return ConcreteProduct{i}()"""
            for i in range(1, num_products + 1)
        ])

        return f"""from abc import ABC, abstractmethod

class {product_name}(ABC):
    @abstractmethod
    def operation(self):
        pass

{products}

class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> {product_name}:
        pass

    def some_operation(self):
        return self.factory_method().operation()

{creators}"""


class AbstractFactory(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Abstract Factory",
            category="Creational",
            description="Provides an interface for creating families of related or dependent objects without specifying their concrete classes.",
            use_cases=[
                "Cross-platform UI toolkits",
                "Database access layers",
                "Document exporters",
            ],
            template="""class AbstractProductA(ABC):
    @abstractmethod
    def operation_a(self):
        pass

class AbstractProductB(ABC):
    @abstractmethod
    def operation_b(self):
        pass

class ConcreteProductA1(AbstractProductA):
    def operation_a(self):
        return "ProductA1"

class ConcreteProductB1(AbstractProductB):
    def operation_b(self):
        return "ProductB1"

class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass"""
        )

    def generate_code(self, **kwargs) -> str:
        factory_name = kwargs.get("factory_name", "Factory")
        family = kwargs.get("family", "1")

        return f"""from abc import ABC, abstractmethod

class AbstractProductA(ABC):
    @abstractmethod
    def operation_a(self):
        pass

class AbstractProductB(ABC):
    @abstractmethod
    def operation_b(self):
        pass

class ConcreteProductA{family}(AbstractProductA):
    def operation_a(self):
        return "ProductA{family}"

class ConcreteProductB{family}(AbstractProductB):
    def operation_b(self):
        return "ProductB{family}"

class {factory_name}(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass

class Concrete{factory_name}({factory_name}):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA{family}()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB{family}()"""


class Builder(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Builder",
            category="Creational",
            description="Separates the construction of a complex object from its representation.",
            use_cases=[
                "Complex object creation",
                "Document builders",
                "Meal builders (like in restaurants)",
            ],
            template="""class Product:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

class Builder(ABC):
    @abstractmethod
    def build_part_a(self):
        pass

    @abstractmethod
    def build_part_b(self):
        pass

    @abstractmethod
    def get_result(self) -> Product:
        pass

class ConcreteBuilder(Builder):
    def __init__(self):
        self._product = Product()

    def build_part_a(self):
        self._product.add_part("PartA")

    def build_part_b(self):
        self._product.add_part("PartB")

    def get_result(self) -> Product:
        return self._product

class Director:
    def construct(self, builder: Builder):
        builder.build_part_a()
        builder.build_part_b()"""
        )

    def generate_code(self, **kwargs) -> str:
        product_name = kwargs.get("product_name", "Product")
        parts = kwargs.get("parts", ["PartA", "PartB"])

        part_declarations = "\n".join([f'        self.parts["{p}"] = None' for p in parts])

        builder_methods = "\n\n    ".join([
        f"""    def build_{p.lower()}(self, value):
        self.parts["{p}"] = value
        return self"""
        for p in parts
        ])

        return f"""class {product_name}:
    def __init__(self):
{part_declarations}

    def __str__(self):
        return str(self.parts)

class {product_name}Builder:
    def __init__(self):
        self._{product_name.lower()} = {product_name}()

{builder_methods}

    def get_result(self) -> {product_name}:
        return self._{product_name.lower()}"""


class Observer(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Observer",
            category="Behavioral",
            description="Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.",
            use_cases=[
                "Event handling systems",
                "Stock price monitors",
                "GUI frameworks",
            ],
            template="""class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class Subject:
    def __init__(self):
        self._observers = []
        self._state = 0

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class ConcreteObserver(Observer):
    def update(self, subject):
        print(f"Observer: State is {subject.state}")"""
        )

    def generate_code(self, **kwargs) -> str:
        subject_name = kwargs.get("subject_name", "Subject")
        observer_name = kwargs.get("observer_name", "Observer")

        return f"""from abc import ABC, abstractmethod

class {observer_name}(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class {subject_name}:
    def __init__(self):
        self._observers = []
        self._state = 0

    def attach(self, observer: {observer_name}):
        self._observers.append(observer)

    def detach(self, observer: {observer_name}):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class Concrete{observer_name}({observer_name}):
    def update(self, subject):
        print("Observer: State is " + str(subject.state))"""


class Strategy(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Strategy",
            category="Behavioral",
            description="Defines a family of algorithms, encapsulates each one, and makes them interchangeable.",
            use_cases=[
                "Sorting algorithms",
                "Payment processing",
                "Compression algorithms",
            ],
            template="""class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return sorted(data)

class ConcreteStrategyB(Strategy):
    def execute(self, data):
        return data[::-1]

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def execute_strategy(self, data):
        return self._strategy.execute(data)"""
        )

    def generate_code(self, **kwargs) -> str:
        context_name = kwargs.get("context_name", "Context")
        strategies = kwargs.get("strategies", ["StrategyA", "StrategyB"])

        strategy_classes = "\n\n".join([
            f"""class Concrete{strategy}(Strategy):
    def execute(self, data):
        # Implementation for {strategy}
        return data"""
            for strategy in strategies
        ])

        strategy_creates = "\n        ".join([
            f'\n            f"{s}": Concrete{s}()'
            for s in strategies
        ])

        return f"""from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

{strategy_classes}

class {context_name}:
    def __init__(self, strategy_name: str = "{strategies[0]}"):
        self._strategies = {{{strategy_creates}
        }}
        self._strategy = self._strategies.get(strategy_name)

    def set_strategy(self, strategy_name: str):
        self._strategy = self._strategies.get(strategy_name)

    def execute_strategy(self, data):
        return self._strategy.execute(data)"""


class Decorator(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Decorator",
            category="Structural",
            description="Attaches additional responsibilities to an object dynamically.",
            use_cases=[
                "Adding features to GUI components",
                "I/O stream wrappers",
                "Logging and authentication",
            ],
            template="""class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"

class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    @abstractmethod
    def added_behavior(self):
        pass

class ConcreteDecorator(Decorator):
    def added_behavior(self):
        return "Decorator"

    def operation(self) -> str:
        return self._component.operation() + " + " + self.added_behavior()"""
    )

    def generate_code(self, **kwargs) -> str:
        component_name = kwargs.get("component_name", "Component")
        decorator_name = kwargs.get("decorator_name", "Decorator")

        return f"""from abc import ABC, abstractmethod

class {component_name}(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class Concrete{component_name}({component_name}):
    def operation(self) -> str:
        return "Concrete{component_name}"

class {decorator_name}({component_name}):
    def __init__(self, component: {component_name}):
        self._component = component

    @abstractmethod
    def added_behavior(self):
        pass

    def operation(self) -> str:
        return self._component.operation() + " + " + self.added_behavior()

class Concrete{decorator_name}({decorator_name}):
    def added_behavior(self):
        return "Decorator" """


class Facade(DesignPattern):
    def get_info(self) -> PatternInfo:
        return PatternInfo(
            name="Facade",
            category="Structural",
            description="Provides a simplified interface to a library, framework, or complex set of classes.",
            use_cases=[
                "Complex subsystem simplification",
                "Legacy system wrapping",
                "Third-party library integration",
            ],
            template="""class SubsystemA:
    def operation_a(self):
        return "SubsystemA operation"

class SubsystemB:
    def operation_b(self):
        return "SubsystemB operation"

class Facade:
    def __init__(self):
        self._subsystem_a = SubsystemA()
        self._subsystem_b = SubsystemB()

    def operation(self):
        return self._subsystem_a.operation_a() + " and " + self._subsystem_b.operation_b()"""""
        )

    def generate_code(self, **kwargs) -> str:
        subsystems = kwargs.get("subsystems", ["SubsystemA", "SubsystemB"])
        sub_a = subsystems[0] if len(subsystems) > 0 else "SubsystemA"
        sub_b = subsystems[1] if len(subsystems) > 1 else "SubsystemB"

        result = f"""class {sub_a}:
    def operation_{sub_a.lower()}(self):
        return "{sub_a} operation"

class {sub_b}:
    def operation_{sub_b.lower()}(self):
        return "Subsystem operation"

class Facade:
    def __init__(self):
        self._{sub_a.lower()} = {sub_a}()"""
        if len(subsystems) > 1:
            result += f"\n        self._{sub_b.lower()} = {sub_b}()"

        result += f"""
    def operation(self):
        results = []
        results.append(self._{sub_a.lower()}.operation_{sub_a.lower()}())"""
        if len(subsystems) > 1:
            result += f"\n        results.append(self._{sub_b.lower()}.operation_{sub_b.lower()}())"

        result += """
        return " and ".join(results)"""

        return result


class PatternLibrary:
    def __init__(self):
        self._patterns: Dict[str, DesignPattern] = {
            "singleton": Singleton(),
            "factory": FactoryMethod(),
            "factory_method": FactoryMethod(),
            "abstract_factory": AbstractFactory(),
            "builder": Builder(),
            "observer": Observer(),
            "strategy": Strategy(),
            "decorator": Decorator(),
            "facade": Facade(),
        }

    def get_pattern(self, name: str) -> Optional[DesignPattern]:
        return self._patterns.get(name.lower())

    def list_patterns(self) -> List[PatternInfo]:
        return [p.get_info() for p in self._patterns.values()]

    def list_by_category(self, category: str) -> List[PatternInfo]:
        return [p.get_info() for p in self._patterns.values() if p.get_info().category.lower() == category.lower()]

    def generate(self, pattern_name: str, **kwargs) -> Optional[str]:
        pattern = self.get_pattern(pattern_name)
        if pattern:
            return pattern.generate_code(**kwargs)
        return None


__all__ = [
    "PatternInfo",
    "DesignPattern",
    "Singleton",
    "FactoryMethod",
    "AbstractFactory",
    "Builder",
    "Observer",
    "Strategy",
    "Decorator",
    "Facade",
    "PatternLibrary",
]
