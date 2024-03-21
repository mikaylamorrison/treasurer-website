def deploy():
    """Run deployment tasks."""
    from app import create_app, db
    from flask_migrate import upgrade, migrate, stamp
    from models import User

	# Create an instance of the Flask application		
    app = create_app()
    # Push an application context so we can use Flask-SQLAlchemy's db object
    app.app_context().push()
    # Create all database tables
    db.create_all()
    
    # Migrate database to latest revision
    # stamp() is used to 'stamp' the current database with the most recent migration
    # This is useful when creating a new database or upgrading an existing one
    stamp()
    # migrate() generates the migration scripts
    migrate()
    # upgrade() applies the migration scripts to the database
    upgrade()
# Call the deploy function
deploy()
