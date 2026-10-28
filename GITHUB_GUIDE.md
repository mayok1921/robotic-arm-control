# Git & GitHub: Beginner's Guide

A practical reference for **any type of project**—Python, Arduino, MATLAB, documents, or other files. The [robotic arm repository](https://github.com/mayok1921/robotic-arm-control) is just an example.

## First: what the words mean

- **Git** tracks changes to files on your computer.
- **GitHub** hosts a copy of your Git project online.
- **Repository (repo)** means a project tracked by Git.
- **Clone** copies a repository to your computer (usually once per computer).
- **Add** selects changes for the next snapshot.
- **Commit** saves the snapshot **locally**.
- **Push** uploads your commits to GitHub.
- **Pull** retrieves and merges remote changes.

## A. Set up on a new computer

1. Install Git (check with `git --version`).
2. Open Terminal, PowerShell, or the VS Code terminal.
3. Copy the repository's HTTPS URL from GitHub → **Code**.
4. In the folder where you want the project, run:

```bash
git clone https://github.com/mayok1921/robotic-arm-control.git
cd robotic-arm-control
```

For a different project, replace the URL with its repository URL. Don't clone the same repo repeatedly just to update it; use `git pull` instead.

## B. Everyday workflow (existing cloned repository)

Open a terminal **inside your repository folder**:

```bash
git status
git pull
```

Edit and test your files using your usual software. Then:

```bash
git status
git diff
git add filename.ext
git diff --staged
git commit -m "Briefly describe what changed"
git push
```

Replace `filename.ext` with your actual file. For example:

```bash
git add s550_control.py
git commit -m "Improve S550 startup communication"
git push
```

If you intend to include *every* changed file under your current folder, use `git add .` instead—but **review `git status` first** to avoid uploading generated files, secrets, or unrelated work.

**Important:** `commit` is a local save; `push` is what sends it to GitHub. Pushing requires internet access and permission to the repository.

## C. Find your folder and repository

```bash
pwd                         # Current folder (Linux/macOS)
ls                          # Files here (also works in PowerShell)
git status                  # Am I in a Git repository?
git remote -v               # Which online repository is connected?
git branch --show-current   # Which branch am I using?
git log --oneline -5        # Last five commits
```

Change folders using `cd path/to/folder`. For example, an Orange Pi project might be at `~/robotic_arm`. **That folder is not automatically linked to GitHub:** check with `git status` and `git remote -v`.

## D. Working with teammates

- Start by using `git status` and `git pull` when your working tree is clean.
- Make focused edits; commit with a meaningful message.
- Pull requests and branches are helpful for changes that need review.
- If `git pull` or `git push` reports a conflict, **do not force-push**. Review the conflicting files or ask a teammate for help.
- Never commit passwords, access tokens, or secret keys.

## E. Common problems

| Message | What to do |
|---|---|
| `not a git repository` | Go to the correct cloned folder, then run `git status`. |
| `nothing to commit, working tree clean` | There are no new changes to commit. |
| `failed to push some refs` | Someone may have uploaded newer changes. Check status and integrate remote work carefully. |
| Authentication or permission error | Check your GitHub access and authentication; HTTPS Git does not accept your normal account password. |
| `Please tell me who you are` | Configure Git's author identity (below). |

Configure your author identity once per computer:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email linked to your GitHub account or your GitHub-provided private commit email.

## F. Starting a brand-new project

The simplest way is to create a repository on GitHub and **clone it**, then add your files to the cloned folder.

For an existing local project, `git init` is possible, but connecting it to a GitHub repository with an existing history needs extra care. Don't run `git init` or force a push without checking what is already there.

## Quick cheat sheet

```bash
git status
git pull
# Edit and test your files
git add filename.ext
git commit -m "Describe the change"
git push
```

**Remember:** pull = get changes; add = select; commit = save locally; push = upload.
