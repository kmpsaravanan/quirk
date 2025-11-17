# GitHub Authentication Setup Guide

## Method 1: Personal Access Token (Recommended for HTTPS)

### Step 1: Create a Personal Access Token on GitHub

1. Go to GitHub.com and sign in
2. Click your profile picture → **Settings**
3. Scroll down to **Developer settings** (left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name: `quirk-repo-access`
7. Select expiration: Choose your preference (90 days, 1 year, or no expiration)
8. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (if you use GitHub Actions)
9. Click **Generate token**
10. **IMPORTANT**: Copy the token immediately (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Use the Token

When you push, use the token as your password:

```bash
cd /Users/psaravanan/Downloads/JSNewDesign/quirk
git push -u origin feature/tender-management-platform-mvp
```

- **Username**: Your GitHub username
- **Password**: Paste your Personal Access Token (not your GitHub password)

### Step 3: Save Credentials (Optional but Recommended)

**For macOS (using Keychain):**
```bash
git config --global credential.helper osxkeychain
```

**For Linux:**
```bash
git config --global credential.helper store
```

After first push with token, it will be saved and you won't need to enter it again.

---

## Method 2: SSH Key (More Secure, Better for Long-term)

### Step 1: Check if you have SSH keys

```bash
ls -al ~/.ssh
```

Look for files named `id_rsa` and `id_rsa.pub` (or `id_ed25519` and `id_ed25519.pub`)

### Step 2: Generate SSH Key (if you don't have one)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Press Enter to accept default file location
- Enter a passphrase (optional but recommended)
- Or press Enter twice for no passphrase

### Step 3: Add SSH Key to SSH Agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Step 4: Copy Your Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`)

### Step 5: Add SSH Key to GitHub

1. Go to GitHub.com → **Settings** → **SSH and GPG keys**
2. Click **New SSH key**
3. **Title**: `MacBook - Quirk Project`
4. **Key**: Paste your public key
5. Click **Add SSH key**

### Step 6: Test SSH Connection

```bash
ssh -T git@github.com
```

You should see: `Hi username! You've successfully authenticated...`

### Step 7: Change Remote URL to SSH

```bash
cd /Users/psaravanan/Downloads/JSNewDesign/quirk
git remote set-url origin git@github.com:kmpsaravanan/quirk.git
git remote -v  # Verify the change
```

### Step 8: Push Using SSH

```bash
git push -u origin feature/tender-management-platform-mvp
```

No password needed! 🎉

---

## Method 3: GitHub CLI (gh) - Easiest Method

### Step 1: Install GitHub CLI

**macOS:**
```bash
brew install gh
```

**Or download from:** https://cli.github.com/

### Step 2: Authenticate

```bash
gh auth login
```

Follow the prompts:
- Choose **GitHub.com**
- Choose **HTTPS** or **SSH**
- Choose **Login with a web browser** (easiest)
- Follow the browser instructions

### Step 3: Push

```bash
cd /Users/psaravanan/Downloads/JSNewDesign/quirk
git push -u origin feature/tender-management-platform-mvp
```

---

## Quick Setup Script

I can create a script to help you set this up. Which method would you prefer?

1. **Personal Access Token** - Quick setup, works immediately
2. **SSH Key** - More secure, better for long-term use
3. **GitHub CLI** - Easiest, handles everything automatically

---

## Troubleshooting

### "Authentication failed" error

**If using HTTPS:**
- Make sure you're using Personal Access Token, not password
- Check if token has expired
- Verify token has `repo` scope

**If using SSH:**
- Test connection: `ssh -T git@github.com`
- Verify SSH key is added to GitHub
- Check remote URL: `git remote -v`

### "Permission denied" error

- Verify you have write access to the repository
- Check if you're using the correct username
- Ensure token/SSH key has proper permissions

### Clear saved credentials (if needed)

**macOS:**
```bash
git credential-osxkeychain erase
host=github.com
protocol=https
# Press Enter twice
```

**Linux:**
```bash
rm ~/.git-credentials
```

---

## Recommended: Use SSH for Long-term

SSH keys are more secure and convenient once set up. You won't need to enter credentials repeatedly.

---

## Need Help?

Run this to check your current setup:
```bash
git remote -v
git config --list | grep credential
```

