## make predictions

Once everything is in postgres we can attempt to predict what games you will like 
based on your existing interactions.

Make a utility matrix using games x users and length of comment representing a rating

m = n users
n = n games

user-user matrix = O(m^2n)
item-item matrix = O(mn^2)

in this case u/u matrix is cheaper although we can try them both

find user-user similarity, make cosine similarity matrix. 

get predictions for user

Things to think about:
- other kinds of similarity
- matrix sparsity
- cold starts
