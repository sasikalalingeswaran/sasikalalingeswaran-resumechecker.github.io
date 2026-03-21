from flask import Flask,request,render_template
from werkzeug.utils import secure_filename
import re

app=Flask(__name__)

def extract(text,section_name):
    lines=text.splitlines()
    inside_section=False
    section_lines=[]
    for l in lines:
        if l.lower()==section_name.lower()+":":
            inside_section=True
            continue
        if inside_section and l.endswith(":"):
            break
        if inside_section and l:
            section_lines.append(l)
    return section_lines

def words(text):
    text=text.lower()
    text=re.sub(r"[^a-z0-9+]",' ',text)
    return set(text.split())

@app.route("/",methods=["GET","POST"])
def check():
    percent_skills=None
    missed_skills=None
    missing_skills=None
    if request.method=="POST":
        jd_file=request.files["jd"]
        filename=secure_filename(jd_file.filename)
        jd_file.save(filename)
        with open(filename,"r") as f:
            jd_read=f.read()
            skills_lines=extract(jd_read,"Skills")
            
            jd_skills=words(" ".join(skills_lines))
            
            res_file=request.files["resume"]
            filename2=secure_filename(res_file.filename)
            res_file.save(filename2)
            with open(filename2,"r") as f:
                res_read=f.read()
                res_words=words(res_read)
                matched_skills=jd_skills&res_words
                percent_skills=round((len(matched_skills)/len(jd_skills))*100)
                missed_skills=jd_skills-res_words
                missing_skills=",".join(missed_skills)
                
    return render_template("index.html",percent_skills=percent_skills,missing_skills=missing_skills)

if __name__ == "__main__":
    app.run(debug=True)