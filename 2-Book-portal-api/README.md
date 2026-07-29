**Book Portal** — a standard Django/DRF theme. The idea: a mini-Goodreads. 
### What will be in the project? 
The user can: 
* register 
* add books 
* search books 
* rate 
* write a review 
* add a book to the list: 
* want to read 
* view book ratings 
* view author profile 
* view recommendations 
### Main Models
Text
User
Book
Author
Genre
Review
Rating
Reading List
Favorite

### Why this topic is good: It teaches more than just CRUD. You'll encounter:
text
ForeignKey
ManyToMany
filtering
search
ratings
aggregations
permissions
pagination
API
JWT
tests
PostgreSQL
Docker
### How to develop step by step 
1. **Django basic** 
* Book, Author, Genre models 
* admin panel 
* book list and detail pages 
2. **CRUD** 
* add book 
* edit book 
* delete book 
* add author/genre 
3. **Auth** 
* registration 
* login/logout 
* only authorized users can write reviews 
4. **Reviews** 
* book reviews 
* ratings from 1 to 5 
* average book rating 
5. **Search & Filters** 
* search by title 
* filter by genre 
* sort by rating 
* pagination 
6. **Reading list** 
* want to read 
* reading 
* read 
7. **DRF** 
* Books API 
* Reviews API 
* Ratings API 
* Reading lists API 
8. **JWT** 
* token authentication 
* access rights 
9. **Advanced** 
* recommendations 
* caching 
* Celery for email 
* Docker 
* deploy