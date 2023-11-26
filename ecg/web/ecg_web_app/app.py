import sys
sys.path.append('D:\Semester 6\Heart-Disease-Prediction-from-ECG-through-Image--Processing\Ecg.py')

from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
from Ecg import  ECG

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(filepath)

            # Create an instance of the ECG class
            ecg_processor = ECG()

            # Instead of getImage(), use the uploaded file
            # image_path = ecg_processor.getImage()

            # Process the uploaded ECG image
            # You may need to adjust the methods of ECG class to accept the filepath directly
            ecg_processor.displayImage(filepath)
            gray_image = ecg_processor.GrayImgae(filepath)
            leads = ecg_processor.DividingLeads(filepath)
            ecg_processor.PreprocessingLeads(leads)
            ecg_processor.SignalExtraction_Scaling(leads)
            final_data = ecg_processor.CombineConvert1Dsignal()
            reduced_data = ecg_processor.DimensionalReduciton(final_data)
            classification_result = ecg_processor.ModelLoad_predict(reduced_data)

            # You would need to implement the logic to gather image file names for rendering
            # images = ['list_of_processed_image_filenames']

            # Render the results template with the classification result and images
            return render_template('result.html', result=classification_result, images=images)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
