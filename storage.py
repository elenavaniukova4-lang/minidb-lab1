import os
from type_serializer import TypeSerializer


class Storage:

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.catalog_file = os.path.join(data_dir, "catalog.dat")
        self.tables = {}
        self._load_catalog()

    def _load_catalog(self):
        if os.path.exists(self.catalog_file):
            with open(self.catalog_file, 'rb') as f:
                data = f.read()
                if data:
                    lines = data.decode('utf-8').strip().split('\n')
                    for line in lines:
                        parts = line.split('|')
                        table_name = parts[0]
                        columns = {}
                        for col in parts[1].split(','):
                            name, type_ = col.split(':')
                            columns[name] = type_
                        pk = parts[2] if len(parts) > 2 else None
                        self.tables[table_name] = {'columns': columns, 'pk': pk}

    def _save_catalog(self):
        with open(self.catalog_file, 'w', encoding='utf-8') as f:
            for table_name, schema in self.tables.items():
                cols = ','.join([f"{name}:{type_}" for name, type_ in schema['columns'].items()])
                pk = schema['pk'] or ''
                f.write(f"{table_name}|{cols}|{pk}\n")

    def create_table(self, table_name: str, columns: dict, pk: str):
        if table_name in self.tables:
            raise ValueError(f"Таблица '{table_name}' уже существует")
        self.tables[table_name] = {'columns': columns, 'pk': pk}
        self._save_catalog()
        table_file = os.path.join(self.data_dir, f"{table_name}.dat")
        with open(table_file, 'wb') as f:
            pass

    def _serialize_row(self, table_name: str, row: dict) -> bytes:
        schema = self.tables[table_name]
        row_bytes = b''
        for col_name, col_type in schema['columns'].items():
            value = row[col_name]
            if col_type == 'INT':
                row_bytes += TypeSerializer.serialize_int(value)
            elif col_type == 'FLOAT':
                row_bytes += TypeSerializer.serialize_float(value)
            elif col_type == 'STRING':
                row_bytes += TypeSerializer.serialize_string(value)
        return row_bytes

    def _deserialize_all(self, table_name: str) -> list:
        schema = self.tables[table_name]
        table_file = os.path.join(self.data_dir, f"{table_name}.dat")
        if not os.path.exists(table_file):
            return []
        with open(table_file, 'rb') as f:
            data = f.read()
        rows = []
        offset = 0
        while offset < len(data):
            row = {}
            for col_name, col_type in schema['columns'].items():
                if col_type == 'INT':
                    row[col_name] = TypeSerializer.deserialize_int(data[offset:offset+4])
                    offset += 4
                elif col_type == 'FLOAT':
                    row[col_name] = TypeSerializer.deserialize_float(data[offset:offset+8])
                    offset += 8
                elif col_type == 'STRING':
                    val, size = TypeSerializer.deserialize_string(data[offset:])
                    row[col_name] = val
                    offset += size
            rows.append(row)
        return rows

    def append_row(self, table_name: str, row_bytes: bytes):
        table_file = os.path.join(self.data_dir, f"{table_name}.dat")
        with open(table_file, 'ab') as f:
            f.write(row_bytes)

    def rewrite_rows(self, table_name: str, rows: list):
        table_file = os.path.join(self.data_dir, f"{table_name}.dat")
        with open(table_file, 'wb') as f:
            for row in rows:
                f.write(self._serialize_row(table_name, row))
