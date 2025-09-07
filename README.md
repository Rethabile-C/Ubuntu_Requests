# Ubuntu_Requests – Advanced Image Fetcher

A Python tool for safely downloading images from the web, built with respect for the wider community and mindful precautions.

This project demonstrates the **Ubuntu principles** in software development:

- **Community**: Connects to the wider web to fetch resources.  
- **Respect**: Handles errors gracefully and avoids harmful downloads.  
- **Sharing**: Collects all downloaded images in a single folder.  
- **Practicality**: Provides a real-world utility for downloading and organizing images.  

---

## ✨ Features

- Accept **multiple URLs** at once (one per line).
- Create a dedicated folder `Fetched_Images` if it doesn’t exist.
- Download images and save them with unique, safe filenames.
- **Precautions against unknown sources**:
  - Check `Content-Type` header (must be `image/*`).
  - Skip files that are not images.
  - Skip files that are too large (> 5 MB by default).
- **Prevent duplicates** by checking file hashes (MD5).
- **Check important HTTP headers** before downloading:
  - `Content-Type`
  - `Content-Length`
  - `Content-Disposition` (if present, can suggest filename).
- Handle connection errors gracefully without crashing.

---

## 🛠 Requirements

- Python 3.8+
- `requests` library

Install dependencies with:

