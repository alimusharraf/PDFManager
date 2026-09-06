# PDF Manager

A simple, smart, and local PDF management application built with **Python, Streamlit, SQLite, and PyMuPDF**. PDF Manager is designed for personal use to organize PDF documents with metadata, search and view them easily, resume reading from the last-read page, and track application usage and reading progress.

## ✨ Features

### 📤 Upload PDF
- Upload PDF documents directly through the Streamlit interface.
- Add comma-separated tags for organization.
- Add a description for each document.
- Optionally specify a lecture date.
- Automatically records the upload date.
- Generates a thumbnail from the first page.
- Detects and stores the total number of pages.
- Converts PDF pages into PNG images for the built-in reader.
- Stores document metadata in SQLite.

### 🔎 Search & View
- Search documents by **tags** or **lecture date**.
- Tag search supports partial matching using SQL `LIKE`.
- When both tag and date are provided, documents matching **either** condition are returned.
- Displays PDF thumbnail and document information.
- Open a document in the built-in reader.
- Navigate using **Previous** and **Next** controls.
- Displays the current page number.
- Shows reading progress as a percentage and page count.
- Saves the last-read page when the reader is closed.
- Automatically resumes from the saved page when the document is opened again.

### 📊 Analytics
- Tracks important application actions such as uploads, searches, opening PDFs, page navigation, and closing PDFs.
- Displays application usage frequency as a bar chart.
- Shows reading progress for all stored PDFs in a table.
- Displays:
  - Document name
  - Pages read
  - Total pages
  - Progress percentage
- Provides a **Reset Analytics** option to clear application activity and last-read records.

### 🔐 Admin Access & Data Control
- Provides a password-protected **Delete All Data** operation.
- Admin password is loaded from the `.env` file.
- Requires password verification and confirmation before deletion.
- Deletes stored PDFs, generated thumbnails, and the SQLite database.
- Recreates the required storage directories after a complete reset.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core application logic |
| **Streamlit** | Web-based user interface |
| **SQLite** | Local database for document metadata, reading progress, and analytics |
| **PyMuPDF** | PDF processing, page counting, thumbnails, and PDF-to-image conversion |
| **Pandas** | Preparing analytics and document progress data |
| **python-dotenv** | Loading the admin password from `.env` |

---

## 🏗️ Project Architecture

PDF Manager follows a modular structure that separates the user interface, business logic, file handling, PDF processing, and database operations.

```text
                 ┌─────────────────────┐
                 │   Streamlit UI      │
                 │    app/main.py      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ DocumentServices    │
                 │   core/service.py   │
                 └──────┬───────┬──────┘
                        │       │
          ┌─────────────┘       └─────────────┐
          ▼                                   ▼
┌─────────────────────┐             ┌─────────────────────┐
│ File/PDF Processing │             │ Database Repository │
│                     │             │                     │
│ filemanager.py      │             │ repository.py       │
│ thumbnail.py        │             │ database.py         │
│ pdfreader.py        │             │                     │
└──────────┬──────────┘             └──────────┬──────────┘
           │                                   │
           ▼                                   ▼
   ┌───────────────┐                 ┌──────────────────┐
   │ Local Storage │                 │ SQLite Database  │
   │               │                 │ documents.db     │
   │ PDFs + Images │                 │                  │
   └───────────────┘                 └──────────────────┘
```

### Core Modules

#### `app/main.py`
The main Streamlit application. It provides:
- Upload interface
- Search and view interface
- PDF reader controls
- Analytics interface
- Admin data reset functionality

#### `core/service.py`
Acts as the document service layer and coordinates:
- File management
- Thumbnail generation
- PDF-to-image conversion
- Database repository operations
- Search
- Last-read page tracking

#### `core/filemanager.py`
Handles saving uploaded PDF files to local storage. Uploaded filenames receive a timestamp prefix before being saved.

#### `core/thumbnail.py`
Uses PyMuPDF to:
- Generate a thumbnail from the first page of a PDF.
- Determine the total number of pages.

#### `core/pdfreader.py`
Converts PDF pages into PNG images using PyMuPDF. These generated images are used by the built-in PDF reader.

#### `core/document.py`
Contains the `Document` model used to represent PDF metadata.

#### `core/analytics.py`
Handles application usage analytics:
- Records application events with timestamps.
- Retrieves event frequencies.
- Clears analytics and last-read data.

#### `db/database.py`
Handles SQLite connection and database initialization.

#### `db/repository.py`
Provides database operations for:
- Adding documents
- Searching documents
- Reading and updating last-read pages
- Retrieving all documents

---

## 📁 Project Structure

```text
PDFManager/
│
├── app/
│   └── main.py                 # Streamlit application
│
├── core/
│   ├── analytics.py            # Application analytics
│   ├── document.py             # Document model
│   ├── filemanager.py          # PDF file storage
│   ├── pdfreader.py            # PDF-to-image conversion
│   ├── service.py              # Document service layer
│   └── thumbnail.py            # Thumbnail and page count generation
│
├── data/
│   └── documents.db            # SQLite database (created automatically)
│
├── db/
│   ├── database.py             # Database initialization/connection
│   └── repository.py           # Database operations
│
├── storage/
│   ├── pdfs/                   # Stored PDFs and generated page images
│   └── thumbnail/              # PDF thumbnails
│
├── .env                        # Local admin password configuration
├── .gitignore
├── .python-version
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

> **Note:** `data/documents.db` is created automatically when the application initializes the database. The PDF and thumbnail storage directories are created/used by the application and do not need to be included as pre-existing data directories in a fresh project checkout.

---

## 🗄️ Database Design

PDF Manager uses a local SQLite database stored at:

```text
data/documents.db
```

### `Documents`

Stores the metadata of uploaded PDFs.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Original PDF filename |
| `path` | TEXT | Stored PDF path |
| `thumbnail_path` | TEXT | Generated thumbnail path |
| `tags` | TEXT | Comma-separated tags |
| `description` | TEXT | PDF description |
| `upload_date` | TEXT | Date the PDF was uploaded |
| `lecture_date` | TEXT | Optional lecture date |
| `total_page` | INTEGER | Total number of PDF pages |

### `last_read`

Stores the last page reached for each document.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Document identifier |
| `last_page` | INTEGER | Last recorded page index |

### `app_visit`

Stores application activity events.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `event_type` | TEXT | Type of application event |
| `timestamp` | TEXT | Time the event occurred |

---

## 🔄 Application Workflow

### Upload Workflow

```text
Upload PDF
    │
    ▼
Enter Tags / Description / Lecture Date
    │
    ▼
Save PDF to Local Storage
    │
    ├──► Generate Thumbnail
    │
    ├──► Calculate Total Pages
    │
    ├──► Store Metadata in SQLite
    │
    └──► Convert PDF Pages to PNG Images
```

### Reading Workflow

```text
Search PDF
    │
    ▼
Select Document
    │
    ▼
Open PDF
    │
    ▼
Check Last-Read Page
    │
    ▼
Resume Reading
    │
    ├── Previous
    ├── Next
    └── Progress
    │
    ▼
Close Reader
    │
    ▼
Save Current Page
```

### Analytics Workflow

```text
User Action
    │
    ▼
Record Event + Timestamp
    │
    ▼
Store in app_visit
    │
    ▼
Aggregate Event Counts
    │
    ▼
Display Usage Chart
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/alimusharraf/PDFManager.git
cd PDFManager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the environment

Create a `.env` file in the project root:

```env
ADMIN_PASSWORD=your_secure_password
```

The `ADMIN_PASSWORD` variable is used for the password-protected **Delete All Data** functionality.

> Never commit your real `.env` file or password to a public repository.

### 4. Run the application

```bash
streamlit run app/main.py
```

The SQLite database is initialized automatically when the application starts.

---

## 🖥️ Using the Application

### Uploading a PDF

1. Open the **Upload** tab.
2. Select a PDF.
3. Enter tags separated by commas.
4. Add a description.
5. Optionally select a lecture date.
6. Click **Upload**.

The application processes the PDF, generates its thumbnail and page images, and stores its metadata.

### Searching for a PDF

1. Open **Search and View**.
2. Enter a tag, a date, or both.
3. Click **Search**.
4. Select **Open** on the desired document.

Tag searches support partial matches. When both filters are provided, the application returns documents satisfying either the tag or date condition.

### Reading a PDF

Use:

- **Previous** — move to the previous page.
- **Next** — move to the next page.
- **Close** — exit the reader and save the current reading position.

When reopening the same document, PDF Manager restores the saved reading position.

### Viewing Analytics

The **Analysis** tab provides:
- Application usage frequency.
- Reading progress for stored documents.
- A progress percentage for each PDF.

**Reset Analytics** clears application activity and saved reading positions without deleting the stored PDF documents.

---

## 🔐 Data Reset

The application provides two different reset mechanisms:

### Reset Analytics

Clears:
- `app_visit` records
- `last_read` records

PDF files and document metadata remain available.

### Delete All Data

The **Delete All Data** operation is protected by the administrator password.

After successful password verification and confirmation, it removes:
- SQLite database
- Stored PDFs
- Generated thumbnails

The required storage directories are then recreated.

**This operation is destructive and cannot be undone.**

---

## 📌 Current Scope

PDF Manager is intended primarily for **local personal use**. It uses local filesystem storage and a local SQLite database rather than a remote database or cloud storage service.

It provides document organization and reading-progress tracking without requiring a separate backend server.

---

## 🔮 Future Improvements

Possible future enhancements include:

- Individual PDF deletion
- Editing PDF metadata after upload
- More advanced sorting and filtering
- Full-text PDF content search
- Bookmarks and reading notes
- Improved PDF navigation
- More detailed analytics
- User authentication and multiple user support
- Cloud storage integration
- Improved document categorization

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

## 👨‍💻 Author

**Musharraf Ali**

GitHub: [alimusharraf](https://github.com/alimusharraf)

---

## 🔗 Repository

**PDF Manager:**  
https://github.com/alimusharraf/PDFManager

---

## ⭐ Acknowledgment

Built as a personal project to make local PDF organization, reading, and progress tracking simpler and more convenient.
