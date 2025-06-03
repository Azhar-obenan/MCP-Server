import pandas as pd
import flask
from flask import Flask, request, jsonify, render_template_string
import json
import os
import sys
from a2a_customer_support import run_a2a_system

app = Flask(__name__)

# HTML template for the MCP interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>A2A Customer Support MCP Interface</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
            padding: 15px;
            margin-bottom: 15px;
            border-left: 5px solid #3498db;
        }
        .card.high {
            border-left-color: #e74c3c;
        }
        .card.medium {
            border-left-color: #f39c12;
        }
        .card.low {
            border-left-color: #2ecc71;
        }
        .status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        .status.open {
            background-color: #3498db;
        }
        .status.progress {
            background-color: #f39c12;
        }
        .status.resolved {
            background-color: #2ecc71;
        }
        .status.closed {
            background-color: #95a5a6;
        }
        .filters {
            margin-bottom: 20px;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 8px;
        }
        select, button {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
        }
        button:hover {
            background-color: #2980b9;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .stat-box {
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
            padding: 15px;
            width: 23%;
            text-align: center;
        }
        .stat-box h3 {
            margin-top: 0;
            color: #7f8c8d;
        }
        .stat-box p {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        #ticketCount {
            color: #3498db;
        }
        #highPriorityCount {
            color: #e74c3c;
        }
        #openCount {
            color: #f39c12;
        }
        #resolvedCount {
            color: #2ecc71;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>A2A Customer Support MCP Interface</h1>
        
        <div class="stats">
            <div class="stat-box">
                <h3>Total Tickets</h3>
                <p id="ticketCount">0</p>
            </div>
            <div class="stat-box">
                <h3>High Priority</h3>
                <p id="highPriorityCount">0</p>
            </div>
            <div class="stat-box">
                <h3>Open Tickets</h3>
                <p id="openCount">0</p>
            </div>
            <div class="stat-box">
                <h3>Resolved</h3>
                <p id="resolvedCount">0</p>
            </div>
        </div>
        
        <div class="filters">
            <select id="priorityFilter">
                <option value="all">All Priorities</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
            </select>
            
            <select id="statusFilter">
                <option value="all">All Statuses</option>
                <option value="Open">Open</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
            </select>
            
            <select id="categoryFilter">
                <option value="all">All Categories</option>
                <option value="Technical">Technical</option>
                <option value="Billing">Billing</option>
                <option value="Account">Account</option>
                <option value="Product">Product</option>
                <option value="General">General</option>
            </select>
            
            <button id="applyFilters">Apply Filters</button>
            <button id="resetFilters">Reset</button>
            <button id="refreshData">Refresh Data</button>
        </div>
        
        <div id="ticketsContainer">
            <!-- Tickets will be dynamically added here -->
            <p>Loading tickets...</p>
        </div>
    </div>

    <script>
        // Global variable to store all tickets data
        let allTickets = [];
        
        // Function to fetch ticket data from the API
        async function fetchTicketData() {
            try {
                const response = await fetch('/api/tickets');
                const data = await response.json();
                allTickets = data;
                updateStats(data);
                displayTickets(data);
            } catch (error) {
                console.error('Error fetching ticket data:', error);
                document.getElementById('ticketsContainer').innerHTML = '<p>Error loading ticket data. Please try again.</p>';
            }
        }
        
        // Function to update stats counters
        function updateStats(tickets) {
            document.getElementById('ticketCount').textContent = tickets.length;
            document.getElementById('highPriorityCount').textContent = tickets.filter(t => t.Priority === 'High').length;
            document.getElementById('openCount').textContent = tickets.filter(t => t.Status === 'Open').length;
            document.getElementById('resolvedCount').textContent = tickets.filter(t => t.Status === 'Resolved').length;
        }
        
        // Function to display tickets in the container
        function displayTickets(tickets) {
            const container = document.getElementById('ticketsContainer');
            
            if (tickets.length === 0) {
                container.innerHTML = '<p>No tickets match the current filters.</p>';
                return;
            }
            
            let html = '';
            tickets.forEach(ticket => {
                let statusClass = '';
                if (ticket.Status === 'Open') statusClass = 'open';
                else if (ticket.Status === 'In Progress') statusClass = 'progress';
                else if (ticket.Status === 'Resolved') statusClass = 'resolved';
                else if (ticket.Status === 'Closed') statusClass = 'closed';
                
                html += `
                    <div class="card ${ticket.Priority.toLowerCase()}">
                        <h3>${ticket['Ticket ID']} - ${ticket['Customer Name']}</h3>
                        <p><strong>Email:</strong> ${ticket.Email}</p>
                        <p><strong>Issue:</strong> ${ticket['Issue Description']}</p>
                        <p>
                            <span class="status ${statusClass}">${ticket.Status}</span>
                            <strong>Priority:</strong> ${ticket.Priority} | 
                            <strong>Category:</strong> ${ticket.Category} | 
                            <strong>Created:</strong> ${ticket['Created At']}
                        </p>
                        <p><strong>Suggested Response:</strong> ${ticket['Suggested Response']}</p>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        // Function to apply filters to ticket data
        function applyFilters() {
            const priorityFilter = document.getElementById('priorityFilter').value;
            const statusFilter = document.getElementById('statusFilter').value;
            const categoryFilter = document.getElementById('categoryFilter').value;
            
            let filteredTickets = [...allTickets];
            
            if (priorityFilter !== 'all') {
                filteredTickets = filteredTickets.filter(ticket => ticket.Priority === priorityFilter);
            }
            
            if (statusFilter !== 'all') {
                filteredTickets = filteredTickets.filter(ticket => ticket.Status === statusFilter);
            }
            
            if (categoryFilter !== 'all') {
                filteredTickets = filteredTickets.filter(ticket => ticket.Category === categoryFilter);
            }
            
            updateStats(filteredTickets);
            displayTickets(filteredTickets);
        }
        
        // Attach event listeners after DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            fetchTicketData();
            
            document.getElementById('applyFilters').addEventListener('click', applyFilters);
            
            document.getElementById('resetFilters').addEventListener('click', () => {
                document.getElementById('priorityFilter').value = 'all';
                document.getElementById('statusFilter').value = 'all';
                document.getElementById('categoryFilter').value = 'all';
                updateStats(allTickets);
                displayTickets(allTickets);
            });
            
            document.getElementById('refreshData').addEventListener('click', fetchTicketData);
        });
    </script>
</body>
</html>
"""

# Route for the main MCP interface
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# API route to get ticket data
@app.route('/api/tickets')
def get_tickets():
    try:
        # Read processed data CSV file
        df = pd.read_csv('processed_customer_data.csv')
        # Convert to list of dictionaries for JSON response
        tickets = df.to_dict('records')
        return jsonify(tickets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to process data (runs A2A system on demand)
@app.route('/api/process', methods=['POST'])
def process_data():
    try:
        csv_path = request.json.get('csv_path', 'customer_support_data.csv')
        # Run the A2A system
        result = run_a2a_system(csv_path)
        return jsonify({"message": f"Processed {len(result)} tickets successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to start the MCP server
def start_mcp_server(host='127.0.0.1', port=5000, debug=True):
    print(f"🌐 Starting A2A MCP Server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    # Check if processed data exists, if not process it
    if not os.path.exists('processed_customer_data.csv'):
        print("🔄 Processed data not found. Running A2A system first...")
        run_a2a_system('customer_support_data.csv')
    
    # Start the MCP server
    start_mcp_server()
