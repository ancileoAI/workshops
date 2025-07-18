# 7. git merge

## What is merging?

Merging is the process of combining the recent changes from several branches into a single new commit. This commit points back to multiple parent commits, creating a merge commit that joins different development histories.

## Types of merges

### 1. Fast-forward merge
When the target branch hasn't diverged from the source branch:

```
main:     A---B---C
feature:          D---E

# After merge:
main:     A---B---C---D---E
```

Git simply moves the branch pointer forward. No merge commit needed.

### 2. Three-way merge
When both branches have diverged from a common ancestor:

```
main:     A---B---C---F
               \
feature:        D---E

# After merge:
main:     A---B---C---F---M
               \         /
feature:        D---E---/
```

Git creates a merge commit (M) with two parents.

## The three-way merge algorithm

Git's merge algorithm uses three commits:
1. **Merge base**: Common ancestor of both branches
2. **Ours**: Current branch (where you're merging into)
3. **Theirs**: Branch being merged

### Step-by-step process

1. **Find merge base**
   ```bash
   git merge-base main feature
   ```

2. **Calculate diffs**
   - Diff from merge base to "ours"
   - Diff from merge base to "theirs"

3. **Apply three-way merge algorithm**
   For each file/line, Git decides:
   - If base = ours ≠ theirs → take theirs
   - If base = theirs ≠ ours → take ours  
   - If ours = theirs ≠ base → take ours/theirs
   - If base = ours = theirs → take any (all same)
   - If all different → **conflict**

## Hands-on merge exploration

### Setup merge scenario (using sample-repo)
```bash
# Navigate to our existing repository
cd sample-repo

# Check current status
git log --oneline
git status

# Create feature branch from current state
git checkout -b feature-branch

# Make a change on feature branch
echo "Feature line added" >> hello.txt
git commit -am "Add feature line"

# Switch back to main and make conflicting change
git checkout main
echo "Main line added" >> hello.txt
git commit -am "Add main line"

# Now we have diverged branches
git log --oneline --graph --all
```

### Examine merge base
```bash
git merge-base main feature-branch
git show <merge-base-sha>

# The merge base should be our original "Initial commit"
git log --oneline main feature-branch
```

### Attempt merge
```bash
# Make sure we're on main branch
git checkout main

# Attempt to merge feature branch
git merge feature-branch
# This will create a conflict in hello.txt!

# Check the conflict
cat hello.txt
git status
```

## Understanding merge conflicts

### What causes conflicts?
Conflicts occur when:
- Same lines modified differently in both branches
- One branch modifies a line, other deletes it
- File added with same name but different content

### Conflict markers
```
<<<<<<< HEAD (ours)
Line 2 from main
=======
Line 2 from feature
>>>>>>> feature (theirs)
```

### Conflict resolution process
1. Edit files to resolve conflicts
2. Remove conflict markers
3. Stage resolved files: `git add <file>`
4. Complete merge: `git commit`

## Advanced merge concepts

### Merge strategies
```bash
# Recursive (default for two branches)
git merge -s recursive feature

# Octopus (for multiple branches)
git merge -s octopus branch1 branch2 branch3

# Ours (ignore other branch's changes)
git merge -s ours feature
```

### Merge options
```bash
# Force merge commit even if fast-forward possible
git merge --no-ff feature

# Abort merge if conflicts occur
git merge --abort

# Use specific strategy for conflicts
git merge -X ours feature    # Prefer our changes
git merge -X theirs feature  # Prefer their changes
```

## What happens during merge

### Successful merge
1. Git finds merge base
2. Calculates and applies diffs
3. Updates working directory and index
4. Creates merge commit (if not fast-forward)
5. Updates current branch pointer

### Conflicted merge
1. Git finds merge base
2. Attempts to apply diffs
3. Stops when conflicts detected
4. Leaves conflict markers in files
5. Waits for manual resolution

## Examining merge commits

### Merge commit structure
```bash
# After successful merge
git show --format=fuller HEAD

# Shows two parents
git cat-file -p HEAD
```

### Merge commit characteristics
- Has multiple parent commits
- Contains metadata about the merge
- Tree represents combined state of both branches

## Best practices

### Before merging
- Ensure working directory is clean
- Review changes being merged
- Consider using `git log --graph` to visualize

### During conflicts
- Understand what each side changed
- Test the resolution
- Make minimal changes to resolve conflict

### After merging
- Verify the merge worked correctly
- Run tests to ensure functionality
- Consider cleaning up feature branches
