**CWE-121: Stack-based Buffer Overflow** occurs when a program writes more data to a buffer located on the **stack** than the buffer can hold.

Pure Python normally prevents this class of vulnerability. A CWE-121 issue can arise when Python calls vulnerable native C/C++ code.

### Vulnerable example with `ctypes`

Suppose a native library contains:

```c
void copy_name(const char *input) {
    char name[16];
    strcpy(name, input);   // No bounds check
}
```

A Python program calling it might look like:

```python
import ctypes

lib = ctypes.CDLL("./vulnerable.so")

lib.copy_name.argtypes = [ctypes.c_char_p]

user_input = b"A" * 100

# Vulnerable native function receives 100 bytes
# but its stack buffer is only 16 bytes.
lib.copy_name(user_input)
```

The native function has:

```text
Stack
┌─────────────────┐
│ name[16]        │  ← destination
├─────────────────┤
│ other stack data│
├─────────────────┤
│ return address  │
└─────────────────┘
```

Writing 100 bytes into `name[16]` can overwrite adjacent stack data, potentially causing a crash or, depending on the surrounding native code and platform protections, more serious memory corruption.

### Safer C implementation

The fix belongs primarily in the native code:

```c
void copy_name(const char *input) {
    char name[16];

    strncpy(name, input, sizeof(name) - 1);
    name[sizeof(name) - 1] = '\0';
}
```

And the Python side can additionally validate input:

```python
import ctypes

lib = ctypes.CDLL("./safe.so")
lib.copy_name.argtypes = [ctypes.c_char_p]

user_input = b"A" * 100

if len(user_input) >= 16:
    raise ValueError("Input is too long")

lib.copy_name(user_input)
```

**CWE-121 vs CWE-120:** CWE-120 describes buffer copying without adequate size checking in general, while **CWE-121 specifically concerns a buffer located on the stack**. In normal Python code, these classic stack-buffer-overflow conditions generally don't occur because Python manages memory bounds; they become relevant when Python interfaces with unsafe native code.
