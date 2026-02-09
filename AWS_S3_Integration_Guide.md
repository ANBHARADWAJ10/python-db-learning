
# AWS S3 File Upload Integration Guide
## Complete Implementation for Local Development & Production (EC2/Cloud)

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [AWS Setup](#aws-setup)
4. [Local Development Setup](#local-development-setup)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Implementation](#frontend-implementation)
7. [Production Deployment (EC2)](#production-deployment-ec2)
8. [Testing & Troubleshooting](#testing--troubleshooting)
9. [Security Best Practices](#security-best-practices)

---

## Overview

This guide explains how to integrate AWS S3 for file uploads in any Node.js/Express application. Files will be uploaded directly to S3 instead of local storage, making your application scalable and cloud-ready.

**Benefits:**
- No local disk space consumed
- Files accessible from anywhere
- Scalable and reliable storage
- Works across multiple server instances
- Automatic file URL generation

---

## Prerequisites

**Required Knowledge:**
- Basic Node.js and Express
- HTML/JavaScript for frontend
- Basic AWS account setup

**Required Tools:**
- Node.js (v14+)
- npm or yarn
- AWS Account
- Code editor (VS Code, etc.)

---

## AWS Setup

### Step 1: Create AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Complete registration (requires credit card)
4. Verify email and phone number

### Step 2: Create S3 Bucket

1. **Login to AWS Console**
   - Go to AWS Management Console
   - Search for "S3" in services

2. **Create Bucket**
   - Click "Create bucket"
   - **Bucket name:** `your-project-name-files` (must be globally unique)
   - **Region:** Choose closest to your users (e.g., `us-east-1`, `ap-south-1`)
   - **Block Public Access:** Uncheck "Block all public access"
   - Check the acknowledgment box
   - Click "Create bucket"

3. **Configure Bucket Policy**
   - Click on your bucket name
   - Go to "Permissions" tab
   - Scroll to "Bucket policy"
   - Click "Edit" and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

   - Replace `your-bucket-name` with your actual bucket name
   - Click "Save changes"

4. **Enable CORS (if needed for direct browser uploads)**
   - In "Permissions" tab, scroll to "CORS"
   - Click "Edit" and paste:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": ["ETag"]
  }
]
```

### Step 3: Create IAM User

1. **Go to IAM Service**
   - Search for "IAM" in AWS Console
   - Click "Users" in left sidebar
   - Click "Create user"

2. **User Details**
   - **Username:** `s3-upload-user`
   - Check "Provide user access to AWS Management Console" (optional)
   - Click "Next"

3. **Set Permissions**
   - Select "Attach policies directly"
   - Search for and select `AmazonS3FullAccess` (for development)
   - Click "Next"
   - Click "Create user"

4. **Create Access Keys**
   - Click on the newly created user
   - Go to "Security credentials" tab
   - Scroll to "Access keys"
   - Click "Create access key"
   - Select "Application running outside AWS"
   - Click "Next"
   - Add description: "S3 file upload"
   - Click "Create access key"
   - **IMPORTANT:** Copy both:
     - Access Key ID
     - Secret Access Key
   - Save them securely (you won't see the secret again!)

### Step 4: Note Down These Values

Create a note with:
```
AWS_REGION=us-east-1 (or your chosen region)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_BUCKET_NAME=your-project-name-files
```

---

## Local Development Setup

### Step 1: Install Required Packages

In your project directory:

```bash
npm install @aws-sdk/client-s3 multer-s3 multer dotenv
```

**Package Purposes:**
- `@aws-sdk/client-s3` - AWS SDK for S3 operations
- `multer-s3` - Multer storage engine for S3
- `multer` - File upload middleware
- `dotenv` - Environment variable management

### Step 2: Create/Update .env File

Create `.env` in your project root:

```env
# Server Configuration
PORT=3000

# AWS S3 Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
S3_BUCKET_NAME=your-bucket-name

# Database (if any)
DATABASE_URL=your-database-url
```

### Step 3: Add .env to .gitignore

Create/update `.gitignore`:

```
node_modules/
.env
.DS_Store
*.log
```

**CRITICAL:** Never commit `.env` to version control!

---

## Backend Implementation

### Step 1: Create S3 Upload Configuration File

Create `config/s3Upload.js`:

```javascript
const { S3Client } = require('@aws-sdk/client-s3');
const multer = require('multer');
const multerS3 = require('multer-s3');
const path = require('path');

// Initialize S3 Client
const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
  }
});

// Configure Multer-S3
const uploadToS3 = (folderName = 'uploads') => {
  return multer({
    storage: multerS3({
      s3: s3Client,
      bucket: process.env.S3_BUCKET_NAME,
      contentType: multerS3.AUTO_CONTENT_TYPE,
      metadata: (req, file, cb) => {
        cb(null, { fieldName: file.fieldname });
      },
      key: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname);
        const baseName = path.basename(file.originalname, ext).replace(/\s+/g, '-');
        cb(null, `${folderName}/${baseName}-${uniqueSuffix}${ext}`);
      }
    }),
    limits: {
      fileSize: 5 * 1024 * 1024 // 5MB limit (adjust as needed)
    },
    fileFilter: (req, file, cb) => {
      // Accept images only (customize based on your needs)
      const allowedMimeTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

      if (allowedMimeTypes.includes(file.mimetype)) {
        cb(null, true);
      } else {
        cb(new Error('Only image files are allowed!'), false);
      }
    }
  });
};

module.exports = { uploadToS3, s3Client };
```

### Step 2: Update Your Server.js

Add dotenv configuration at the top of `server.js`:

```javascript
require('dotenv').config();
const express = require('express');
const app = express();

// Your other configurations...

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Step 3: Create Upload Routes

Create `routes/uploadRoutes.js`:

```javascript
const express = require('express');
const router = express.Router();
const { uploadToS3 } = require('../config/s3Upload');

// Single file upload
router.post('/upload-single', uploadToS3('logos').single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // S3 URL is in req.file.location
    res.json({
      message: 'File uploaded successfully',
      fileUrl: req.file.location,
      fileName: req.file.key,
      fileSize: req.file.size
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Multiple files upload
router.post('/upload-multiple', uploadToS3('documents').array('files', 5), (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: 'No files uploaded' });
    }

    const fileData = req.files.map(file => ({
      fileUrl: file.location,
      fileName: file.key,
      fileSize: file.size
    }));

    res.json({
      message: 'Files uploaded successfully',
      files: fileData
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

### Step 4: Register Routes in Server

In `server.js`:

```javascript
const uploadRoutes = require('./routes/uploadRoutes');

// Register upload routes
app.use('/api', uploadRoutes);
```

### Step 5: Create a Sample Data Route with File Upload

Example: User profile with avatar upload

`routes/userRoutes.js`:

```javascript
const express = require('express');
const router = express.Router();
const { uploadToS3 } = require('../config/s3Upload');
const User = require('../models/User'); // Your user model

// Create/Update user with avatar
router.post('/user/profile', uploadToS3('avatars').single('avatar'), async (req, res) => {
  try {
    const { name, email } = req.body;

    // Build user data
    const userData = { name, email };

    // Add S3 URL if file was uploaded
    if (req.file) {
      userData.avatarUrl = req.file.location; // S3 URL
    }

    // Save to database
    const user = await User.create(userData);

    res.json({
      message: 'User created successfully',
      user: user
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user profile
router.get('/user/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

---

## Frontend Implementation

### Step 1: HTML Form for File Upload

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>File Upload</title>
</head>
<body>
  <h1>Upload File to S3</h1>

  <!-- Single File Upload -->
  <form id="uploadForm" enctype="multipart/form-data">
    <input type="file" id="fileInput" name="file" accept="image/*" required>
    <button type="submit">Upload</button>
  </form>

  <div id="result"></div>
  <img id="preview" style="max-width: 300px; display: none;">

  <script src="upload.js"></script>
</body>
</html>
```

### Step 2: JavaScript for Upload

Create `public/upload.js`:

```javascript
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('fileInput');
  const resultDiv = document.getElementById('result');
  const preview = document.getElementById('preview');

  if (!fileInput.files[0]) {
    alert('Please select a file');
    return;
  }

  // Create FormData
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  // Show loading
  resultDiv.innerHTML = 'Uploading...';

  try {
    // Upload to server
    const response = await fetch('/api/upload-single', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      resultDiv.innerHTML = `
        <p style="color: green;">Upload successful!</p>
        <p>File URL: <a href="${data.fileUrl}" target="_blank">${data.fileUrl}</a></p>
      `;

      // Show preview
      preview.src = data.fileUrl;
      preview.style.display = 'block';

      // Clear input
      fileInput.value = '';
    } else {
      resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
    }
  } catch (error) {
    resultDiv.innerHTML = `<p style="color: red;">Upload failed: ${error.message}</p>`;
  }
});
```

### Step 3: Fetch and Display S3 Images

```javascript
// Fetch user profile with S3 avatar
async function loadUserProfile(userId) {
  try {
    const response = await fetch(`/api/user/${userId}`);
    const { user } = await response.json();

    // Display user data
    document.getElementById('userName').textContent = user.name;
    document.getElementById('userEmail').textContent = user.email;

    // Display S3 avatar (if exists)
    if (user.avatarUrl) {
      document.getElementById('userAvatar').src = user.avatarUrl;
    } else {
      document.getElementById('userAvatar').src = 'default-avatar.png';
    }
  } catch (error) {
    console.error('Error loading profile:', error);
  }
}

// Load on page load
document.addEventListener('DOMContentLoaded', () => {
  loadUserProfile('user-id-here');
});
```

### Step 4: Update Existing Images (Replace Local URLs)

If you have existing code using local URLs:

```javascript
// OLD CODE (local storage):
document.getElementById('logo').src = `/uploads/${filename}`;

// NEW CODE (S3):
document.getElementById('logo').src = fileUrlFromDatabase; // Complete S3 URL
```

**Key Difference:** S3 URLs are complete (e.g., `https://bucket.s3.amazonaws.com/file.jpg`), 
so you don't need to prepend any base URL.

---

## Production Deployment (EC2)

### Method 1: Using Environment Variables (Quick Setup)

#### Step 1: Connect to EC2

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

#### Step 2: Navigate to Project

```bash
cd /path/to/your/project
```

#### Step 3: Create .env File

```bash
nano .env
```

Add your AWS credentials:

```env
PORT=3000
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
S3_BUCKET_NAME=your-bucket-name
```

Save and exit (Ctrl+X, Y, Enter)

#### Step 4: Install Dependencies

```bash
npm install
```

#### Step 5: Restart Application

```bash
# If using PM2
pm2 restart all

# If using systemd
sudo systemctl restart your-app

# If running directly
pkill node
node server.js &
```

---

### Method 2: Using IAM Roles (Recommended for Production)

This is more secure - no credentials stored in files!

#### Step 1: Create IAM Role for EC2

1. Go to IAM in AWS Console
2. Click "Roles" → "Create role"
3. Select "AWS service" → "EC2"
4. Click "Next"

#### Step 2: Attach S3 Policy

1. Search for "AmazonS3FullAccess"
2. Select it and click "Next"
3. Name: `EC2-S3-Access-Role`
4. Click "Create role"

#### Step 3: Attach Role to EC2 Instance

1. Go to EC2 Console
2. Select your instance
3. Click "Actions" → "Security" → "Modify IAM role"
4. Select `EC2-S3-Access-Role`
5. Click "Update IAM role"

#### Step 4: Update Backend Code

Remove AWS credentials from `.env`:

```env
# Remove these lines:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...

# Keep these:
PORT=3000
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

#### Step 5: Update S3 Config

In `config/s3Upload.js`, modify S3 client initialization:

```javascript
const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  // No credentials needed - will use IAM role automatically
});
```

#### Step 6: Restart Application

```bash
pm2 restart all
```

---

### Frontend Updates for Production

#### Remove Hardcoded URLs

**Before (Development):**
```javascript
const response = await fetch('http://localhost:3000/api/upload-single', {
  method: 'POST',
  body: formData
});
```

**After (Production-ready):**
```javascript
const response = await fetch('/api/upload-single', {
  method: 'POST',
  body: formData
});
```

Using relative URLs makes your code work in both development and production.

---

## Testing & Troubleshooting

### Test Checklist

- [ ] Files upload successfully
- [ ] S3 bucket receives files
- [ ] File URLs are returned correctly
- [ ] Images display from S3 URLs
- [ ] File size limits work
- [ ] File type validation works
- [ ] Error handling displays properly

### Common Issues & Solutions

#### 1. "Access Denied" Error

**Cause:** IAM user lacks S3 permissions

**Solution:**
- Verify IAM user has `AmazonS3FullAccess` policy
- Check bucket policy allows uploads

#### 2. "Cannot read property 'location' of undefined"

**Cause:** File upload failed or multer not configured

**Solution:**
```javascript
if (!req.file) {
  return res.status(400).json({ error: 'No file uploaded' });
}
```

#### 3. Images Don't Display

**Cause:** S3 bucket not public or CORS issue

**Solution:**
- Check bucket policy allows public reads
- Verify CORS configuration
- Open S3 URL directly in browser to test

#### 4. "Region is Required"

**Cause:** AWS_REGION not set

**Solution:**
```javascript
// Verify .env has:
AWS_REGION=us-east-1
```

#### 5. Files Upload but URLs Don't Work

**Cause:** Bucket name mismatch

**Solution:**
- Verify `S3_BUCKET_NAME` in `.env` matches actual bucket name
- Check `req.file.location` returns correct URL

### Debug Mode

Add logging to see what's happening:

```javascript
router.post('/upload', uploadToS3('test').single('file'), (req, res) => {
  console.log('File received:', req.file); // Log file details

  if (!req.file) {
    console.error('No file in request');
    return res.status(400).json({ error: 'No file uploaded' });
  }

  console.log('S3 URL:', req.file.location);
  res.json({ fileUrl: req.file.location });
});
```

---

## Security Best Practices

### 1. Never Commit Credentials

```bash
# Always in .gitignore
.env
config/secrets.js
*.pem
```

### 2. Use IAM Roles in Production

- Eliminates credential storage
- Automatic key rotation
- Better audit trails

### 3. Restrict S3 Bucket Access

Only allow what's needed:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket/public/*"
    }
  ]
}
```

### 4. Validate File Uploads

```javascript
fileFilter: (req, file, cb) => {
  // Check file type
  const allowedTypes = ['image/jpeg', 'image/png'];
  if (!allowedTypes.includes(file.mimetype)) {
    return cb(new Error('Invalid file type'), false);
  }

  // File is valid
  cb(null, true);
}
```

### 5. Set File Size Limits

```javascript
limits: {
  fileSize: 5 * 1024 * 1024, // 5MB
  files: 10 // Max 10 files at once
}
```

### 6. Sanitize File Names

```javascript
key: (req, file, cb) => {
  // Remove special characters
  const safeName = file.originalname.replace(/[^a-zA-Z0-9.-]/g, '-');
  cb(null, `uploads/${Date.now()}-${safeName}`);
}
```

### 7. Use Environment-Specific Buckets

```env
# Development
S3_BUCKET_NAME=myapp-dev-files

# Production
S3_BUCKET_NAME=myapp-prod-files
```

### 8. Enable S3 Versioning

In S3 Console:
- Go to bucket → Properties
- Enable "Bucket Versioning"
- Prevents accidental file deletion

### 9. Set up Lifecycle Rules

Automatically delete old files:
- S3 Console → Management → Lifecycle rules
- Create rule to delete files after X days

### 10. Monitor Costs

- Set up AWS Budget alerts
- Monitor S3 usage in AWS Cost Explorer
- Use S3 Storage Class analysis

---

## Advanced Features

### 1. Generate Signed URLs (Private Files)

For files that shouldn't be public:

```javascript
const { GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

async function generateSignedUrl(fileKey) {
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET_NAME,
    Key: fileKey
  });

  // URL valid for 1 hour
  const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 });
  return url;
}
```

### 2. Delete Files from S3

```javascript
const { DeleteObjectCommand } = require('@aws-sdk/client-s3');

router.delete('/file/:key', async (req, res) => {
  try {
    const command = new DeleteObjectCommand({
      Bucket: process.env.S3_BUCKET_NAME,
      Key: req.params.key
    });

    await s3Client.send(command);
    res.json({ message: 'File deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### 3. Image Processing Before Upload

Using Sharp library:

```javascript
const sharp = require('sharp');

router.post('/upload-image', uploadToS3('images').single('image'), async (req, res) => {
  try {
    // Resize image before uploading
    const buffer = await sharp(req.file.buffer)
      .resize(800, 600)
      .jpeg({ quality: 80 })
      .toBuffer();

    // Continue with S3 upload...
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## Quick Reference

### Environment Variables

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=your-bucket
```

### Basic Upload Route

```javascript
const { uploadToS3 } = require('./config/s3Upload');

router.post('/upload', uploadToS3('folder').single('file'), (req, res) => {
  res.json({ fileUrl: req.file.location });
});
```

### Frontend Upload

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/api/upload', {
  method: 'POST',
  body: formData
});

const { fileUrl } = await response.json();
```

### Display Image

```javascript
document.getElementById('image').src = fileUrl; // S3 URL
```

---

## Conclusion

You now have a complete S3 integration that works in both development and production! 

**Key Takeaways:**
- Use environment variables for credentials
- IAM roles are more secure than access keys in production
- Always validate file uploads
- S3 URLs are complete - no need to prepend base URLs
- Test thoroughly before deploying to production

**Need Help?**
- AWS Documentation: docs.aws.amazon.com
- Multer-S3: github.com/badunk/multer-s3
- AWS SDK v3: docs.aws.amazon.com/AWSJavaScriptSDK/v3

---

*Document Version: 1.0*  
*Last Updated: December 2025*
