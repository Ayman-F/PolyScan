# PolyScan - Regulatory Risk Analysis Platform (By Ayman Fasly, Sylverson Charles, Adam Azrou)

A Flask-based web application that analyzes regulatory documents and assesses their impact on publicly traded companies using AI-powered analysis and real-time market data.

## 🚀 Features

- **Document Analysis**: Upload and process regulatory documents (XML/TXT/HTML) with intelligent text extraction
- **AI-Powered Impact Assessment**: Uses Claude AI via AWS Bedrock to analyze regulatory impact on specific companies
- **Company Analysis Search**: Search bar to analyze any company's, even if not mentioned in the report that our code generate
- **Real-Time Market Data**: Integration with Yahoo Finance API for live stock prices
- **Interactive Dashboard**: S&P 500, NASDAQ indices, and Fear & Greed Index with visual gauges all done using API's.
- **Cyberpunk UI**: Futuristic design with neon effects, glass morphism, and responsive layout
- **Progress Tracking**: Real-time progress bars with time estimation for document processing

## 🛠 Technology Stack

- **Backend**: Flask (Python)
- **AI Integration**: AWS Bedrock (Claude AI)
- **Market Data**: Yahoo Finance API
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JavaScript
- **Document Processing**: Custom XML/PDF parser with chunked analysis
- **Styling**: Cyberpunk theme with gradients, animations, and neon colors

## 📁 Project Structure

```
PolyScan/
├── app.py                 # Main Flask application with API routes
├── chunked_analyzer.py    # Document processing and AI analysis engine
├── templates/
│   └── index.html        # Main UI template with dashboard and forms
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Installation & Setup

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ayman-F/PolyScan.git
   cd PolyScan
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials** for Bedrock access:
   ```bash
   aws configure
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**: 
    
   - **SageMaker**: Use `https://dbkteg3a3epmwcc.studio.us-west-2.sagemaker.aws/jupyterlab/default/proxy/8080/`(RECOMMENDED)
   - **Local**: Open `http://localhost:8080` in your browser

### 🚨 Important SageMaker Notes

- **Use Classic SageMaker Studio**: The application requires the old SageMaker Studio interface, not the new version
- **Proxy URL**: The SageMaker proxy URL format is required for proper routing in the cloud environment: https://<APP_ID>.studio.<REGION>.sagemaker.aws/jupyterlab/default/proxy/8501/
- **Port Configuration**: Application runs on port 8080 for both local and SageMaker environments

## 📋 Dependencies

```
Flask==2.3.3
boto3==1.28.85
yfinance==0.2.28
requests==2.31.0
beautifulsoup4==4.12.2
```

## 🎯 Usage Workflow

1. **Upload Regulation Document**: Select and upload regulatory document (XML/PDF/HTML format)
2. **Document Processing**: System extracts and analyzes regulatory content using chunked processing
3. **Company Analysis**: Enter company ticker symbol for AI-powered impact assessment
4. **View Results**: Review color-coded analysis with highlighted key terms and risk factors
5. **Monitor Markets**: Track real-time market data and sentiment indicators

## 🔍 Key Components

### Flask Routes (`app.py`)
- `/` - Main dashboard interface
- `/portfolio-overview` - Market data API endpoint
- `/analyze-company` - Company impact analysis API
- `/upload` - Document upload and processing

### Analysis Engine (`chunked_analyzer.py`)
- Document text extraction and preprocessing
- Claude AI integration for regulatory impact analysis
- Chunked processing for large documents
- Color-coded result formatting with term highlighting

### Frontend Features (`index.html`)
- Responsive cyberpunk-themed interface
- Real-time progress tracking with JavaScript
- Interactive market data displays
- Form validation and error handling
- Dynamic content updates via AJAX

## 🎨 Design Features

- **Cyberpunk Aesthetic**: Neon colors, gradients, and futuristic styling
- **Glass Morphism**: Translucent cards with backdrop blur effects
- **Responsive Design**: Mobile-friendly layout with Bootstrap 5
- **Interactive Elements**: Hover effects, animations, and visual feedback
- **Color Coding**: Highlighted terms for easy identification of key regulatory concepts

## 🔒 Security & Validation

- File type validation for document uploads
- Company ticker validation before analysis
- Secure AWS Bedrock integration
- Input sanitization and error handling

## 📊 Performance Optimizations

- Chunked document processing for large files
- Optimized XML text extraction
- Efficient API endpoint design
- Minimal code implementation following best practices

## 🌐 Live Demo

Repository: [https://github.com/Ayman-F/PolyScan](https://github.com/Ayman-F/PolyScan)

## 📝 Development Notes

This project was developed with a focus on:
- Clean, maintainable code architecture
- Efficient document processing algorithms
- Modern UI/UX design principles
- Real-time data integration
- AI-powered regulatory analysis

The application successfully processes complex regulatory documents and provides actionable insights for investment decision-making through an intuitive, visually appealing interface.
