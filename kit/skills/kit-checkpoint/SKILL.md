---
name: kit-checkpoint
description: Saves the current state of a project in git with a clear message, so it can always be got back, and optionally backs it up to GitHub. Use when the person says "save", "checkpoint", "commit", "back this up", "I want to be able to undo", after a piece of work starts working, or before a risky change.
---

# Checkpoint

A checkpoint is a git commit: a saved snapshot of the project that can be compared with or restored later.

1. **Find the repository.** Run `git status` in the project folder. If it is not a git repository, offer to make it one (`git init`) and explain why in one line. If git is not installed, offer to install it (Windows: `winget install --id Git.Git -e`; macOS: `xcode-select --install`).
2. **Look before saving.** Summarize the changes in plain words (which files, what changed). Check for things that must never be committed: `.env` files, keys, tokens, passwords, large build output, `node_modules/`. Add them to `.gitignore` and leave them out. If a secret was already committed earlier, say so and explain the fix (rotate the secret, then clean history) before going further.
3. **Commit.** Stage the files by path (not `git add -A` blindly), then commit with a short message that says what now works, for example "Add the chore list page with weekly rotation". If git asks who they are, set `user.name` and `user.email` for this repository after asking what to use.
4. **Back up (optional).** If the repository has a remote, offer to push. If it has none and they want an online backup, offer a **private** GitHub repository: with the GitHub CLI (`gh repo create <name> --private --source . --push`, after `gh auth login`) or the VS Code Source Control view's "Publish to GitHub" button. Never make a repository public unless they ask for that.
5. **Report.** One line: what was saved, and how to get back to it ("ask me to show the checkpoints, or to go back to this one").

Restoring: when asked to go back, show recent checkpoints (`git log --oneline -10`), confirm which one, and prefer non-destructive ways (a new branch, or `git revert`) over discarding work. Never run `git reset --hard` or delete branches without explaining what would be lost and getting a clear yes.
