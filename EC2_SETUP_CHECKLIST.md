# EC2 Setup Checklist for CNN Feature Extractor

## Pre-Deployment Checklist ✅

- [ ] AWS account created and configured
- [ ] EC2 instance launched (Amazon Linux 2, t2.micro or larger)
- [ ] Security group configured with proper ports (80, 443, 22)
- [ ] Key pair (.pem file) downloaded and secured
- [ ] All project files ready (app.py, wsgi.py, requirements.txt, templates/index.html)

## Step-by-Step Deployment ✅

### 1. Launch EC2 Instance
- [ ] Go to AWS Console → EC2 → Launch Instance
- [ ] Choose Amazon Linux 2 AMI
- [ ] Select t2.micro (free tier) or larger
- [ ] Configure Security Group:
  - [ ] HTTP (Port 80) - Source: 0.0.0.0/0
  - [ ] HTTPS (Port 443) - Source: 0.0.0.0/0  
  - [ ] SSH (Port 22) - Source: Your IP address
- [ ] Launch instance and download key pair

### 2. Connect to EC2
- [ ] Open terminal/PowerShell
- [ ] Navigate to directory with .pem file
- [ ] Connect via SSH:
  ```bash
  # Windows (PowerShell)
  ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
  
  # Mac/Linux
  chmod 400 your-key.pem
  ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
  ```

### 3. Upload Project Files
- [ ] Create application directory: `mkdir ~/cnn_app && cd ~/cnn_app`
- [ ] Upload files using one of these methods:
  - [ ] **Method A**: Copy-paste file contents directly
  - [ ] **Method B**: Use SCP from your local machine:
    ```bash
    scp -i "your-key.pem" app.py ec2-user@your-ec2-public-ip:~/cnn_app/
    scp -i "your-key.pem" wsgi.py ec2-user@your-ec2-public-ip:~/cnn_app/
    scp -i "your-key.pem" requirements.txt ec2-user@your-ec2-public-ip:~/cnn_app/
    scp -i "your-key.pem" -r templates ec2-user@your-ec2-public-ip:~/cnn_app/
    ```
  - [ ] **Method C**: Use the automated deployment script:
    ```bash
    chmod +x deploy.sh
    ./deploy.sh
    ```

### 4. Install Dependencies
- [ ] Update system: `sudo yum update -y`
- [ ] Install Python and tools:
  ```bash
  sudo yum install python3 python3-pip -y
  sudo yum groupinstall "Development Tools" -y
  sudo yum install python3-devel -y
  ```
- [ ] Install scientific computing dependencies:
  ```bash
  sudo yum install atlas-devel lapack-devel blas-devel -y
  ```
- [ ] Install Python packages: `pip3 install -r requirements.txt`

### 5. Test Application
- [ ] Test locally: `python3 app.py`
- [ ] Check if app responds: `curl http://localhost:5000/health`
- [ ] Stop test server (Ctrl+C)

### 6. Production Deployment
- [ ] Install Gunicorn: `pip3 install gunicorn`
- [ ] Create systemd service file (see README.md or use deploy.sh)
- [ ] Enable and start service:
  ```bash
  sudo systemctl enable cnn_app
  sudo systemctl start cnn_app
  ```
- [ ] Check service status: `sudo systemctl status cnn_app`

### 7. Configure Nginx (Optional)
- [ ] Install Nginx: `sudo yum install nginx -y`
- [ ] Create configuration file (see README.md or use deploy.sh)
- [ ] Test configuration: `sudo nginx -t`
- [ ] Start and enable Nginx:
  ```bash
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```

### 8. Final Testing
- [ ] Test from your local machine:
  - [ ] With Nginx: `http://your-ec2-public-ip`
  - [ ] Without Nginx: `http://your-ec2-public-ip:8000`
- [ ] Test health endpoint: `http://your-ec2-public-ip/health`
- [ ] Upload an image and test the full pipeline

## Troubleshooting Checklist ✅

### Common Issues
- [ ] **Permission denied**: Check .pem file permissions (chmod 400)
- [ ] **Port already in use**: Check what's using port 8000: `sudo netstat -tlnp | grep :8000`
- [ ] **Dependencies not found**: Install system-level scientific computing packages
- [ ] **Service won't start**: Check logs: `sudo journalctl -u cnn_app -f`
- [ ] **Can't access from browser**: Check security group and firewall settings

### Useful Commands
- [ ] Check service status: `sudo systemctl status cnn_app`
- [ ] View logs: `sudo journalctl -u cnn_app -f`
- [ ] Restart service: `sudo systemctl restart cnn_app`
- [ ] Check Nginx status: `sudo systemctl status nginx`
- [ ] Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

## Security Checklist ✅

- [ ] Change secret key in app.py for production
- [ ] Restrict SSH access to your IP address only
- [ ] Consider setting up HTTPS with Let's Encrypt
- [ ] Regularly update system packages
- [ ] Monitor application logs for suspicious activity

## Performance Checklist ✅

- [ ] Use appropriate instance size for your needs
- [ ] Consider using Nginx for better performance
- [ ] Monitor CPU and memory usage
- [ ] Set up CloudWatch alarms if needed
- [ ] Consider using a load balancer for high traffic

## Success Indicators ✅

- [ ] Application accessible from browser
- [ ] Image upload and processing working
- [ ] All CNN operations (convolution, ReLU, pooling) functioning
- [ ] Service starts automatically on reboot
- [ ] Health endpoint responding correctly
- [ ] No errors in logs

## Next Steps ✅

- [ ] Share your app with classmates
- [ ] Add more CNN filters and operations
- [ ] Improve the UI/UX
- [ ] Add more educational content
- [ ] Consider adding user accounts and saved results
- [ ] Deploy to other cloud providers for comparison

---

**🎉 Congratulations!** You've successfully deployed a CNN visualization tool to the cloud!

**📚 Learning Outcomes:**
- Understanding CNN operations through visualization
- Deploying web applications to cloud infrastructure
- Managing production services and configurations
- Troubleshooting deployment issues

**🔍 Remember:** This is a learning project - experiment, break things, and learn from the process!
