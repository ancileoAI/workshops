# 6. Branching internals

## What is a branch really?

A branch in Git is simply a lightweight, movable pointer to a specific commit. That's it. Nothing more, nothing less.

```bash
# A branch is just a file containing a commit SHA
cat .git/refs/heads/main
# Output: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t

# HEAD points to the current branch
cat .git/HEAD
# Output: ref: refs/heads/main
```

## How branches work internally

### Branch creation
```bash
git branch feature-xyz
```

What Git does:
1. Creates file `.git/refs/heads/feature-xyz`
2. Writes current commit SHA to that file
3. That's it - no copying, no complex operations

### Branch switching
```bash
git checkout feature-xyz
# or
git switch feature-xyz
```

What Git does:
1. Updates `.git/HEAD` to point to the new branch
2. Updates working directory and index to match the commit
3. Very fast operation - just changing file contents

## Hands-on branch exploration

### Create and examine branches
```bash
# Create a new branch
git branch experimental

# See what was created
cat .git/refs/heads/experimental
cat .git/refs/heads/main

# They point to the same commit!
```

### Observe HEAD movement
```bash
# Check current HEAD
cat .git/HEAD

# Switch branches
git switch experimental
cat .git/HEAD

# Switch back
git switch main
cat .git/HEAD
```

### Make commits on different branches
```bash
# On main branch
echo "Main branch content" > main-file.txt
git add main-file.txt
git commit -m "Main branch commit"

# Switch to experimental
git switch experimental
echo "Experimental content" > exp-file.txt
git add exp-file.txt
git commit -m "Experimental commit"

# Compare branch pointers
cat .git/refs/heads/main
cat .git/refs/heads/experimental
# Now they point to different commits!
```

## Branch references and HEAD

### HEAD states
- **Attached HEAD**: Points to a branch (normal state)
- **Detached HEAD**: Points directly to a commit

```bash
# Normal attached HEAD
cat .git/HEAD
# Output: ref: refs/heads/main

# Create detached HEAD
git checkout <commit-sha>
cat .git/HEAD
# Output: <commit-sha>
```

### Why branching is cheap in Git

1. **No data copying**: Creating a branch just creates a 41-byte file
2. **No directory duplication**: All commits share the same object database
3. **Instant operation**: Just writing a SHA to a file
4. **Minimal storage**: Thousands of branches add almost no disk space

## Practical branching insights

### Branch naming and organization
```bash
# Branches are stored as files in refs/heads/
ls .git/refs/heads/

# You can organize with subdirectories
git branch feature/user-auth
git branch feature/payment-system
git branch bugfix/critical-security

# Creates directory structure
ls .git/refs/heads/feature/
ls .git/refs/heads/bugfix/
```

### Remote tracking branches
```bash
# Remote branches stored separately
ls .git/refs/remotes/origin/

# They're just pointers too
cat .git/refs/remotes/origin/main
```

### What happens during commit

When you commit on a branch:
1. Git creates new commit object
2. Updates current branch pointer to new commit
3. New commit points to previous commit as parent

```bash
# Before commit
cat .git/refs/heads/main
# e.g., abc123...

# Make commit
echo "New content" > file.txt
git add file.txt
git commit -m "New commit"

# After commit
cat .git/refs/heads/main
# e.g., def456... (different SHA)
```

## Advanced branch concepts

### Symbolic references
```bash
# HEAD is a symbolic reference
git symbolic-ref HEAD
# Output: refs/heads/main

# You can create custom symbolic refs
git symbolic-ref refs/myref refs/heads/experimental
```

### Packed references
For repositories with many branches, Git can pack references:
```bash
# References can be packed for efficiency
cat .git/packed-refs
# Contains multiple refs in one file
```

## Key insights

- Branches are just 41-byte files containing commit SHAs
- HEAD determines which branch is "current"
- Creating branches is O(1) - constant time regardless of project size
- Switching branches updates working directory to match commit
- This design enables Git's powerful branching workflows
