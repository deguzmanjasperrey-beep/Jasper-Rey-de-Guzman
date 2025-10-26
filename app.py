@app.route('/student/profile')
def get_student_profile():
    return jsonify({
        "name": "Jasper Rey de Guzman",
        "grade": 10,
        "section": "Zechariah",
        "height": "5'7\"",
        "weight": "65 kg"
    })
