from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host= '100.115.92.199', debug=True)