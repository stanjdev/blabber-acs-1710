import os
from flask import Flask
from views import routes

app = Flask(__name__)
app.register_blueprint(routes)






# """ CHARITIES ROUTES """

# # GET ALL Charities /charities
# @app.route('/charities')
# def charities_all():
#   return render_template('charities_all.html', charities=charities.find())


# # GET SHOW one Charity profile page
# # GET — /charities:/charity_name — SHOW one charity {k: v}
# @app.route('/charities/<charity_name>')
# def charity_profile(charity_name):
#   charity = charities.find_one({'name': charity_name})
#   return render_template('charity.html', charity=charity, donations=donations.find({'charity_name': charity_name}))

# # # POST - /charities create a new charity when a new one is entered in the donation form
# # ADDING A NEW DONATION CREATES ONE ALREADY.


# # GET - EDIT form for charity
# @app.route('/charities/<charity_name>/edit')
# def charity_edit_form(charity_name):
#   charity = charities.find_one({'name': charity_name})
#   # get the charity object with the info to put in 'value' in each input
#   return render_template('charity_edit_form.html', charity=charity)


# # PUT/PATCH - UPDATE charity information
# @app.route('/charities/<charity_name>', methods=['POST'])
# def charities_update(charity_name):
#   updated_charity = {
#     'name': request.form.get('charity_name'),
#     'category': request.form.get('charity_category'),
#     'about': request.form.get('about_charity')
#   }
#   charities.update_one(
#     {'name': charity_name},
#     {'$set': updated_charity}
#   )
#   return redirect(url_for('charity_profile', charity_name=updated_charity['name']))


# # DELETE a charity
# @app.route('/charities/<charity_name>/delete')
# def charity_delete(charity_name):
#   print(charity_name)
#   charities.delete_one({'name': charity_name})
#   return redirect(url_for('charities_all'))




if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

