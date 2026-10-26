import os
import shutil
from engine import MiniDB


def clear_data():
    if os.path.exists("data"):
        shutil.rmtree("data")


def create_tables(db):
    print("=== Создание таблиц ===")

    db.create_table("datasets",
                    columns={"id": "INT", "name": "STRING",
                             "task": "STRING", "size": "INT"},
                    pk="id")
    print("✅ Таблица 'datasets' создана")

    db.create_table("models",
                    columns={"id": "INT", "name": "STRING",
                             "version": "STRING"},
                    pk="id")
    print("✅ Таблица 'models' создана")

    db.create_table("experiments",
                    columns={"id": "INT", "dataset_id": "INT", "model_id": "INT",
                             "accuracy": "FLOAT", "status": "STRING"},
                    pk="id")
    print("✅ Таблица 'experiments' создана")


def insert_test_data(db):
    print("\n=== Вставка тестовых данных ===")

    # datasets
    d1 = {"id": 1, "name": "MNIST", "task": "classification", "size": 60000}
    d2 = {"id": 2, "name": "CIFAR-10", "task": "classification", "size": 50000}
    d3 = {"id": 3, "name": "ImageNet", "task": "classification", "size": 1000000}
    d4 = {"id": 4, "name": "COCO", "task": "detection", "size": 330000}
    d5 = {"id": 5, "name": "SQuAD", "task": "qa", "size": 150000}

    for d in [d1, d2, d3, d4, d5]:
        db.insert_row("datasets", d)
    print("✅ Вставлено 5 datasets")

    # models
    m1 = {"id": 1, "name": "ResNet-50", "version": "1.0"}
    m2 = {"id": 2, "name": "BERT-base", "version": "1.0"}
    m3 = {"id": 3, "name": "YOLOv5", "version": "2.0"}
    m4 = {"id": 4, "name": "GPT-2", "version": "1.5"}
    m5 = {"id": 5, "name": "EfficientNet", "version": "1.0"}

    for m in [m1, m2, m3, m4, m5]:
        db.insert_row("models", m)
    print("✅ Вставлено 5 models")

    # experiments - тут много данных, поэтому списком
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
            "accuracy": 0.91, "status": "running"}
    ]

    for e in experiments:
        db.insert_row("experiments", e)
    print("✅ Вставлено {} experiments".format(len(experiments)))


def demonstrate_operations(db):
    print("\n=== SELECT: experiments со статусом completed ===")
    r = db.select_all("experiments", filters={"status": "completed"})
    print("Найдено " + str(len(r)) + " записей:")
    for row in r[:3]:
        print("  id={}, dataset_id={}, accuracy={}".format(
            row['id'], row['dataset_id'], row['accuracy']))
    print("  ... (всего {})".format(len(r)))

    print("\n=== UPDATE: меняем accuracy у id=3 ===")
    db.update_row("experiments", pk_value=3,
                  updates={"accuracy": 0.78, "status": "completed"})
    row = db.select_all("experiments", filters={"id": 3})[0]
    print("  Обновлено: accuracy={}, status={}".format(
        row['accuracy'], row['status']))

    print("\n=== DELETE: удаляем id=10 ===")
    db.delete_row("experiments", pk_value=10)
    r = db.select_all("experiments")
    print("  Осталось {} экспериментов".format(len(r)))


def demonstrate_errors(db):
    print("\n=== Ошибка: дубликат PK ===")
    try:
        db.insert_row("datasets",
                      {"id": 1, "name": "Duplicate", "task": "test", "size": 100})
        print("   должно было быть ошибка!")
    except ValueError as e:
        print("  ✅ поймали ошибку:", e)

    print("\n=== Ошибка: нет такой таблицы ===")
    try:
        db.select_all("nonexistent_table")
        print("  должно было быть ошибка!")
    except ValueError as e:
        print("  ✅ поймали ошибку:", e)


def demonstrate_persistence():
    print("\n=== Проверяем сохранение (перезапуск) ===")
    print("Создаём новый MiniDB...")
    db2 = MiniDB(data_dir="data")

    r1 = db2.select_all("datasets")
    r2 = db2.select_all("models")
    r3 = db2.select_all("experiments")

    print("✅ datasets: {} записей".format(len(r1)))
    print("✅ models: {} записей".format(len(r2)))
    print("✅ experiments: {} записей".format(len(r3)))


if __name__ == "__main__":
    print("=" * 60)
    print("MiniDB — демонстрация работы")
    print("=" * 60)

    clear_data()

    db = MiniDB(data_dir="data")
    create_tables(db)
    insert_test_data(db)
    demonstrate_operations(db)
    demonstrate_errors(db)
    demonstrate_persistence()

    print("\n" + "=" * 60)
    print("✅ Все тесты пройдены!")
    print("=" * 60)
