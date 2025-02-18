# 🦁 Animal Lens

**Animal Lens** is an AI-powered web application that allows users to upload images and analyze animals using AWS Rekognition. The app integrates AWS services for image storage (S3) and image analysis (Rekognition) and provides detailed information about recognized animals. Images with unrecognized animals are flagged for further review.

## 🚀 Features

- 📷 **Image Upload** - Users can easily upload images via an intuitive UI.
- 🧠 **Animal Detection** - Utilizes AWS Rekognition to analyze uploaded images and identify animals.
- 📖 **Detailed Animal Information** - Displays species, habitat, diet, and description for recognized animals.
- ⚠ **Unknown Animal Handling** - Saves unrecognized animal data for later review.
- 📱 **Responsive Design** - Fully responsive UI built with Next.js and Tailwind CSS.

---

## 📸 Preview

<img src="https://github.com/user-attachments/assets/df5eef92-baba-4e6c-8baa-8d3bf0526fc3" width="600">
<img src="https://github.com/user-attachments/assets/2d11638d-3b8f-49da-a12f-9bbe499efe5c" width="500">
<img src="https://github.com/user-attachments/assets/d9ef2b3d-f767-424e-a805-f9f719d145b3" width="500">

---

## 🛠 Tech Stack

### **Frontend**
- Next.js (React & TypeScript)
- Tailwind CSS

### **Backend**
- FastAPI (Python)
- PostgreSQL (Database)
- AWS S3 (Image Storage)
- AWS Rekognition (Image Analysis)

### **Containerization & Deployment**
- Docker & Docker Compose

---

## 📂 Project Structure

```plaintext
├── backend
│   ├── app
│   │   ├── main.py         # FastAPI main app with API endpoints
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database connection & transaction management
│   │   ├── models.py       # SQLAlchemy models (Animal & AnalysisResult)
│   │   ├── logger.py       # Logging configuration
│   │   ├── services        # AWS S3 and Rekognition integration
│   └── db
│       ├── init.sql        # Initial database setup
│       ├── init_tables.sql # Table creation script
│       ├── migrate.py      # Schema migration script
│       ├── create_db.sql   # Database creation script
│       └── check_db.py     # Database verification script
├── frontend
│   ├── app                # Next.js application pages
│   ├── components         # Reusable UI components
│   ├── lib                # API communication and utility functions
│   ├── public             # Static assets
│   └── next.config.ts     # Next.js configuration
├── docker-compose.dev.yml  # Docker Compose config for development
├── docker-compose.prod.yml # Docker Compose config for production
├── Dockerfile              # Dockerfile for backend & frontend
├── run-dev.sh              # Shell script for development mode
├── run-prod.sh             # Shell script for production mode
└── README.md               # This README file
```

---

## 🔧 Installation & Setup

### **Prerequisites**
- Docker & Docker Compose
- Node.js & pnpm (for frontend development)
- Python 3.12 (for backend development)

### **Environment Variables**

Create the following environment files with your configuration:

#### **Backend** (`backend/.env.development` or `backend/.env.production`)

```ini
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=your_s3_bucket_name

# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=postgres # Use Docker service name for local development
DB_PORT=5432
DB_NAME=animallens
```

#### **Frontend** (`frontend/.env.development`)

```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Running the Application

### **Development Mode**

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Start the Development Environment:**
   ```bash
   ./run-dev.sh
   ```
   This command runs the Docker Compose configuration (`docker-compose.dev.yml`), setting up PostgreSQL, FastAPI backend, and Next.js frontend.

### **Production Mode**

1. **Ensure Production Environment Variables Are Set**
2. **Build and Run the Production Environment:**
   ```bash
   ./run-prod.sh
   ```
   This uses `docker-compose.prod.yml` to build and start the application in detached mode.

---

## 🎯 Usage

- **Frontend:**
  Open [http://localhost:3000](http://localhost:3000) to upload and analyze animal images.
- **Backend:**
  API runs at [http://localhost:8000](http://localhost:8000) for further integration or testing.

---

## 📊 Database Migration

To modify or initialize the database schema, use the scripts in `backend/db`:

- `init.sql` / `init_tables.sql` - Initial setup and table creation.
- `migrate.py` - Run this for schema modifications.

---

## 📜 Logging

Backend logs are configured in `backend/app/logger.py` and output to the console for debugging and monitoring in development and production.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with your changes.

---

## 🙌 Acknowledgments

- Built using **AWS Rekognition** for advanced image analysis.
- Thanks to the communities behind **FastAPI** and **Next.js** for their powerful frameworks.

---

🚀 **Happy Coding!** 🎉

