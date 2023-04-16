# imports
from flask import Flask, jsonify, render_template, request, Response
import database as db
import uuid

# set up applications
app = Flask(__name__, static_folder='static')


project_db = db.Database()

# route for all projects
@app.route('/projects', methods=['GET'])
def list_all_projects():
    # return jsonified list of all project dictionaries
    if request.method == 'GET':
        projects = project_db.get_all_projects()
        return jsonify([project.__dict__ for project in projects])


# route for specific project
@app.route('/project', methods=['GET', 'DELETE', 'PATCH', 'POST'])
def project():
    # get project based on project id if it exists
    if request.method == 'GET':
        project_input = request.json
        project_id = project_input['project_id']
        
        try:
            project = project_db.get_project(project_id)
        except:
            return Response("{'error:':'project not found'}", status=400, mimetype='application/json')
        
        return jsonify(project.__dict__)
    
    # delete project if project id exists
    if request.method == 'DELETE':
        project_input = request.json
        project_id = project_input['project_id']
        
        try:
            project = project_db.get_project(project_id)
        except:
            return Response("{'error:':'project not found'}", status=400, mimetype='application/json')

        project_db.delete_project(project_id)
        return jsonify({'success': True})
    
    # modify project if project id exists
    if request.method == 'PATCH':
        for key in project_db.project_map:
            print("Have key: ", key)
        project_input = request.json
        project_id = project_input['project_id']
        
        try:
            project = project_db.get_project(project_id)
        except:
            return Response("{'error:':'project not found'}", status=400, mimetype='application/json')

        # modify any attributes of project requested to be changed
        if 'name' in project_input:
            project.name = project_input['name']
        if 'description' in project_input:
            project.description = project_input['description']
        if 'pm_email' in project_input:
            project.pm_email = project_input['pm_email']
        if 'date_created' in project_input:
            project.date_created = project_input['date_created']
        if 'date_completed' in project_input:
            project.date_completed = project_input['date_completed']
        if 'status' in project_input:
            project.status = project_input['status']
        project_db.update_project(project_id, project)
        return jsonify({'success': True})




    # create project based on user input
    if request.method == 'POST':
        id = uuid.uuid4()
        project_input = request.json
        
        project = db.Project(
        id= str(id),
        name=project_input.get('name'),
        description=project_input.get('description'),
        pm_email=project_input.get('pm_email'),
        date_created=project_input.get('date_created'),
        status= db.Status.ACTIVE, # initialize status as active but users can modify it
        date_completed=project_input.get('date_completed'),
        tasks=[]
    )
    # add project to database and return success
    project_db.add_project(project)
    return jsonify({'success': True, 'newProjectId': project.id})


# create index route (so when we browse to the url, dont immediately just 404)
@app.route('/') # Can pass in url string of your route in here
# define function for that route
def index():
    return render_template('front_end.html')

# run the Flask main file to test our API endpoints in the developing environment.
if __name__ == "__main__": # two underscores both sides
    app.run(debug=True) # debug=True means if any errors, they'll pop up on the webpage for us to see