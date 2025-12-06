from flask import Flask, render_template, request, redirect, url_for, flash
@app.route('/predict', methods=['POST'])
def predict():
# Two input methods supported:
# 1) comma-separated numbers in textarea named 'features'
# 2) JSON-like single-line in textarea
raw = request.form.get('features', '')


if not raw:
flash('Please provide feature values (comma-separated).')
return redirect(url_for('index'))


# try parse comma separated
try:
# Accept both newline or comma separated values
parts = [p for line in raw.splitlines() for p in line.replace(';',',').split(',')]
parts = [p.strip() for p in parts if p.strip() != '']
feature_list = [float(x) for x in parts]
except Exception as e:
flash('Could not parse input. Please enter numbers separated by commas (e.g. 12.3, 45, 6).')
return redirect(url_for('index'))


try:
pred, prob = predict_from_list(feature_list)
except Exception as e:
flash(f'Prediction failed: {e}')
return redirect(url_for('index'))


# format outputs
prediction = pred[0]
probability = None
if prob is not None:
# if multiclass, show all; else show single probability for predicted class
try:
if prob.shape[1] == 1:
probability = float(prob[0,0])
else:
# probability of predicted class
probability = float(prob[0, int(prediction)])
except Exception:
probability = None


return render_template('result.html', prediction=prediction, probability=probability, features=feature_list)


if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000, debug=True)