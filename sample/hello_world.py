import pyrlkit


if __name__ == "__main__":
    buffer = pyrlkit.MatrixBuffer(80, 30)

    buffer.print("Hello world")

    print(buffer.queue)
    print(list(filter(bool, buffer.queue)))