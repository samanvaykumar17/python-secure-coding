**CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')** occurs when a program copies data into a fixed-size buffer without ensuring that the destination is large enough.

Python itself generally prevents classic C-style buffer overflows because `bytes`, `bytearray`, and strings manage their bounds. However, **C/C++ extensions accessed from Python through `ctypes` can introduce CWE-120**.

### Vulnerable Python example using `ctypes`

```python
import ctypes

# Create a fixed-size buffer: 8 bytes
buffer = ctypes.create_string_buffer(8)

user_input = b"AAAAAAAAAAAAAAAAAAAA"

# Vulnerable: copies more data than the destination buffer can safely hold
ctypes.memmove(buffer, user_input, len(user_input))

print(buffer.raw)
```

Here the destination buffer is only **8 bytes**, while the copy operation attempts to write **20 bytes**. This can corrupt adjacent memory and potentially crash the process or create a security vulnerability.

### Safer version

Check the size before copying:

```python
import ctypes

buffer = ctypes.create_string_buffer(8)

user_input = b"AAAAAAAAAAAAAAAAAAAA"

copy_size = min(len(user_input), len(buffer) - 1)

ctypes.memmove(buffer, user_input, copy_size)

print(buffer.value)
```

Or, when possible, avoid low-level memory operations altogether:

```python
buffer = bytearray(8)

user_input = b"AAAAAAAAAAAAAAAAAAAA"

buffer[:len(user_input)] = user_input[:len(buffer)]

print(buffer)
```

### Key point

CWE-120 is primarily a **low-level memory-safety issue**. In ordinary Python code such as:

```python
data = [0] * 8
data[100] = 1
```

Python raises an exception rather than writing beyond the allocated memory. The risk becomes relevant when Python interacts with **native C/C++ code, `ctypes`, C extensions, or unsafe foreign-function interfaces**.
