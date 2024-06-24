# CS305 Park University
# Assignment #7 Solution Code
# Datalog

from pyDatalog import pyDatalog

# In this assignment you will do some simple knowledge representation
# and reasoning within datalog within Python. The domain you will be
# working within will be academic degree program requirements checking.

# 1.
# TODO: complete the definition of the load_course_catalog function.
# This function should assert facts for which courses teach which
# subjects. You *MUST* use the predicate name 'subject' with the
# first argument being the literal name of the class and the second
# being the literal name of the subject for the tests to pass.
#
# assert the following information:
# 1. cs101 is a stem class
# 2. mat167 is a stem class
# 3. art310 is a humanities class
# 4. eng101 is a humanities class
# 5. his110 is a social science class
# 6. psy150 is a social science class
def load_course_catalog():
    """asserts all knowledge of classes and their subjects"""
    pyDatalog.assert_fact('subject', 'cs101', 'stem')
    pyDatalog.assert_fact('subject', 'mat167', 'stem')
    pyDatalog.assert_fact('subject', 'art310', 'humanities')
    pyDatalog.assert_fact('subject', 'eng101', 'humanities')
    pyDatalog.assert_fact('subject', 'his110', 'social science')
    pyDatalog.assert_fact('subject', 'psy150', 'social science')

# 2.
# TODO: implement assert_student_completed_class. It is up to you
# how you represent this knowledge in datalog. Student id's will be
# literals. 
def assert_student_completed_class(studentid, courseid):
    """asserts that the specified student has completed the specified course"""
    pyDatalog.assert_fact('completed', studentid, courseid)

# 3.
# TODO: implement load_graduation_rules. This function should simply
# make one call to pyDatalog.load. This call should contain all needed
# clauses (only 1 is necessary) to ensure any student that has met the
# graduation requirements will be considered a graduate (in queries).
# The graduation requirements are simply that a student has taken at
# least one course from each of the available subjects. It is up to
# you how to implement these clauses.
def load_graduation_rules():
    """loads rules for determining if a student has graduated"""
    pyDatalog.load("""
        # Rule to check if a student (S) has completed a subject (Sub).
        # It's true if the student completed a course (C) that belongs to this subject.
        
        has_subject(S, Sub) <= completed(S, C) & subject(C, Sub)
        
        # Rule to determine if a student (S) has graduated.
        # A student is 'graduated' if they have completed courses in three areas:
        # STEM, humanities, and social science.

        graduated(S) <= has_subject(S, 'stem') & has_subject(S, 'humanities') & has_subject(S, 'social science')
    """)

# 4.
# TODO: return the results of a call to pyDatalog.ask. Form a
# query that determines if the student graduated or not. 
def ask_if_graduated(studentid):
    """determines if the given student has graduated or not"""
    return pyDatalog.ask(f"graduated('{studentid}')") is not None


# 5. complete the definition of find_graduates below.
def find_graduates():
    res = set()
    # Query all students, then check if each has graduated
    ans = pyDatalog.ask("completed(S, _)")
    if ans:
        for student in ans.answers:
            student_id = student[0]
            if pyDatalog.ask(f"graduated('{student_id}')"):
                res.add(student_id)
    return res



def main():
    assert_student_completed_class('s001', 'psy150')
    assert_student_completed_class('s001', 'eng101')
    assert_student_completed_class('s001', 'mat167')
    assert_student_completed_class('s001', 'cs101')
    assert_student_completed_class('s002', 'psy150')
    assert_student_completed_class('s002', 'his101')
    assert_student_completed_class('s002', 'cs101')
    assert_student_completed_class('s002', 'mat167')

    # Adding new students
    # Student s003 - Has graduated (completed courses)
    assert_student_completed_class('s003', 'cs101')
    assert_student_completed_class('s003', 'eng101')
    assert_student_completed_class('s003', 'psy150')

    # Student s004 - Has not graduated (missing a course in humanitiest)
    assert_student_completed_class('s004', 'cs101')
    assert_student_completed_class('s004', 'mat167')
    assert_student_completed_class('s004', 'psy150')
    
    load_course_catalog()
    load_graduation_rules()
    
    print('Student s001 did ' +
          ('' if ask_if_graduated('s001') else 'not ') +
          'graduate.')
    
    print('Student s002 did ' +
          ('' if ask_if_graduated('s002') else 'not ') +
          'graduate.')
    print('Student s003 did ' +
      ('' if ask_if_graduated('s003') else 'not ') +
      'graduate.')
    print('Student s004 did ' +
      ('' if ask_if_graduated('s004') else 'not ') +
      'graduate.')
    
    # 6. 
    # If you completed everything correctly, you should see that
    # s001 graduated and s002 did not.
    # TODO: add a few more students, some that have graduated and
    # some that have not. Feel free to add additional courses as
    # well. 
    print('Graduating students:', find_graduates())
    
    
  
if __name__ == '__main__':
  main()
