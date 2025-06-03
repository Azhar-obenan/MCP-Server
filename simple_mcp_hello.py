from flask import Flask, render_template_string

# Create a Flask app (this is the MCP server)
app = Flask(__name__)

# Simple HTML template with Hello World
HELLO_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple MCP Hello World</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f5f5f5;
        }
        .container {
            text-align: center;
            padding: 40px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #3498db;
        }
        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background-color: #2980b9;
        }
        #message {
            margin-top: 20px;
            font-size: 18px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>MCP Hello World</h1>
        <p>This is a simple demonstration of MCP (Model Context Protocol)</p>
        <button id="helloButton">Say Hello</button>
        <div id="message"></div>
        
        <script>
            document.getElementById('helloButton').addEventListener('click', async () => {
                try {
                    // Call the MCP API endpoint
                    const response = await fetch('/api/hello');
                    const data = await response.json();
                    
                    // Display the message
                    document.getElementById('message').textContent = data.message;
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('message').textContent = 'Error: ' + error.message;
                }
            });
        </script>
    </div>
</body>
</html>
"""

# Route for the main page
@app.route('/')
def index():
    return render_template_string(HELLO_TEMPLATE)

# API endpoint that returns a Hello World message
@app.route('/api/hello')
def hello_api():
    return {"message": "Hello World from MCP!"}

# Start the MCP server
if __name__ == "__main__":
    print("🌐 Starting Simple MCP Server on http://127.0.0.1:5001")
    print("🔍 Open this URL in your browser to see the Hello World message")
    app.run(host="127.0.0.1", port=5001, debug=True)
