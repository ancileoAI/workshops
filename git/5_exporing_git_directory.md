# 5. Exploring the .git directory

## Hands-on exploration setup

Let's create a simple repository to explore Git's internals:

```bash
mkdir sample-repo
cd sample-repo
git init
echo "Hello Git" > hello.txt
git add hello.txt
git commit -m "Initial commit"
```

## Anatomy of the .git directory

```
.git/
├── HEAD              # Points to current branch
├── config            # Repository configuration
├── description       # Repository description
├── hooks/            # Custom scripts for Git events
├── info/             # Global exclude patterns
├── objects/          # All Git objects (blobs, trees, commits)
├── refs/             # References (branches, tags)
│   ├── heads/        # Local branches
│   ├── tags/         # Tags
│   └── remotes/      # Remote tracking branches
├── index             # Staging area (binary file)
└── logs/             # Reference logs (reflog)
```

## Exploring with plumbing commands

### 1. Understanding HEAD
```bash
cat .git/HEAD
# Output: ref: refs/heads/main

cat .git/refs/heads/main
# Output: <commit-sha>
```

### 2. Examining objects
```bash
# List all objects
find .git/objects -type f

# Get object type
git cat-file -t <sha>

# Get object content
git cat-file -p <sha>

# Get object size
git cat-file -s <sha>
```

### 3. Creating objects manually
```bash
# Create a blob object
echo "Manual blob content" | git hash-object -w --stdin

# Create a tree object
git write-tree

# Create a commit object
git commit-tree <tree-sha> -m "Manual commit"
```

## Hands-on exercises

### Exercise 1: Object exploration
1. Create a file and add it to staging
2. Find the blob object in `.git/objects/`
3. Use `git cat-file` to examine its content
4. Verify the SHA-1 matches what Git calculated

### Exercise 2: Tree structure
1. Create a directory with multiple files
2. Add and commit the changes
3. Find the commit object SHA
4. Use `git cat-file -p <commit-sha>` to see the tree reference
5. Explore the tree object to see how it references blobs

### Exercise 3: Commit chain
1. Make several commits
2. Use `git cat-file -p` on each commit
3. Follow the parent chain manually
4. Compare with `git log --oneline`

## Understanding the staging area (index)

### Examining the index
```bash
# Show staged files
git ls-files --stage

# Show index content in detail
git ls-files --stage --debug
```

### Index structure
The index file contains:
- File paths
- SHA-1 hashes of blob objects
- File metadata (timestamps, permissions)
- Stage numbers (for merge conflicts)

### Index vs working directory
```bash
# Compare index to HEAD
git diff --cached

# Compare working directory to index
git diff

# Compare working directory to HEAD
git diff HEAD
```

## Practical insights

### What happens during git add
1. Git calculates SHA-1 hash of file content
2. Creates blob object in `.git/objects/`
3. Updates index to reference the blob
4. Working directory file remains unchanged

### What happens during git commit
1. Git creates tree objects from index
2. Creates commit object pointing to root tree
3. Updates current branch reference
4. Clears index (it now matches HEAD)

### Why .git/objects uses subdirectories
- Performance: Avoids too many files in single directory
- Uses first 2 characters of SHA-1 as subdirectory name
- Remaining 38 characters as filename
