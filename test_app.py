
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qVTFRMFkzTURGRU5FVkROemxGUlRKQlJqVkZPVVEwUVVJd05qRkJNRU0wTVRFM016QkNPQSJ9.eyJpc3MiOiJodHRwczovL25rZWNoaS1rZWNoeXkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMTM5MDUzODQ4M2E1MTBjYjczNjYwNiIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU3ODM5MTg2NywiZXhwIjoxNTc4NDc4MjY1LCJhenAiOiJHSDVVTmRlTjlzRW5BRGJ0RHRTOU94Vjg0dVVwMllNZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.TyoVbWaOqrvFnO5tMnenJpcUJ95TnMIEfIjcgdZcioNuY6zCybbjjQ0ZjK-Sra2xCvuRFoHpVCHup-cZnwbe2r3NYEZM0sFLSeWIkH5ys5NauCaqW5WZqJ6QmUHULDsm5513-JDShuC_vcJYt75KL2zE6xmZr8AsdCA5jF0jY4UeNBjjxtclWUUs8iAYkJ7fcb4hd-6_00N7bzYGQSrFYqhwtBAYSKfc1THGqS9HINxZqO_eRGFA6VwfTDH7zpRilOsKNLZqmxzQPXcG7lGIshFMZRjI9b5J4b1s630e0KltigEPP-ut_vc_EpEvEzbW7Coi_2hKI5ZC4SBkZyr9jA'

CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qVTFRMFkzTURGRU5FVkROemxGUlRKQlJqVkZPVVEwUVVJd05qRkJNRU0wTVRFM016QkNPQSJ9.eyJpc3MiOiJodHRwczovL25rZWNoaS1rZWNoeXkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMTM5MGQxY2IzNjBiMTA5ODFkM2ZkYiIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU3ODM5MDY5NywiZXhwIjoxNTc4NDc3MDk1LCJhenAiOiJHSDVVTmRlTjlzRW5BRGJ0RHRTOU94Vjg0dVVwMllNZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.QSA1-0xVMoCXLAFb0Gs0pllk7SoX3jgjvQPajLCYHjQynbB8ZWDkifxtXCoeAJtgWjGOM-oSOcQcNB_HH1G1ziL4PyACK1J7z2I2NbY3hS7ytHv8nFxwGZHWRi-Yr9ld8_lX4pKz5bm85ijbrpRPmDu1fJFvSMDm6q44NN6GM0XtRBJcyfwLrb8UM2Ys9oMm_ObMXE6FjtKrPYLEWtj4k6auxQfrkSjiSms5PmVD_Bpe0oVL54P1tEsmeR4hPDN6t294ezsvEd7fvrJ8HhdqgWO6RF7IhYEv9qh8D53lHDuMDTdq6ad5R0xkmkiZ6KCXDd9mYQ20o4GQkIOzja56Pw'

CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qVTFRMFkzTURGRU5FVkROemxGUlRKQlJqVkZPVVEwUVVJd05qRkJNRU0wTVRFM016QkNPQSJ9.eyJpc3MiOiJodHRwczovL25rZWNoaS1rZWNoeXkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlMTM5MGY1Y2IzNjBiMTA5ODFkM2ZkZiIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTU3ODM5MDk2NCwiZXhwIjoxNTc4NDc3MzYyLCJhenAiOiJHSDVVTmRlTjlzRW5BRGJ0RHRTOU94Vjg0dVVwMllNZyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.JR_Dc13v660UTcYASKwMLSTBfV4DOB3bBYzR7YRXii1R6C1ZBUuD0z8VduXRqYdzn7Z_zrzPrFrxkInsAPpYwwcG2Z9hUJFzUaQa7d6E49YpxGx7OtEVKErV2l7nUr5fm5JFZE-N6ahx8qgnVFPjtDFb1xa0D7Eaq-2AGQvhh0aLNrMn2bz9aFYwQVtamWKm8juSKCQC2006D9vfaHljSdmoQLwJArFhi3JM5R7COyjLbrs6Ehn510yS1sfd4FmXmIxV0LOrvOHJzBvrrnbn7KSZFJuQrK0lu4dgZsTw0TRtXtGIg85ofy-z30V_OwStxC9zndgM90gcKtoyJBn1ig'


class MHTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DB_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

#####################    MOVIE TEST STARTS #################################################

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies/id
    def test_get_movie_byId(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Sugar Rush')

    def test_get_movie_byId_404(self):
        response = self.client().get(
            '/movies/333333',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Sigidi', 'release_date': "2017-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie created successfully')
        self.assertEqual(data['movie']['title'], 'Sigidi')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Unauthorize movie', 'release_date': "2019-12-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Squash', 'release_date': "2000-10-19"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Squash')


    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/4444444',
            json={'title': 'New Life', 'release_date': "2003-09-16"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/11111111',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

#####################    MOVIE TEST ENDS #################################################



#####################    ACTORS TEST START #################################################
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    # GET /actors/id
    def test_get_actor_byId(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Marlon Brando')

    def test_get_actor_byId_404(self):
        response = self.client().get(
            '/actors/121234',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Julius', 'age': 24, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'Julius')


    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    
    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Czar', 'age': 14, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Emily', 'age': 37, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Emily')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/9999999',
            json={'name': 'Mike', 'age': 65, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    
    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    
    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/545432',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()