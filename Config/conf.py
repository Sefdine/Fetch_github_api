

# Define my github access token
access_token = input('Veuillez entrer votre token : ')
ACCESS_TOKEN = 'Bearer '+access_token

# Define the url(based on the search repositories)
URL = "https://api.github.com/search/repositories"