from flask import Flask, render_template, request, redirect, make_response, url_for, flash

app = Flask(__name__)
app.secret_key = "una_clave_secreta_segura"  # Necesario para mensajes flash


@app.route('/')
def index():
    # Verificar si el usuario ha dado consentimiento sobre cookies
    cookie_consent = request.cookies.get('cookie_consent')
    return render_template('index.html', cookie_consent=cookie_consent)


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        consent_value = request.form.get('consent')
        response = make_response(redirect(url_for('index')))
        if consent_value == 'accept':
            response.set_cookie("cookie_consent", 'accepted', max_age=365*24*60*60)  # Cookie por 1 año
        elif consent_value == 'reject':
            response.set_cookie('cookie_consent', 'rejected', max_age=365*24*60*60)
        flash('Tus preferencias han sido guardadas.')
        return response
    return render_template('consent.html')


@app.route('/change_consent', methods=['POST'])
def change_consent():
    # Eliminar la cookie de consentimiento para que el banner aparezca nuevamente
    response = make_response(redirect('/'))
    response.delete_cookie('cookie_consent')  # Eliminar la cookie de consentimiento
    return response


@app.route('/policy')
def policy():
    return render_template('policy.html')


if __name__ == '__main__':
    app.run(debug=True)
