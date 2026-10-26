import struct


class TypeSerializer:

    @staticmethod
    def serialize_int(val: int) -> bytes:
        return struct.pack('<i', val)

    @staticmethod
    def deserialize_int(data: bytes) -> int:
        return struct.unpack('<i', data)[0]

    @staticmethod
    def serialize_float(val: float) -> bytes:
        return struct.pack('<d', val)

    @staticmethod
    def deserialize_float(data: bytes) -> float:
        return struct.unpack('<d', data)[0]

    @staticmethod
    def serialize_string(val: str) -> bytes:
        encoded = val.encode('utf-8')
        return struct.pack('<I', len(encoded)) + encoded

    @staticmethod
    def deserialize_string(data: bytes) -> tuple:
        length = struct.unpack('<I', data[:4])[0]
        val = data[4:4 + length].decode('utf-8')
        return val, 4 + length

