
---

# 🎮 **GameSite - Flask App** 🎮

Welcome to **[GameSite](https://www.wkcustoms.com/)**, your go-to web app for discovering the best deals on video games! 🚀 This project, powered by Flask, helps users find and track trending games with the best prices across various platforms. With flexible deployment options, you can run this app using Docker on any service of your choice.

---

## 🌟 **Features**

- **💰 Game Deals by Genre**: Browse and track game deals categorized by genre, from action-packed adventures to strategy-based challenges.
- **📈 Real-Time Updates**: Periodically fetches and updates pricing data via integrated APIs.
- **📦 Portable Deployment**: Run GameSite on any deployment service (AWS EC2, local, or your preferred hosting solution).
- **💻 Simple UI**: Built with CSS and HTML for an intuitive and responsive design.
- **🔒 Secure Configuration**: Keep your database and API credentials secure using environment variables.

---

## 🛠️ **Tech Stack**

This project is built with:
- **Backend**: Python with Flask Framework 🐍
- **Database**: MySQL (AWS RDS recommended for hosting) 💾
- **Frontend**: CSS and HTML 🎨
- **Containerization**: Docker for easy setup and deployment 🐳
- **Deployment**: Designed for flexibility (AWS EC2, local hosting, or other platforms) ☁️

---

## 🚀 **Installation and Setup**

Here’s how you can set up GameSite for yourself:

### 1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/gamesite.git
   cd gamesite
   ```

### 2. **Set Up the `.env` File**
   Create a `.env` file in the root directory and include the following configuration:
   ```env
   DB_HOST=your-database-host
   DB_USER=your-database-username
   DB_PASS=your-database-password
   DB_NAME=your-database-name
   ```

### 3. **Run the Fetch Script**
   - The `fetch_games.py` script will automatically create tables (if they don’t exist) and populate them with game data.
   - Run the script:
     ```bash
     python fetch_games.py
     ```

### 4. **Build and Run with Docker**
   Build the Docker image:
   ```bash
   sudo docker build -t gamesite-image .
   ```
   Run the container:
   ```bash
   sudo docker run --name gamesite -p 5000:5000 gamesite-image
   ```

### 5. **Access the App**
   Open your browser and navigate to ```http://<your-app-url>:5000```

   Replace ```<your-app-url>``` with the actual URL where the app is hosted.

---

## 📊 **Database Schema**

Each genre has its own table, sharing the same schema. Here's the structure:

### Example Table: `action_games`

| Column Name         | Data Type   | Description                          |
|---------------------|-------------|--------------------------------------|
| `appid`             | INT         | Unique identifier for the game (Primary Key) |
| `name`              | VARCHAR(255)| Title of the game                   |
| `header_image`      | TEXT        | URL to the game’s header image       |
| `short_description` | TEXT        | A brief description of the game      |
| `price`             | VARCHAR(50) | Game price or pricing details        |
| `store_link`        | TEXT        | URL to the game's store page         |
| `last_updated`      | TIMESTAMP   | Time when the data was last updated  |

### Other Genre Tables

The same structure applies to all genre-specific tables:
- `adventure_games`
- `earlyaccess_games`
- `free_games`
- `indie_games`
- `mmo_games`
- `rpg_games`
- `simulation_games`
- `sports_games`
- `strategy_games`

---

## 🔄 **Fetching Game Data**

The `fetch_games.py` script is the backbone of data management in GameSite. It performs the following functions:

### 1. **Table Creation**:
   - Automatically creates tables for each genre if they don’t already exist in the database.

### 2. **Data Fetching**:
   - Uses the [SteamSpy API](https://steamspy.com/api.php?request=genre&genre) to fetch genre-specific game data.
   - Retrieves detailed game information (title, image, price, etc.) using the Steam API.

### 3. **Data Insertion**:
   - Populates or updates records in the corresponding genre tables using the `ON DUPLICATE KEY UPDATE` query to avoid duplicate entries.

### How to Run the Script:
   - Ensure your `.env` file is correctly configured.
   - Run the script:
     ```bash
     python fetch_games.py
     ```
   - Automate this process using a scheduler (e.g., [cron](https://www.geeksforgeeks.org/how-to-schedule-python-scripts-as-cron-jobs-with-crontab/) on Linux or Task Scheduler on Windows) for periodic updates.

---

## 🌐 **Flexible Deployment**

You can deploy the GameSite app on any service or platform that supports Docker. While we recommend AWS EC2 and AWS RDS for hosting the app and database, you are free to use your preferred solution.

Deployment Steps:
1. Set up a host service (e.g., AWS EC2, Google Cloud, Azure, or local hosting).
2. Install Docker on the host.
3. Follow the steps to build and run the Docker container.
4. Configure your database and environment variables appropriately.

---

## 🔒 Optional: SSL Configuration and Nginx Setup

For users who want to secure their app with SSL, you can configure Nginx as a reverse proxy and obtain an SSL certificate for your domain. Here’s how:

### 1. Install Nginx:
   On your server (e.g., AWS EC2):
   ```bash
   sudo apt update
   sudo apt install nginx
   ```
### 2. Set Up Nginx as  Reverse Proxy:
   Create a configuration file for your Flask app:
   ```bash
   sudo nano /etc/nginx/sites-available/gamesite
   ```

   Add the following configuration (adjust for your domain and Flask app location):
   ```bash
      server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

   Enable the configuration:
   ```bash
   sudo ln -s /etc/nginx/sites-available/gamesite /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### 3. Obtain an SSL Certificate:
   Use Certbot to obtain a free SSL certificate:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```
   Follow the prompts to complete the process.

### 4. Test the Configuration:
   Access your site using HTTPS:
   ```bash
   https://your-domain.com
   ```

---

## 📚 **Sources**

This app relies on the following key resources and tools:

### Resources and Tools

1. **APIs for Game Data**:
   - [Steamspy](https://steamspy.com/api.php?request=genre&genre) - The primary source for fetching game data by genre, including game titles, descriptions, images, and pricing details.

2. **Frameworks and Libraries**:
   - [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework for backend development.
   - [MySQL](https://www.mysql.com/) - A relational database system for storing game information.

3. **Containerization**:
   - [Docker](https://www.docker.com/) - Used for application packaging and deployment, ensuring consistency across environments.

4. **Hosting**:
   - [AWS RDS](https://aws.amazon.com/rds/) - Provides scalable and managed MySQL database hosting.
   - [AWS EC2](https://aws.amazon.com/ec2/) - Recommended for deploying and running the Dockerized app.

5. **Development Tools**:
   - [Python](https://www.python.org/) - The core programming language used for backend development.
   - [PyCharm](https://www.jetbrains.com/pycharm/) or any preferred IDE - For writing, debugging, and managing code.
   - [Docker](https://www.docker.com/) - Used here as both a containerization and development tool.

6. **Frontend Tools**:
   - [HTML & CSS](https://developer.mozilla.org/en-US/docs/Web) - For designing and structuring the user interface. Special thanks to [Kevin Powell](https://www.youtube.com/c/KevinPowell) for web design ideas.
   - [Bootstrap](https://getbootstrap.com/) - For responsive design and enhanced styling.
   - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - To add interactivity to the user interface.

7. **Additional Resources**:
   - [Flask Documentation](https://flask.palletsprojects.com/) - Comprehensive guides and references for Flask.
   - [Docker Hub](https://hub.docker.com/) - For managing and sharing Docker images.
   - [AWS Free Tier](https://aws.amazon.com/free/) - Information about free-tier resources for AWS.

---

⭐ **If you enjoy this project, star the repository and share it with your friends!** ⭐

--- 
