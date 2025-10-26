from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample student data
students = [
    {
        "id": 1,
        "name": "Jasper Rey",
        "grade": BSIT3,
        "section": "Stallman",
        "age": 15,
        "height": 165,  # in cm
        "weight": 55    # in kg
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Information System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 20px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }

        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }

        .info-row:last-child {
            border-bottom: none;
        }

        .label {
            font-weight: 600;
            color: #555;
        }

        .value {
            color: #333;
            font-weight: 500;
        }

        .form-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .cards-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 Student Information System</h1>
            <p class="subtitle">Manage and view student records</p>
        </header>

        <div id="studentsContainer" class="cards-container"></div>

        <div class="form-card">
            <h2 style="color: #667eea; margin-bottom: 20px;">Add New Student</h2>
            <form id="studentForm">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" required>
                </div>
                <div class="form-group">
                    <label for="grade">Grade</label>
                    <input type="number" id="grade" required>
                </div>
                <div class="form-group">
                    <label for="section">Section</label>
                    <input type="text" id="section" required>
                </div>
                <div class="form-group">
                    <label for="age">Age (years)</label>
                    <input type="number" id="age" required>
                </div>
                <div class="form-group">
                    <label for="height">Height (cm)</label>
                    <input type="number" id="height" required>
                </div>
                <div class="form-group">
                    <label for="weight">Weight (kg)</label>
                    <input type="number" id="weight" required>
                </div>
                <button type="submit" class="btn">Add Student</button>
            </form>
        </div>
    </div>

    <script>
        function calculateBMI(weight, height) {
            const heightInMeters = height / 100;
            return (weight / (heightInMeters * heightInMeters)).toFixed(1);
        }

        function getBMICategory(bmi) {
            if (bmi < 18.5) return 'Underweight';
            if (bmi < 25) return 'Normal';
            if (bmi < 30) return 'Overweight';
            return 'Obese';
        }

        function loadStudents() {
            fetch('/api/students')
                .then(response => response.json())
                .then(students => {
                    const container = document.getElementById('studentsContainer');
                    container.innerHTML = students.map(student => {
                        const bmi = calculateBMI(student.weight, student.height);
                        const bmiCategory = getBMICategory(bmi);
                        
                        return `
                            <div class="card">
                                <h2>${student.name}</h2>
                                <div class="info-row">
                                    <span class="label">Grade:</span>
                                    <span class="value">${student.grade}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Section:</span>
                                    <span class="value">${student.section}</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Age:</span>
                                    <span class="value">${student.age} years</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Height:</span>
                                    <span class="value">${student.height} cm</span>
                                </div>
                                <div class="info-row">
                                    <span class="label">Weight:</span>
                                    <span class="value">${student.weight} kg</span>
                                </div>
                                <div class="stats-grid">
                                    <div class="stat-box">
                                        <div class="stat-value">${bmi}</div>
                                        <div class="stat-label">BMI</div>
                                    </div>
                                    <div class="stat-box">
                                        <div class="stat-value" style="font-size: 1.2em;">${bmiCategory}</div>
                                        <div class="stat-label">Category</div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('');
                });
        }

        document.getElementById('studentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const student = {
                name: document.getElementById('name').value,
                grade: parseInt(document.getElementById('grade').value),
                section: document.getElementById('section').value,
                age: parseInt(document.getElementById('age').value),
                height: parseInt(document.getElementById('height').value),
                weight: parseInt(document.getElementById('weight').value)
            };

            fetch('/api/students', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(student)
            })
            .then(response => response.json())
            .then(data => {
                alert('Student added successfully!');
                this.reset();
                loadStudents();
            })
            .catch(error => {
                alert('Error adding student: ' + error);
            });
        });

        // Load students on page load
        loadStudents();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/student')
def get_student():
    return jsonify(students[0] if students else {})

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = {
        "id": len(students) + 1,
        "name": data.get('name'),
        "grade": data.get('grade'),
        "section": data.get('section'),
        "age": data.get('age'),
        "height": data.get('height'),
        "weight": data.get('weight')
    }
    students.append(new_student)
    return jsonify(new_student), 201

if __name__ == '__main__':
    app.run(debug=True)
