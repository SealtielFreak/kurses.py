import pyrlkit
from pyrlkit.buffer_matrix import BufferMatrix


if __name__ == "__main__":
    buffer = BufferMatrix(80, 30)

    buffer.print("Hello world")

    print(buffer.queue)
    print(list(filter(bool, buffer.queue)))
