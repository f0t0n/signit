# Key
---

#### Module description

The module **``signit.key``** implements a functionality that allows you to generate random keys to use later for HMAC signature creating and user identification.

---

#### Module interface

> **``signit.key.generate(key_length=KEY_LENGTH, key_chars=KEY_CHARS)``**

Generates a random key.

**Parameters:**

- **key_length** (*int*) - a length of key to generate (default ``32``)
- **key_chars** (*str*) - chars to use for random key generating (default ``[a-zA-Z0-9]``)

**Returns** (*str*) - a generated key.

**Example of usage:**

```python
import signit
import string

if __name__ == '__main__':
    print('Access key:',
          signit.key.generate(key_length=8, key_chars=string.ascii_lowercase))
    print('Secret key:',
          signit.key.generate(key_length=32, key_chars=string.ascii_uppercase))
```
