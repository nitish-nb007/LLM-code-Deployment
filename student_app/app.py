import os
import json
import time
import threading
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from github import Github, GithubException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
APP_SECRET = os.getenv('APP_SECRET', 'default-secret-123')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# In-memory storage for deployment status (in production, use a database)
deployments = {}

class AppGenerator:
    """Generates web applications based on task briefs"""
    
    @staticmethod
    def generate_app(brief, attachments=None):
        """Generate application code based on the brief"""
        brief_lower = brief.lower()
        
        if any(word in brief_lower for word in ['calculator', 'calc', 'math']):
            return AppGenerator._generate_calculator()
        elif any(word in brief_lower for word in ['counter', 'count', 'increment']):
            return AppGenerator._generate_counter()
        elif any(word in brief_lower for word in ['todo', 'task', 'checklist']):
            return AppGenerator._generate_todo()
        elif any(word in brief_lower for word in ['timer', 'stopwatch', 'countdown']):
            return AppGenerator._generate_timer()
        elif any(word in brief_lower for word in ['markdown', 'md', 'convert']):
            return AppGenerator._generate_markdown_editor()
        elif any(word in brief_lower for word in ['github', 'user', 'profile']):
            return AppGenerator._generate_github_lookup()
        else:
            return AppGenerator._generate_default_app(brief)

    @staticmethod
    def _generate_calculator():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .calculator { max-width: 400px; margin: 50px auto; }
        .display { font-size: 2rem; text-align: right; padding: 20px; background: #f8f9fa; border: 1px solid #dee2e6; }
        .btn { font-size: 1.2rem; padding: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="calculator">
            <h1 class="text-center mb-4">Calculator</h1>
            <input type="text" class="form-control display mb-3" id="display" readonly>
            <div class="row g-2">
                <div class="col-3"><button class="btn btn-danger w-100" onclick="clearDisplay()">C</button></div>
                <div class="col-3"><button class="btn btn-secondary w-100" onclick="appendToDisplay('/')">/</button></div>
                <div class="col-3"><button class="btn btn-secondary w-100" onclick="appendToDisplay('*')">×</button></div>
                <div class="col-3"><button class="btn btn-secondary w-100" onclick="appendToDisplay('-')">-</button></div>
                
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('7')">7</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('8')">8</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('9')">9</button></div>
                <div class="col-3"><button class="btn btn-secondary w-100" onclick="appendToDisplay('+')">+</button></div>
                
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('4')">4</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('5')">5</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('6')">6</button></div>
                <div class="col-3"><button class="btn btn-success w-100" onclick="calculate()" style="height: 100%">=</button></div>
                
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('1')">1</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('2')">2</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('3')">3</button></div>
                <div class="col-3"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('0')">0</button></div>
                
                <div class="col-6"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('00')">00</button></div>
                <div class="col-6"><button class="btn btn-outline-primary w-100" onclick="appendToDisplay('.')">.</button></div>
            </div>
        </div>
    </div>

    <script>
        const display = document.getElementById('display');
        
        function appendToDisplay(value) {
            display.value += value;
        }
        
        function clearDisplay() {
            display.value = '';
        }
        
        function calculate() {
            try {
                display.value = eval(display.value.replace('×', '*'));
            } catch (error) {
                display.value = 'Error';
            }
        }
        
        // Keyboard support
        document.addEventListener('keydown', function(event) {
            if (event.key >= '0' && event.key <= '9') appendToDisplay(event.key);
            else if (['+', '-', '*', '/', '.'].includes(event.key)) appendToDisplay(event.key);
            else if (event.key === 'Enter') calculate();
            else if (event.key === 'Escape') clearDisplay();
        });
    </script>
</body>
</html>''',
            'README.md': '''# Calculator App

A responsive calculator web application built with Bootstrap.

## Features
- Basic arithmetic operations
- Keyboard support
- Responsive design
- Error handling

## Usage
Click the buttons or use your keyboard to perform calculations.

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_counter():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Counter App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .counter { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    </style>
</head>
<body class="d-flex align-items-center">
    <div class="container">
        <div class="counter text-center p-5">
            <h1 class="mb-4">Counter App</h1>
            <div class="display-1 fw-bold text-primary mb-4" id="count">0</div>
            <div class="btn-group" role="group">
                <button class="btn btn-danger btn-lg" onclick="changeCount(-1)">-1</button>
                <button class="btn btn-secondary btn-lg" onclick="resetCount()">Reset</button>
                <button class="btn btn-success btn-lg" onclick="changeCount(1)">+1</button>
            </div>
        </div>
    </div>

    <script>
        let count = 0;
        const countElement = document.getElementById('count');
        
        function updateDisplay() {
            countElement.textContent = count;
            document.title = `Counter: ${count}`;
        }
        
        function changeCount(value) {
            count += value;
            updateDisplay();
        }
        
        function resetCount() {
            count = 0;
            updateDisplay();
        }
        
        updateDisplay();
    </script>
</body>
</html>''',
            'README.md': '''# Counter App

A simple counter application with increment, decrement, and reset functionality.

## Features
- Beautiful gradient background
- Responsive design
- Real-time display updates

## Usage
Click the buttons to change the counter value.

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_todo():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .completed { text-decoration: line-through; opacity: 0.6; }
        .todo-item { transition: all 0.3s ease; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h1 class="text-center mb-4">Todo List</h1>
                <div class="input-group mb-3">
                    <input type="text" class="form-control" id="todoInput" placeholder="Enter a new task...">
                    <button class="btn btn-primary" onclick="addTodo()">Add Task</button>
                </div>
                <div id="todoList"></div>
            </div>
        </div>
    </div>

    <script>
        let todos = JSON.parse(localStorage.getItem('todos')) || [];
        
        function renderTodos() {
            const todoList = document.getElementById('todoList');
            todoList.innerHTML = '';
            
            todos.forEach((todo, index) => {
                const todoItem = document.createElement('div');
                todoItem.className = 'todo-item d-flex justify-content-between align-items-center p-2 border-bottom';
                todoItem.innerHTML = `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" ${todo.completed ? 'checked' : ''} 
                               onchange="toggleTodo(${index})" id="todo-${index}">
                        <label class="form-check-label ${todo.completed ? 'completed' : ''}" for="todo-${index}">
                            ${todo.text}
                        </label>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteTodo(${index})">Delete</button>
                `;
                todoList.appendChild(todoItem);
            });
            
            localStorage.setItem('todos', JSON.stringify(todos));
        }
        
        function addTodo() {
            const input = document.getElementById('todoInput');
            const text = input.value.trim();
            
            if (text) {
                todos.push({ text, completed: false });
                input.value = '';
                renderTodos();
            }
        }
        
        function toggleTodo(index) {
            todos[index].completed = !todos[index].completed;
            renderTodos();
        }
        
        function deleteTodo(index) {
            todos.splice(index, 1);
            renderTodos();
        }
        
        document.getElementById('todoInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') addTodo();
        });
        
        renderTodos();
    </script>
</body>
</html>''',
            'README.md': '''# Todo List App

A feature-rich todo list application with local storage persistence.

## Features
- Add, delete, and mark tasks as complete
- Persistent storage using localStorage
- Clean and modern interface
- Keyboard support

## Usage
1. Type a task and press Enter or click "Add Task"
2. Check tasks to mark as complete
3. Click Delete to remove tasks

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_timer():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timer App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); min-height: 100vh; }
        .timer { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .time-display { font-family: 'Courier New', monospace; }
    </style>
</head>
<body class="d-flex align-items-center">
    <div class="container">
        <div class="timer text-center p-5">
            <h1 class="mb-4">Timer</h1>
            <div class="time-display display-1 fw-bold mb-4" id="display">00:00</div>
            
            <div class="row mb-4">
                <div class="col">
                    <label class="form-label">Minutes</label>
                    <input type="number" class="form-control text-center" id="minutes" value="1" min="0">
                </div>
                <div class="col">
                    <label class="form-label">Seconds</label>
                    <input type="number" class="form-control text-center" id="seconds" value="0" min="0" max="59">
                </div>
            </div>
            
            <div class="btn-group" role="group">
                <button class="btn btn-success btn-lg" onclick="startTimer()">Start</button>
                <button class="btn btn-warning btn-lg" onclick="pauseTimer()">Pause</button>
                <button class="btn btn-danger btn-lg" onclick="resetTimer()">Reset</button>
            </div>
        </div>
    </div>

    <script>
        let totalSeconds = 0;
        let timerInterval = null;
        let isRunning = false;
        
        const display = document.getElementById('display');
        const minutesInput = document.getElementById('minutes');
        const secondsInput = document.getElementById('seconds');
        
        function updateDisplay() {
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;
            display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            document.title = `Timer: ${display.textContent}`;
        }
        
        function startTimer() {
            if (isRunning) return;
            
            if (totalSeconds === 0) {
                const minutes = parseInt(minutesInput.value) || 0;
                const seconds = parseInt(secondsInput.value) || 0;
                totalSeconds = minutes * 60 + seconds;
            }
            
            if (totalSeconds > 0) {
                isRunning = true;
                timerInterval = setInterval(() => {
                    totalSeconds--;
                    updateDisplay();
                    
                    if (totalSeconds <= 0) {
                        clearInterval(timerInterval);
                        isRunning = false;
                        alert('Timer finished!');
                    }
                }, 1000);
            }
        }
        
        function pauseTimer() {
            if (isRunning) {
                clearInterval(timerInterval);
                isRunning = false;
            }
        }
        
        function resetTimer() {
            clearInterval(timerInterval);
            isRunning = false;
            totalSeconds = 0;
            updateDisplay();
            minutesInput.value = 1;
            secondsInput.value = 0;
        }
        
        updateDisplay();
    </script>
</body>
</html>''',
            'README.md': '''# Timer App

A countdown timer application with start, pause, and reset functionality.

## Features
- Customizable timer duration
- Visual countdown display
- Alert when timer completes
- Beautiful gradient background

## Usage
1. Set minutes and seconds
2. Click Start to begin countdown
3. Use Pause to stop temporarily
4. Use Reset to clear

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_markdown_editor():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Editor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highlight.js@11.7.0/lib/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.7.0/styles/github.min.css">
    <style>
        .editor-container { height: 400px; }
        textarea, #preview { height: 100%; font-family: 'Monaco', 'Menlo', monospace; }
        #preview { overflow-y: auto; padding: 15px; border: 1px solid #dee2e6; border-radius: 0.375rem; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Markdown Editor</h1>
        <div class="row editor-container">
            <div class="col-md-6">
                <textarea class="form-control" id="markdown-input" placeholder="Enter your markdown here..."># Welcome
**This is a markdown editor**

- Feature 1
- Feature 2
- Feature 3

`console.log("Hello World");`</textarea>
            </div>
            <div class="col-md-6">
                <div id="preview"></div>
            </div>
        </div>
    </div>

    <script>
        const input = document.getElementById('markdown-input');
        const preview = document.getElementById('preview');
        
        function updatePreview() {
            const markdown = input.value;
            preview.innerHTML = marked.parse(markdown);
            preview.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }
        
        input.addEventListener('input', updatePreview);
        updatePreview();
    </script>
</body>
</html>''',
            'README.md': '''# Markdown Editor

A real-time Markdown editor with live preview and syntax highlighting.

## Features
- Live Markdown preview
- Syntax highlighting for code blocks
- Split-pane editor
- Bootstrap styling

## Usage
Type Markdown in the left pane and see the rendered HTML in the right pane.

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_github_lookup():
        return {
            'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub User Lookup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">GitHub User Lookup</h1>
        <div class="row justify-content-center">
            <div class="col-md-6">
                <form id="github-form" class="mb-4">
                    <div class="input-group">
                        <input type="text" class="form-control" id="username" placeholder="Enter GitHub username" required>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </div>
                </form>
                <div id="result" class="text-center"></div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('github-form');
        const result = document.getElementById('result');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value.trim();
            
            if (!username) return;
            
            result.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
            
            try {
                const response = await fetch(`https://api.github.com/users/${username}`);
                if (!response.ok) throw new Error('User not found');
                
                const user = await response.json();
                
                result.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <img src="${user.avatar_url}" class="rounded-circle mb-3" width="100" height="100">
                            <h3>${user.name || user.login}</h3>
                            <p>${user.bio || 'No bio available'}</p>
                            <div class="row text-center">
                                <div class="col">
                                    <strong>${user.public_repos}</strong><br>Repos
                                </div>
                                <div class="col">
                                    <strong>${user.followers}</strong><br>Followers
                                </div>
                                <div class="col">
                                    <strong>${user.following}</strong><br>Following
                                </div>
                            </div>
                            <a href="${user.html_url}" target="_blank" class="btn btn-outline-primary mt-3">View Profile</a>
                        </div>
                    </div>
                `;
            } catch (error) {
                result.innerHTML = `<div class="alert alert-danger">User not found. Please check the username.</div>`;
            }
        });
    </script>
</body>
</html>''',
            'README.md': '''# GitHub User Lookup

A simple application to look up GitHub user profiles.

## Features
- Search GitHub users by username
- Display user information and statistics
- Responsive design with Bootstrap

## Usage
Enter a GitHub username and click Search to view profile information.

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _generate_default_app(brief):
        return {
            'index.html': f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .app-container {{ background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
    </style>
</head>
<body class="d-flex align-items-center">
    <div class="container">
        <div class="app-container text-center p-5">
            <h1 class="mb-4">🚀 Your Generated App</h1>
            <p class="lead mb-4">This application was automatically generated based on your request.</p>
            
            <div class="alert alert-info mb-4">
                <strong>Original Request:</strong><br>
                "{brief}"
            </div>
            
            <div class="row text-start mb-4">
                <div class="col-md-6">
                    <h5>Features Included:</h5>
                    <ul>
                        <li>Responsive Design</li>
                        <li>Modern UI/UX</li>
                        <li>Bootstrap 5</li>
                        <li>Cross-browser Compatible</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5>Next Steps:</h5>
                    <ul>
                        <li>Customize the code</li>
                        <li>Add your features</li>
                        <li>Deploy to your server</li>
                    </ul>
                </div>
            </div>
            
            <button class="btn btn-primary btn-lg" onclick="showAlert()">Get Started</button>
        </div>
    </div>

    <script>
        function showAlert() {{
            alert('Your app is ready! Feel free to customize it.');
        }}
    </script>
</body>
</html>''',
            'README.md': f'''# Generated Application

This application was automatically generated based on the request: "{brief}"

## Features
- Modern, responsive design
- Bootstrap 5 integration
- Clean and professional interface
- Easy to customize

## Getting Started
Open `index.html` in your web browser to view the application.

## Customization
Feel free to modify the code to add your specific features and functionality.

## License
MIT License
''',
            'LICENSE': AppGenerator._get_mit_license()
        }

    @staticmethod
    def _get_mit_license():
        return '''MIT License

Copyright (c) 2024 LLM Generated App

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


class GitHubManager:
    """Manages GitHub repository operations"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GitHub token not configured")
        self.g = Github(self.github_token)
        self.user = self.g.get_user()

    def create_repository(self, task_id, app_files, email):
        """Create a new repository and deploy app files"""
        try:
            # Create unique repo name
            repo_name = f"llm-app-{task_id}".lower().replace('_', '-')
            
            # Create repository
            repo = self.user.create_repo(
                name=repo_name,
                description=f"LLM-generated app for {task_id}",
                private=False,
                auto_init=False,
                license_template="mit"
            )
            print(f"✅ Repository created: {repo.html_url}")

            # Create files
            commit_message = f"Initial commit for {task_id}"
            for filename, content in app_files.items():
                repo.create_file(filename, commit_message, content)
                print(f"📁 Created file: {filename}")

            # Enable GitHub Pages
            try:
                repo.create_pages_site(build_type="workflow", source={"branch": "main", "path": "/"})
                print("🌐 GitHub Pages site created")
                time.sleep(3)  # Wait for initial build
            except GithubException as e:
                print(f"⚠️  Pages setup might be delayed: {str(e)}")

            pages_url = f"https://{self.user.login}.github.io/{repo_name}"
            commit_sha = repo.get_commits()[0].sha

            return {
                'success': True,
                'repo_url': repo.html_url,
                'pages_url': pages_url,
                'commit_sha': commit_sha
            }

        except GithubException as e:
            error_msg = f"GitHub API error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}

    def update_repository(self, task_id, brief, email):
        """Update an existing repository"""
        try:
            repo_name = f"llm-app-{task_id}".lower().replace('_', '-')
            repo = self.user.get_repo(repo_name)
            print(f"📁 Found existing repository: {repo.html_url}")

            # Generate updated app
            updated_files = AppGenerator.generate_app(brief)
            commit_message = f"Round 2 update: {brief[:50]}..."

            for filename, content in updated_files.items():
                try:
                    # Update existing file
                    file_contents = repo.get_contents(filename)
                    repo.update_file(filename, commit_message, content, file_contents.sha)
                    print(f"📝 Updated file: {filename}")
                except GithubException:
                    # Create new file
                    repo.create_file(filename, commit_message, content)
                    print(f"📁 Created file: {filename}")

            commit_sha = repo.get_commits()[0].sha
            pages_url = f"https://{self.user.login}.github.io/{repo_name}"

            return {
                'success': True,
                'repo_url': repo.html_url,
                'pages_url': pages_url,
                'commit_sha': commit_sha
            }

        except GithubException as e:
            return {'success': False, 'error': f"GitHub error: {str(e)}"}


class NotificationManager:
    """Handles evaluation notifications with retry logic"""
    
    @staticmethod
    def send_evaluation_notification(evaluation_url, data, max_retries=5):
        """Send notification with exponential backoff"""
        for attempt in range(max_retries):
            try:
                print(f"📤 Attempt {attempt + 1} to notify evaluation URL...")
                
                response = requests.post(
                    evaluation_url,
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print("✅ Successfully notified evaluation URL")
                    return True
                else:
                    print(f"⚠️  Evaluation URL returned status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Request failed (attempt {attempt + 1}): {str(e)}")
            
            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        print("❌ Failed to notify evaluation URL after all retries")
        return False


def process_deployment(data):
    """Process deployment in background thread"""
    task_id = data.get('task', 'unknown')
    round_number = data.get('round', 1)
    
    try:
        print(f"🚀 Starting deployment for task: {task_id}, round: {round_number}")
        print(f"📝 Brief: {data['brief']}")
        
        # Generate app code
        app_files = AppGenerator.generate_app(data['brief'], data.get('attachments'))
        print("✅ App code generated")
        
        # Deploy to GitHub
        github_manager = GitHubManager()
        
        if round_number == 1:
            github_result = github_manager.create_repository(task_id, app_files, data['email'])
        else:
            github_result = github_manager.update_repository(task_id, data['brief'], data['email'])
        
        if github_result['success']:
            # Store deployment info
            deployments[task_id] = {
                'status': 'completed',
                'round': round_number,
                'github_result': github_result,
                'timestamp': datetime.now().isoformat()
            }
            
            # Send evaluation notification
            evaluation_data = {
                'email': data['email'],
                'task': data['task'],
                'round': data['round'],
                'nonce': data['nonce'],
                'repo_url': github_result['repo_url'],
                'commit_sha': github_result['commit_sha'],
                'pages_url': github_result['pages_url']
            }
            
            if data.get('evaluation_url'):
                print(f"📤 Sending evaluation notification to: {data['evaluation_url']}")
                NotificationManager.send_evaluation_notification(data['evaluation_url'], evaluation_data)
            else:
                print("ℹ️  No evaluation URL provided, skipping notification")
            
            print(f"✅ Deployment completed successfully!")
            print(f"🔗 Repository: {github_result['repo_url']}")
            print(f"🌐 Live URL: {github_result['pages_url']}")
            
        else:
            deployments[task_id] = {
                'status': 'failed',
                'round': round_number,
                'error': github_result.get('error', 'Unknown error'),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ Deployment failed: {github_result.get('error')}")
            
    except Exception as e:
        error_msg = f"Deployment failed: {str(e)}"
        print(f"❌ {error_msg}")
        deployments[task_id] = {
            'status': 'failed',
            'round': round_number,
            'error': error_msg,
            'timestamp': datetime.now().isoformat()
        }


# Flask Routes
@app.route('/', methods=['POST'])
def handle_deployment():
    """Main deployment endpoint"""
    try:
        data = request.json
        print(f"📥 Received deployment request: {data.get('task')}")
        
        # Verify secret
        if data.get('secret') != APP_SECRET:
            return jsonify({'error': 'Invalid secret'}), 401
        
        # Send immediate response
        response = {
            'status': 'accepted',
            'message': 'Deployment request received and processing',
            'task': data.get('task'),
            'round': data.get('round', 1),
            'timestamp': datetime.now().isoformat()
        }
        
        # Process in background
        thread = threading.Thread(target=process_deployment, args=(data,))
        thread.daemon = True
        thread.start()
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """Check deployment status"""
    deployment = deployments.get(task_id)
    if deployment:
        return jsonify(deployment)
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'github_configured': bool(GITHUB_TOKEN)
    })


@app.route('/')
def home():
    """Home page with documentation"""
    return jsonify({
        'message': 'LLM Code Deployment API',
        'endpoints': {
            'POST /': 'Submit deployment request',
            'GET /status/<task_id>': 'Check deployment status',
            'GET /health': 'Health check'
        },
        'github_configured': bool(GITHUB_TOKEN)
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("🚀 Starting LLM Deployment API...")
    print(f"🔑 GitHub Token: {'✅ Configured' if GITHUB_TOKEN else '❌ Not configured'}")
    print(f"🌐 Server running on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)