from flask import Flask, render_template, request, jsonify
from flask import session as web_session
from akkadian import *
from ..hammurabi.us.fed.tax.indiv import withholding as withholding


app = Flask(__name__)

#keep it secret, keep it safe
#generated by secrets.token_hex() function from secrets module
app.secret_key = '5555bf3986fa767556a744c5123afbaf8807a012b0fa45260a6fd18c919d648e'


goal = withholding.form_w4_complete

# set FLASK_APP=interview.py
@app.route("/")
def investigate_goal():
    web_session['factSet'] = []
    # return render_template('main_interview.html')
    # return Investigate([(form_w4_complete, "Hub", "Wife")])
    return web_apply_rules([(goal, "Hub", "Wife")])
   

@app.route('/', methods=['POST'])
def call_on_form_post():
    answer = request.form['answer']
    
    # print(answer)
    print(web_session.get('queued_attr'))
    #add user input and attribute to fact set
    fs = web_session['factSet']
    attr = web_session['queued_attr']
    
    fs.append(Fact(attr[1], attr[2], attr[3], convert_input(attr[0], answer)))
   
    print("Fact Set:")
    for f in fs:
        print(f)
    web_apply_rules(goal, fs)
    return answer


def web_apply_rules(goals: list, fs=[]):
    #for debugging
    # return jsonify(ApplyRules(goals, fs))
    
    # Call the "apply rules" interface
    results = ApplyRules(goals, fs)

    # If all of the goals have been determined, present the results
    if results["complete"]:
        return results["msg"]  # TODO

    # Otherwise, ask the next question...
    else:
        # Find out what the next question is
        nxt = results["missing_info"][0]

        # Ask it
        return collect_input(nxt)
        # new = collect_input(nxt)

        # Add the newly acquired fact to the fact list
        # fs.append(Fact(attr[1], attr[2], attr[3], convert_input(attr[0], new)))

        # Go to step 1
        # return web_apply_rules(goals, fs)

def collect_input(attr):
    
    #store attribute in session so we know which question was being answered by the user
    web_session["queued_attr"] = attr

    type = attr[0]
    public_name = attr[1]
    subject = attr[2]
    obj = attr[3]
    question = attr[4]

    if(attr[0] == "bool"):
        return render_template('main_interview.html', type=type, question=question)

    #for debugging
    return jsonify(attr)
