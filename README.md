# 📬 Gmail Attachment Downloader

This Python script uses the **Gmail API** to authenticate a user's Gmail account, search for all emails with attachments, download those attachments, and automatically unzip `.zip` files. Attachments are organized into folders based on the sender's email domain.

---

## 🚀 Features

- Authenticate Gmail account using OAuth 2.0
- Search emails with attachments
- Download attachments from all matching emails
- Automatically unzip `.zip` files
- Organize files by sender domain

---

## 📁 Folder Structure

Attachments are saved in a folder structure like:

```
attachments/
├── example_com/
│   ├── file1.pdf
│   └── archive.zip
```

---

## 🛠️ Requirements

- Python 3.7+
- Gmail account with API access enabled

### Python Packages

Install required packages using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 🔐 Setup

1. **Enable Gmail API**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project
   - Enable the **Gmail API**
   - Create **OAuth 2.0 Client ID credentials**
   - Download the file as `credentials.json`

2. **Save `credentials.json`** in the same directory as the script.

---

## 🧪 How to Run

```bash
python your_script_name.py
```

- A browser window will open for Gmail account authentication.
- After authentication, all attachments from emails will be downloaded.

---

## 📂 Output

- All attachments are saved in a directory named `attachments/`.
- Files are grouped by sender’s email domain (e.g., `example_com`).
- `.zip` attachments are automatically extracted and the original zip is deleted.

---

## ⚠️ Notes

- This script only has **read-only** access to Gmail (`gmail.readonly` scope).
- Only messages with attachments are processed (`q="has:attachment"`).
- Ensure `credentials.json` is secure and not shared.

---

## 📄 License

This project is open-source and free to use under the [MIT License](https://opensource.org/licenses/MIT).
