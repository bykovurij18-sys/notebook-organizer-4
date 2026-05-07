import sys
from graph_factory import GraphFactory

def print_menu():
    print("\n" + "=" * 50)
    print("        🗺️  GRAPH NAVIGATOR  🗺️")
    print("=" * 50)
    print("1. Создать новый граф")
    print("2. Загрузить граф из JSON")
    print("3. Добавить вершину")
    print("4. Удалить вершину")
    print("5. Добавить ребро")
    print("6. Удалить ребро")
    print("7. Показать граф")
    print("8. BFS (поиск пути)")
    print("9. DFS (поиск пути)")
    print("10. Кратчайший путь")
    print("11. Сохранить граф в JSON")
    print("0. Выход")
    print("=" * 50)

def create_graph_menu():
    print("\n--- Типы графов ---")
    print("1. Ориентированный (Directed)")
    print("2. Неориентированный (Undirected)")
    print("3. Взвешенный (Weighted)")
    choice = input("Выберите тип: ")

    if choice == "1":
        return GraphFactory.create_graph("directed")
    elif choice == "2":
        return GraphFactory.create_graph("undirected")
    elif choice == "3":
        return GraphFactory.create_graph("weighted")
    else:
        print("Неверный выбор. Создан неориентированный граф.")
        return GraphFactory.create_graph("undirected")

def add_node_menu(graph):
    name = input("Введите название вершины: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым")
        return
    if graph.add_node(name):
        print(f"Вершина '{name}' добавлена")
    else:
        print(f"Ошибка: вершина '{name}' уже существует")

def remove_node_menu(graph):
    name = input("Введите название вершины для удаления: ").strip()
    if graph.remove_node(name):
        print(f"Вершина '{name}' удалена")
    else:
        print(f"Ошибка: вершина '{name}' не найдена")

def add_edge_menu(graph):
    from_name = input("От вершины: ").strip()
    to_name = input("До вершины: ").strip()

    weight = 1
    if isinstance(graph, WeightedGraph) or "weighted" in str(type(graph)):
        try:
            weight_input = input("Вес ребра (по умолчанию 1): ").strip()
            if weight_input:
                weight = float(weight_input)
                if weight <= 0:
                    print("Ошибка: вес должен быть положительным")
                    return
        except ValueError:
            print("Ошибка: вес должен быть числом")
            return

    try:
        graph.add_edge(from_name, to_name, weight)
        print(f"Ребро {from_name} -> {to_name} добавлено")
    except ValueError as e:
        print(f"Ошибка: {e}")

def remove_edge_menu(graph):
    from_name = input("От вершины: ").strip()
    to_name = input("До вершины: ").strip()
    if graph.remove_edge(from_name, to_name):
        print(f"Ребро {from_name} -> {to_name} удалено")
    else:
        print(f"Ошибка: ребро не найдено")

def show_graph(graph):
    print("\n" + str(graph))

def bfs_menu(graph):
    start = input("Стартовая вершина: ").strip()
    target = input("Целевая вершина: ").strip()
    path = graph.bfs(start, target)
    if path:
        print(f"Путь (BFS): {' -> '.join(path)}")
    else:
        print("Путь не найден")

def dfs_menu(graph):
    start = input("Стартовая вершина: ").strip()
    target = input("Целевая вершина: ").strip()
    path = graph.dfs(start, target)
    if path:
        print(f"Путь (DFS): {' -> '.join(path)}")
    else:
        print("Путь не найден")

def shortest_path_menu(graph):
    start = input("Стартовая вершина: ").strip()
    target = input("Целевая вершина: ").strip()
    path = graph.shortest_path(start, target)
    if path:
        print(f"Кратчайший путь: {' -> '.join(path)}")
    else:
        print("Путь не найден")

def save_graph_menu(graph):
    filename = input("Имя файла (по умолчанию data/graph.json): ").strip()
    if not filename:
        filename = "data/graph.json"
    graph.save_to_json(filename)
    print(f"Граф сохранён в {filename}")

def main():
    graph = None
    print("\n🌟 Добро пожаловать в Graph Navigator! 🌟")

    while True:
        if graph is None:
            print("\n⚠️  Граф не загружен. Сначала создайте или загрузите граф.")
            print("\n1. Создать новый граф")
            print("2. Загрузить из JSON")
            choice = input("\nВыберите действие: ")

            if choice == "1":
                graph = create_graph_menu()
                print("Граф создан!")
            elif choice == "2":
                graph = GraphFactory.create_from_json()
                if graph:
                    print("Граф загружен!")
                else:
                    print("Ошибка: файл не найден")
            else:
                print("Неверный выбор")
        else:
            print_menu()
            choice = input("\nВыберите действие: ")

            if choice == "1":
                confirm = input("Текущий граф будет потерян. Продолжить? (y/n): ")
                if confirm.lower() == 'y':
                    graph = create_graph_menu()
            elif choice == "2":
                confirm = input("Текущий граф будет потерян. Продолжить? (y/n): ")
                if confirm.lower() == 'y':
                    new_graph = GraphFactory.create_from_json()
                    if new_graph:
                        graph = new_graph
                        print("Граф загружен!")
                    else:
                        print("Ошибка: файл не найден")
            elif choice == "3":
                add_node_menu(graph)
            elif choice == "4":
                remove_node_menu(graph)
            elif choice == "5":
                add_edge_menu(graph)
            elif choice == "6":
                remove_edge_menu(graph)
            elif choice == "7":
                show_graph(graph)
            elif choice == "8":
                bfs_menu(graph)
            elif choice == "9":
                dfs_menu(graph)
            elif choice == "10":
                shortest_path_menu(graph)
            elif choice == "11":
                save_graph_menu(graph)
            elif choice == "0":
                confirm = input("Сохранить граф перед выходом? (y/n): ")
                if confirm.lower() == 'y':
                    save_graph_menu(graph)
                print("До свидания! 👋")
                sys.exit(0)
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    main()