from storage import Storage


class MiniDB:
    """
    Уровень целостности: проверяет PK, FK и валидирует данные.
    Делегирует файловые операции классу Storage.
    """

    def __init__(self, data_dir: str = "data"):
        self.storage = Storage(data_dir)

    def create_table(self, table_name: str, columns: dict, pk: str):
        self.storage.create_table(table_name, columns, pk)

    def select_all(self, table_name: str, filters: dict = None) -> list:
        if table_name not in self.storage.tables:
            raise ValueError(f"Таблица '{table_name}' не существует")
        rows = self.storage._deserialize_all(table_name)
        if filters:
            return [r for r in rows if all(r.get(k) == v for k, v in filters.items())]
        return rows

    def insert_row(self, table_name: str, row: dict):
        if table_name not in self.storage.tables:
            raise ValueError(f"Таблица '{table_name}' не существует")
        schema = self.storage.tables[table_name]

        for col in schema['columns']:
            if col not in row:
                raise ValueError(f"Отсутствует значение для колонки '{col}'")

        pk_col = schema['pk']
        if pk_col and pk_col in row:
            rows = self.storage._deserialize_all(table_name)
            if any(r[pk_col] == row[pk_col] for r in rows):
                raise ValueError(
                    f"Нарушение уникальности PK: значение '{row[pk_col]}' "
                    f"уже существует в таблице '{table_name}'"
                )

        self._check_fk(table_name, row)

        row_bytes = self.storage._serialize_row(table_name, row)
        self.storage.append_row(table_name, row_bytes)

    def update_row(self, table_name: str, pk_value, updates: dict):
        if table_name not in self.storage.tables:
            raise ValueError(f"Таблица '{table_name}' не существует")
        pk_col = self.storage.tables[table_name]['pk']
        rows = self.storage._deserialize_all(table_name)

        updated = False
        for row in rows:
            if row[pk_col] == pk_value:
                row.update(updates)
                updated = True
        if not updated:
            raise ValueError(f"Строка с PK='{pk_value}' не найдена")

        self.storage.rewrite_rows(table_name, rows)

    def delete_row(self, table_name: str, pk_value):
        if table_name not in self.storage.tables:
            raise ValueError(f"Таблица '{table_name}' не существует")
        pk_col = self.storage.tables[table_name]['pk']
        rows = self.storage._deserialize_all(table_name)

        new_rows = [r for r in rows if r[pk_col] != pk_value]
        if len(new_rows) == len(rows):
            raise ValueError(f"Строка с PK='{pk_value}' не найдена")

        self.storage.rewrite_rows(table_name, new_rows)

    def _check_fk(self, table_name: str, row: dict):
        if table_name != "experiments":
            return
        if "dataset_id" in row:
            datasets = self.storage._deserialize_all("datasets")
            if not any(d["id"] == row["dataset_id"] for d in datasets):
                raise ValueError(
                    f"Нарушение FK: dataset_id={row['dataset_id']} "
                    f"не существует в таблице 'datasets'"
                )
        if "model_id" in row:
            models = self.storage._deserialize_all("models")
            if not any(m["id"] == row["model_id"] for m in models):
                raise ValueError(
                    f"Нарушение FK: model_id={row['model_id']} "
                    f"не существует в таблице 'models'"
                )
