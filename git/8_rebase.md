# 8. git rebase

## What is rebasing?

Rebasing is the process of moving or combining a sequence of commits to a new base commit. Unlike merging, which preserves the history of parallel development, rebasing rewrites history to create a linear progression.

## Rebase vs merge comparison

### Merge approach
```
main:     A---B---C---F---M
               \         /
feature:        D---E---/
```
Creates a merge commit (M) preserving both histories.

### Rebase approach
```
# Before rebase:
main:     A---B---C---F
               \
feature:        D---E

# After rebase:
main:     A---B---C---F
feature:              D'---E'
```
Replays feature commits on top of main, creating new commits (D', E').

## How rebase works internally

### Step-by-step process
1. **Find common ancestor** between current branch and target branch
2. **Store commits** that exist on current branch but not on target
3. **Reset current branch** to target branch
4. **Replay stored commits** one by one on the new base
5. **Update branch pointer** to the final replayed commit

### What "replay" means
For each commit being rebased:
1. Calculate the diff between the commit and its parent
2. Apply that diff to the current state
3. Create a new commit with the same message but new SHA
4. Handle any conflicts that arise during application

## Hands-on rebase exploration

### Setup rebase scenario (using sample-repo)
```bash
# Navigate to sample-repo and clean up previous merge
cd sample-repo
git merge --abort  # If previous merge is still in progress
git reset --hard HEAD  # Clean any changes

# Create a clean feature branch
git checkout main
git checkout -b rebase-feature

# Make commits on feature branch
echo "Rebase feature line 1" >> rebase-file.txt
git add rebase-file.txt
git commit -m "Rebase feature commit 1"

echo "Rebase feature line 2" >> rebase-file.txt
git commit -am "Rebase feature commit 2"

# Switch to main and add commits there
git checkout main
echo "Main development" >> main-development.txt
git add main-development.txt
git commit -m "Main development commit"

# View the diverged history
git log --oneline --graph --all
```

### Examine before rebase
```bash
# Check current commit SHAs
git rev-parse rebase-feature
git rev-parse main

# See the common ancestor
git merge-base main rebase-feature
```

### Perform the rebase
```bash
# Switch to feature branch
git checkout rebase-feature

# Rebase onto main
git rebase main

# Check new commit SHAs (they should be different!)
git rev-parse rebase-feature
git log --oneline --graph --all
```

## Interactive rebase

Interactive rebase allows you to edit the commit history during the replay process.

### Basic interactive rebase
```bash
# Edit last 3 commits
git rebase -i HEAD~3

# Edit commits from a specific point
git rebase -i <commit-sha>
```

### Interactive rebase options
- **pick**: Use the commit as-is
- **reword**: Use commit but edit the message
- **edit**: Use commit but stop to make changes
- **squash**: Combine with previous commit
- **fixup**: Like squash but discard commit message
- **drop**: Remove the commit entirely

### Hands-on interactive rebase
```bash
# Create multiple small commits
echo "Small change 1" >> small-changes.txt
git add small-changes.txt
git commit -m "Small change 1"

echo "Small change 2" >> small-changes.txt
git commit -am "Small change 2"

echo "Small change 3" >> small-changes.txt
git commit -am "Small change 3"

# Interactive rebase to squash them
git rebase -i HEAD~3

# In the editor, change:
# pick abc123 Small change 1
# squash def456 Small change 2
# squash ghi789 Small change 3
```

## Advanced rebase scenarios

### Rebase with conflicts
When conflicts occur during rebase:
```bash
git rebase main
# Conflict occurs

# Resolve conflicts in files
# Then continue:
git add <resolved-files>
git rebase --continue

# Or abort if needed:
git rebase --abort
```

### Rebase onto specific commit
```bash
# Rebase onto a specific commit instead of branch tip
git rebase <commit-sha>

# Rebase a range of commits
git rebase --onto <new-base> <old-base> <branch>
```

## When to use rebase vs merge

### Use rebase when:
- You want a linear, clean history
- Working on a private feature branch
- Commits haven't been shared/pushed yet
- You want to incorporate upstream changes

### Use merge when:
- You want to preserve the context of feature development
- Working on shared/public branches
- You want to maintain the true history of parallel development
- Collaborating with others who might have based work on your commits

## Golden rule of rebasing

**Never rebase commits that have been pushed and shared with others.**

Why? Because rebase creates new commits with different SHAs, anyone who has based work on the original commits will have problems when you force-push the rebased version.

## Practical rebase workflows

### Feature branch workflow
```bash
# Start feature
git checkout -b feature
# Make commits...

# Before merging, rebase to get latest main
git checkout main
git pull origin main
git checkout feature
git rebase main

# Now merge with clean history
git checkout main
git merge feature  # Fast-forward merge
```

### Cleaning up commits before push
```bash
# Interactive rebase to clean up commit history
git rebase -i HEAD~5

# Squash related commits
# Fix commit messages
# Remove unnecessary commits
```

## Key insights

- Rebase rewrites history by creating new commits
- Each replayed commit gets a new SHA-1 hash
- Interactive rebase is powerful for cleaning up commit history
- Rebase creates linear history, merge preserves parallel development
- Never rebase shared/public commits
- Rebase is excellent for incorporating upstream changes
- Conflicts during rebase are resolved commit-by-commit
