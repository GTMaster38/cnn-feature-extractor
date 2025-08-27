# CNN Feature Extractor

A Flask web application that visualizes the core operations of a Convolutional Neural Network (CNN) layer. This interactive tool helps beginners understand how CNNs work by showing the step-by-step process of feature extraction.

## Features

- **Step-by-step CNN visualization**: Upload an image and see how it transforms through each CNN operation
- **Convolution filters**: Multiple pre-defined filters (Edge Detection, Sharpen, Blur, etc.)
- **ReLU activation**: Visualize how ReLU removes negative values
- **Max Pooling**: See how pooling reduces image dimensions while preserving features
- **Educational**: Learn CNN concepts through interactive visualization

## How It Works

1. **Upload Image**: Start with any image file
2. **Convolution**: Apply a filter to detect features like edges and textures
3. **ReLU**: Remove negative values to introduce non-linearity
4. **Max Pooling**: Downsample the image while preserving important features

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000`

## EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose Amazon Linux 2 AMI (free tier eligible)
3. Select t2.micro (free tier) or larger instance
4. Configure Security Group:
   - HTTP (Port 80) - Source: 0.0.0.0/0
   - HTTPS (Port 443) - Source: 0.0.0.0/0
   - SSH (Port 22) - Source: Your IP address
5. Launch and download your key pair (.pem file)

### Step 2: Connect to EC2 Instance

```bash
# On Windows (PowerShell)
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip

# On Mac/Linux
chmod 400 your-key.pem
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3.8 and pip
sudo yum install python3 python3-pip -y

# Install development tools
sudo yum groupinstall "Development Tools" -y
sudo yum install python3-devel -y

# Install additional system dependencies for scientific computing
sudo yum install atlas-devel lapack-devel blas-devel -y
```

### Step 4: Deploy Application

```bash
# Create application directory
mkdir ~/cnn_app
cd ~/cnn_app

# Upload your files (use scp or copy-paste)
# You'll need: app.py, wsgi.py, requirements.txt, templates/index.html

# Install Python dependencies
pip3 install -r requirements.txt

# Test the application
python3 app.py
```

### Step 5: Production Deployment with Gunicorn

```bash
# Install Gunicorn
pip3 install gunicorn

# Create systemd service file
sudo nano /etc/systemd/system/cnn_app.service
```

Add this content to the service file:
```ini
[Unit]
Description=CNN Feature Extractor
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/cnn_app
Environment="PATH=/home/ec2-user/.local/bin"
ExecStart=/home/ec2-user/.local/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start the service
sudo systemctl enable cnn_app
sudo systemctl start cnn_app
sudo systemctl status cnn_app
```

### Step 6: Configure Nginx (Optional but Recommended)

```bash
# Install Nginx
sudo yum install nginx -y

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure Nginx
sudo nano /etc/nginx/conf.d/cnn_app.conf
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 7: Access Your Application

Open your browser and go to:
- `http://your-ec2-public-ip` (if using Nginx)
- `http://your-ec2-public-ip:8000` (if using Gunicorn directly)

## File Structure

```
cnn_visualizer/
├── app.py              # Main Flask application
├── wsgi.py             # WSGI configuration for production
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # HTML template
└── README.md          # This file
```

## Available Filters

- **Identity**: No change to the image
- **Sharpen**: Enhances edges and details
- **Edge Detect**: Detects edges in the image
- **Strong Edge Detect**: More aggressive edge detection
- **Sobel Top**: Detects horizontal edges
- **Box Blur**: Smooths the image

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` or kill the process using that port
2. **Permission denied**: Make sure your key file has correct permissions (chmod 400)
3. **Dependencies not found**: Install system-level dependencies for scientific computing
4. **Image upload fails**: Check file size limits and supported formats

### Logs

```bash
# Check application logs
sudo journalctl -u cnn_app -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Security Considerations

- Change the secret key in `app.py` for production
- Restrict SSH access to your IP address only
- Consider using HTTPS with Let's Encrypt
- Regularly update your system and dependencies

## Contributing

This is a learning project. Feel free to:
- Add new filters
- Improve the UI/UX
- Add more CNN operations
- Fix bugs or improve performance

## License

This project is for educational purposes. Feel free to use and modify as needed.

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Check system logs for errors
4. Ensure proper file permissions

Happy learning about CNNs! 🧠🔍
