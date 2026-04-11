
Before destructive operations (`reset --hard`, `rebase`, `force push`):

- [ ] Is this a shared branch? → Don't rewrite history
- [ ] Do I have uncommitted changes? → Stash or commit first
- [ ] Am I on the right branch? → `git branch` to verify
- [ ] Is remote up to date? → `git fetch` first

## Common Traps

- **git user.email wrong** — Verify with `git config user.email` before important commits
- **Empty directories** — Git doesn't track them, add `.gitkeep`
- **Submodules** — Always clone with `--recurse-submodules`
- **Detached HEAD** — Use `git switch -` to return to previous branch
- **Push rejected** — Usually needs `git pull --rebase` first
- **stash pop on conflict** — Stash disappears. Use `stash apply` instead
- **Large files** — Use Git LFS for files >50MB, never commit secrets
- **Case sensitivity** — Mac/Windows ignore case, Linux doesn't — causes CI failures

## Recovery Commands

- Undo last commit keeping changes: `git reset --soft HEAD~1`
- Discard unstaged changes: `git restore filename`
- Find lost commits: `git reflog` (keeps ~90 days of history)
- Recover deleted branch: `git checkout -b branch-name <sha-from-reflog>`
- Use `git add -p` for partial staging when commit mixes multiple changes

## Debugging with Bisect

Find the commit that introduced a bug:
```bash
git bisect start
git bisect bad                    # current commit is broken
git bisect good v1.0.0            # this version worked
# Git checks out middle commit, test it, then:
git bisect good                   # or git bisect bad
# Repeat until Git finds the culprit
git bisect reset                  # return to original branch
```

## Quick Summary

```bash
git status -sb                    # short status with branch
git log --oneline -5              # last 5 commits
git shortlog -sn                  # contributors by commit count
git diff --stat HEAD~5            # changes summary last 5 commits
git branch -vv                    # branches with tracking info
git stash list                    # pending stashes
```

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `gitlab` — GitLab CI/CD and merge requests
- `docker` — Containerization workflows
- `code` — Code quality and best practices

## Feedback

- If useful: `clawhub star git`
- Stay updated: `clawhub sync`
