#!/bin/bash

# CNN Feature Extractor - EC2 Deployment Script
# Run this script on your EC2 instance after connecting via SSH

echo "🚀 Starting CNN Feature Extractor deployment..."

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python and development tools
echo "🐍 Installing Python and development tools..."
sudo yum install python3 python3-pip -y
sudo yum groupinstall "Development Tools" -y
sudo yum install python3-devel -y

# Install system dependencies for scientific computing
echo "🔬 Installing scientific computing dependencies..."
sudo yum install atlas-devel lapack-devel blas-devel -y

# Create application directory
echo "📁 Creating application directory..."
mkdir -p ~/cnn_app
cd ~/cnn_app

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Gunicorn for production
echo "🦄 Installing Gunicorn..."
pip3 install gunicorn

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/cnn_app.service > /dev/null <<EOF
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
EOF

# Enable and start the service
echo "🚀 Starting CNN Feature Extractor service..."
sudo systemctl daemon-reload
sudo systemctl enable cnn_app
sudo systemctl start cnn_app

# Check service status
echo "📊 Checking service status..."
sudo systemctl status cnn_app --no-pager

# Install and configure Nginx (optional)
read -p "Do you want to install Nginx for better performance? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Installing Nginx..."
    sudo yum install nginx -y
    
    # Create Nginx configuration
    echo "⚙️ Configuring Nginx..."
    sudo tee /etc/nginx/conf.d/cnn_app.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Test and reload Nginx
    sudo nginx -t
    sudo systemctl start nginx
    sudo systemctl enable nginx
    sudo systemctl reload nginx
    
    echo "✅ Nginx installed and configured!"
    echo "🌐 Your app is now accessible at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
else
    echo "✅ Skipping Nginx installation."
    echo "🌐 Your app is accessible at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
fi

# Display final information
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Useful commands:"
echo "  Check service status: sudo systemctl status cnn_app"
echo "  View logs: sudo journalctl -u cnn_app -f"
echo "  Restart service: sudo systemctl restart cnn_app"
echo "  Stop service: sudo systemctl stop cnn_app"
echo ""
echo "🔍 To test your application:"
echo "  curl http://localhost:8000/health"
echo ""
echo "📚 Check the README.md file for more information and troubleshooting tips."
echo ""
echo "Happy learning about CNNs! 🧠🔍"
