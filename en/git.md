# 🔧 Git and GitHub CLI Cheat Sheet

> 📘 Basic and advanced Git commands for version control, branching, remote repos, stash, tags and GitHub CLI.

---

## 📂 Contents

- [🔧 Git and GitHub CLI Cheat Sheet](#-git-and-github-cli-cheat-sheet)
  - [📂 Contents](#-contents)
  - [🔹 Basic Commands](#-basic-commands)
  - [🌿 Branching and Merging](#-branching-and-merging)
  - [📡 Remote Repositories](#-remote-repositories)
  - [📦 Stash and Cleanup](#-stash-and-cleanup)
  - [🏷️ Tags](#️-tags)
  - [🛠️ Conflict Resolution](#️-conflict-resolution)
  - [⚙️ Advanced Commands](#️-advanced-commands)
  - [🐙 GitHub CLI](#-github-cli)
  - [💡 Git Aliases (Useful Shortcuts)](#-git-aliases-useful-shortcuts)
  - [🚀 Advanced Git Commands for Professionals](#-advanced-git-commands-for-professionals)
  - [🧰 Pro Workflow Tips and Automation](#-pro-workflow-tips-and-automation)
  - [Additional resources](#additional-resources)

---

## 🔹 Basic Commands

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`git add`**](https://git-scm.com/docs/git-add) | | **Add a file to the staging area** |
|               | `git add file.txt`                  | Stage a specific file for the next commit |
|               | `git add .`                         | Stage all changes in the current directory and below |
|               | `git add -p`                        | Interactively choose which parts of files to stage (useful for partial commits) |
| [**`git clone`**](https://git-scm.com/docs/git-clone) | | **Clone a repository into a new directory** |
|               | `git clone -b branch_name URL`      | Clone only the specified branch (instead of the default) |
|               | `git clone --depth 1 URL`           | Clone only the latest commit, making a shallow copy to save time and space |
| [**`git commit`**](https://git-scm.com/docs/git-commit) | | **Record changes to the repository** |
|               | `git commit -m "Initial commit"`    | Commit with a message without opening the editor |
|               | `git commit -a -m "Fix bugs"`       | Stage and commit all modified tracked files with a message |
|               | `git commit --amend`                | Update the last commit (change message or include more changes) |
|               | `git commit --fixup abc1234`        | Create a fixup commit to automatically squash later during interactive rebase |
| [**`git config`**](https://git-scm.com/docs/git-config) | | **Get and set repository or global options** |
|               | `git config --global user.name "Name"`  | Set global Git username |
|               | `git config --global user.email "email@example.com"` | Set global Git email |
|               | `git config --list`                 | List all Git settings (name, email, editor, etc.) |
| [**`git diff`**](https://git-scm.com/docs/git-diff) | | **Show changes between commits, commit and working tree, etc.** |
|               | `git diff HEAD`                     | Show what you changed since the last commit (unstaged changes) |
|               | `git diff --staged`                 | Show what will be included in the next commit |
|               | `git diff --word-diff HEAD~1`       | Show changes with word-level differences |
| [**`git grep`**](https://git-scm.com/docs/git-grep) | | **Search inside repository files** |
|               | `git grep "functionName"`           | Find all mentions of `functionName` in all project files |
|               | `git grep -n "TODO"`                | Find lines containing `TODO` and show line numbers (useful for finding code notes) |
|               | `git grep -i "login"`               | Search for the word `login` case-insensitively (matches `Login`, `LOGIN`, `login`, etc.) |
| [**`git init`**](https://git-scm.com/docs/git-init) | | **Create an empty Git repository or reinitialize an existing one** |
|               | `git init my-project`               | Initialize a new repo in directory my-project |
|               | `git init --bare`                   | Initialize a bare repository |
| [**`git log`**](https://git-scm.com/docs/git-log) | | **Show commit logs** |
|               | `git log --oneline`                 | Show commit history in a compact one-line format |
|               | `git log --graph --all`             | Show all branches in a visual graph of commits |
|               | `git log -p --stat`                 | Show patch and file change stats for commits |
| [**`git reset`**](https://git-scm.com/docs/git-reset) | | **Unstage files, keeping changes in the working directory** |
|               | `git reset HEAD file.txt`           | Remove a file from staging (keeps your edits) |
|               | `git reset --hard HEAD~1`           | Go back one commit and delete all changes (irreversible!) |
|               | `git reset --soft HEAD~1`           | Undo last commit but keep the changes ready to commit again |
|               | `git reset --mixed HEAD~1`          | Undo a commit but keep changes unstaged in working directory |
| [**`git show`**](https://git-scm.com/docs/git-show) | | **Show various types of objects** |
|               | `git show <commit_hash>`            | Show changes and message of a specific commit |
|               | `git show HEAD~1`                   | Show the previous commit before the current one |
|               | `git show --stat`                   | Show a summary of file changes for the latest commit |
| [**`git status`**](https://git-scm.com/docs/git-status) | | **Show the working tree status** |
|               | `git status -s`                     | Show status in short format |
|               | `git status -b`                     | Show current branch and status of files |

---

## 🌿 Branching and Merging

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`git branch`**](https://git-scm.com/docs/git-branch) | | **Create, list or delete branches** |
|               | `git branch new-feature`            | Create a new branch called `new-feature` |
|               | `git branch -d old-feature`         | Delete a local branch named `old-feature` |
| [**`git checkout`**](https://git-scm.com/docs/git-checkout) | | **Switch branches or restore files from another commit** |
|               | `git checkout main`                 | Switch to the `main` branch |
|               | `git checkout -b new-branch`        | Create and switch to a new branch named `new-branch` |
| [**`git switch`**](https://git-scm.com/docs/git-switch) | | **Switch branches (simplified alternative to `checkout`)** |
|               | `git switch main`                   | Switch to the `main` branch |
|               | `git switch -c feature-x`           | Create and switch to a new branch named `feature-x` |
|               | `git switch new-feature`            | Switch to an existing branch named `new-feature` |
| [**`git merge`**](https://git-scm.com/docs/git-merge) | | **Combine changes from another branch into the current one** |
|               | `git merge new-feature`             | Merge the `new-feature` branch into the current branch |
|               | `git merge --no-ff new-feature`     | Always create a merge commit (even if fast-forward is possible) |
|               | `git merge --abort`                 | Cancel the merge and revert changes if conflicts occur |
| [**`git rebase`**](https://git-scm.com/docs/git-rebase) | | **Move or reapply commits onto a new base commit** |
|               | `git rebase main`                   | Reapply your branch commits on top of the `main` branch |
|               | `git rebase -i HEAD~3`              | Interactively edit the last 3 commits |
|               | `git rebase --abort`                | Stop and undo an in-progress rebase |
|               | `git rebase -i --autosquash HEAD~5` | Automatically squash commits marked as fixup or squash during interactive rebase |
| [**`git cherry-pick`**](https://git-scm.com/docs/git-cherry-pick) | | **Apply specific commits from another branch** |
|               | `git cherry-pick <hash>`            | Apply a specific commit (by hash) to the current branch |
|               | `git cherry-pick --continue`        | Continue cherry-pick after resolving conflicts |
|               | `git cherry-pick A^..B`             | Apply a range of commits from `A` (excluding) to `B` (including) |

---

## 📡 Remote Repositories

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`git remote`**](https://git-scm.com/docs/git-remote) | | **Manage links to remote repositories (like GitHub)** |
|               | `git remote -v`                     | Show remote names and their URLs |
|               | `git remote add origin URL`         | Add a remote repository named `origin` |
| [**`git pull`**](https://git-scm.com/docs/git-pull) | | **Download and automatically merge changes from a remote branch** |
|               | `git pull origin main`              | Fetch and merge changes from remote `main` branch into your current branch |
|               | `git pull --rebase origin main`     | Fetch and rebase your current branch on top of the remote branch instead of merging |
| [**`git push`**](https://git-scm.com/docs/git-push) | | **Upload your local changes to a remote repository** |
|               | `git push origin main`              | Push your local `main` branch to the remote `origin` |
| [**`git fetch`**](https://git-scm.com/docs/git-fetch) | | **Download changes from remote without merging** |
|               | `git fetch origin`                  | Fetch all updates from remote `origin`, but don’t apply them yet |
|               | `git fetch origin main`             | Fetch only the `main` branch from remote |
|               | `git fetch --all`                   | Fetch updates from all remotes |
|               | `git fetch --prune`                 | Clean up deleted branches — remove local refs to branches that were deleted remotely |
|               | `git fetch --dry-run`               | Show what would be fetched, without actually downloading anything |
|               | `git fetch origin +main`            | Forcefully update your local tracking branch (`origin/main`), overwriting conflicts |

---

## 📦 Stash and Cleanup

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`git stash`**](https://git-scm.com/docs/git-stash) | | **Temporarily save uncommitted changes (work in progress)** |
|               | `git stash`                         | Save modified and staged files, then revert working directory to last commit |
|               | `git stash apply`                   | Reapply the latest stashed changes (stash remains saved) |
|               | `git stash pop`                     | Reapply and remove the latest stash |
|               | `git stash list`                    | Show list of all stashed changes |
|               | `git stash branch feature-fix`      | Create a new branch and apply the latest stash to it |
| [**`git clean`**](https://git-scm.com/docs/git-clean) | | **Permanently delete untracked files (not in Git)** |
|               | `git clean -f`                      | Delete untracked files in the current directory |
|               | `git clean -fd`                     | Delete untracked files and folders |
|               | `git clean -n`                      | Preview what will be deleted (safe dry run) |

---

## 🏷️ Tags

| Command       | Example                            | Description |
| ------------- | ---------------------------------- | ----------- |
| [**`git tag`**](https://git-scm.com/docs/git-tag) | | **Create, list or delete tags to mark specific points in history (like releases)** |
|               | `git tag -a v1.0 -m "Version 1.0"` | Create an annotated tag named `v1.0` with a message (saved as a full Git object, good for releases) |
|               | `git tag -d v1.0`                  | Delete the local tag named `v1.0` (does not affect remote) |
| [**`git push`**](https://git-scm.com/docs/git-push) | | **Upload commits, branches and tags from local to remote repository** |
|               | `git push origin --tags`           | Push all local tags to the remote (useful after tagging multiple versions) |
|               | `git push origin v1.0`             | Push a specific tag (e.g. `v1.0`) to the remote repository |
|               | `git push origin :refs/tags/v1.0`  | Delete the remote tag `v1.0` (note the colon syntax) |

---

## 🛠️ Conflict Resolution

| Command          | Example                                   | Description |
| ---------------- | ----------------------------------------- | ----------- |
| [**`git mergetool`**](https://git-scm.com/docs/git-mergetool) | | **Open a visual tool to help resolve merge conflicts** |
|                  | `git mergetool --tool=meld`               | Use a specific merge tool (like Meld) to fix conflicts |
| [**`git rerere`**](https://git-scm.com/docs/git-rerere) | | **Let Git remember how you solved merge conflicts before** |
|                  | `git config --global rerere.enabled true` | Enable automatic reuse of past conflict resolutions |
|                  | `git rerere status`                       | Show which files have saved conflict resolutions |
|                  | `git rerere diff`                         | Show what changes Git saved for future reuse |

---

## ⚙️ Advanced Commands

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`git bisect`**](https://git-scm.com/docs/git-bisect) | | **Use binary search to find the commit that introduced a bug** |
|               | `git bisect start`                  | Start a binary search between a known good and a bad commit to locate a bug |
|               | `git bisect bad`                    | Mark the current commit as "bad" (contains the bug) |
|               | `git bisect good <commit>`          | Mark a known "good" commit where the bug did not exist |
| [**`git blame`**](https://git-scm.com/docs/git-blame) | | **Show who last modified each line of a file, with revision and author** |
|               | `git blame file.txt`                | Show the author and commit info for every line in the file |
|               | `git blame -L 10,20 file.txt`       | Show blame info only for lines 10 through 20 |
|               | `git blame --show-email file.txt`   | Show authors’ email addresses alongside line changes |
| [**`git reflog`**](https://git-scm.com/docs/git-reflog) | | **View and manage the reference log (reflog) of branch movements and HEAD** |
|               | `git reflog show main@{1.week.ago}` | See where the `main` branch pointed one week ago |
|               | `git reflog expire --expire=30.days --dry-run` | Preview which reflog entries older than 30 days can be cleaned up (no changes made) |
|               | `git reflog delete HEAD@{2}`        | Delete a specific reflog entry (use carefully, as it can affect recovery) |
| [**`git submodule`**](https://git-scm.com/docs/git-submodule) | | **Add, initialize, update, or inspect submodules (repositories inside repositories)** |
|               | `git submodule add URL path`        | Add an external repository as a submodule in the specified path |
|               | `git submodule update --init`       | Initialize and download all submodules listed in the repository |
|               | `git submodule foreach git pull`    | Run `git pull` inside each submodule to update them to their latest commit |
|               | `git submodule sync --recursive`    | Synchronize submodule URLs after changes in `.gitmodules` file |
|               | `git submodule update --remote --merge` | Update submodules to the latest commit from their remote branches |
| [**`git archive`**](https://git-scm.com/docs/git-archive) | | **Create an archive (zip, tar, etc.) of files from a specific commit or branch** |
|               | `git archive --format=zip HEAD > archive.zip` | Create a ZIP archive of the current project files at HEAD |
|               | `git archive -o release.tar.gz HEAD` | Create a compressed `.tar.gz` archive from the current HEAD |
|               | `git archive --format=tar --prefix=project/ HEAD \| gzip > project.tar.gz` | Create a compressed `.tar.gz` archive of the current project, placing all files inside a folder named `project/` inside the archive |
| [**`git gc`**](https://git-scm.com/docs/git-gc) | | **Clean up unnecessary files and optimize the repository for performance** |
|               | `git gc --aggressive`               | Perform a thorough cleanup and optimization (can be slow but effective) |
|               | `git gc --prune=now`                | Remove all unreachable objects immediately (dangerous if unsure) |
| [**`git shortlog`**](https://git-scm.com/docs/git-shortlog) | | **Quick summary of authors and their commits** |
|               | `git shortlog -e`                   | Show a list of authors with their email addresses (e.g., to analyze who contributed and how much) |
|               | `git shortlog -s -n`                | Show how many commits each author made, sorted by number of commits |
|               | `git shortlog -sne`                 | Same as above, but also includes names and email addresses — useful for detailed activity tracking |
| [**`git revert`**](https://git-scm.com/docs/git-revert) | | **Create a new commit that undoes changes from a previous commit without rewriting history** |
|               | `git revert HEAD`                   | Undo the last commit by creating a new commit that reverses its changes |
|               | `git revert <commit_hash>`          | Undo a specific commit by hash, safely adding a new commit that reverses it |

---

## 🐙 GitHub CLI

> `gh` lets you manage GitHub from the terminal.

| Command       | Example                             | Description |
| ------------- | ----------------------------------- | ----------- |
| [**`gh auth login`**](https://cli.github.com/manual/gh_auth_login) | | **Authenticate with a GitHub host to allow CLI commands to interact with your account** |
|               | `gh auth login --with-token < mytoken.txt` | Authenticate using a personal access token stored in a file (`mytoken.txt`) |
|               | `gh auth login --hostname enterprise.internal` | Authenticate to a GitHub Enterprise server (not github.com) |
| [**`gh repo clone`**](https://cli.github.com/manual/gh_repo_clone) | | **Clone a GitHub repository to your local machine** |
|               | `gh repo clone user/repo`           | Clone the repository repo owned by `user` into a folder named `repo` |
|               | `gh repo clone cli/cli -- --depth=1` | Clone the repository but only download the latest commit for a faster, smaller clone |
|               | `gh repo clone cli/cli workspace/cli` | Clone the repository into a custom folder `workspace/cli` |
| [**`gh issue list`**](https://cli.github.com/manual/gh_issue_list) | | **List issues in a GitHub repository, optionally filtered by various criteria** |
|               | `gh issue list --assignee "@me"`    | List issues assigned to you |
|               | `gh issue list --state all`         | List issues regardless of state (open or closed) |
|               | `gh issue list --search "error no:assignee sort:created-asc"` | List issues matching "error", unassigned, sorted by creation date ascending |
| [**`gh pr create`**](https://cli.github.com/manual/gh_pr_create) | | **Create a pull request on GitHub via CLI** |
|               | `gh pr create --title "..."`        | Create a pull request with the given title |
|               | `gh pr create --project "Roadmap"`  | Link the pull request to a GitHub project named "Roadmap" |
|               | `gh pr create --base develop --head monalisa:feature` | Create a PR from branch `feature` in fork `monalisa` into `develop` branch |
| [**`gh repo create`**](https://cli.github.com/manual/gh_repo_create) | | **Create a new GitHub repository from CLI** |
|               | `gh repo create my-project`         | Create a new repository called `my-project` on GitHub (interactive prompts follow) |
|               | `gh repo create my-project --public --clone` | Create a public repository and clone it locally |
|               | `gh repo create my-project --private --source=. --remote=upstream` | Create a private remote repo from current folder and add remote named `upstream` |

---

## 💡 Git Aliases (Useful Shortcuts)

Set up convenient aliases to speed up common Git commands:

```bash
git config --global alias.br branch                                       # shortcut for: git branch
git config --global alias.ci commit                                       # shortcut for: git commit
git config --global alias.co checkout                                     # shortcut for: git checkout
git config --global alias.graph "log --oneline --graph --all --decorate"  # pretty history graph
git config --global alias.last "log -1 HEAD"                              # show the last commit
git config --global alias.st status                                       # shortcut for: git status
```

---

## 🚀 Advanced Git Commands for Professionals

| Command       | Example                                   | Description & Usage |
| ------------- | ----------------------------------------- | ------------------- |
| [**`git filter-repo`**](https://github.com/newren/git-filter-repo) | | **A powerful and performant tool for rewriting Git history to remove or modify files, authorship, or paths; replaces git filter-branch with improved speed and safety** |
|               | `git filter-repo --path secret.txt --invert-paths` | Efficiently rewrite repository history to remove sensitive files or directories without the performance issues of `git filter-branch`. Use with care |
|               | `git filter-repo --replace-text replacements.txt` | Bulk replace strings or patterns across entire history (e.g., sanitize credentials) |
|               | `git filter-repo --subdirectory-filter src` | Extract subdirectory history into a new repository, preserving commit metadata |
| [**`git worktree`**](https://git-scm.com/docs/git-worktree) | | **Manage multiple working directories linked to a single repository, allowing concurrent work on different branches without cloning** |
|               | `git worktree add ../feature feature-branch` | Create an additional working tree attached to the same repository, enabling parallel branch checkouts without clones |
|               | `git worktree list`                       | List all active worktrees, their paths and associated branches |
|               | `git worktree remove ../feature`          | Remove a linked worktree when no longer needed, cleaning up working directories safely |
| [**`git replace`**](https://git-scm.com/docs/git-replace) | | **Create temporary references that replace existing objects, enabling non-destructive local history manipulation and testing** |
|               | `git replace <old_commit> <new_commit>` | Temporarily swap one commit for another in your local repo, useful for testing or patching history without rewriting it |
|               | `git replace --list`                      | Show all active replacement refs |
|               | `git replace -d <replace_ref>`            | Delete a specific replacement reference to revert behavior |
| [**`git stash`**](https://git-scm.com/docs/git-stash) | | **Temporarily save uncommitted changes to a stack, allowing context switches without committing unfinished work** |
|               | `git stash push -p`                       | Interactively select hunks of changes to stash, providing granular control over what is saved |
|               | `git stash push -m "WIP selective stash"` | Create a stash with a custom message for easier identification |
|               | `git stash apply stash@{2}`               | Apply a specific stash from the stash list, without dropping it |
| [**`git rebase`**](https://git-scm.com/docs/git-rebase) | | **Reapply commits on top of another base tip, facilitating a cleaner, linear project history and interactive history editing** |
|               | `git rebase --interactive --autosquash`   | Start an interactive rebase session that automatically reorders and squashes commits marked as fixup or squash, streamlining history cleanup |
|               | `git rebase -i --autosquash HEAD~10`      | Automatically reorder and squash commits marked as fixup or squash, cleaning commit history before pushing |
|               | `git commit --fixup <commit>`             | Create a fixup commit that will be autosquashed during interactive rebase |
|               | `git commit --squash <commit>`            | Create a squash commit to combine with the specified commit on rebase |
| [**`git bisect`**](https://git-scm.com/docs/git-bisect) | | **Binary search tool to efficiently identify the commit that introduced a bug by testing successive commits and narrowing down the faulty change** |
|               | `git bisect run` | Automate the bisect process by running a specified test script on each commit to quickly identify the commit that introduced a bug without manual intervention |
|               | `git bisect start; git bisect bad; git bisect good v1.0; git bisect run ./test.sh` | Automate bisection by running a test script on each commit, significantly speeding up bug identification |
|               | `git bisect visualize`                    | Open a graphical tool to visualize the bisection process |
|               | `git bisect reset`                        | Exit bisect mode and return to the original HEAD |
| [**`git commit`**](https://git-scm.com/docs/git-commit) | | **Record changes to the repository with detailed options for amend, sign, fixup, and message customization to maintain high-quality project history** |
|               | `git commit --gpg-sign` | Create a commit signed with your GPG key to ensure cryptographic verification of the commit’s authenticity and authorship |
|               | `git commit -S -m "Signed commit"`        | Cryptographically sign your commits with your GPG key, ensuring integrity and authorship verification |
|               | `git config --global user.signingkey <key_id>` | Configure the GPG key used to sign commits globally |
|               | `git log --show-signature`                | Verify and display GPG signature info for commits. |
| [**`git reflog`**](https://git-scm.com/docs/git-reflog) | | **Keep a log of updates to HEAD and branches, essential for recovering lost commits and understanding local history movements** |
|               | `git reset --hard HEAD@{3}`               | Reset the current branch to a previous state from reflog to recover or undo changes |
|               | `git reflog expire --expire=now --all`    | Immediately expire all reflog entries, cleaning up reflog history (use with caution) |

---

## 🧰 Pro Workflow Tips and Automation

| Topic                        | Commands / Example                      | Explanation & Pro Tips |
| ---------------------------- | --------------------------------------- | ---------------------- |
| **Aggressive Repo Cleanup**  | `git gc --aggressive --prune=now`       | Performs deep garbage collection and prunes unreachable objects immediately for repository optimization. Use during maintenance windows |
| **Parallel Branch Worktrees** | `git worktree add ../feature-branch feature` | Keep multiple working trees for simultaneous feature development, avoids clone overhead |
| **Clean, Linear History**    | `git rebase -i --autosquash`            | Before pushing, rebase interactively with autosquash to keep history clean and readable |
| **Secure Commits**           | `git commit -S`                         | Sign commits with GPG to enhance trustworthiness in shared repositories, mandatory in many enterprise environments |
| **Automated Bisecting**      | `git bisect run ./test-script.sh`       | Automate bug hunting by running a test script on each candidate commit during bisect |
| **Conflict Resolution Cache** | `git config --global rerere.enabled true` | Enable reuse of conflict resolutions to speed up resolving repeated merge conflicts across rebases or merges |
| **Shared Aliases and Hooks** | | Store common Git aliases and commit hooks in a shared repo or CI pipeline to enforce team standards and improve productivity |

---

## Additional resources

🌐 Useful links:

📘 **Official Git documentation** — detailed manual for all Git commands:  
[https://git-scm.com/docs](https://git-scm.com/docs)

📙 **Learn Git Branching** — interactive visual tutorial to master branching concepts:  
[https://learngitbranching.js.org](https://learngitbranching.js.org)

📕 **Pro Git book** (free, by Scott Chacon & Ben Straub):  
[https://git-scm.com/book](https://git-scm.com/book)

📗 **Git Cheatsheet** (official concise reference):  
[https://education.github.com/git-cheat-sheet-education.pdf](https://education.github.com/git-cheat-sheet-education.pdf)

🧠 **Tip:** Don't try to memorize everything. Use `--help`, explore, and practice regularly:

```bash
git help <command>
git status
```
