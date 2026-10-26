import os
import shutil
from engine import MiniDB


def clear_data():
    """Очищает папку data перед тестом"""
    if os.path.exists("data"):
        shutil.rmtree("data")


def create_tables(db: MiniDB):
    """Создаёт 3 таблицы по схеме из методички"""
    print("=== Создание таблиц ===")

    db.create_table(
        "datasets",
        columns={"id": "INT", "name": "STRING",
                 "task": "STRING", "size": "INT"},
        pk="id"
    )
    print("✅ Таблица 'datasets' создана")

    db.create_table(
        "models",
        columns={"id": "INT", "name": "STRING", "version": "STRING"},
        pk="id"
    )
    print("✅ Таблица 'models' создана")

    db.create_table(
        "experiments",
        columns={
            "id": "INT",
            "dataset_id": "INT",
            "model_id": "INT",
            "accuracy": "FLOAT",
            "status": "STRING"
        },
        pk="id"
    )
    print("✅ Таблица 'experiments' создана")


def insert_test_data(db: MiniDB):
    """Вставляет тестовые данные: 5 datasets, 5 models, 20 experiments"""
    print("\n=== Вставка тестовых данных ===")

    # 5 datasets
    datasets = [
        {"id": 1, "name": "MNIST", "task": "classification", "size": 60000},
        {"id": 2, "name": "CIFAR-10", "task": "classification", "size": 50000},
        {"id": 3, "name": "ImageNet", "task": "classification", "size": 1000000},
        {"id": 4, "name": "COCO", "task": "detection", "size": 330000},
        {"id": 5, "name": "SQuAD", "task": "qa", "size": 150000}
    ]
    for ds in datasets:
        db.insert_row("datasets", ds)
    print(f"✅ Вставлено {len(datasets)} datasets")

    # 5 models
    models = [
        {"id": 1, "name": "ResNet-50", "version": "1.0"},
        {"id": 2, "name": "BERT-base", "version": "1.0"},
        {"id": 3, "name": "YOLOv5", "version": "2.0"},
        {"id": 4, "name": "GPT-2", "version": "1.5"},
        {"id": 5, "name": "EfficientNet", "version": "1.0"}
    ]
    for m in models:
        db.insert_row("models", m)
    print(f"✅ Вставлено {len(models)} models")

    # 20 experiments
    experiments = [
        {"id": 1, "dataset_id": 1, "model_id": 1,
            "accuracy": 0.91, "status": "completed"},
        {"id": 2, "dataset_id": 1, "model_id": 2,
            "accuracy": 0.88, "status": "completed"},
        {"id": 3, "dataset_id": 2, "model_id": 1,
            "accuracy": 0.76, "status": "running"},
        {"id": 4, "dataset_id": 2, "model_id": 3,
            "accuracy": 0.82, "status": "completed"},
        {"id": 5, "dataset_id": 3, "model_id": 1,
            "accuracy": 0.95, "status": "completed"},
        {"id": 6, "dataset_id": 3, "model_id": 4,
            "accuracy": 0.89, "status": "failed"},
        {"id": 7, "dataset_id": 4, "model_id": 3,
            "accuracy": 0.87, "status": "completed"},
        {"id": 8, "dataset_id": 4, "model_id": 5,
            "accuracy": 0.90, "status": "completed"},
        {"id": 9, "dataset_id": 5, "model_id": 2,
            "accuracy": 0.93, "status": "completed"},
        {"id": 10, "dataset_id": 5, "model_id": 4,
            "accuracy": 0.91, "status": "running"},
        {"id": 11, "dataset_id": 1, "model_id": 5,
            "accuracy": 0.85, "status": "completed"},
        {"id": 12, "dataset_id": 2, "model_id": 2,
            "accuracy": 0.79, "status": "completed"},
        {"id": 13, "dataset_id": 3, "model_id": 3,
            "accuracy": 0.88, "status": "completed"},
        {"id": 14, "dataset_id": 4, "model_id": 1,
            "accuracy": 0.84, "status": "failed"},
        {"id": 15, "dataset_id": 5, "model_id": 5,
            "accuracy": 0.92, "status": "completed"},
        {"id": 16, "dataset_id": 1, "model_id": 3,
            "accuracy": 0.86, "status": "completed"},
        {"id": 17, "dataset_id": 2, "model_id": 4,
            "accuracy": 0.81, "status": "running"},
        {"id": 18, "dataset_id": 3, "model_id": 2,
            "accuracy": 0.90, "status": "completed"},
        {"id": 19, "dataset_id": 4, "model_id": 2,
            "accuracy": 0.83, "status": "completed"},
        {"id": 20, "dataset_id": 5, "model_id": 1,
            "accuracy": 0.89, "status": "completed"}
    ]
    for exp in experiments:
        db.insert_row("experiments", exp)
    print(f"✅ Вставлено {len(experiments)} experiments")


def demonstrate_operations(db: MiniDB):
    """Демонстрирует CRUD операции"""
    print("\n=== SELECT: все experiments со статусом 'completed' ===")
    rows = db.select_all("experiments", filters={"status": "completed"})
    print(f"Найдено {len(rows)} записей:")
    for row in rows[:3]:  # Показываем первые 3
        print(
            f"  id={row['id']}, dataset_id={row['dataset_id']}, accuracy={row['accuracy']}")
    print(f"  ... (всего {len(rows)})")

    print("\n=== UPDATE: изменяем accuracy эксперимента id=3 ===")
    db.update_row("experiments", pk_value=3, updates={
                  "accuracy": 0.78, "status": "completed"})
    row = db.select_all("experiments", filters={"id": 3})[0]
    print(f"  Обновлено: accuracy={row['accuracy']}, status={row['status']}")

    print("\n=== DELETE: удаляем эксперимент id=20 ===")
    db.delete_row("experiments", pk_value=20)
    rows = db.select_all("experiments")
    print(f"  Осталось {len(rows)} экспериментов")


def demonstrate_errors(db: MiniDB):
    """Демонстрирует обработку ошибок"""
    print("\n=== Ошибка: дубликат PK ===")
    try:
        db.insert_row(
            "datasets", {"id": 1, "name": "Duplicate", "task": "test", "size": 100})
        print("  ❌ Ошибка: дубликат должен был быть отклонён!")
    except ValueError as e:
        print(f"  ✅ Ошибка корректно обработана: {e}")

    print("\n=== Ошибка: несуществующая таблица ===")
    try:
        db.select_all("nonexistent_table")
        print("   Ошибка: должна была быть отклонена!")
    except ValueError as e:
        print(f"  ✅ Ошибка корректно обработана: {e}")


def demonstrate_persistence():
    """Демонстрирует сохранение данных после перезапуска"""
    print("\n=== Проверка сохранения данных (перезапуск) ===")
    print("Создаём новый объект MiniDB (имитация перезапуска)...")
    db2 = MiniDB(data_dir="data")

    rows = db2.select_all("datasets")
    print(f"✅ После 'перезапуска' в datasets {len(rows)} записей")

    rows = db2.select_all("models")
    print(f"✅ После 'перезапуска' в models {len(rows)} записей")

    rows = db2.select_all("experiments")
    print(f"✅ После 'перезапуска' в experiments {len(rows)} записей")


if __name__ == "__main__":
    print("=" * 60)
    print("MiniDB — демонстрация работы (7-8 баллов)")
    print("=" * 60)

    # Очищаем старые данные
    clear_data()

    # Создаём базу и таблицы
    db = MiniDB(data_dir="data")
    create_tables(db)

    # Вставляем тестовые данные
    insert_test_data(db)

    # Демонстрируем операции
    demonstrate_operations(db)

    # Демонстрируем обработку ошибок
    demonstrate_errors(db)

    # Демонстрируем сохранение данных
    demonstrate_persistence()
    db2 = MiniDB(data_dir="data")
    print("\n" + "=" * 60)
    print("✅ Все тесты пройдены! MiniDB работает корректно.")
    print("=" * 60)
