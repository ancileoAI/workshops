# 3. Git fundamentals

## The three states

Git has three main states that your files can be in:

### 1. Working directory
- The files you're currently working on in your filesystem
- Contains the actual files you edit with your text editor or IDE
- May contain files that are tracked, untracked, or ignored by Git
- This is your "workspace" where you make changes

### 2. Staging area (index)
- A file that stores information about what will go into your next commit
- Located at `.git/index`
- Acts as a "preparation area" for your next commit
- Allows you to selectively choose which changes to commit

### 3. Repository
- Where Git stores the complete history and metadata for your project
- Located in the `.git` directory
- Contains all commits, branches, tags, and configuration
- This is the "database" of your project's history

## The basic Git workflow

```
Working Directory  →  Staging Area  →  Repository
     (edit)            (git add)       (git commit)
```

1. **Modify** files in your working directory
2. **Stage** changes you want to include in your next commit
3. **Commit** the staged changes to the repository

## How Git thinks about data

### Snapshots, not differences
- Most VCS systems store information as changes to files (deltas)
- Git stores data as snapshots of the entire filesystem
- Each commit points to a complete snapshot
- Unchanged files are not duplicated, just referenced

### Example comparison:
**Traditional VCS (delta-based):**
```
File A | Version 1 → +line 5 → +line 12 → -line 3
```

**Git (snapshot-based):**
```
Commit 1: [File A v1, File B v1, File C v1]
Commit 2: [File A v2, File B v1, File C v1]
Commit 3: [File A v2, File B v2, File C v2]
```

## Working directory details

### File states in working directory
- **Tracked**: Files that Git knows about
  - **Unmodified**: File hasn't changed since last commit
  - **Modified**: File has changes but not staged
  - **Staged**: File is ready for next commit
- **Untracked**: Files that Git doesn't know about yet
- **Ignored**: Files that Git is told to ignore (via `.gitignore`)

### Checking status
```bash
git status          # See current state
git status --short  # Abbreviated output
```

## Staging area concepts

### Why staging exists
- Allows you to craft commits with precision
- Review changes before committing
- Include only some changes from a file
- Create logical, atomic commits

### Staging operations
```bash
git add file.txt        # Stage specific file
git add .              # Stage all changes
git add -p             # Stage interactively (patch mode)
git reset HEAD file.txt # Unstage file
```

## Repository structure

### What's in .git directory
```
.git/
├── objects/     # All content (blobs, trees, commits)
├── refs/        # Pointers to commits (branches, tags)
├── HEAD         # Points to current branch
├── index        # Staging area information
├── config       # Repository configuration
└── hooks/       # Custom scripts for Git events
```
