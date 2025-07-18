# Webhook Receiver

A simple webhook receiver tool that can receive webhook data from Fluent Booking or other services and display the results in real-time on a web page.

## Features

- 🔗 Auto-generate webhook URL
- 📊 Real-time display of received data
- 📋 One-click copy webhook URL and data
- 🔄 Support GET and POST requests
- 📱 Responsive design, mobile-friendly
- 🧹 Clear data functionality
- 🎨 Beautiful modern UI with animations

## Deployment on Zeabur

### Quick Deploy

1. Fork this repository
2. Go to [Zeabur](https://zeabur.com)
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

### Environment Variables (Optional)

You can set these environment variables in Zeabur:
- `PORT`: Port number (default: 5000)
- `DEBUG`: Set to 'true' for debug mode (default: false)

## Local Development

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

4. Copy the webhook URL to your service (e.g., Fluent Booking)

## API Endpoints

- `GET /` - Main page
- `POST /webhook` - Receive webhook data
- `GET /webhook` - Can also receive GET webhook requests
- `GET /events` - Server-Sent Events stream
- `GET /api/data` - Get all received data
- `POST /api/clear` - Clear all data

## Supported Data Formats

- JSON data
- Form data
- Query parameters
- Raw text data

## Use Cases

- Test webhook integration
- Debug webhook data
- Monitor webhook calls
- Develop webhook processing logic

## File Structure

```
Hooky/
├── server.py          # Flask server
├── index.html         # Web interface
├── requirements.txt   # Python dependencies
├── zbpack.json        # Zeabur deployment config
├── Dockerfile         # Docker configuration
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.