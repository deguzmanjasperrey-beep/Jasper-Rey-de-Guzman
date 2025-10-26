from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Jasper Rey de Guzman",
        "grade": bsit3,
        "section": "Stallman",
        "height": 165,  # in cm
        "weight": 55    # in kg
    })

@app.route('/student/<name>')
def get_student_details(name):
    # Sample student data
    students = {
        "jasper": {
            "name": "Jasper Rey de Guzman",
            "grade": bsit3,
            "section": "Stallman",
            "height": 165,  # in cm
            "weight": 55    # in kg
        },
        "maria": {
            "name": "jedidiah defacto",
            "grade": bsit3,
            "section": "Stallman",
            "height": 158,
            "weight": 50
        }
    }
    
    student = students.get(name.lower())
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
