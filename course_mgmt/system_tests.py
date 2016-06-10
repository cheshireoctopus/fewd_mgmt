__author__ = 'mmoisen'

from course_mgmt.models import db, all_models
import unittest
import requests

URL = 'http://localhost:5000'

class SqliteSequence(db.Model):
    __tablename__ = 'sqlite_sequence'
    name = db.Column(db.String, primary_key=True)
    seq = db.Column(db.Integer)

def get_first_id_from_response(r):
    '''
    Utility method to pull the first ID from a response object
    Remember responses look like this:
        {
            "data": [
                { ... },
                { ...}
            ]
        }
    :param r: response object from requests
    :return: id
    '''
    return r.json()['data'][0]['id']

def hit_api(api, data=None, params=None, method='POST'):
    '''
    Utility method to hit any of the APIs
    :param api: Full API after host:port
                /api/course/create/
    :param data: Dict containing the data to hit the API with
    :param method: 'POST', 'GET', 'PUT', 'DELETE'
    :return: a response object from requests
    '''
    r = getattr(requests, method.lower())(URL + api, json=data, params=params)
    return r

def drop_and_create_db():
    api = '/api/drop/'
    r = hit_api(api)

    # Change the starting sequences to try to find bugs in join conditions
    index = 1
    db.session.query(SqliteSequence).delete()
    for table in all_models:
        s = SqliteSequence(name=table.__tablename__, seq=index)
        db.session.add(s)
        index += 100

    db.session.commit()


    return r

class TestLol(unittest.TestCase):
    def test_lol(self):
        drop_and_create_db()

def create_course(name):
    '''
    Utility function to create a single course
    '''
    api = '/api/course/'
    method = 'POST'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_course(id, name):
    api = '/api/course/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_course(id):
    api = '/api/course/{}'.format(id)  # No trailing slashes on ID due to flask-classy constraint
    method = 'GET'
    return hit_api(api, method=method)

def create_class_lecture(class_id, name, description, dt):
    # Utility function to create a single lecture
    api = '/api/lecture/'
    method = 'POST'
    data = {
        'data': [
            {
                'class_id': class_id,
                'name': name,
                'description': description,
                'dt': dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_course_lecture(course_id, name, description):
    api = '/api/lecture/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name,
                'description': description,
            }
        ]
    }

    return hit_api(api, data, method=method)


def update_lecture(id, name, description, dt):
    # Utility function to create a single lecture
    api = '/api/lecture/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name,
                'description': description,
                'dt': dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_lecture(id):
    api = '/api/lecture/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)


def create_class(course_id, name, start_dt, end_dt):
    '''
    Utility function to create a single class
    '''
    api = '/api/class/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name,
                'start_dt': start_dt,
                'end_dt': end_dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_class(id, name, start_dt, end_dt):
    api = '/api/class/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'start_dt': start_dt,
                'end_dt': end_dt,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_class(id):
    api = '/api/class/{}'.format(id)
    method = 'GET'
    return hit_api(api, method=method)

def create_homework_independent(name):
    # Creates an indepenent homework
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_homework(id, name):
    api = '/api/homework/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_homework(id):
    api = '/api/homework/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)

def add_homework_independent_to_course(course_id, homework_id):
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'id': homework_id,
                'course_id': course_id
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_homework_dependent(course_id, name):
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_student_independent(first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_student(id, first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_student(id):
    api = '/api/student/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)

def add_student_independent_to_class(class_id, student_id):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'id': student_id,
                'class_id': class_id
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_student_dependent(class_id, first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'class_id': class_id,
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

class TestAll(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

    def assert_data_equals(self, r, **kwargs):
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['data'], kwargs)

    def test_all_create(self):
        '''
        This system test hits all of the create APIs happy path
        The purpose of this is to quickly tell if anything major is broken
        :return:
        '''
        ## Create Course
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        # Get Course
        r = get_course(id=course_id)
        self.assert_data_equals(r, id=course_id, name='Matthew''s Course')
        #self.assertEquals(r.json()['name'], 'Matthew''s Course')

        ## Update Course

        r = update_course(id=course_id, name='Chandler''s Course')
        self.assertEquals(r.status_code, 200)

        # Get Course
        r = get_course(id=course_id)
        self.assert_data_equals(r, id=course_id, name='Chandler''s Course')

        ## Create Class
        r = create_class(course_id=course_id, name='Spring 2016', start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        # Get Class
        r = get_class(class_id)
        self.assert_data_equals(r, id=class_id, name='Spring 2016', start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00',
                                course_id=course_id)

        ## Update Class
        r = update_class(id=class_id, name='Spring 2015', start_dt='2015-01-01 00:00:00', end_dt='2015-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        # Get Class
        r = get_class(class_id)
        self.assert_data_equals(r, id=class_id, name='Spring 2015', start_dt='2015-01-01 00:00:00', end_dt='2015-05-30 00:00:00', course_id=course_id)


        #r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        #self.assertEquals(r.status_code, 200)

        ## Create Course Lecture
        r = create_course_lecture(course_id=course_id, name='Lecture 1', description='The first lecture1')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        # Get Lecture
        r = get_lecture(lecture_id)
        self.assert_data_equals(r, id=lecture_id, name='Lecture 1', description='The first lecture1')

        # Update lecture
        #r = update_lecture(id=lecture_id, name='Lecture 2', description='The second lecture', dt='2015-01-01 00:00:00')
        #self.assertEquals(r.status_code, 200)

        # Get Lecture
        #r = get_lecture(lecture_id)
        #self.assert_data_equals(r, id=lecture_id, class_id=class_id, name='Lecture 2', description='The second lecture', dt='2015-01-01 00:00:00')

        ## Create Independent Homework and add to Course
        # Create Independent Homework
        r = create_homework_independent(name='Homework 1')
        self.assertEquals(r.status_code, 200)

        homework_independent_id = get_first_id_from_response(r)

        # Get Homework
        r = get_homework(homework_independent_id)
        # Shouldn't parent id be null not empty string
        self.assert_data_equals(r, parent_id='', id=homework_independent_id, name='Homework 1')

        # Update homework
        #r = update_homework(id=homework_independent_id, name='Homework 2')
        #self.assertEquals(r.status_code, 200)

        # Get Homework
        #r = get_homework(homework_independent_id)
        #self.assert_data_equals(r, parent_id='', id=homework_independent_id, name='Homework 2')

        # Add independent homework to Course
        r = add_homework_independent_to_course(course_id=course_id, homework_id=homework_independent_id)
        self.assertEquals(r.status_code, 200)

        course_homework_id_1 = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 2')
        self.assertEquals(r.status_code, 200)
        course_homework_id_2 = get_first_id_from_response(r)

        ## Create Independent Student and Add to Class
        # Create Independent Student
        r = create_student_independent(first_name='Matthew', last_name='Moisen', github_username='mkmoisen',
                                       email='mkmoisen@gmail.com', photo_url='http://matthewmoisen.com/pic.jpg')

        self.assertEquals(r.status_code, 200)

        student_independent_id = get_first_id_from_response(r)

        # Get Student
        r = get_student(student_independent_id)
        self.assert_data_equals(r, id=student_independent_id, first_name='Matthew', last_name='Moisen',
                                github_username='mkmoisen', email='mkmoisen@gmail.com',
                                photo_url='http://matthewmoisen.com/pic.jpg')

        # Update Student
        r = update_student(id=student_independent_id, first_name='Chandler', last_name='Moisen', github_username='ches',
                           email='hello@chandlermoisen.com', photo_url='http://chandlermoisen.com/pic/jpg')
        self.assertEquals(r.status_code, 200)

        # Get Student
        r = get_student(student_independent_id)
        self.assert_data_equals(r, id=student_independent_id, first_name='Chandler', last_name='Moisen',
                                github_username='ches', email='hello@chandlermoisen.com',
                                photo_url='http://chandlermoisen.com/pic/jpg')

        # Add Independent Student to Class
        r = add_student_independent_to_class(class_id, student_independent_id)
        self.assertEquals(r.status_code, 200)

        class_student_id_1 = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id_2 = get_first_id_from_response(r)


class TestInitializations(unittest.TestCase):
    '''
    When a new Student is added to a Class, all Assignments and Attendance should be initialized for him

    When a new CourseHomework is added, Assignments should be initialized for all Students

    When a new Lecture is added, Attendances should be initialized for all Students
    '''
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

        '''
        Create a completely different course/class/lecture/homework/student to see if it interferes
        '''

        # Course
        r = create_course(name='Interference Course')
        self.assertEquals(r.status_code, 200)
        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2015", start_dt='2015-01-01 00:00:00', end_dt='2015-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)
        class_id = get_first_id_from_response(r)

        ## Create Lecture
        r = create_class_lecture(class_id=class_id, name='Interference Lecture', description='The first interference', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Interference Homework 2')
        self.assertEquals(r.status_code, 200)

        ############
        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Inter', last_name='Ference', github_username='interference',
                                     email='inter@ference.com', photo_url='http://interference.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

    def _read_attendance_by_lecture(self, lecture_id):
        api = '/api/lecture/{}/attendance/'.format(lecture_id)
        return hit_api(api, method='GET')

    def _read_assignment(self, class_id, course_homework_id):
        api = '/api/class/{}/assignment'.format(class_id)
        params = {'course_homework_id': course_homework_id}
        return hit_api(api, method='GET', params=params)

    def test_add_student(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Lecture
        r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)
        course_homework_id = get_first_id_from_response(r)


        ############
        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        ############
        ## Query for proof

        ## Attendance
        r = self._read_attendance_by_lecture(lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]

        self.assertEquals(attendance['attendance']['lecture_id'], lecture_id)
        # attendance defaults to False
        self.assertEquals(attendance['attendance']['did_attend'], False)
        #self.assertEquals(attendance['student']['id'], student_id)

        ## Assignments
        r = self._read_assignment(class_id, course_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assertEquals(assignment['assignment']['course_homework_id'], course_homework_id)
        self.assertEquals(assignment['assignment']['class_student_id'], class_student_id)
        self.assertEquals(assignment['homework']['name'], 'Homework 1')



    def test_add_lecture(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)


        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        #######
        ## Create Lecture
        r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        # Query Attendance for proof
        r = self._read_attendance_by_lecture(lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]

        self.assertEquals(attendance['attendance']['lecture_id'], lecture_id)
        # attendance defaults to False
        self.assertEquals(attendance['attendance']['did_attend'], False)
        self.assertEquals(attendance['attendance']['class_student_id'], class_student_id)

    def test_add_homework(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)
        course_homework_id = get_first_id_from_response(r)


        ## Query Assignments for Proof
        ## Assignments
        r = self._read_assignment(class_id, course_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assertEquals(assignment['assignment']['course_homework_id'], course_homework_id)
        self.assertEquals(assignment['assignment']['class_student_id'], class_student_id)
        self.assertEquals(assignment['homework']['name'], 'Homework 1')








class TestException(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

    def test_class_fk(self):
        '''
        Test exception path for creating a class with a bad foreign key
        '''
        ## Create Course
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=10, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 400)

        j = r.json()


if __name__ == '__main__':
    import nose
    nose.run()
