# 4. Git object model

## Understanding Git's object database

Git is fundamentally a content-addressable filesystem with a version control system built on top. Everything in Git is stored as objects in a database, and each object is identified by a unique SHA-1 hash.

## The four types of Git objects

### 1. Blob objects
- Store file contents (binary large objects)
- Contains only the file data, no metadata like filename or permissions
- Same content always produces the same SHA-1 hash
- Shared across commits if content is identical

### 2. Tree objects
- Represent directories in the filesystem
- Contain references to blobs and other trees
- Store filenames, permissions, and object references
- Like a directory listing pointing to other objects

### 3. Commit objects
- Represent snapshots of the entire working tree
- Point to a root tree object
- Contain metadata: author, committer, timestamp, message
- Reference parent commit(s) creating the history chain

### 4. Tag objects
- Provide human-readable names for specific commits
- Can be lightweight (just a reference) or annotated (full objects)
- Annotated tags are objects with their own SHA-1

## SHA-1 hashing system

Git uses SHA-1 cryptographic hash function to identify all objects:

```bash
# Example SHA-1 hash
da39a3ee5e6b4b0d3255bfef95601890afd80709
```

### Properties of SHA-1 hashes
- **Deterministic**: Same content always produces same hash
- **Unique**: Practically impossible for different content to have same hash (2^160)
- **Fixed length**: Always 40 hexadecimal characters (160 bits)
- **One-way**: Cannot derive original content from hash

### Why this matters
- Data integrity: Any corruption is immediately detectable
- Deduplication: Identical content is stored only once
- Distributed systems: Objects can be verified across different repositories
- Immutability: Objects cannot be changed without changing their hash

## How objects relate to each other

```
Commit Object (abc123...)
├── Tree (root directory) (def456...)
│   ├── Blob (file1.txt) (789abc...)
│   ├── Blob (file2.txt) (def012...)
│   └── Tree (subdirectory) (345678...)
│       └── Blob (file3.txt) (9abcde...)
└── Parent Commit(s) (fedcba...)
```

## Object storage in .git directory

Objects are stored in `.git/objects/` using the first two characters of the SHA-1 as a directory name and the remaining 38 characters as the filename:

```
.git/objects/
├── da/
│   └── 39a3ee5e6b4b0d3255bfef95601890afd80709
├── ab/
│   └── cd1234567890abcdef1234567890abcdef1234
└── pack/    # Compressed objects for efficiency
    ├── pack-*.idx
    └── pack-*.pack
```

### Storage optimization
- Git compresses and packs objects for efficiency
- Delta compression reduces storage for similar objects
- Packed objects share common parts to save space

## Content-addressable storage benefits

### Immutability
- Once an object is created, it cannot be modified
- Any change creates a new object with new hash
- History is tamper-evident

### Deduplication
- Identical files across different commits share the same blob
- Only store unique content once
- Efficient storage even for large repositories

### Integrity
- SHA-1 hash serves as checksum
- Corruption is immediately detectable
- Objects can be verified independently
