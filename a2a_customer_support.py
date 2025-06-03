import csv
import pandas as pd
import re
import time
from datetime import datetime

# Agent class - Base class for all agents
class Agent:
    def __init__(self, name):
        self.name = name
        
    def process(self, data):
        # Base processing method to be overridden by subclasses
        pass
    
    def communicate(self, target_agent, message):
        print(f"🔄 {self.name} → {target_agent.name}: Sending data")
        return target_agent.process(message)

# Reader Agent - Reads and loads the customer data
class ReaderAgent(Agent):
    def __init__(self):
        super().__init__("Reader Agent")
    
    def process(self, csv_path):
        print(f"📂 {self.name}: Loading customer data from {csv_path}")
        try:
            # Read CSV file
            df = pd.read_csv(csv_path)
            print(f"✅ {self.name}: Successfully loaded {len(df)} records")
            return df
        except Exception as e:
            print(f"❌ {self.name}: Error loading data - {str(e)}")
            return None

# Analyzer Agent - Analyzes and categorizes customer issues
class AnalyzerAgent(Agent):
    def __init__(self):
        super().__init__("Analyzer Agent")
        # Define issue categories and their keywords
        self.categories = {
            "Technical": ["error", "bug", "broken", "failed", "crash", "technical"],
            "Billing": ["payment", "charge", "bill", "refund", "price", "cost", "money"],
            "Account": ["login", "password", "account", "profile", "access", "sign"],
            "Product": ["feature", "product", "service", "quality", "performance"],
            "Shipping": ["delivery", "shipping", "ship", "package", "track", "arrive"],
            "General": []  # Default category
        }
    
    def process(self, data):
        print(f"🔍 {self.name}: Analyzing {len(data)} customer issues")
        # Add a category column
        data['Category'] = data['Issue Description'].apply(self.categorize_issue)
        print(f"✅ {self.name}: Categorized all issues")
        return data
    
    def categorize_issue(self, issue_text):
        issue_lower = issue_text.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in issue_lower:
                    return category
        
        return "General"  # Default category

# Prioritizer Agent - Prioritizes tickets based on various factors
class PrioritizerAgent(Agent):
    def __init__(self):
        super().__init__("Prioritizer Agent")
    
    def process(self, data):
        print(f"⚖️ {self.name}: Prioritizing {len(data)} tickets")
        
        # Calculate time since creation
        current_time = datetime.now()
        data['Created At'] = pd.to_datetime(data['Created At'])
        data['Days Open'] = (current_time - data['Created At']).dt.total_seconds() / (24 * 3600)
        
        # Priority scoring system
        def calculate_priority(row):
            score = 0
            
            # Status factor
            if row['Status'] == 'Open':
                score += 3
            elif row['Status'] == 'In Progress':
                score += 2
            
            # Time factor - older tickets get higher priority
            score += min(row['Days Open'] * 0.5, 5)  # Cap at 5 points
            
            # Category factor
            if row['Category'] == 'Technical':
                score += 2
            elif row['Category'] == 'Billing':
                score += 3
            
            return score
        
        data['Priority Score'] = data.apply(calculate_priority, axis=1)
        data['Priority'] = pd.qcut(data['Priority Score'], 
                                 q=3, 
                                 labels=['Low', 'Medium', 'High'])
        
        print(f"✅ {self.name}: Assigned priority to all tickets")
        return data

# Response Agent - Generates appropriate responses
class ResponseAgent(Agent):
    def __init__(self):
        super().__init__("Response Agent")
        # Template responses for different categories
        self.templates = {
            "Technical": [
                "Our technical team is looking into the issue you reported. We'll update you as soon as we have more information.",
                "We apologize for the technical difficulties. Our engineers are working on a fix.",
                "Thank you for reporting this technical issue. We're investigating and will get back to you shortly."
            ],
            "Billing": [
                "Our billing department is reviewing your payment concern and will reach out with a resolution.",
                "We've noted your billing query and are processing it with priority.",
                "Thank you for bringing this billing matter to our attention. We'll resolve it as quickly as possible."
            ],
            "Account": [
                "We're addressing your account-related concern and will ensure everything is working correctly.",
                "Our account specialists are looking into this issue and will help you regain access.",
                "We understand the importance of account security and are working to resolve your issue."
            ],
            "Product": [
                "Thank you for your feedback about our product. We're taking your suggestions into consideration.",
                "We appreciate your insights about our service and will use them to improve.",
                "Your product experience matters to us. We're addressing the points you've raised."
            ],
            "Shipping": [
                "We're tracking your shipment and will update you on its status.",
                "Our shipping department is looking into the delivery issue you reported.",
                "We apologize for any shipping inconvenience and are working to resolve it quickly."
            ],
            "General": [
                "Thank you for contacting our support team. We're reviewing your inquiry.",
                "We appreciate you reaching out to us. Our team is working on addressing your concern.",
                "We've received your message and are working on the best solution for you."
            ]
        }
    
    def process(self, data):
        print(f"✍️ {self.name}: Generating responses for {len(data)} tickets")
        
        import random
        data['Suggested Response'] = data['Category'].apply(
            lambda cat: random.choice(self.templates.get(cat, self.templates['General']))
        )
        
        print(f"✅ {self.name}: Generated responses for all tickets")
        return data

# Orchestrator Agent - Coordinates the entire A2A system
class OrchestratorAgent(Agent):
    def __init__(self):
        super().__init__("Orchestrator Agent")
        self.reader = ReaderAgent()
        self.analyzer = AnalyzerAgent()
        self.prioritizer = PrioritizerAgent()
        self.responder = ResponseAgent()
    
    def process(self, csv_path):
        print(f"🚀 {self.name}: Starting A2A process for {csv_path}")
        
        # Step 1: Read data
        data = self.communicate(self.reader, csv_path)
        if data is None:
            return "Process failed at data reading stage"
        
        # Step 2: Analyze issues
        data = self.communicate(self.analyzer, data)
        
        # Step 3: Prioritize tickets
        data = self.communicate(self.prioritizer, data)
        
        # Step 4: Generate responses
        data = self.communicate(self.responder, data)
        
        print(f"🏁 {self.name}: A2A process completed successfully")
        return data
    
    def summarize_results(self, processed_data):
        # Create summary statistics
        category_counts = processed_data['Category'].value_counts()
        priority_counts = processed_data['Priority'].value_counts()
        status_counts = processed_data['Status'].value_counts()
        
        print("\n===== SUMMARY REPORT =====")
        print("\nCategories:")
        for category, count in category_counts.items():
            print(f"  - {category}: {count} tickets")
        
        print("\nPriorities:")
        for priority, count in priority_counts.items():
            print(f"  - {priority}: {count} tickets")
        
        print("\nStatuses:")
        for status, count in status_counts.items():
            print(f"  - {status}: {count} tickets")
        
        # Save processed data
        processed_data.to_csv('processed_customer_data.csv', index=False)
        print("\nProcessed data saved to 'processed_customer_data.csv'")

# Main function to run the A2A system
def run_a2a_system(csv_path):
    print("🤖 Starting A2A Customer Support System")
    orchestrator = OrchestratorAgent()
    
    # Process the data through the A2A system
    processed_data = orchestrator.process(csv_path)
    
    # Display summary of results
    orchestrator.summarize_results(processed_data)
    
    return processed_data

# If run directly
if __name__ == "__main__":
    csv_path = 'customer_support_data.csv'
    result = run_a2a_system(csv_path)
    
    # Show a sample of processed tickets
    print("\n===== SAMPLE PROCESSED TICKETS =====")
    sample = result.sample(min(5, len(result)))
    
    for _, ticket in sample.iterrows():
        print("\n" + "="*50)
        print(f"Ticket: {ticket['Ticket ID']}")
        print(f"Customer: {ticket['Customer Name']} ({ticket['Email']})")
        print(f"Status: {ticket['Status']} | Priority: {ticket['Priority']} | Category: {ticket['Category']}")
        print(f"Issue: {ticket['Issue Description']}")
        print(f"Suggested Response: {ticket['Suggested Response']}")
