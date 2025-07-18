# 2. Git distributed model

## Centralized vs distributed version control

### Centralized model (SVN, CVS, Perforce)
- Single central server holds the entire history
- Developers check out working copies from the server
- All operations (commit, log, diff) require server communication
- Single point of failure - if server goes down, no one can work
- Network dependency for most operations
- Branching and merging are expensive operations

### Distributed model (Git, Mercurial)
- Every clone is a complete repository with full history
- Most operations are local and fast
- Multiple backup points (every clone is a backup)
- Can work offline indefinitely
- Flexible workflows - no single "correct" way to collaborate
- Branching and merging are lightweight operations

## How Git's distributed nature works

### Every repository is equal
- No single repository is more "official" than others
- Each clone contains the complete project history
- You can work entirely locally and sync with others later
- Multiple remotes possible (origin, upstream, fork, etc.)

### Local operations are fast
Since you have the complete history locally:
- `git log` - instant, no server needed
- `git diff` - compare any two commits instantly
- `git branch` - create branches in milliseconds
- `git commit` - record changes without network

### Network operations are explicit
Only these operations require network access:
- `git clone` - get initial copy
- `git fetch` / `git pull` - get updates from remote
- `git push` - send your changes to remote

## Advantages of Git's approach

### Performance
- Most operations are instant (local filesystem speed)
- Only sync with network when you choose to
- Large projects remain fast due to efficient storage

### Reliability
- Every clone is a complete backup
- No single point of failure
- Work continues even if central server is down

### Flexibility
- Support for various workflows (centralized, feature branch, fork/PR)
- Can collaborate without a central server
- Easy to experiment with branches and merge strategies

### Offline capability
- Full functionality without internet connection
- Commit, branch, merge, view history all work offline
- Sync when connectivity returns
