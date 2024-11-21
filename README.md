
---

# 🎮 **GameSite - Flask App** 🎮

Welcome to **GameSite**, your go-to web app for discovering the best deals on video games! 🚀 This project, powered by Flask, helps users find and track trending games with the best prices across various platforms. With flexible deployment options, you can run this app using Docker on any service of your choice.

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
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

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
   - Automate this process using a scheduler (e.g., `cron` on Linux or Task Scheduler on Windows) for periodic updates.

---

## 🌐 **Flexible Deployment**

You can deploy the GameSite app on any service or platform that supports Docker. While we recommend AWS EC2 and AWS RDS for hosting the app and database, you are free to use your preferred solution.

Deployment Steps:
1. Set up a host service (e.g., AWS EC2, Google Cloud, Azure, or local hosting).
2. Install Docker on the host.
3. Follow the steps to build and run the Docker container.
4. Configure your database and environment variables appropriately.

---

## 📚 **Sources**

This app relies on the following key resources and tools:

1. **APIs for Game Data**:
   - [Steamspy](https://steamspy.com/api.php?request=genre&genre) - The primary source for fetching game data by genre, including game titles, descriptions, images, and pricing details.

2. **Frameworks and Libraries**:
   - [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework.
   - [MySQL](https://www.mysql.com/) - Database system for storing game information.

3. **Containerization**:
   - [Docker](https://www.docker.com/) - Used for application packaging and deployment.

4. **Hosting**:
   - **AWS RDS**: For scalable and managed MySQL database hosting.
   - **AWS EC2**: Recommended for deploying and running the Dockerized app.
   - 

5. **Development Tools**:
   - [Python](https://www.python.org/) - The core programming language for backend development.
   - [HTML & CSS](https://developer.mozilla.org/en-US/docs/Web) - For building the user interface.
   - [PyCharm](https://www.jetbrains.com/pycharm/) or any preferred IDE for code editing.

6. **Frontend Tools**:
   - [source1]
   - [source2]

6. **Additional Resources**:
   - Flask Documentation: [Flask Docs](https://flask.palletsprojects.com/)
   - Docker Hub: [Docker Hub](https://hub.docker.com/)
   - AWS: [AWS Free Tier](https://aws.amazon.com/free/)


---

⭐ **If you enjoy this project, star the repository and share it with your friends!** ⭐

--- 