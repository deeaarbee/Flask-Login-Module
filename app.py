from flask import Flask,session,jsonify,url_for,redirect,request
from users import main as user

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))

@app.route("/login",methods=['POST'])
def loginMain():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        token = user.login(data['username'],data['password'])
        print(token)
        if token:
            dict = {"token" : token}
            print("login was successful")
            session['loggedIn'] = True
            session['token'] = token
            session['username'] = data['username']
            return jsonify({"token" : token, "status" : "login successful"})
        else:
            return jsonify({"status" : "login failed", "reason":"invalid credentials"})


@app.route("/register",methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    check = user.registerUser(data['username'],data['email'],data['mobile'],data['password'])
    if check == 1:
        token = user.login(data['username'],data['password'])
        session['token'] = token
        return jsonify({"token" : token})
    elif check== -1:
        return jsonify({"status" : "registration failed", "reason" : "credentials are already taken"})
    else:
        return jsonify({"status" : "registration failed"})


@app.route("/logout",methods=['POST'])
def logoutMain():
    if "loggedIn" in session.keys():
        session['loggedIn'] = False
    data = request.get_json()
    check = user.logout(data['token'])
    if check==1:
        session.clear()
        return jsonify({"status" : "successfully logged out"})
    else:
        return jsonify({"status" : "something fishy"})


if __name__ == '__main__':
    app.run(debug=True)
