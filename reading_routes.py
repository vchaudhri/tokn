from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.logic.decorators import login_required
from wrst.forms.reading_forms import ReadingForm
import time
from wrst.logic.experiment import task_queue

reading_routes = Blueprint('reading_routes', __name__)

# TODO: Make reading link dynamic based on cohort
@reading_routes.route('/display_reading_instructions', methods=['GET', 'POST'])
@login_required
def display_reading_instructions():

    total_reading_time = session['required_reading_time']
    total_reading_time = 5


    # Load the form
    form = ReadingForm(request.form)
    reading_link = session["reading_link"]
#    header = "First, you are going to read a brief section from an introductory Biology textbook"
    header = "First please read chapter 48 of the LIFE textbook."
    content_items = Markup(
        """<p>Please ensure that you have read the Chapter 48 of the LIFE textbook and understand its content 
        thoroughly as you 
        will be presented sentences from this chapter.<br></p>
        """
    )
    content = Markup(header)

    if not form.validate_on_submit():

        if not session.get('reading_start_time'):
            session['reading_start_time'] = time.time()

        current_time_reading = time.time() - session['reading_start_time']

        return render_template('reading_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               reading_link=reading_link,
                               num=total_reading_time-current_time_reading)
    if request.method == 'POST':

        # Verify that the user has spent the required reading time
        # If so, they can pass on
        current_time_reading = time.time() - session['reading_start_time']
        if (current_time_reading>=total_reading_time):
            return redirect(url_for('instruction_routes.generic_reroute'))
        else:
            flash("You need to spend at least ten minutes reading before moving on to the next activity!")
            return redirect(url_for('reading_routes.display_reading_instructions')
                            )
        # Else, flash a message and re-render the page
