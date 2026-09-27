**CWE-122: Heap-based Buffer Overflow** occurs when a program writes beyond the boundaries of a buffer allocated on the **heap**.

Pure Python normally prevents this because Python objects perform bounds checking. A CWE-122 vulnerability can appear when Python calls unsafe C/C++ code.

### Vulnerable Python example using `ctypes`

Imagine a native library has this C function:

```c
#include <stdlib.h>
#include <string.h>

void copy_data(const char *input, size_t length) {
    char *buffer = malloc(16);

    // Vulnerable: buffer is only 16 bytes,
    // but length can be larger.
    memcpy(buffer, input, length);

    free(buffer);
}
```

Python calls it like this:

```python
import ctypes

lib = ctypes.CDLL("./vulnerable.so")

lib.copy_data.argtypes = [
    ctypes.c_char_p,
    ctypes.c_size_t
]

user_input = b"A" * 100

# Native code allocates 16 bytes on the heap
# but attempts to copy 100 bytes.
lib.copy_data(user_input, len(user_input))
```

Conceptually:

```text
Heap
┌────────────────┐
│ buffer[16]     │
├────────────────┤
│ Other heap data│
└────────────────┘
        ↑
        │
   100 bytes written
        └──────────────► beyond buffer
```

This can corrupt adjacent heap memory and potentially crash the process or create a more serious security vulnerability.

### Safer native implementation

The native code should enforce the destination size:

```c
void copy_data(const char *input, size_t length) {
    size_t size = 16;

    if (length > size) {
        length = size;
    }

    char *buffer = malloc(size);

    if (buffer == NULL) {
        return;
    }

    memcpy(buffer, input, length);

    free(buffer);
}
```

The Python layer can also reject oversized input:

```python
import ctypes

lib = ctypes.CDLL("./safe.so")

MAX_SIZE = 16
user_input = b"A" * 100

if len(user_input) > MAX_SIZE:
    raise ValueError("Input exceeds maximum size")

lib.copy_data(user_input, len(user_input))
```

### CWE comparison

| CWE         | Buffer location                             |
| ----------- | ------------------------------------------- |
| **CWE-120** | Buffer overflow from improper size checking |
| **CWE-121** | **Stack-based** buffer overflow             |
| **CWE-122** | **Heap-based** buffer overflow              |

So, for Python, the most realistic CWE-122 examples involve **`ctypes`, C/C++ extensions, native libraries, or other foreign-function interfaces** rather than ordinary Python lists or strings.
