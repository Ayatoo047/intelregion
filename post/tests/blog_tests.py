
# blog Endpoints:
# GET /api/posts - Retrieve all posts (Paginated)
# just one test for work fine

# GET /api/posts/:id - Retrieve a single post by ID
# just one test for work fine


# POST /api/posts - Create a new post (Authenticated)
# auth and no auth
# bad data and good data



# PUT /api/posts/:id - Update a post by ID (Authenticated & Author only)
# bad data and good data
# auth === # user is the owner and not the owner

# DELETE /api/posts/:id - Delete a post by ID (Authenticated & Author only)
# bad data and good data
# auth === # user is the owner and not the owner


# Comment Endpoints:
# GET /api/posts/:postId/comments - Retrieve all comments for a post (Paginated)
# POST /api/posts/:postId/comments - Create a new comment on a post (Authenticated)
# PUT /api/comments/:id - Update a comment by ID (Authenticated & Author only)
# DELETE /api/comments/:id - Delete a comment by ID (Authenticated & Author only)