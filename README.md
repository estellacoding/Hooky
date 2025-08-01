# Hooky Webhook Receiver
A powerful tool to receive, filter, and analyze webhook data in real-time from any service.

## Features
- 🔗 Auto-generate webhook URL
- 📋 One-click copy webhook URL and data
- 📊 Real-time display of received data with live statistics dashboard  
- 🔄 Support GET and POST requests
- 🧹 Clear data functionality with backend API integration
- 📤 Export webhook data to JSON
- 🎨 Beautiful modern UI with animated gradient background
- 🎛️ Modern card-based interface with Font Awesome icons

## Deployment on Zeabur
### Quick Deploy
1. Fork this repository
2. Go to [Zeabur](https://zeabur.com/referral?referralCode=stelladai1028)
3. Create a new project
4. Import from GitHub and select your forked repository
5. Zeabur will automatically detect and deploy the Flask application

### Manual Setup
1. Clone the repository:
```bash
git clone <your-repo-url>
cd Hooky
```
2. Push to your GitHub repository
3. In Zeabur dashboard:
   - Create new project
   - Add service from GitHub
   - Select your repository
   - Deploy automatically

### Demo
🚀 **Live Demo**: [Hooky Webhook Receiver](https://hooky.zeabur.app/)

## Local Development
**Note**: Most webhook providers require HTTPS endpoints and won't accept HTTP URLs. Local development with HTTP is only suitable for testing with tools like curl or Postman. For actual webhook integration, deploy to a cloud platform (like [Zeabur](https://zeabur.com/referral?referralCode=stelladai1028)) with HTTPS.
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Start the server:
```bash
python server.py
```
3. Open browser and visit:
```
http://localhost:5000
```
4. For testing locally:
   - Use tools like curl, Postman, or browser for manual testing
   - The local HTTP endpoint is: `http://localhost:5000/webhook`
   - **Important**: This HTTP URL cannot be used with real webhook services
5. For production webhook integration:
   - Deploy to a cloud platform (like [Zeabur](https://zeabur.com/referral?referralCode=stelladai1028)) to get HTTPS URL
   - Use the HTTPS webhook URL from your deployment

## API Endpoints
- `GET /` - Main page with advanced UI
- `POST /webhook` - Receive webhook data (primary endpoint)
- `GET /webhook` - Can also receive GET webhook requests  
- `GET /events` - Server-Sent Events stream for real-time updates
- `GET /api/data` - Get all received webhook data
- `POST /api/clear` - Clear all stored data
- `GET /api/health` - Health check endpoint for monitoring

## Supported Data Formats
- JSON data
- Form data
- Query parameters
- Raw text data

## Use Cases
- Test webhook integration with simulation features
- Debug webhook data with advanced filtering
- Monitor webhook calls with real-time statistics
- Develop webhook processing logic
- Export webhook data for analysis
- Real-time webhook monitoring dashboard

## File Structure
```
Hooky/
├── server.py          # Flask server with SSE support
├── index.html         # Advanced web interface with modern UI
├── wsgi.py            # WSGI entry point for deployment
├── requirements.txt   # Python dependencies  
├── assets/            # Static assets
│   ├── site.webmanifest
│   └── images/
│       ├── hooky-logo.png
│       ├── hooky-logo-1080.png
│       ├── hooky-logo-1080-white.png
│       ├── browser-logo.png
│       └── favicon.ico
├── LICENSE
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is open source and available under the MIT License.