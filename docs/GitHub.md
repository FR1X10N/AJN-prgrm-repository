# GitHub Collaboration Guide

This document explains how to use Git and GitHub to collaborate on our project.

It covers cloning the repository, creating branches, committing changes, pushing code, and using GitHub directly from the website or VS Code.

## 1. Getting Started

### Clone the Repository

To download the project to your computer:

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

Replace `USERNAME` and `REPOSITORY` with the actual GitHub repository information.

### Configure Git

If you haven't configured Git yet:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 2. Working with Branches

To avoid conflicts, each team member should work on their own branch.

### Create a New Branch

First, update your local main branch:

```bash
git switch main
git pull origin main
```

Create and switch to a new branch:

```bash
git switch -c feature/your-feature-name
```

Examples:
- `feature/api-connection`
- `feature/movie-search`
- `feature/error-handling`
- `docs/update-readme`
- `fix/input-validation`

### Switch Between Branches

```bash
git switch branch-name
```

### View All Branches

```bash
git branch -a
```

## 3. Commit and Push Using the Terminal

### Step 1: Check Your Changes

```bash
git status
```

This shows modified, added, and deleted files.

### Step 2: Stage Your Changes

Add all modified files:

```bash
git add .
```

Or add a specific file:

```bash
git add main.py
```

### Step 3: Commit Your Changes

```bash
git commit -m "feat: add movie search functionality"
```

### Step 4: Push to GitHub

For a new branch:

```bash
git push -u origin feature/your-feature-name
```

For an existing branch with upstream configured:

```bash
git push
```

## 4. Commit and Push Using VS Code

You can manage Git without using the terminal.

1. Open the project in VS Code.
2. Click the **Source Control** icon in the sidebar.
3. Review your modified files.
4. Click the `+` icon to stage your changes.
5. Enter a commit message.
6. Click **Commit**.
7. Click **Sync Changes** or **Push** to upload your changes to GitHub.

Make sure you are working on the correct branch before committing.

## 5. Editing Files Directly on GitHub

You can make changes directly from the GitHub website.

### Edit an Existing File

1. Open the repository on GitHub.
2. Navigate to the file you want to modify.
3. Click the pencil icon (**Edit this file**).
4. Make your changes.
5. Click **Commit changes**.
6. Enter a descriptive commit message.
7. Prefer **Create a new branch for this commit and start a pull request**.
8. Submit your changes.

### Upload New Files

1. Open the repository.
2. Click **Add file** → **Upload files**.
3. Select or drag your files.
4. Enter a commit message.
5. Commit to a new branch when possible.

### Create a New File

1. Click **Add file** → **Create new file**.
2. Enter the filename, such as `utils.py`.
3. Add your content.
4. Click **Commit changes**.

Note: GitHub website edits create commits directly on GitHub. You do not need to run `git push` afterward.

## 6. Creating a Pull Request

Pull requests allow teammates to review changes before merging them into `main`.

### From the GitHub Website

1. Push your branch to GitHub.
2. Open the repository.
3. Click **Compare & pull request**, or open the **Pull requests** tab.
4. Click **New pull request**.
5. Set the base branch to `main`.
6. Select your feature branch.
7. Add a title and description.
8. Click **Create pull request**.
9. Ask a teammate to review your changes.
10. Once approved, click **Merge pull request** if you have permission.

### After Merging

Update your local repository:

```bash
git switch main
git pull origin main
```

## 7. Keeping Your Branch Updated

Before starting new work, update your local branch with the latest changes from `main`.

```bash
git switch main
git pull origin main
git switch feature/your-feature-name
git merge main
```

If Git reports conflicts, resolve them before completing the merge.

## 8. Handling Merge Conflicts

Conflicts can occur when two people modify the same part of a file.

Git may show:

```text
<<<<<<< HEAD
Your changes
=======
Other changes
>>>>>>> main
```

To resolve a conflict:

1. Open the affected file.
2. Decide which changes to keep or combine.
3. Remove the conflict markers.
4. Save the file.
5. Stage the resolved file:

```bash
git add filename.py
```

6. Complete the merge:

```bash
git commit
```

If you want to cancel an unfinished merge:

```bash
git merge --abort
```

Never delete someone else's work without discussing it with the team.

## 9. Commit Message Guidelines

Use clear and descriptive commit messages.

| Prefix | Purpose | Example |
|---|---|---|
| `feat:` | New functionality | `feat: add movie search` |
| `fix:` | Bug fix | `fix: handle invalid input` |
| `docs:` | Documentation | `docs: update README` |
| `test:` | Tests | `test: add API parsing tests` |
| `refactor:` | Code improvements | `refactor: simplify JSON parsing` |
| `chore:` | Maintenance | `chore: update gitignore` |

Avoid messages such as `update`, `stuff`, or `changes`.

## 10. Useful Git Commands

| Command | Description |
|---|---|
| `git status` | Show current changes |
| `git branch` | Show local branches |
| `git switch main` | Switch to main |
| `git pull` | Download and integrate remote changes |
| `git add .` | Stage changes |
| `git commit -m "message"` | Create a commit |
| `git push` | Upload commits |
| `git log --oneline` | Show commit history |
| `git diff` | Show unstaged changes |
| `git stash` | Temporarily save uncommitted changes |
| `git stash pop` | Restore stashed changes |
| `git fetch` | Download remote information without merging |

## 11. Team Collaboration Rules

To keep the repository organized:

1. **Do not push directly to `main`** unless the team explicitly agrees.
2. Create a separate branch for each feature or bug fix.
3. Write meaningful commit messages.
4. Pull the latest changes before starting work.
5. Create pull requests for code reviews.
6. Review teammates' code before merging.
7. Never commit API keys, passwords, or sensitive information.
8. Use `.gitignore` to exclude temporary files, local environments, and secrets.
9. Make small, focused commits.
10. Communicate with teammates before making major changes.

## 12. Recommended Daily Workflow

```bash
# Update main
git switch main
git pull origin main

# Create a feature branch
git switch -c feature/my-feature

# Make your changes...

# Check and stage changes
git status
git add .

# Commit
git commit -m "feat: implement my feature"

# Push
git push -u origin feature/my-feature
```

Finally, open GitHub and create a pull request to merge your work into `main`.

---

**Remember:** Always check your current branch, review your changes, and communicate with