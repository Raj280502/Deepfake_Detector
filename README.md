# 🛡️ DeepFake Detector

An AI-powered web application for detecting deepfake videos and images using deep learning.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

- **Video Analysis** - Frame-by-frame deepfake detection in videos
- **Image Detection** - Analyze static images for AI manipulation
- **Modern UI** - Beautiful glassmorphism design with animations
- **Detection History** - Track all past analyses with statistics
- **Confidence Scores** - Detailed probability scores for each detection
- **Fast Processing** - Optimized inference pipeline

## 🖼️ Screenshots

| Home Page | Detection Page | History |
|-----------|----------------|---------|
| Modern landing page with features | Upload & analyze media | View past detections |

## 🧠 Technology

### Model Architecture
- **Xception Neural Network** - Deep CNN architecture optimized for deepfake detection
- **Transfer Learning** - Pre-trained on extensive deepfake datasets
- **Frame Extraction** - Analyzes 1 frame per second for video content

### Tech Stack
| Component | Technology |
|-----------|------------|
| Backend | Django 5.2 |
| ML Framework | PyTorch + timm |
| Computer Vision | OpenCV, Pillow |
| Frontend | Bootstrap 5, CSS3 |
| Database | SQLite |

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Raj280502/Deepfake_Detector.git
   cd Deepfake_Detector
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

## 📁 Project Structure

```
DeepFakeDetector/
├── App/                    # Main Django application
│   ├── views.py           # View controllers
│   ├── models.py          # Database models
│   ├── inference.py       # ML inference logic
│   └── urls.py            # URL routing
├── DeepFakeDetector/      # Django project settings
│   ├── settings.py        # Configuration
│   └── urls.py            # Main URL config
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── detect.html        # Detection page
│   ├── history.html       # History page
│   └── about.html         # About page
├── static/                # Static files
├── media/                 # User uploads
├── best_xception_model.pth # Trained model weights
├── requirements.txt       # Python dependencies
└── manage.py             # Django CLI
```

## 📦 Dependencies

```
Django>=5.2
torch>=2.0
torchvision>=0.15
timm>=0.9
opencv-python>=4.8
Pillow>=10.0
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for production:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
```

### GPU Support
The application automatically uses CUDA if available:
```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/detect/` | GET, POST | Upload and analyze media |
| `/history/` | GET | View detection history |
| `/history/delete/<id>/` | POST | Delete history record |
| `/about/` | GET | About page |

## 🎮 Usage

1. Navigate to the **Detect** page
2. Choose between **Video** or **Image** tab
3. Drag & drop or click to upload your file
4. Click **Analyze Media**
5. View results with confidence score

## ⚠️ Disclaimer

This tool is for educational and research purposes. While the AI model achieves high accuracy, no detection system is 100% perfect. Results should be used as one factor in assessing media authenticity.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Raj** - [GitHub](https://github.com/Raj280502)

## 🙏 Acknowledgments

- [timm](https://github.com/huggingface/pytorch-image-models) - PyTorch Image Models
- [Django](https://www.djangoproject.com/) - Web Framework
- [Bootstrap](https://getbootstrap.com/) - CSS Framework

---

<p align="center">
  Made with ❤️ for fighting misinformation
</p>
