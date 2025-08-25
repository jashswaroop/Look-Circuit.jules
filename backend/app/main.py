from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .analysis import detect_face_shape, analyze_skin_tone
from .models import UserImage
from .scraper import scrape_myntra
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

from .forms import UpdateProfileForm, StyleGuideForm
from . import db
import json

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.height = form.height.data
        current_user.body_shape = form.body_shape.data
        current_user.location_climate = form.location_climate.data
        current_user.fashion_style = form.fashion_style.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.age.data = current_user.age
        form.gender.data = current_user.gender
        form.height.data = current_user.height
        form.body_shape.data = current_user.body_shape
        form.location_climate.data = current_user.location_climate
        form.fashion_style.data = current_user.fashion_style
    return render_template('profile.html', title='Profile', form=form)

@main.route('/style_guide', methods=['GET', 'POST'])
@login_required
def style_guide():
    form = StyleGuideForm()
    if form.validate_on_submit():
        guide_data = {
            'fashion_preferences': form.fashion_preferences.data,
            'budget': form.budget.data,
            'lifestyle': form.lifestyle.data,
            'social_activities': form.social_activities.data,
            'fashion_risk_tolerance': form.fashion_risk_tolerance.data,
            'comfort_vs_style': form.comfort_vs_style.data,
            'preferred_colors': form.preferred_colors.data,
            'avoided_colors': form.avoided_colors.data,
            'brand_preferences': form.brand_preferences.data,
            'preferred_stores': form.preferred_stores.data,
        }
        current_user.style_guide_data = json.dumps(guide_data)
        db.session.commit()
        flash('Your Style Guide has been saved!', 'success')
        return redirect(url_for('main.style_guide'))
    elif request.method == 'GET' and current_user.style_guide_data:
        guide_data = json.loads(current_user.style_guide_data)
        form.fashion_preferences.data = guide_data.get('fashion_preferences')
        form.budget.data = guide_data.get('budget')
        form.lifestyle.data = guide_data.get('lifestyle')
        form.social_activities.data = guide_data.get('social_activities')
        form.fashion_risk_tolerance.data = guide_data.get('fashion_risk_tolerance')
        form.comfort_vs_style.data = guide_data.get('comfort_vs_style')
        form.preferred_colors.data = guide_data.get('preferred_colors')
        form.avoided_colors.data = guide_data.get('avoided_colors')
        form.brand_preferences.data = guide_data.get('brand_preferences')
        form.preferred_stores.data = guide_data.get('preferred_stores')

    return render_template('style_guide.html', title='Style Guide', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@main.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Need to get the app context to get the upload folder
            from flask import current_app
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Perform analysis
            face_shape = detect_face_shape(filepath)
            skin_tone = analyze_skin_tone(filepath)

            # Save to database
            image_record = UserImage(
                user_id=current_user.id,
                filename=filename,
                face_shape=face_shape,
                skin_tone=skin_tone,
                analysis_complete=True
            )
            db.session.add(image_record)
            db.session.commit()

            flash('Image analyzed successfully!', 'success')
            return render_template('analysis_result.html', image=image_record)

    return render_template('analysis.html', title='Analyze Photo')

@main.route('/search')
@login_required
def search():
    query = request.args.get('query')
    if not query:
        flash('Please enter a search query.', 'danger')
        return redirect(url_for('main.dashboard'))

    # For PoC, we only scrape Myntra
    products = scrape_myntra(query)

    if not products:
        flash(f'No results found for "{query}" on Myntra.', 'info')

    return render_template('search_results.html', title=f'Search Results for "{query}"', products=products, query=query)
