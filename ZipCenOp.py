import mmap
import sys
# Modify to https://github.com/442048209as/ZipCenOp

cenFlag = bytearray([80, 75, 1, 2])
cenEncryptedFlag = bytearray([9, 8])
cenNotEncryptedFlag = bytearray([0, 8])


def operate(file, method):
    with open(file, "r+b") as f:
        length = f.seek(0, 2)  # 获取文件长度
        f.seek(0)  # 将文件指针移回文件开头
        buffer = mmap.mmap(f.fileno(), length,
                           access=mmap.ACCESS_WRITE)  # 将文件映射到内存中的缓冲区

        position = 0
        while position < length:
            offset = 0
            while offset < 4 and position + offset < length and buffer[position + offset] == cenFlag[offset]:
                offset += 1
            if offset == 4:
                if method == "r":
                    buffer[position + 8:position + 10] = cenNotEncryptedFlag
                elif method == "e":
                    buffer[position + 8:position + 10] = cenEncryptedFlag
                position += 10
            else:
                position += 1

        buffer.close()
    print("success!")


def main():
    args = sys.argv[1:]
    if len(args) != 2 or args[0] not in ["r", "e"]:
        print("""
            usage:
            python ZipCenOp.py <option> <file>
            option:
                r : recover a PKZip
                e : do a fake encryption
            """)
        return

    try:
        operate(args[1], args[0])
    except IOError as e:
        print("IO error:", e)
    except:
        print("internal error.")


if __name__ == "__main__":
    main()
