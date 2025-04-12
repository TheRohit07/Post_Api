from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage for submissions
Data = []

class Submission:
    def __init__(self, category_id, latitude, longitude):
        # Default/static fields
        self.id = len(Data) + 1
        self.platform = 'ios'
        self.customer_id = '0'
        self.config = 'dark_stores-config-1'
        self.include_component_types = ['multi_list']
        self.is_darkstore = True
        self.language_code = 'en'
        self.vendor_id = 'a67ba893-443c-41b6-ba70-fc35a9b2f9f3'
        self.include_fields = ['feed']
        self.page_name = 'default_page'
        self.brand = 'hungerstation'
        self.country_code = 'sa'
        
        # Dynamic fields
        self.category_id = category_id
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "id": self.id,
            "platform": self.platform,
            "customer_id": self.customer_id,
            "config": self.config,
            "category_id": self.category_id,
            "location": {
                "point": {
                    "latitude": self.latitude,
                    "longitude": self.longitude
                }
            },
            "include_component_types": self.include_component_types,
            "is_darkstore": self.is_darkstore,
            "language_code": self.language_code,
            "vendor_id": self.vendor_id,
            "include_fields": self.include_fields,
            "page_name": self.page_name,
            "brand": self.brand,
            "country_code": self.country_code
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/get')
def get_data():
    return jsonify([submission.to_dict() for submission in Data])

@app.route('/create', methods=['POST'])
def submit_data():
    data = request.get_json()

    # Validate the dynamic input fields
    try:
        category_id = data.get('category_id')
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'error': 'latitude and longitude must be numbers'}), 400

    # Check if required fields exist
    if not category_id:
        return jsonify({'error': 'category_id is required'}), 400

    # Validate Latitude and Longitude ranges
    if not (-90 <= latitude <= 90):
        return jsonify({'error': 'latitude must be between -90 and 90'}), 400
    if not (-180 <= longitude <= 180):
        return jsonify({'error': 'longitude must be between -180 and 180'}), 400

    # Clear previous submissions
    Data.clear()
    
    # Create a new Submission record
    new_submission = Submission(category_id, latitude, longitude)
    Data.append(new_submission)

    return jsonify({
        "message": "Data received successfully",
        "data": new_submission.to_dict()
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=9000)
