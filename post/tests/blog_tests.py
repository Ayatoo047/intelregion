from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from post.models import Blog, Comment
from intelregion.settings import X_API_KEY



@pytest.fixture
def create_blog(api_client : APIClient):
    def do_create_blog(blog:str, is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
        
        if blog == 'good':
           blog_detail =  {
            "requestType": "inbound",
            "data": {
                    "title": "testing",
                    "content": "testing"
                }
            }
        else:
            blog_detail =  {
            "requestType": "inbound",
            "data": {
                    "title": "",
                    "content": ""
                }
            }
        
        if is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)

        response = api_client.post('/api/blog/', blog_detail, format="json", **header)
        
        return response
    return do_create_blog


@pytest.fixture
def create_comment(api_client : APIClient):
    def do_create_comment(comment:str, is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
        create_blog = baker.make(Blog)
        
        
        if comment == 'good':
           comment_detail =  {
            "requestType": "inbound",
            "data": {
                    "content": "testting"
                }
            }
        else:
            comment_detail =  {
            "requestType": "inbound",
            "data": {}
            }
        
        if is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)

        response = api_client.post(f'/api/blog/{create_blog.id}', comment_detail, format="json", **header)
        
        return response
    return do_create_comment


@pytest.fixture
def update_blog(api_client : APIClient):
    def do_update_blog(blog:str, method:str, is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
        
        if blog == 'good':
           blog_detail =  {
            "requestType": "inbound",
            "data": {
                   "title": "testing",
                   "content": "testing"
                }
            }
        else:
            blog_detail =  {
            "requestType": "inbound",
            "data": {
                "title": "",
                "content": ""
            }
            }
        
        if is_auth and blog == 'good':
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_blog = baker.make(Blog, owner=new_user)
            
        if is_auth and blog == 'bad':
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_blog = baker.make(Blog, owner=new_user)
            
    
        elif not is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_blog = baker.make(Blog)
            
            
        if method == 'put':
            response = api_client.put(f'/api/blog/{created_blog.id}/', blog_detail, format="json", **header)
        elif method == 'patch':
            response = api_client.patch(f'/api/blog/{created_blog.id}/', blog_detail, format="json", **header)
        
        return response
    return do_update_blog


@pytest.fixture
def comment_update(api_client : APIClient):
    def do_comment_update(comment:str, method:str, is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
        
        if comment == 'good':
           blog_detail =  {
            "requestType": "inbound",
            "data": {
                    "content": "testing comments"
                }
            }
        else:
            blog_detail =  {
            "requestType": "inbound",
            "data": {
                "content": ""
                
            }
            }
        
        if is_auth and comment == 'good':
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_comment = baker.make(Comment, owner=new_user)
            
        elif is_auth and comment == 'bad':
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_comment = baker.make(Comment, owner=new_user)
            
        elif not is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_comment = baker.make(Comment)
            
        if method == 'put':
            response = api_client.put(f'/api/comment/{created_comment.id}/', blog_detail, format="json", **header)
        elif method == 'patch':
            response = api_client.patch(f'/api/comment/{created_comment.id}/', blog_detail, format="json", **header)
        
        return response
    return do_comment_update


@pytest.fixture
def comment_delete(api_client : APIClient):
    def do_comment_delete(comment:str, is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
        
        if is_auth and comment == 'good':
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_comment = baker.make(Comment, owner=new_user)
        else:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_comment = baker.make(Comment)
            
        response = api_client.delete(f'/api/comment/{created_comment.id}/', **header)
        
        return response
    return do_comment_delete


@pytest.fixture
def delete_blog(api_client : APIClient):
    def do_delete_blog(is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
                
        if is_auth:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_blog = baker.make(Blog, owner=new_user)
        else:
            new_user = baker.make(User)
            api_client.force_authenticate(user=new_user)
            created_blog = baker.make(Blog)
            
        
        response = api_client.delete(f'/api/blog/{created_blog.id}/', **header)
        
        return response
    return do_delete_blog

@pytest.fixture
def get_allblog(api_client : APIClient):
    def do_get_allblog():
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
                
        baker.make(Blog, _quantity=10)
        
        response = api_client.get(f'/api/blog/', **header)
        
        return response
    
    return do_get_allblog

@pytest.fixture
def get_a_blog(api_client : APIClient):
    def do_get_a_blog(is_auth=False):
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
                
        blog = baker.make(Blog)
        
        response = api_client.get(f'/api/blog/{blog.id}/', **header)
        
        return response
    return do_get_a_blog

@pytest.fixture
def get_blog_comments(api_client : APIClient):
    def do_get_blog_comments():
        header = {'HTTP_X-Api-Key':str(X_API_KEY)}
                
        blog = baker.make(Blog)
        comments = baker.make(Comment, blogs=blog, _quantity=15)
        
        response = api_client.get(f'/api/blog/{blog.id}/comments', **header)
        
        return response
    return do_get_blog_comments


@pytest.mark.django_db  
class TestGetBlog():
    def test_200_if_okay(self, get_allblog):
        response = get_allblog()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']['results']) == 10
        
    def test_getSingle_200_if_okay(self, get_a_blog):

        response = get_a_blog()
        
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db  
class TestCreateBlog():
    def test_200_if_okay(self, create_blog):
        response = create_blog('good', True)

        assert response.status_code == status.HTTP_200_OK
        
    
    
    def test_401_if_anonymous(self, create_blog):
        response = create_blog('good', False)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_400_if_bad_data(self, create_blog):
        response = create_blog('bad', True)
        
        response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db  
class TestUpdateBlog():
    def test_200_if_put_okay(self, update_blog):
        response = update_blog('good', 'put', True)
        
        response.status_code == status.HTTP_200_OK
    
    def test_200_if_patch_okay(self, update_blog):
        response = update_blog('good', 'patch', True)
        
        assert response.status_code == status.HTTP_200_OK
    
    
    def test_403_if_put_not_author(self, update_blog):
        response = update_blog('good', 'put',False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_403_if_patch_not_author(self, update_blog):
        response = update_blog('good', 'patch',False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_400_if_put_bad_data(self, update_blog):
        response = update_blog('bad', 'put',True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_400_if_patch_bad_data(self, update_blog):
        response = update_blog('bad', 'patch',True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
@pytest.mark.django_db  
class TestUpdateComment():
    def test_200_if_put_okay(self, comment_update):
        response = comment_update('good', 'put', True)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_200_if_patch_okay(self, comment_update):
        response = comment_update('good', 'patch', True)
        
        assert response.status_code == status.HTTP_200_OK
    
    
    def test_403_if_put_not_author(self, comment_update):
        response = comment_update('good', 'put',False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_403_if_patch_not_author(self, comment_update):
        response = comment_update('good', 'patch',False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_400_if_put_bad_data(self, comment_update):
        response = comment_update('bad', 'put',True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_400_if_patch_bad_data(self, comment_update):
        response = comment_update('bad', 'patch',True)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        
@pytest.mark.django_db
class TestDeleteComment():
    def test_204_if_okay(self, comment_delete):
        response = comment_delete('good',True)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    
    def test_403_if_not_author(self, comment_delete):
        response = comment_delete('bad',False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
@pytest.mark.django_db 
class TestDeleteBlog():
    def test_204_if_okay(self, delete_blog):
        response = delete_blog(True)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    
    def test_403_if_not_author(self, delete_blog):
        response = delete_blog(False)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        