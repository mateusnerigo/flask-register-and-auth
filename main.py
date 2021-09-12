# imports
from website import create_app
# imports

app = create_app()

# only works when this file is running directly from the app
if __name__ == '__main__' :
  # rerun on change
  app.run(debug=True)
