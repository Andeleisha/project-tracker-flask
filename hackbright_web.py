"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    row = hackbright.get_student_by_github(github)

    project_rows = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
    						first=row[0],
    						last=row[1],
    						github=row[2], projects=project_rows)

    # return "{} is the GitHub account for {} {}".format(github, first, last)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add")
def student_add():
	"""Form input to create a new student"""

	return render_template("student_add.html")


@app.route("/student-added", methods=['POST'])
def student_added():
	"""Add a student"""
	first_n = request.form.get("first_name")
	last_n = request.form.get("last_name")
	gh = request.form.get("github")

	hackbright.make_new_student(first_n, last_n, gh)

	return render_template("student-added.html", github=gh)


@app.route("/project", methods=['GET'])
def get_project():
	"""Show project information"""
	title = request.args.get('project')

	project_info = hackbright.get_project_by_title(title)

	return render_template("project.html", project_name=project_info[0],
											project_des=project_info[1],
											points=project_info[2])

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
