# 9. git reset

## What is git reset?

Git reset is a powerful command that moves the current branch pointer and optionally updates the staging area and working directory to match. It's essentially a way to "undo" commits by moving backwards in history.

## The three modes of reset

### 1. --soft (move branch pointer only)
```bash
git reset --soft HEAD~1
```
- Moves branch pointer to specified commit
- Leaves staging area and working directory unchanged
- Previous commit's changes remain staged

### 2. --mixed (default - move pointer and update staging)
```bash
git reset --mixed HEAD~1
# or simply
git reset HEAD~1
```
- Moves branch pointer to specified commit
- Updates staging area to match the commit
- Leaves working directory unchanged
- Previous commit's changes become unstaged

### 3. --hard (move pointer, update staging and working directory)
```bash
git reset --hard HEAD~1
```
- Moves branch pointer to specified commit
- Updates staging area to match the commit
- Updates working directory to match the commit
- **Destructive**: Previous commit's changes are lost

## Visual representation

```
Before reset:
Working Dir: [modified files]
Staging:     [staged changes]
Repository:  A---B---C (HEAD)

After git reset --soft HEAD~1:
Working Dir: [modified files]
Staging:     [staged changes + C's changes]
Repository:  A---B (HEAD)

After git reset --mixed HEAD~1:
Working Dir: [modified files + C's changes]
Staging:     [empty]
Repository:  A---B (HEAD)

After git reset --hard HEAD~1:
Working Dir: [clean - matches B]
Staging:     [empty]
Repository:  A---B (HEAD)
```

## Hands-on reset exploration

### Setup reset scenario (using sample-repo)
```bash
cd sample-repo

# Ensure we're on main and clean
git checkout main
git status

# Create a series of commits to practice with
echo "Reset demo line 1" > reset-demo.txt
git add reset-demo.txt
git commit -m "Reset demo commit 1"

echo "Reset demo line 2" >> reset-demo.txt
git commit -am "Reset demo commit 2"

echo "Reset demo line 3" >> reset-demo.txt
git commit -am "Reset demo commit 3"

# Check our history
git log --oneline -5
```

### Experiment with --soft reset
```bash
# Save current commit SHA for reference
git rev-parse HEAD

# Soft reset - move back one commit
git reset --soft HEAD~1

# Check status - changes should be staged
git status
cat reset-demo.txt  # File still has all 3 lines
git log --oneline -3  # Should show we're back one commit

# The last commit's changes are now staged
git diff --cached
```

### Experiment with --mixed reset
```bash
# First, recommit to get back to 3 commits
git commit -m "Reset demo commit 3 (recreated)"

# Mixed reset (default)
git reset HEAD~1

# Check status - changes should be unstaged
git status
cat reset-demo.txt  # File still has all 3 lines
git diff  # Shows unstaged changes

# Stage and recommit
git add reset-demo.txt
git commit -m "Reset demo commit 3 (recreated again)"
```

### Experiment with --hard reset (careful!)
```bash
# Save the content first to demonstrate data loss
cp reset-demo.txt reset-demo-backup.txt

# Hard reset - this will lose changes!
git reset --hard HEAD~1

# Check what happened
git status  # Should be clean
cat reset-demo.txt  # Should only have 2 lines now
git log --oneline -3

# The third line is gone! (but we have backup)
```

## Advanced reset scenarios

### Resetting to specific commits
```bash
# Reset to a specific commit SHA
git reset --mixed abc123f

# Reset to a tag
git reset --soft v1.2.0

# Reset to a branch
git reset --hard origin/main
```

### Partial resets (affecting specific files)
```bash
# Reset specific files from staging area
git reset HEAD file1.txt file2.txt

# Reset specific files to a previous commit
git reset abc123f -- file1.txt

# This affects staging area only, not working directory
```

### Using reset with paths
```bash
# Unstage a file (same as git restore --staged)
git reset HEAD file.txt

# Reset file to state from previous commit
git reset HEAD~1 -- file.txt
```

## Recovery from reset

### Using reflog to recover "lost" commits
```bash
# View reflog to see where HEAD has been
git reflog

# Reflog shows something like:
# abc123f HEAD@{0}: reset: moving to HEAD~1
# def456g HEAD@{1}: commit: Reset demo commit 3
# ghi789h HEAD@{2}: commit: Reset demo commit 2

# Recover the "lost" commit
git reset --hard HEAD@{1}
# or
git reset --hard def456g
```

### What reflog tracks
- Every time HEAD moves
- Commits, resets, checkouts, merges, rebases
- Local only (not shared with remotes)
- Expires after ~90 days by default

## Reset vs other commands

### Reset vs revert
```bash
# Reset removes commits from history
git reset --hard HEAD~1  # Commit disappears

# Revert creates new commit that undoes changes
git revert HEAD  # Creates new commit undoing HEAD
```

### Reset vs checkout/switch
```bash
# Reset moves current branch pointer
git reset --hard abc123f  # Branch moves to abc123f

# Checkout/switch moves HEAD (possibly detaching)
git checkout abc123f  # HEAD detaches to abc123f
```

### Reset vs restore
```bash
# Reset affects branch pointer and optionally staging/working
git reset --hard HEAD~1

# Restore only affects working directory or staging area
git restore file.txt  # Restore working directory
git restore --staged file.txt  # Restore staging area
```

## Common reset patterns

### Undo last commit but keep changes
```bash
git reset --soft HEAD~1
# Changes from last commit are now staged
```

### Unstage all files
```bash
git reset HEAD
# or
git reset
```

### Completely undo last commit
```bash
git reset --hard HEAD~1
# Commit and its changes are gone
```

### Move uncommitted changes to different base
```bash
# You're on wrong branch with uncommitted changes
git stash
git checkout correct-branch
git stash pop
```

## Safety considerations

### Before using --hard reset
- Check `git status` to see what will be lost
- Consider `git stash` to save changes
- Remember that reflog can help recover

### Reset safety levels
- **Safe**: `--soft` and `--mixed` (can always recover)
- **Dangerous**: `--hard` (can lose uncommitted work)
- **Recovery**: Use `git reflog` and `git reset` to recover
