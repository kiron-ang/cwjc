import sys,os,re
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pdfquery
dictionary_of_page_numbers = ({

"Study pages 60-61 ": "",
"Study pages 62-63 ": "",
"Study pages 64-65; 70-73 ": "",
"Study pages 66-67; 100-105 ": "",
"Study pages 70-73 ": "",
"Study pages 74-75; 110-111 ": "",
"Study pages 74-77; 78-79; 108-109 ": "",
"Study pages 78-79 ": "",
"Study pages 84-85 ": "",
"Study pages 86-87 ": "",
"Study pages 86-89 ": "",
"Study pages 88-89 ": "",
"Study pages 90-93 ": "",
"Study pages 92-93 ": "",
"Study pages 94-95 ": "",
"Study pages 100-101 ": "",
"Study pages 100-105 ": "",
"Study pages 102-103 ": "",
"Study pages 106-107 ": "",
"Study pages 220-223; 240-243; 246- ": "",
"Study pages 232-233 ": "",
"Study pages 260-263 ": "",
"Study pages 264-265; 272-275; 266- ": "",
"Study pages 282-287 ": "",
"Study pages 288-291 ": "",
"Study pages 292-295 ": "",
"Study pages 296-299 ": "",
"Study pages 300-305 ": "",
"Study pages 306-308 ": "",
"Study pages 320-321 ": "",
"Study pages 320-321; 324-325 ": "",
"Study pages 322-323 ": "",
"Study pages 326-327 ": "",
"Study pages 328-329 ": "",
"Study pages 328-331 ": "",
"Study pages 332-333 ": "",
"Study pages 336-347 ": "",
"Study pages 352-355 ": "",
"Study pages 356-357 ": "",
"Study pages 358-359 ": "",
"Study pages 360-361 ": "",
"Study pages 364-365 ": "",
"Study pages 366-367 ": "",
"Study pages 368-369 ": "",
"Study pages 370-371 ": "",
"Study pages 372-375 ": "",
"Study pages 378-381 ": "",
"Study pages 382-383 ": "",
"Study pages 390-391; 394-395 ": "",
"Study pages 394-395 ": "",
"Study pages 396-397 ": "",
"Study pages 398-405 ": "",
"Study pages 420-421 ": "",
"Study pages 422-423 ": "",
"Study pages 424-425 ": "",
"Study pages 426-427 ": "",
"Study pages 428-431 ": "",
"Study pages 432-433 ": "",
"Study pages 432-433; 502-505 ": "",
"Study pages 500-501 ": "",
"Study pages 500-501; 508-509 ": "",
"Study pages 502-505 ": "",
"Study pages 504-505 ": "",
"Study pages 506-507 ": "",
"Study pages 508-509 ": "",
"Study pages 510-511 ": "",
"Study pages 510-511; 296-299 ": "",
"Study pages 510-511; 300-305 ": "",
"Study pages 512-513 ":"PLACEHOLDER"

})

# maximum filesize in megabytes
file_mb_max = 100
# encryption key
app_key = 'any_non_empty_string'
# full path destination for our upload files
upload_dest = os.path.join(os.getcwd(), 'uploads_folder')
# list of allowed allowed extensions
extensions = set(['pdf'])
app=Flask(__name__)
app.secret_key = app_key
if not os.path.isdir(upload_dest):
  os.mkdir(upload_dest)
app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/')
def main_page():
  return """
<!DOCTYPE html>
<title>Analyze Score Reports from GED Manager! A CWJC Project</title>
<style>
  body {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>
<body>
  <form method="post" action="/" enctype="multipart/form-data">
    <p><input type="file" name="files[]" multiple="true" autocomplete="off" required></p>
    <p><input type="submit" value="Click this button to analyze these PDF files!"></p>
  </form>
</body>
  """


@app.route('/analysis')
def page_two():

  main_string = ""
  start_string = """
<!DOCTYPE html>
<title>Analyze Score Reports from GED Manager! A CWJC Project</title>
<style>
  body {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
  }
  p {
    flex: 0 1 50%;
  }
</style>
<body>

  """
  end_string = """

  </body>
  """

  # THIS IS SCORE REPORT ANALYSIS CODE

  list_of_pdf_names = []
  list_of_study_goals = []
  number_of_students = 0
  list_containing_students_and_their_goals = []
  for path, subdirs, files in os.walk(upload_dest):
    for name in files:
      list_of_pdf_names.append(name)

  # main_string = main_string + "<p>This is executing!!!!!</p>"
  #read the PDFs
  for name in list_of_pdf_names:
    pdf = pdfquery.PDFQuery(f"/home/kiron/uploads_folder/{name}")
    # main_string = main_string + "<p>This is executing!!!!!</p>"
    pdf.load()

    #convert each PDF to XML
    pdf.tree.write(f"/home/kiron/uploads_folder/{name}.xml", pretty_print = True)
    with open(f"/home/kiron/uploads_folder/{name}.xml", "r") as file:
      lines_of_xml = file.readlines()
    # lines_of_xml = [line for line in lines_of_xml if "Study" in line] This line
    # is only useful if One PDF = One Student

    temp_student = []
    for line in lines_of_xml:
      if "Although" in line:
        number_of_students += 1
        list_containing_students_and_their_goals.append(temp_student)
        temp_student = []
      elif "Study" in line:
        temp_student.append(line)

    # Now for each PDF, look for the "Study" string that contains page numbers.
    # print(f"These are the study goals from score report #{name}:")
    # temp_list_of_study_goals = []
    start_position = 0
    end_position = 0
    # start_found = False
    # end_found = False
  for student in list_containing_students_and_their_goals:
    temp_list_of_study_goals = []
    for line in student:
      start_position = 0
      end_position = 0
      start_found = False
      end_found = False
      position_in_line = 0
      for character in line:
        if start_found == False and character == "S":
        # print("S found!")
          start_position = position_in_line
          start_found = True
        if start_found == True and character == "<":
          end_position = position_in_line
          end_found = True
        if end_found == True:
          break
        position_in_line += 1
    # print("  *", line[start_position:end_position])
      if (any(char.isdigit() for char in line[start_position:end_position])) and (line[start_position:end_position] not in temp_list_of_study_goals):
        temp_list_of_study_goals.append(line[start_position:end_position])
        list_of_study_goals.append(line[start_position:end_position])


    # Now we should try various things to get some useful information
    # such as printing out the study pages that show up in all of the score
    # reports.
  set_of_study_goals = []
  for goal in list_of_study_goals:
    if goal not in set_of_study_goals:
      set_of_study_goals.append(goal)
  set_of_study_goals.sort()
  list_of_two_page_goals = []
  list_of_three_page_goals = []
  for goal in set_of_study_goals:
    if goal[12].isdigit() and goal[13].isdigit() and goal[14].isdigit():
      list_of_three_page_goals.append(goal)
    else:
      list_of_two_page_goals.append(goal)
  set_of_study_goals = []
  list_of_two_page_goals.sort()
  list_of_three_page_goals.sort()
  for goal in list_of_two_page_goals:
    set_of_study_goals.append(goal)
  for goal in list_of_three_page_goals:
    set_of_study_goals.append(goal)
  main_string = main_string + "<p> Hi there! Here is a summary of your study goals and the number of score reports that mentioned the study goal: </p>"
  # main_string = main_string + "<p> </p>"
  for set_goal in set_of_study_goals:
    goal_shows_up = 0
    for list_goal in list_of_study_goals:
      if set_goal == list_goal:
        goal_shows_up += 1
    main_string = main_string + f"<p>  ☐ {set_goal}: {goal_shows_up} | {dictionary_of_page_numbers[set_goal]} </p> "
    # do a breakdown by test and subject
    # take a practice test and get everything WRONG!
    # Break it down by practice tests or real tests.
    # Automatically write to a text file and then move those less than 100 to the top!
    # Move PDFs in a separate subdirectory and DELETE everything (or maybe only XML files) in that directory.

  # THIS IS THE END OF SCORE REPORT ANALYSIS CODE

  """ THIS IS A TESTING SNIPPET USED TO PROVE THAT I COULD DISPLAY OUTPUT!
  list_of_pdfs = []
  for path, subdirs, files in os.walk(upload_dest):
    for name in files:
      list_of_pdfs.append(os.path.join(path, name))
  for pdf in list_of_pdfs:
    main_string = main_string + "<p>" + pdf + "</p>"
  """

  for path, subdirs, files in os.walk(upload_dest):
    for name in files:
      os.remove(os.path.join(path, name))

  return start_string + main_string + end_string


@app.route('/', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    for path, subdirs, files in os.walk(upload_dest):
      for name in files:
        os.remove(os.path.join(path, name))
    if 'files[]' not in request.files:
      return redirect(request.url)

    files = request.files.getlist('files[]')

    for file in files:
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_dest, filename))

    return redirect('/analysis')




